"""
Exercises package - organized by body part category
All exercise coordinate trackers for the fitness application
"""

# Upper body exercises
from .upper_body import (
    BicepCurlCoordinates,
    PushupCoordinates,
    BenchPressCoordinates,
    RopePulldownCoordinates,
    BentTricepPullCoordinates,
    PullupCoordinates,
    ChestSupportedRowCoordinates,
    WideGripPulldownCoordinates,
)

# Lower body exercises
from .lower_body import (
    SquatCoordinates,
    LegPressCoordinates,
)

# Core exercises
from .core import (
    PlankCoordinates,
    CrunchCoordinates,
)

# Shoulder exercises
from .shoulders import (
    ChestSupportedShoulderPressCoordinates,
    OverheadShoulderPressCoordinates,
)

__all__ = [
    # Upper body
    'BicepCurlCoordinates',
    'PushupCoordinates',
    'BenchPressCoordinates',
    'RopePulldownCoordinates',
    'BentTricepPullCoordinates',
    'PullupCoordinates',
    'ChestSupportedRowCoordinates',
    'WideGripPulldownCoordinates',
    # Lower body
    'SquatCoordinates',
    'LegPressCoordinates',
    # Core
    'PlankCoordinates',
    'CrunchCoordinates',
    # Shoulders
    'ChestSupportedShoulderPressCoordinates',
    'OverheadShoulderPressCoordinates',
]
