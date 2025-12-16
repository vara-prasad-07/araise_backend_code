import json
import logging
import uuid
import asyncio
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from exercises import (
    BicepCurlCoordinates,
    SquatCoordinates,
    PushupCoordinates,
    PlankCoordinates,
    BenchPressCoordinates,
    RopePulldownCoordinates,
    BentTricepPullCoordinates,
    CrunchCoordinates,
    PullupCoordinates,
    ChestSupportedRowCoordinates,
    WideGripPulldownCoordinates,
    LegPressCoordinates,
    ChestSupportedShoulderPressCoordinates,
    OverheadShoulderPressCoordinates,
)
from utils.redis_client import redis_client
from config import config

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection on startup"""
    await redis_client.connect()
    logging.info("🚀 Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Close Redis connection on shutdown"""
    await redis_client.disconnect()
    logging.info("👋 Application shutdown complete")


class FastConnectionManager:
    """Manage multiple WebSocket connections with isolated exercise instances"""
    
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, Any]] = {}
    
    def connect(self, websocket: WebSocket, exercise: str, user_id: str) -> str:
        """Create a new connection with unique exercise instances"""
        connection_id = str(uuid.uuid4())
        
        # Create coordinate-based exercise instances with user_id for Redis
        exercise_instances = {
            "biceps": BicepCurlCoordinates(user_id=user_id),
            "squats": SquatCoordinates(user_id=user_id), 
            "pushups": PushupCoordinates(user_id=user_id),
            "plank": PlankCoordinates(user_id=user_id),
            "benchpress": BenchPressCoordinates(user_id=user_id),
            "ropepulldown": RopePulldownCoordinates(user_id=user_id),
            "benttricep": BentTricepPullCoordinates(user_id=user_id),
            "crunch": CrunchCoordinates(user_id=user_id),
            "pullup": PullupCoordinates(user_id=user_id),
            "chestsupportedrow": ChestSupportedRowCoordinates(user_id=user_id),
            "widegrippulldown": WideGripPulldownCoordinates(user_id=user_id),
            "legpress": LegPressCoordinates(user_id=user_id),
            "chestsupportedshoulderpress": ChestSupportedShoulderPressCoordinates(user_id=user_id),
            "overheadshoulderpress": OverheadShoulderPressCoordinates(user_id=user_id)
        }
        
        self.active_connections[connection_id] = {
            "websocket": websocket,
            "exercise": exercise,
            "exercise_instances": exercise_instances,
            "current_instance": exercise_instances.get(exercise)
        }
        
        logging.info(f"New connection {connection_id} for exercise: {exercise}")
        return connection_id
    
    def disconnect(self, connection_id: str):
        """Remove connection and clean up resources"""
        if connection_id in self.active_connections:
            exercise = self.active_connections[connection_id]["exercise"]
            del self.active_connections[connection_id]
            logging.info(f"Connection {connection_id} disconnected from exercise: {exercise}")
    
    def get_connection(self, connection_id: str) -> Dict[str, Any]:
        """Get connection data"""
        return self.active_connections.get(connection_id)
    
    def get_stats(self) -> Dict[str, int]:
        """Get connection statistics"""
        stats = {"total": len(self.active_connections)}
        for conn_data in self.active_connections.values():
            exercise = conn_data["exercise"]
            stats[exercise] = stats.get(exercise, 0) + 1
        return stats

# Global connection manager
manager = FastConnectionManager()

@app.get("/")
async def root():
    return {
        "message": "Fast Coordinate-based Exercise Server",
        "mode": "coordinates",
        "redis_enabled": redis_client.is_available(),
        "version": "2.0"
    }

@app.get("/stats")
async def get_stats():
    """Get current connection statistics"""
    return {
        "stats": manager.get_stats(),
        "server": "coordinate_processor"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    redis_status = "connected" if redis_client.is_available() else "disconnected"
    
    return {
        "status": "healthy",
        "mode": "coordinate_processing",
        "active_connections": len(manager.active_connections),
        "redis_status": redis_status,
        "features": {
            "state_persistence": redis_client.is_available(),
            "workout_history": config.ENABLE_WORKOUT_HISTORY,
            "leaderboards": config.ENABLE_LEADERBOARDS
        }
    }

@app.websocket("/ws/{exercise}")
async def websocket_endpoint(websocket: WebSocket, exercise: str, user_id: str = None):
    await websocket.accept()
    
    # Generate user_id if not provided
    if not user_id:
        user_id = str(uuid.uuid4())
    
    # Create a unique connection with dedicated exercise instances
    connection_id = manager.connect(websocket, exercise, user_id)
    connection_data = manager.get_connection(connection_id)
    
    if not connection_data:
        await websocket.close(code=1003)
        return
    
    current_exercise_instance = connection_data["current_instance"]
    
    if not current_exercise_instance:
        await websocket.send_json({"error": f"Exercise '{exercise}' not supported"})
        await websocket.close(code=1003)
        return

    try:
        while True:
            # Receive coordinates from client
            data = await websocket.receive_text()
            if not data:
                continue

            try:
                # Parse coordinate data
                coordinate_data = json.loads(data)
                
                # Validate coordinate data format
                if not isinstance(coordinate_data, dict) or 'coordinates' not in coordinate_data:
                    await websocket.send_json({
                        "error": "Invalid data format. Expected: {'coordinates': {...}}"
                    })
                    continue
                
                coordinates = coordinate_data['coordinates']
                
                # Process coordinates super fast (no video processing!)
                reps, feedback, angle, stage = current_exercise_instance.process_coordinates(coordinates)
                
                # Instant response with exercise data
                response = {
                    "exercise": exercise,
                    "reps": reps,
                    "feedback": feedback,
                    "angle": angle,
                    "stage": stage,
                    "connection_id": connection_id[:8],  # Short ID for debugging
                    "processed_at": asyncio.get_event_loop().time()
                }
                
                await websocket.send_json(response)
                
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON format"})
                continue
            except Exception as e:
                logging.error(f"Processing error for connection {connection_id}: {e}")
                await websocket.send_json({"error": "Processing error"})
                continue

    except WebSocketDisconnect:
        logging.info(f"WebSocket disconnected: {connection_id}")
    except Exception as e:
        logging.error(f"WebSocket error for connection {connection_id}: {e}")
    finally:
        # Always clean up the connection
        manager.disconnect(connection_id)

# Example endpoint to show expected coordinate format
@app.get("/coordinate-format/{exercise}")
async def get_coordinate_format(exercise: str):
    """Get the expected coordinate format for each exercise"""
    formats = {
        "biceps": {
            "description": "Bicep curl requires shoulder, elbow, and wrist coordinates",
            "format": {
                "coordinates": {
                    "right_shoulder": [100, 200],  # [x, y]
                    "right_elbow": [150, 250],
                    "right_wrist": [180, 300]
                }
            }
        },
        "squats": {
            "description": "Squat requires hip, knee, and ankle coordinates", 
            "format": {
                "coordinates": {
                    "right_hip": [100, 200],
                    "right_knee": [120, 350],
                    "right_ankle": [130, 450]
                }
            }
        },
        "pushups": {
            "description": "Pushup requires shoulder, elbow, and wrist coordinates",
            "format": {
                "coordinates": {
                    "right_shoulder": [100, 200],
                    "right_elbow": [150, 250], 
                    "right_wrist": [200, 260]
                }
            }
        },
        "plank": {
            "description": "Plank requires shoulder, hip, and knee coordinates",
            "format": {
                "coordinates": {
                    "right_shoulder": [100, 200],
                    "right_hip": [100, 300],
                    "right_knee": [100, 400]
                }
            }
        }
    }
    
    return formats.get(exercise, {"error": f"Exercise '{exercise}' not found"})
