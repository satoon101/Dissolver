# ../dissolver/__init__.py

"""Plugin that dissolves ragdolls when a player dies."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package Imports
#   Configobj
from configobj import ConfigObj

# Source.Python Imports
#   Core
from core import GAME_NAME
#   Paths
from paths import PLUGIN_DATA_PATH

# Script Imports
from dissolver.info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Validate that the game is supported and store the ragdoll entity name
try:
    ragdoll_classname = ConfigObj(
        PLUGIN_DATA_PATH.joinpath(info.basename + '.ini'))[GAME_NAME]
except KeyError:
    raise NotImplementedError('Game "{0}" not supported.'.format(GAME_NAME))
