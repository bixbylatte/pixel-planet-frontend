"""
API Client for Pixel Planet Weather Agent

Based on the official API documentation and examples.
"""

import requests
from typing import Dict, Any, Optional
from datetime import datetime


class WeatherAPIClient:
    """Client for interacting with the Pixel Planet Weather Agent API"""

    def __init__(self, base_url: str = "https://pixel-planet-api-eixw6uscdq-uc.a.run.app"):
        self.base_url = base_url.rstrip('/')
        self.timeout = 180
        self.session = requests.Session()

    def check_health(self) -> Dict[str, Any]:
        """
        Check if the API is healthy and running.

        Returns:
            dict: Health status response with agent status, project_id, and model

        Example response:
            {
                "status": "healthy",
                "agent_initialized": true,
                "project_id": "...",
                "model": "gemini-2.0-flash-exp"
            }
        """
        url = f"{self.base_url}/health"
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def assess_activity(
        self,
        location_name: str,
        latitude: float,
        longitude: float,
        start_time: datetime,
        end_time: datetime,
        activity_type: str
    ) -> Dict[str, Any]:
        """
        Get AI-powered activity assessment with weather forecasts.

        Args:
            location_name: Name of the location (e.g., "Mt. Apo", "Boracay")
            latitude: Latitude in decimal degrees (-90 to 90)
            longitude: Longitude in decimal degrees (-180 to 180)
            start_time: Start datetime for the activity
            end_time: End datetime for the activity
            activity_type: Type of activity (e.g., "hiking", "beach day", "cycling")

        Returns:
            dict: Complete assessment with AI reasoning, forecasts, and chart data

        Response structure:
            {
                "assessment": {
                    "suitable": bool,
                    "risk_level": str,
                    "confidence": str,
                    "concerns": [str],
                    "recommendations": [str],
                    "alternative_times": [str]
                },
                "forecast_summary": {
                    "parameter_name": {"min": float, "max": float, "avg": float}
                },
                "location": {
                    "name": str,
                    "coordinates": {"lat": float, "lon": float},
                    "interpolation_used": bool,
                    "confidence": str,
                    "confidence_message": str
                },
                "chart_data": {
                    "forecasts": {
                        "parameter_name": [
                            {"timestamp": str, "value": float, "lower": float, "upper": float}
                        ]
                    }
                }
            }

        Raises:
            requests.exceptions.RequestException: If API call fails
        """

        url = f"{self.base_url}/api/v1/assess-activity"

        payload = {
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "activity_type": activity_type
        }

        response = self.session.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_forecast_data(
        self,
        location_name: str,
        latitude: float,
        longitude: float,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, Any]:
        """
        Get raw forecast data without AI analysis.

        Args:
            location_name: Name of the location
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            start_time: Start datetime
            end_time: End datetime

        Returns:
            dict: Raw forecast data with all parameters

        Response structure:
            {
                "location": {
                    "name": str,
                    "coordinates": {"lat": float, "lon": float}
                },
                "total_records": int,
                "forecasts": {
                    "parameter_name": [
                        {"timestamp": str, "value": float, "lower": float, "upper": float}
                    ]
                }
            }
        """

        url = f"{self.base_url}/api/v1/forecast-data"

        payload = {
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }

        response = self.session.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()


# Helper functions for parsing API responses
def parse_assessment_response(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and structure the assessment API response for easier use

    Args:
        result: Raw API response from assess_activity

    Returns:
        Structured data dictionary with clean access to all fields
    """

    assessment = result.get('assessment', {})
    location = result.get('location', {})
    forecast_summary = result.get('forecast_summary', {})
    chart_data = result.get('chart_data', {})

    return {
        # Assessment details
        'suitable': assessment.get('suitable', False),
        'risk_level': assessment.get('risk_level', 'unknown'),
        'confidence': assessment.get('confidence', 'unknown'),
        'concerns': assessment.get('concerns', []),
        'recommendations': assessment.get('recommendations', []),
        'alternative_times': assessment.get('alternative_times', []),

        # Location info
        'location_name': location.get('name', 'Unknown'),
        'coordinates': location.get('coordinates', {}),
        'interpolation_used': location.get('interpolation_used', False),
        'location_confidence': location.get('confidence', 'unknown'),
        'confidence_message': location.get('confidence_message', ''),

        # Forecast data
        'forecast_summary': forecast_summary,
        'chart_data': chart_data,

        # Raw response (for debugging)
        'raw': result
    }


def extract_temperature_range(forecast_summary: Dict[str, Any]) -> str:
    """
    Extract temperature range from forecast summary

    Args:
        forecast_summary: Forecast summary from API response

    Returns:
        Formatted temperature range string (e.g., "20-25°C")
    """
    if 'temperature' in forecast_summary:
        temp = forecast_summary['temperature']
        min_temp = temp.get('min', 0)
        max_temp = temp.get('max', 0)
        return f"{min_temp:.0f}-{max_temp:.0f}°C"
    return "N/A"


def extract_primary_concern(assessment: Dict[str, Any]) -> Optional[str]:
    """
    Extract the primary concern from assessment

    Args:
        assessment: Assessment dict from API response

    Returns:
        First concern or None if no concerns
    """
    concerns = assessment.get('concerns', [])
    return concerns[0] if concerns else None


def get_chart_metrics(chart_data: Dict[str, Any]) -> list:
    """
    Get list of available chart metrics from chart data

    Args:
        chart_data: Chart data from API response

    Returns:
        List of available metric names
    """
    forecasts = chart_data.get('forecasts', {})
    return list(forecasts.keys())
