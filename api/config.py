"""
Configuration for Pixel Planet Frontend
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""

    # API Configuration
    API_BASE_URL = os.getenv(
        "API_BASE_URL",
        "https://pixel-planet-api-eixw6uscdq-uc.a.run.app"
    )
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "180"))

    # App Configuration
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PAGE_TITLE = os.getenv("PAGE_TITLE", "PixelCast")

    # Default values
    DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "San Francisco, CA")
    DEFAULT_LATITUDE = float(os.getenv("DEFAULT_LATITUDE", "37.7749"))
    DEFAULT_LONGITUDE = float(os.getenv("DEFAULT_LONGITUDE", "-122.4194"))

    # Geocoding (Nominatim) configuration
    # See usage policy: https://operations.osmfoundation.org/policies/nominatim/
    GEOCODING_BASE_URL = os.getenv(
        "GEOCODING_BASE_URL",
        "https://nominatim.openstreetmap.org"
    )
    GEOCODING_TIMEOUT = int(os.getenv("GEOCODING_TIMEOUT", "10"))
    # Provide a descriptive UA and a contact email to comply with policy
    GEOCODING_USER_AGENT = os.getenv(
        "GEOCODING_USER_AGENT",
        "PixelCast/1.0 (Streamlit)"
    )
    GEOCODING_EMAIL = os.getenv("GEOCODING_EMAIL", "")


config = Config()
