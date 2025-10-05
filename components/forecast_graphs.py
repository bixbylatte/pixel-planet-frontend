import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional

# ---- QC: clamp negatives to 0 for specified params ----
def qc_nonnegative_df(df: pd.DataFrame, param: str) -> pd.DataFrame:
    """Clamp metric values < 0 to 0.0. No dropping, no warnings."""
    if 'value' not in df.columns:
        return df
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    neg_mask = df['value'] < 0
    if neg_mask.any():
        df.loc[neg_mask, 'value'] = 0.0
    return df


def render_forecast_graphs(chart_data: Dict[str, Any], selected_metrics: Optional[List[str]] = None):
    forecasts = chart_data.get('forecasts', {}) if isinstance(chart_data, dict) else {}
    if not forecasts:
        st.warning("No chart data available")
        return

    param_info = {
        'precipitation':   {'name': 'Precipitation',   'unit': 'mm',  'color': '#3b82f6', 'icon': '💧'},
        'temperature':     {'name': 'Temperature',     'unit': '°C',  'color': '#f59e0b', 'icon': '🌡️'},
        'wind':            {'name': 'Wind Speed',      'unit': 'm/s', 'color': '#10b981','icon': '💨'},
        'humidity':        {'name': 'Humidity',        'unit': '%',   'color': '#60a5fa','icon': '💦'},
        'solar_radiation': {'name': 'Solar Radiation', 'unit': 'W/m²','color': '#fbbf24','icon': '☀️'},
        'cloud_cover':     {'name': 'Cloud Cover',     'unit': '%',   'color': '#94a3b8','icon': '☁️'},
        'air_quality':     {'name': 'Air Quality',     'unit': 'AQI', 'color': '#8b5cf6','icon': '🌫️'}
    }

    if selected_metrics:
        forecasts = {k: v for k, v in forecasts.items() if k in selected_metrics}

    for param, data_points in forecasts.items():
        if not data_points or not isinstance(data_points, list):
            continue

        info = param_info.get(param, {
            'name': param.replace('_', ' ').title(),
            'unit': '',
            'color': '#6b7280',
            'icon': '📊'
        })

        try:
            df = pd.DataFrame(data_points)
            if df.empty or 'timestamp' not in df.columns or 'value' not in df.columns:
                continue
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        except Exception as e:
            st.warning(f"Could not parse data for {param}: {e}")
            continue

        # QC: clamp negatives to 0 for precipitation and humidity
        if param in ('precipitation', 'humidity'):
            df = qc_nonnegative_df(df, param)

        # Visualization constraints only for precipitation and wind
        force_nonnegative_axis = param in ('precipitation', 'wind')

        fig = go.Figure()

        # Confidence band (clip to 0 for precip/wind so band doesn’t extend below axis)
        if 'lower' in df.columns and 'upper' in df.columns:
            lower = df['lower'].copy()
            upper = df['upper'].copy()
            if force_nonnegative_axis:
                lower = pd.to_numeric(lower, errors='coerce').clip(lower=0)
                upper = pd.to_numeric(upper, errors='coerce').clip(lower=0)

            color_hex = info['color'].lstrip('#')
            r, g, b = (int(color_hex[i:i+2], 16) for i in (0, 2, 4))
            fig.add_trace(go.Scatter(
                x=df['timestamp'].tolist() + df['timestamp'].tolist()[::-1],
                y=upper.tolist() + lower.tolist()[::-1],
                fill='toself',
                fillcolor=f"rgba({r},{g},{b},0.15)",
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=True,
                name='Uncertainty Band'
            ))

        # Main line (clip to 0 for precip/wind axes only)
        y_vals = pd.to_numeric(df['value'], errors='coerce')
        if force_nonnegative_axis:
            y_vals = y_vals.clip(lower=0)

        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=y_vals,
            mode='lines+markers',
            name=info['name'],
            line=dict(color=info['color'], width=3),
            marker=dict(size=6, color=info['color'])
        ))

        # Axis range control
        if force_nonnegative_axis:
            cols = [y_vals]
            if 'upper' in df.columns:
                cols.append(pd.to_numeric(df['upper'], errors='coerce').clip(lower=0))
            ymax = pd.concat(cols, axis=1).max(axis=1).max()
            ymax = float(ymax) if pd.notna(ymax) and ymax > 0 else 1.0
            yaxis_cfg = dict(range=[0, ymax * 1.1])
        else:
            yaxis_cfg = {}

        fig.update_layout(
            title={'text': f"{info['icon']} {info['name']} Forecast",
                   'font': {'size': 20, 'color': '#1f2937'}},
            xaxis_title="Time",
            yaxis_title=f"{info['name']} ({info['unit']})",
            hovermode='x unified',
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="system-ui, -apple-system, sans-serif"),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', zeroline=False, **yaxis_cfg)
        )

        st.plotly_chart(fig, use_container_width=True)


def render_forecast_grid(chart_data: Dict[str, Any], columns: int = 2):
    forecasts = chart_data.get('forecasts', {}) if isinstance(chart_data, dict) else {}
    if not forecasts:
        st.warning("No chart data available")
        return

    items = list(forecasts.items())
    for i in range(0, len(items), columns):
        cols = st.columns(columns)
        for j, col in enumerate(cols):
            if i + j < len(items):
                param, data_points = items[i + j]
                with col:
                    mini_chart_data = {'forecasts': {param: data_points}}
                    render_forecast_graphs(mini_chart_data)


def get_forecast_summary_stats(chart_data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    forecasts = chart_data.get('forecasts', {}) if isinstance(chart_data, dict) else {}
    summary: Dict[str, Dict[str, float]] = {}

    for param, data_points in forecasts.items():
        if not data_points or not isinstance(data_points, list):
            continue
        try:
            df = pd.DataFrame(data_points)
            if 'value' not in df.columns:
                continue
            # apply same QC for stats as for charts
            if param in ('precipitation', 'humidity'):
                df = qc_nonnegative_df(df, param)
            s = pd.to_numeric(df['value'], errors='coerce').dropna()
            if not s.empty:
                summary[param] = {
                    'min': float(s.min()),
                    'max': float(s.max()),
                    'avg': float(s.mean()),
                    'std': float(s.std())
                }
        except Exception:
            continue
    return summary
