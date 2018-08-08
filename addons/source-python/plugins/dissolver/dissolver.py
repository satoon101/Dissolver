# ../dissolver/dissolver.py

"""Dissolves player ragdolls on death."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from random import randrange
from warnings import warn

# Source.Python
from entities.constants import INVALID_ENTITY_INTHANDLE
from entities.entity import Entity
from entities.helpers import index_from_inthandle
from events import Event
from listeners.tick import Delay
from players.entity import Player

# Plugin
from .config import (
    NUM_DISSOLVE_TYPES, dissolver_delay, dissolver_magnitude, dissolver_type,
)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _dissolve_player_ragdoll(game_event):
    """Dissolve/remove the player's ragdoll on death."""
    # Get the type of dissolver to use
    current_type = dissolver_type.get_int()

    # Is the type valid?
    if current_type < 0 or current_type > NUM_DISSOLVE_TYPES + 2:

        # Raise a warning
        warn(
            'Invalid value for {name} cvar "{dissolve_type}".'.format(
                name=dissolver_type.name,
                dissolve_type=current_type
            )
        )

        # Use the remove setting
        current_type = NUM_DISSOLVE_TYPES + 2

    # Delay the dissolving
    Delay(
        delay=max(0, dissolver_delay.get_int()),
        callback=_dissolve_ragdoll,
        args=(game_event['userid'], current_type),
    )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _dissolve_ragdoll(userid, current_type):
    """Dissolve/remove the player's ragdoll."""
    # Get the ragdoll entity
    inthandle = Player.from_userid(userid).ragdoll
    if inthandle == INVALID_ENTITY_INTHANDLE:
        return
    entity = Entity(index_from_inthandle(inthandle))

    # Should the ragdoll just be removed?
    if current_type == NUM_DISSOLVE_TYPES + 2:
        entity.remove()
        return

    # Set the target name for the player's ragdoll
    entity.target_name = 'ragdoll_{userid}'.format(userid=userid)

    # Get the dissolver entity
    dissolver_entity = Entity.find_or_create('env_entity_dissolver')

    # Should a random dissolve type be chosen?
    if current_type == NUM_DISSOLVE_TYPES + 1:
        current_type = randrange(NUM_DISSOLVE_TYPES)

    # Set the magnitude
    dissolver_entity.magnitude = dissolver_magnitude.get_int()

    # Set the dissolve type
    dissolver_entity.dissolve_type = current_type

    # Dissolve the ragdoll
    dissolver_entity.dissolve('ragdoll_{userid}'.format(userid=userid))
