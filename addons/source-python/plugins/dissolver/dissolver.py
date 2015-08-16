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
#   Cvars
from cvars.flags import ConVarFlags
#   Entities
from entities.constants import DissolveType
from entities.entity import Entity
#   Events
from events import Event
#   Filters
from filters.entities import EntityIter
#   Players
from players.helpers import inthandle_from_userid
#   Translations
from translations.strings import LangStrings

# Script Imports
from dissolver import ragdoll_classname
from dissolver.info import info


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
    dissolver_type = _config.cvar(
        'type', 0, ConVarFlags.NONE, _config_strings['Type'])

    # Loop through all dissolver types
    for _name in DissolveType.__members__:

        # Add the current dissolver type to the list of options
        dissolver_type.Options.append('{0} = {1}'.format(
            getattr(DissolveType, _name).real, _name))

    # Add random and remove to the list of options
    dissolver_type.Options.append('{0} = RANDOM'.format(_num_dissolve_types))
    dissolver_type.Options.append(
        '{0} = REMOVE'.format(_num_dissolve_types + 1))

    # Create the dissolver magnitude cvar
    dissolver_magnitude = _config.cvar(
        'magnitude', 2, ConVarFlags.NONE, _config_strings['Magnitude'])


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def dissolve_ragdoll(game_event):
    """Dissolve/remove the player's ragdoll on death."""
    # Get the type of dissolver to use
    current_type = dissolver_type.get_int()

    # Is the type valid?
    if current_type < 0 or current_type > _num_dissolve_types + 2:

        # Raise a warning
        warn('Invalid value for {0} cvar "{1}".'.format(
            dissolver_type.name, current_type))

    # Should the ragdoll just be removed?
    if current_type == _num_dissolve_types + 2:

        # Get the player's integer handle
        inthandle = inthandle_from_userid(game_event.get_int('userid'))

        # Loop through all current ragdolls
        for entity in EntityIter(ragdoll_classname, return_types='entity'):

            # Does the current one belong to the player?
            if entity.owner == inthandle:

                # Remove the ragdoll
                entity.remove()

                # No need to loop further
                return

    # Get the dissolver entity
    dissolver_entity = _get_dissolver_entity()

    # Should a random dissolve type be chosen?
    if current_type == _num_dissolve_types + 1:

        # Get a random dissolve type
        current_type = randrange(_num_dissolve_types)

    # Set the magnitude
    dissolver_entity.magnitude = dissolver_magnitude.get_int()

    # Set the dissolve type
    dissolver_entity.dissolve_type = current_type

    # Dissolve the ragdoll
    dissolver_entity.dissolve(ragdoll_classname)


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _get_dissolver_entity():
    """Return an env_entity_dissolver instance."""
    # Loop through all current dissolver entities on the server
    for entity in EntityIter('env_entity_dissolver', return_types='entity'):

        # Return the first entity
        return entity

    # If no dissolver entities exist, create one and return its instance
    return Entity.create('env_entity_dissolver')
