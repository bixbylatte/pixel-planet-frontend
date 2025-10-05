import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional


def render_forecast_graphs(
    chart_data: Dict[str, Any],
    selected_metrics: Optional[List[str]] = None
):
    """
    Renders weather forecast charts using Plotly

    Args:
        chart_data: Dictionary containing forecast data from API
                   Expected structure: {'forecasts': {'param_name': [data_points]}}
        selected_metrics: Optional list of metrics to display. If None, displays all available.
    """

    # Extract forecasts from chart_data
    forecasts = chart_data.get('forecasts', {}) if isinstance(
        chart_data, dict) else {}

    if not forecasts:
        st.warning("No chart data available")
        return

    # Parameter info and units with colors matching your design
    param_info = {
        'precipitation': {
            'name': 'Precipitation',
            'unit': 'mm',
            'color': '#3b82f6',  # Blue
            'icon': '💧'
        },
        'temperature': {
            'name': 'Temperature',
            'unit': '°C',
            'color': '#f59e0b',  # Amber/Orange
            'icon': '🌡️'
        },
        'wind': {
            'name': 'Wind Speed',
            'unit': 'm/s',
            'color': '#10b981',  # Emerald/Green
            'icon': '💨'
        },
        'humidity': {
            'name': 'Humidity',
            'unit': '%',
            'color': '#60a5fa',  # Light Blue
            'icon': '💦'
        },
        'solar_radiation': {
            'name': 'Solar Radiation',
            'unit': 'W/m²',
            'color': '#fbbf24',  # Yellow
            'icon': '☀️'
        },
        'cloud_cover': {
            'name': 'Cloud Cover',
            'unit': '%',
            'color': '#94a3b8',  # Slate/Gray
            'icon': '☁️'
        },
        'air_quality': {
            'name': 'Air Quality',
            'unit': 'AQI',
            'color': '#8b5cf6',  # Purple
            'icon': '🌫️'
        }
    }

    # Filter forecasts based on selected metrics
    if selected_metrics:
        forecasts = {k: v for k, v in forecasts.items()
                     if k in selected_metrics}

    # Create chart for each parameter
    for param, data_points in forecasts.items():
        if not data_points or not isinstance(data_points, list):
            continue

        info = param_info.get(param, {
            'name': param.replace('_', ' ').title(),
            'unit': '',
            'color': '#6b7280',
            'icon': '📊'
        })

        # Convert to DataFrame
        try:
            df = pd.DataFrame(data_points)
            if df.empty or 'timestamp' not in df.columns or 'value' not in df.columns:
                continue
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        except Exception as e:
            st.warning(f"Could not parse data for {param}: {str(e)}")
            continue

        # Create plotly figure
        fig = go.Figure()

        # Add confidence interval (if available)
        if 'lower' in df.columns and 'upper' in df.columns:
            # Convert hex color to rgba for confidence interval
            color_hex = info['color'].lstrip('#')
            r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))

            fig.add_trace(go.Scatter(
                x=df['timestamp'].tolist() + df['timestamp'].tolist()[::-1],
                y=df['upper'].tolist() + df['lower'].tolist()[::-1],
                fill='toself',
                fillcolor=f"rgba({r}, {g}, {b}, 0.15)",
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=True,
                name='Uncertainty Band'
            ))

        # Add main forecast line
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['value'],
            mode='lines+markers',
            name=info['name'],
            line=dict(color=info['color'], width=3),
            marker=dict(size=6, color=info['color'])
        ))

        # Update layout with modern styling
        fig.update_layout(
            title={
                'text': f"{info['icon']} {info['name']} Forecast",
                'font': {'size': 20, 'color': '#1f2937'}
            },
            xaxis_title="Time",
            yaxis_title=f"{info['name']} ({info['unit']})",
            hovermode='x unified',
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="system-ui, -apple-system, sans-serif"),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)',
                zeroline=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)',
                zeroline=False
            )
        )

        # Display chart
        st.plotly_chart(fig, use_container_width=True)


def render_forecast_grid(
    chart_data: Dict[str, Any],
    columns: int = 2
):
    """
    Renders forecast charts in a grid layout

    Args:
        chart_data: Dictionary containing forecast data from API
        columns: Number of columns in the grid (default: 2)
    """

    forecasts = chart_data.get('forecasts', {}) if isinstance(
        chart_data, dict) else {}

    if not forecasts:
        st.warning("No chart data available")
        return

    # Create columns
    forecast_items = list(forecasts.items())

    for i in range(0, len(forecast_items), columns):
        cols = st.columns(columns)

        for j, col in enumerate(cols):
            if i + j < len(forecast_items):
                param, data_points = forecast_items[i + j]

                with col:
                    # Render individual chart with smaller height
                    mini_chart_data = {
                        'forecasts': {param: data_points}
                    }
                    render_forecast_graphs(mini_chart_data)


def get_forecast_summary_stats(chart_data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    """
    Extracts summary statistics from forecast data

    Args:
        chart_data: Dictionary containing forecast data from API

    Returns:
        Dictionary with summary stats for each parameter
        Example: {'temperature': {'min': 20, 'max': 30, 'avg': 25}}
    """

    forecasts = chart_data.get('forecasts', {}) if isinstance(
        chart_data, dict) else {}
    summary = {}

    for param, data_points in forecasts.items():
        if not data_points or not isinstance(data_points, list):
            continue

        try:
            df = pd.DataFrame(data_points)
            if 'value' in df.columns:
                summary[param] = {
                    'min': float(df['value'].min()),
                    'max': float(df['value'].max()),
                    'avg': float(df['value'].mean()),
                    'std': float(df['value'].std())
                }
        except Exception:
            continue

    return summary
