# ../dissolver/config.py

"""Creates server configuration and user settings."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from config.manager import ConfigManager
from entities.constants import DissolveType

# Plugin
from .info import info
from .strings import CONFIG_STRINGS


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'NUM_DISSOLVE_TYPES',
    'dissolver_delay',
    'dissolver_magnitude',
    'dissolver_type',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store the number of dissolve types
NUM_DISSOLVE_TYPES = len(DissolveType)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
# Create the dissolver.cfg file and execute it upon __exit__
with ConfigManager(info.name, 'dissolver_') as _config:

    # Create the dissolver type cvar
    dissolver_type = _config.cvar('type', 0, CONFIG_STRINGS['Type'])

    # Loop through all dissolver types
    for _obj in DissolveType:

        # Add the current dissolver type to the list of options
        dissolver_type.Options.append(f'{_obj.real} = {_obj.name}')

    # Add random and remove to the list of options
    for _num, _option in enumerate(
        ('RANDOM', 'REMOVE'),
        start=NUM_DISSOLVE_TYPES + 1
    ):
        dissolver_type.Options.append(f'{_num} = {_option}')

    # Create the dissolver magnitude cvar
    dissolver_magnitude = _config.cvar(
        'magnitude', 2, CONFIG_STRINGS['Magnitude']
    )

    # Create the delay cvar
    dissolver_delay = _config.cvar('delay', 0, CONFIG_STRINGS['Delay'])
