from extras.plugins import PluginConfig


class FusionInventoryConfig(PluginConfig):
    """
    This class defines attributes for the NetBox FI Gateway plugin.
    """
    # Plugin package name
    name = 'netbox_fusioninventory_plugin'

    # Human-friendly name and description
    verbose_name = 'Fusion inventory plugin'
    description = 'A Plugin for import devices from fusion inventory agent'

    # Plugin version
    version = '0.1'

    # Plugin author
    author = 'Michaël Ricart'
    author_email = 'michael.ricart@0w.tf'

    # Configuration parameters that MUST be defined by the user (if any)
    required_settings = []

    # Default configuration parameter values, if not set by the user
    default_settings = {
        'loud': True
    }

    # Base URL path. If not set, the plugin name will be used.
    base_url = 'fusion-inventory'

    # Caching config
    caching_config = {}


config = FusionInventoryConfig

