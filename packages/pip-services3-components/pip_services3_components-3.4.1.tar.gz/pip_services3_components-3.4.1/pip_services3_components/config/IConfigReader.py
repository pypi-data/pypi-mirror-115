# -*- coding: utf-8 -*-
"""
    pip_services3_components.config.IConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    interface for configuration readers
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC, abstractmethod
from typing import Optional

from pip_services3_commons.config import ConfigParams


class IConfigReader(ABC):
    """
    Interface for configuration readers that retrieve configuration from various sources
    and make it available for other components.

    Some IConfigReader implementations may support configuration parameterization.
    The parameterization allows to use configuration as a template and inject there dynamic values.
    The values may come from application command like arguments or environment variables.
    """

    def _read_config(self, correlation_id: Optional[str], parameters: ConfigParams) -> ConfigParams:
        """
        Reads configuration and parameterize it with given values.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param parameters: values to parameters the configuration or null to skip parameterization.

        :return: ConfigParams configuration.
        """
        raise NotImplementedError('Method from interface definition')
