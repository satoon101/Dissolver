# ../dissolver/dissolver.py

"""Dissolves player ragdolls on death."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from random import randrange
from warnings import warn

# Source.Python
from entities.entity import Entity
from entities.helpers import index_from_inthandle
from events import Event
from listeners.tick import Delay
from players.entity import Player

# Plugin
from .config import (
    NUM_DISSOLVE_TYPES,
    dissolver_delay,
    dissolver_magnitude,
    dissolver_type,
)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("player_death")
def _dissolve_player_ragdoll(game_event):
    """Dissolve/remove the player's ragdoll on death."""
    # Get the type of dissolver to use
    current_type = dissolver_type.get_int()

    # Is the type valid?
    if current_type < 0 or current_type > NUM_DISSOLVE_TYPES + 2:

        # Raise a warning
        warn(
            f'Invalid value for {dissolver_type.name} cvar "{current_type}".',
            stacklevel=2,
        )

        # Use the remove setting
        current_type = NUM_DISSOLVE_TYPES + 2

    player = Player.from_userid(game_event["userid"])

    # Delay the dissolving
    Delay(
        delay=max(0, dissolver_delay.get_int()),
        callback=_dissolve_ragdoll,
        args=(player.ragdoll, current_type),
    )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _dissolve_ragdoll(inthandle, current_type):
    """Dissolve/remove the player's ragdoll."""
    try:
        entity = Entity(index_from_inthandle(inthandle))
    except (OverflowError, ValueError):
        return

    # Should the ragdoll just be removed?
    if current_type == NUM_DISSOLVE_TYPES + 2:
        entity.remove()
        return

    # Set the target name for the player's ragdoll
    entity.target_name = f"ragdoll_{inthandle}"

    # Get the dissolver entity
    dissolver_entity = Entity.find_or_create("env_entity_dissolver")

    # Should a random dissolve type be chosen?
    if current_type == NUM_DISSOLVE_TYPES + 1:
        current_type = randrange(NUM_DISSOLVE_TYPES)

    # Set the magnitude
    dissolver_entity.magnitude = dissolver_magnitude.get_int()

    # Set the dissolve type
    dissolver_entity.dissolve_type = current_type

    # Dissolve the ragdoll
    dissolver_entity.dissolve(f"ragdoll_{inthandle}")
