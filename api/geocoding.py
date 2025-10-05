"""
Geocoding service to convert location names to coordinates
Using Nominatim (OpenStreetMap) - free and no API key required
"""

import requests
from typing import List, Dict, Optional
from dataclasses import dataclass


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
        self.base_url = "https://nominatim.openstreetmap.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Pixelast-Weather-App/1.0'
        })

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
                timeout=10
            )
            response.raise_for_status()
            results = response.json()

            locations = []
            for result in results:
                location = Location(
                    display_name=result.get('display_name', ''),
                    latitude=float(result.get('lat', 0)),
                    longitude=float(result.get('lon', 0)),
                    place_id=result.get('place_id', '')
                )
                locations.append(location)

            return locations

        except Exception as e:
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
