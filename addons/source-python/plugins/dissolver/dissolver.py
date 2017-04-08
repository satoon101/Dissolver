# ../dissolver/dissolver.py

"""Dissolves player ragdolls on death."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from random import randrange
from warnings import warn

# Source.Python
from config.manager import ConfigManager
from entities.constants import DissolveType
from entities.constants import INVALID_ENTITY_INTHANDLE
from entities.entity import Entity
from entities.helpers import index_from_inthandle
from events import Event
from listeners.tick import Delay
from players.entity import Player
from translations.strings import LangStrings

# Plugin
from .info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store the number of dissolve types
_num_dissolve_types = len(DissolveType)

# Get the configuration strings
_config_strings = LangStrings(info.name)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
# Create the cfg file
with ConfigManager(info.name, 'dissolver_') as _config:

    # Create the dissolver type cvar
    dissolver_type = _config.cvar('type', 0, _config_strings['Type'])

    # Loop through all dissolver types
    for _name in DissolveType.__members__:

        # Add the current dissolver type to the list of options
        dissolver_type.Options.append(
            '{value} = {text}'.format(
                value=getattr(DissolveType, _name).real,
                text=_name
            )
        )

    # Add random and remove to the list of options
    for _num, _option in enumerate(('RANDOM', 'REMOVE')):
        dissolver_type.Options.append(
            '{value} = {text}'.format(
                value=_num_dissolve_types + _num,
                text=_option
            )
        )

    # Create the dissolver magnitude cvar
    dissolver_magnitude = _config.cvar(
        'magnitude', 2, _config_strings['Magnitude']
    )

    # Create the delay cvar
    dissolver_delay = _config.cvar('delay', 0, _config_strings['Delay'])


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _dissolve_player_ragdoll(game_event):
    """Dissolve/remove the player's ragdoll on death."""
    # Get the type of dissolver to use
    current_type = dissolver_type.get_int()

    # Is the type valid?
    if current_type < 0 or current_type > _num_dissolve_types + 2:

        # Raise a warning
        warn(
            'Invalid value for {name} cvar "{dissolve_type}".'.format(
                name=dissolver_type.name,
                dissolve_type=current_type
            )
        )

        # Use the remove setting
        current_type = _num_dissolve_types + 2

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
    if current_type == _num_dissolve_types + 2:
        entity.remove()
        return

    # Set the target name for the player's ragdoll
    entity.target_name = 'ragdoll_{userid}'.format(userid=userid)

    # Get the dissolver entity
    dissolver_entity = Entity.find_or_create('env_entity_dissolver')

    # Should a random dissolve type be chosen?
    if current_type == _num_dissolve_types + 1:
        current_type = randrange(_num_dissolve_types)

    # Set the magnitude
    dissolver_entity.magnitude = dissolver_magnitude.get_int()

    # Set the dissolve type
    dissolver_entity.dissolve_type = current_type

    # Dissolve the ragdoll
    dissolver_entity.dissolve('ragdoll_{userid}'.format(userid=userid))
