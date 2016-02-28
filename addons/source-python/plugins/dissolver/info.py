# ../dissolver/info.py

"""Provides/stores information about the plugin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.public import PublicConVar
#   Plugins
from plugins.info import PluginInfo


# =============================================================================
# >> PLUGIN INFO
# =============================================================================
info = PluginInfo()
info.name = 'Dissolver'
info.author = 'Satoon101'
info.version = '1.1a'
info.basename = 'dissolver'
info.variable = info.basename + '_version'
info.url = ''
info.convar = PublicConVar(info.variable, info.version, info.name + ' Version')
