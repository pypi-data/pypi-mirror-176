"""
This module is part of the 'pelican-gesetze' package,
which is released under GPL-3.0-only license.
"""

import logging
from typing import Dict, Union

import gesetze

from pelican import Pelican, signals

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def worker(pelican: Pelican):
    """
    Wrapper for 'gesetze'

    :param pelican: pelican.Pelican Pelican object
    :return: None
    """

    # Initialize object
    obj = gesetze.Gesetz(pelican.settings.get("GESETZE_DRIVER_ORDER", None))

    # Report initialization
    LOGGER.info("PLUGIN pelican-gesetze was loaded")

    # Apply configuration
    # (1) 'title' attribute
    obj.title: Union[str, False] = pelican.settings.get(
        "GESETZE_TITLE_ATTRIBUTE", False
    )

    # (2) Custom attributes
    obj.attributes: Dict[str, str] = pelican.settings.get(
        "GESETZE_CUSTOM_ATTRIBUTES", {"target": "_blank"}
    )

    # Add filter
    pelican.env.filters.update({"gesetzify": obj.gesetzify})


def register() -> None:
    """
    Registers 'pelican-gesetze' plugin

    For more information,
    see https://docs.getpelican.com/en/latest/plugins.html

    :return: None
    """

    signals.generator_init.connect(worker)
