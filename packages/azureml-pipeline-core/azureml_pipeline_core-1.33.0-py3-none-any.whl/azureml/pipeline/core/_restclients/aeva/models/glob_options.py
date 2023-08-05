# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GlobOptions(Model):
    """GlobOptions.

    :param glob_patterns:
    :type glob_patterns: list[str]
    """

    _attribute_map = {
        'glob_patterns': {'key': 'GlobPatterns', 'type': '[str]'},
    }

    def __init__(self, glob_patterns=None):
        super(GlobOptions, self).__init__()
        self.glob_patterns = glob_patterns
