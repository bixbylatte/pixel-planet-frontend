import streamlit as st
from datetime import datetime
from components.header import render_header
from components.sidebar import render_sidebar
from components.results_ai import render_ai_analysis_card
from components.forecast_graphs import render_forecast_graphs
from api.client import WeatherAPIClient, parse_assessment_response, extract_temperature_range, extract_primary_concern
from api.config import config
import requests

st.set_page_config(
    page_title="Pixelcast",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Tailwind CSS
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

render_header()

# Initialize API client
if 'api_client' not in st.session_state:
    st.session_state.api_client = WeatherAPIClient(
        base_url=config.API_BASE_URL)

# Render sidebar and get the form data
sidebar_data = render_sidebar()

# Main content area
st.markdown("<br>", unsafe_allow_html=True)

# Handle button click from sidebar
if sidebar_data['assess_clicked']:
    # Validate location selection
    if not sidebar_data['location']['name'] or not sidebar_data['location']['latitude']:
        st.error("❌ Please search and select a location first!")
        st.stop()

    # Get start and end datetime directly
    start_datetime = sidebar_data['start_datetime']
    end_datetime = sidebar_data['end_datetime']

    if end_datetime <= start_datetime:
        st.error("❌ End date/time must be after start date/time!")
        st.stop()

    # Show loading spinner
    with st.spinner("🤖 AI Agent is analyzing weather data..."):
        try:
            # Call API
            result = st.session_state.api_client.assess_activity(
                location_name=sidebar_data['location']['name'],
                latitude=sidebar_data['location']['latitude'],
                longitude=sidebar_data['location']['longitude'],
                start_time=start_datetime,
                end_time=end_datetime,
                activity_type=sidebar_data['activity']
            )

            # Parse response
            data = parse_assessment_response(result)

            # Store in session state
            st.session_state.api_result = data
            st.session_state.has_results = True
            st.session_state.sidebar_snapshot = sidebar_data.copy()

            st.success("✅ Analysis complete!")
            st.rerun()

        except requests.exceptions.Timeout:
            st.error(
                "❌ Request timed out. The API might be processing a large dataset. Please try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API Error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                with st.expander("🔍 Error Details"):
                    st.code(e.response.text)
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")
            if config.DEBUG:
                st.exception(e)

# Display results if available
if st.session_state.get('has_results') and st.session_state.get('api_result'):
    data = st.session_state.api_result
    snapshot = st.session_state.get('sidebar_snapshot', sidebar_data)

    # Get assessment data
    assessment = data['raw'].get('assessment', {})

    # Extract temperature range
    temp_range = extract_temperature_range(data['forecast_summary'])

    # Format date range for display
    start_dt = snapshot['start_datetime']
    end_dt = snapshot['end_datetime']

    if start_dt.date() == end_dt.date():
        # Same day
        date_display = f"{start_dt.strftime('%B %d, %Y')} ({start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')})"
    else:
        # Multiple days
        date_display = f"{start_dt.strftime('%b %d')} - {end_dt.strftime('%b %d, %Y')}"

    # Render AI Weather Analysis Card with proper assessment data
    render_ai_analysis_card(
        location=data['location_name'],
        date=date_display,
        activity=snapshot['activity'],
        suitable=assessment.get('suitable', False),
        risk_level=assessment.get('risk_level', 'UNKNOWN'),
        confidence_level=assessment.get('confidence', 'medium'),
        temperature_range=temp_range,
        primary_concerns=assessment.get('primary_concerns', []),
        recommendation=assessment.get('recommendation', ''),
    )

    # Render Forecast Graphs
    st.markdown("## 📊 Weather Forecast")

    # Map selected metrics
    metric_mapping = {
        'temperature': 'temperature',
        'precipitation': 'precipitation',
        'wind_speed': 'wind',
        'humidity': 'humidity'
    }

    selected_metrics = [
        metric_mapping[k]
        for k, v in snapshot['metrics'].items()
        if v and k in metric_mapping
    ]

    if data.get('chart_data'):
        render_forecast_graphs(
            data['chart_data'],
            selected_metrics=selected_metrics if selected_metrics else None
        )
    else:
        st.info("No forecast data available")

    # Debug expander
    if config.DEBUG:
        with st.expander("🔍 Debug: API Response"):
            st.json(data['raw'])

else:
    # Show placeholder
    st.info("👈 Enter your activity details in the sidebar and click **Assess Activity** to get started!")
