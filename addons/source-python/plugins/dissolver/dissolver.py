# ../dissolver/dissolver.py

"""Dissolves player ragdolls on death."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Random
from random import randrange
#   Warnings
from warnings import warn

# Source.Python Imports
#   Config
from config.manager import ConfigManager
#   Entities
from entities.constants import DissolveType
from entities.constants import INVALID_ENTITY_INTHANDLE
from entities.entity import Entity
from entities.helpers import index_from_inthandle
#   Events
from events import Event
#   Listeners
from listeners.tick import Delay
#   Players
from players.entity import Player
from players.helpers import index_from_userid
#   Translations
from translations.strings import LangStrings

# Script Imports
from .info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store the number of dissolve types
_num_dissolve_types = len(DissolveType)

# Get the configuration strings
_config_strings = LangStrings(info.basename)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
# Create the cfg file
with ConfigManager(info.basename, 'dissolver_') as _config:

    # Create the dissolver type cvar
    dissolver_type = _config.cvar('type', 0, _config_strings['Type'])

    # Loop through all dissolver types
    for _name in DissolveType.__members__:

        # Add the current dissolver type to the list of options
        dissolver_type.Options.append('{0} = {1}'.format(
            getattr(DissolveType, _name).real, _name))

    # Add random and remove to the list of options
    for _num, _option in enumerate(('RANDOM', 'REMOVE')):
        dissolver_type.Options.append('{0} = {1}'.format(
            _num_dissolve_types + _num, _option))

    # Create the dissolver magnitude cvar
    dissolver_magnitude = _config.cvar(
        'magnitude', 2, _config_strings['Magnitude'])

    # Create the delay cvar
    dissolver_delay = _config.cvar('delay', 0, _config_strings['Delay'])


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def dissolve_player_ragdoll(game_event):
    """Dissolve/remove the player's ragdoll on death."""
    # Get the type of dissolver to use
    current_type = dissolver_type.get_int()

    # Is the type valid?
    if current_type < 0 or current_type > _num_dissolve_types + 2:

        # Raise a warning
        warn('Invalid value for {0} cvar "{1}".'.format(
            dissolver_type.name, current_type))

        # Use the remove setting
        current_type = _num_dissolve_types + 2

    # Delay the dissolving
    Delay(
        max(0, dissolver_delay.get_int()),
        dissolve_ragdoll, game_event['userid'], current_type)


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def dissolve_ragdoll(userid, current_type):
    """Dissolve/remove the player's ragdoll."""
    # Get the ragdoll entity
    inthandle = Player(index_from_userid(userid)).ragdoll
    if inthandle == INVALID_ENTITY_INTHANDLE:
        return
    entity = Entity(index_from_inthandle(inthandle))

    # Should the ragdoll just be removed?
    if current_type == _num_dissolve_types + 2:
        entity.remove()
        return

    # Set the target name for the player's ragdoll
    entity.target_name = 'ragdoll_{1}'.format(userid)

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
    dissolver_entity.dissolve('ragdoll_{1}'.format(userid))
