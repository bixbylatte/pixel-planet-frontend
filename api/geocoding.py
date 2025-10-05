"""
Geocoding service to convert location names to coordinates
Using Nominatim (OpenStreetMap) - free and no API key required
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from .config import config


@dataclass
class Location:
    """Location data structure"""
    display_name: str
    latitude: float
    longitude: float
    place_id: str

    def __str__(self):
        return self.display_name


class GeocodingService:
    """Service for geocoding location names to coordinates"""

    def __init__(self):
        self.base_url = config.GEOCODING_BASE_URL.rstrip("/")
        self.timeout = config.GEOCODING_TIMEOUT
        self.session = requests.Session()

        # Build compliant User-Agent with optional contact email
        user_agent = config.GEOCODING_USER_AGENT
        if config.GEOCODING_EMAIL:
            user_agent = f"{user_agent} ({config.GEOCODING_EMAIL})"

        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'application/json'
        })

        # Configure retries for transient failures and 429 rate limits
        retry = Retry(
            total=3,
            backoff_factor=0.8,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        # track last error/status for UI messaging
        self.last_status: Optional[int] = None
        self.last_error: Optional[str] = None

    def search_locations(self, query: str, limit: int = 5) -> List[Location]:
        """
        Search for locations matching the query

        Args:
            query: Location name to search for
            limit: Maximum number of results to return

        Returns:
            List of Location objects
        """
        if not query or len(query) < 2:
            return []

        try:
            params = {
                'q': query,
                'format': 'json',
                'limit': limit,
                'addressdetails': 1
            }

            response = self.session.get(
                f"{self.base_url}/search",
                params=params,
                timeout=self.timeout
            )
            self.last_status = response.status_code
            if response.status_code == 403:
                # Likely blocked due to UA/policy; do not raise
                self.last_error = "Geocoding service blocked (403)."
                return []
            if response.status_code == 429:
                # Rate limited
                self.last_error = "Rate limited by geocoding service (429). Please wait and try again."
                return []
            response.raise_for_status()
            results = response.json()

            locations = []
            for result in results:
                location = Location(
                    display_name=result.get('display_name', ''),
                    latitude=float(result.get('lat', 0)),
                    longitude=float(result.get('lon', 0)),
                    place_id=str(result.get('place_id', ''))
                )
                locations.append(location)

            return locations

        except Exception as e:
            self.last_error = str(e)
            print(f"Geocoding error: {e}")
            return []

    def get_location(self, display_name: str) -> Optional[Location]:
        """
        Get a specific location by its display name

        Args:
            display_name: Full display name of the location

        Returns:
            Location object or None if not found
        """
        locations = self.search_locations(display_name, limit=1)
        return locations[0] if locations else None
