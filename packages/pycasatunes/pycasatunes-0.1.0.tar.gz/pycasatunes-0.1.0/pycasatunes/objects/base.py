"""CasaTunes: Base"""
import logging


class CasaBase:
    """Base class for CasaTunes."""

    logger = logging.getLogger(__name__)

    def __init__(self, attributes) -> None:
        """Initialize."""
        self.attributes = attributes


class CasaBaseClient(CasaBase):
    """Base class for CasaTunes."""

    def __init__(self, client, attributes: dict) -> None:
        """Initialise."""
        super().__init__(attributes)
        self.client = client
