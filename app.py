import streamlit as st
from datetime import datetime
from components.header import render_header
from components.sidebar import render_sidebar
from components.results_ai import render_ai_analysis_card
from components.forecast_graphs import render_forecast_graphs
from api.client import WeatherAPIClient, parse_assessment_response, extract_temperature_range
from api.config import config
import requests

# -------------------------------
# Streamlit page setup
# -------------------------------
st.set_page_config(
    page_title="Pixelcast",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Global CSS (Tailwind)
# -------------------------------
st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: {
                            50: '#ecfdf5',
                            100: '#d1fae5',
                            500: '#10b981',
                            600: '#059669',
                            700: '#047857',
                        }
                    }
                }
            }
        }
    </script>
    <style type="text/tailwindcss">
        @layer base {
            * {
                @apply antialiased;
            }
        }
        
        @layer components {
            .card {
                @apply bg-gradient-to-br from-slate-800 to-slate-700 rounded-2xl p-8 shadow-xl;
            }
            
            .badge-success {
                @apply px-4 py-2 rounded-lg text-sm font-medium bg-emerald-500/15 border border-emerald-500/40 text-emerald-500;
            }
            
            .badge-info {
                @apply px-4 py-2 rounded-lg text-sm font-medium bg-blue-500/15 border border-blue-500/40 text-blue-400;
            }
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Header and Sidebar
# -------------------------------
render_header()

if 'api_client' not in st.session_state:
    st.session_state.api_client = WeatherAPIClient(base_url=config.API_BASE_URL)

sidebar_data = render_sidebar()
st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------
# Handle "Assess Activity" button
# -------------------------------
if sidebar_data['assess_clicked']:
    if not sidebar_data['location']['name'] or not sidebar_data['location']['latitude']:
        st.error("❌ Please search and select a location first!")
        st.stop()

    start_datetime = sidebar_data['start_datetime']
    end_datetime = sidebar_data['end_datetime']

    if end_datetime <= start_datetime:
        st.error("❌ End date/time must be after start date/time!")
        st.stop()

    with st.spinner("🤖 AI Agent is analyzing weather data..."):
        try:
            result = st.session_state.api_client.assess_activity(
                location_name=sidebar_data['location']['name'],
                latitude=sidebar_data['location']['latitude'],
                longitude=sidebar_data['location']['longitude'],
                start_time=start_datetime,
                end_time=end_datetime,
                activity_type=sidebar_data['activity']
            )

            data = parse_assessment_response(result)
            st.session_state.api_result = data
            st.session_state.has_results = True
            st.session_state.sidebar_snapshot = sidebar_data.copy()

            st.success("✅ Analysis complete!")
            st.rerun()

        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API Error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                with st.expander("🔍 Error Details"):
                    st.code(e.response.text)
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")
            if config.DEBUG:
                st.exception(e)

# -------------------------------
# Display Results
# -------------------------------
if st.session_state.get('has_results') and st.session_state.get('api_result'):
    data = st.session_state.api_result
    snapshot = st.session_state.get('sidebar_snapshot', sidebar_data)

    raw = data.get("raw", data)
    assessment = raw.get("assessment", {})
    forecast_summary = raw.get("forecast_summary", {})
    location_info = raw.get("location_info") or raw.get("location", {})
    alt_times = raw.get("alternative_times", [])
    summary_text = raw.get("summary")
    chart_data = raw.get("chart_data")

    # -------------------------------
    # Temperature Range
    # -------------------------------
    temp_min = forecast_summary.get("temperature", {}).get("min")
    temp_max = forecast_summary.get("temperature", {}).get("max")
    if temp_min is not None and temp_max is not None:
        temperature_range = f"{round(float(temp_min),1)}–{round(float(temp_max),1)}°C"
    else:
        try:
            temperature_range = extract_temperature_range(data.get("forecast_summary", "")) or "—"
        except Exception:
            temperature_range = "—"

    # -------------------------------
    # Date Display
    # -------------------------------
    tr = raw.get("time_range", {})
    tr_start = tr.get("start")
    tr_end = tr.get("end")
    if tr_start and tr_end:
        try:
            start_dt = datetime.fromisoformat(tr_start)
            end_dt = datetime.fromisoformat(tr_end)
        except Exception:
            start_dt = snapshot['start_datetime']
            end_dt = snapshot['end_datetime']
    else:
        start_dt = snapshot['start_datetime']
        end_dt = snapshot['end_datetime']

    if start_dt.date() == end_dt.date():
        date_display = f"{start_dt.strftime('%B %d, %Y')} ({start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')})"
    else:
        date_display = f"{start_dt.strftime('%b %d')} - {end_dt.strftime('%b %d, %Y')}"

    loc_name = location_info.get("name") or data.get("location_name") or "—"

    # -------------------------------
    # Render AI Analysis Card
    # -------------------------------
    render_ai_analysis_card(
        location=loc_name,
        date=date_display,
        activity=snapshot.get('activity', 'activity'),
        suitable=bool(assessment.get('suitable', False)),
        risk_level=str(assessment.get('risk_level', 'UNKNOWN')),
        temperature_range=temperature_range,
        primary_concerns=assessment.get('primary_concerns', []) or [],
        recommendation=assessment.get('recommendation', '') or summary_text or '',
        alternatives=alt_times  # embedded inside card
    )

    # -------------------------------
    # Forecast Graphs
    # -------------------------------
    st.markdown("## 📊 Weather Forecast")

    metric_mapping = {
        'temperature': 'temperature',
        'precipitation': 'precipitation',
        'wind_speed': 'wind',
        'humidity': 'humidity'
    }
    selected_metrics = [
        metric_mapping[k]
        for k, v in snapshot.get('metrics', {}).items()
        if v and k in metric_mapping
    ]

    if chart_data:
        render_forecast_graphs(
            chart_data,
            selected_metrics=selected_metrics if selected_metrics else None
        )
    else:
        st.info("No forecast data available")

    if config.DEBUG:
        with st.expander("🔍 Full API response (raw)"):
            st.json(raw)

else:
    st.info("👈 Enter your activity details in the sidebar and click **Assess Activity** to get started!")
