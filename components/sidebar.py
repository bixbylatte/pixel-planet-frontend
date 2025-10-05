import streamlit as st
from datetime import datetime, time, timedelta
from api.geocoding import GeocodingService


def render_sidebar():
    """
    Renders the left sidebar with location, date/time, activity, and weather metrics
    Using Tailwind-inspired styling for consistency
    """

    # Tailwind-inspired CSS for sidebar styling
    st.markdown("""
        <style>
        /* Sidebar - Tailwind gray-50 equivalent */
        [data-testid="stSidebar"] {
            background-color: #f9fafb !important;
            padding: 1.5rem 1rem;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            background-color: #f9fafb !important;
        }
        
        /* Section headers - Tailwind text-gray-800, text-base, font-semibold */
        [data-testid="stSidebar"] h3 {
            color: #1f2937 !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.75rem !important;
            margin-top: 1.5rem !important;
        }
        
        [data-testid="stSidebar"] h3:first-of-type {
            margin-top: 0 !important;
        }
        
        /* Text inputs - Tailwind bg-white, border-gray-300, rounded-lg */
        [data-testid="stSidebar"] input[type="text"] {
            background-color: #ffffff !important;
            color: #1f2937 !important;
            padding: 0.75rem !important;
            font-size: 0.875rem !important;
        }
        
        /* Placeholder - Tailwind text-gray-400 */
        [data-testid="stSidebar"] input[type="text"]::placeholder {
            color: #9ca3af !important;
        }
        
        /* Focus state - Tailwind ring-emerald-500, border-emerald-500 */
        [data-testid="stSidebar"] input[type="text"]:focus {
            border-color: #10b981 !important;
            outline: none !important;
        }
        
        /* Date and time inputs - matching text inputs */
        [data-testid="stSidebar"] input[type="date"],
        [data-testid="stSidebar"] input[type="time"] {
            background-color: #ffffff !important;
            color: #1f2937 !important;
            padding: 0.75rem !important;
            font-size: 0.875rem !important;
        }
        
        [data-testid="stSidebar"] input[type="date"]:focus,
        [data-testid="stSidebar"] input[type="time"]:focus {
            border-color: #10b981 !important;
            outline: none !important;
        }
        
        /* Icons - Tailwind text-gray-500 */
        [data-testid="stSidebar"] svg {
            color: #6b7280 !important;
        }
        
        /* Selectbox - Tailwind styling */
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 0.5rem !important;
            min-height: 44px !important;
        }
        
        [data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
            border-color: #10b981 !important;
        }
        
        [data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
            border-color: #10b981 !important;
        }
        
        [data-testid="stSidebar"] [data-baseweb="select"] div[role="button"] {
            color: #1f2937 !important;
        }
        
        /* Column spacing - Tailwind gap-1 */
        [data-testid="stSidebar"] [data-testid="column"] {
            padding: 0 0.25rem !important;
        }
        
        [data-testid="stSidebar"] [data-testid="column"]:first-child {
            padding-left: 0 !important;
        }
        
        [data-testid="stSidebar"] [data-testid="column"]:last-child {
            padding-right: 0 !important;
        }
        
        /* Spacing - Tailwind mb-2 */
        [data-testid="stSidebar"] .element-container {
            margin-bottom: 0.5rem !important;
        }
        
        /* Full width containers */
        [data-testid="stSidebar"] [data-testid="stDateInput"],
        [data-testid="stSidebar"] [data-testid="stTimeInput"] {
            width: 100%;
        }
        
        /* Assess Activity Button Styling */
        [data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 0.75rem !important;
            border: none !important;
            width: 100% !important;
            font-size: 1rem !important;
            margin-top: 1.5rem !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
            transition: all 0.2s !important;
        }
        
        [data-testid="stSidebar"] button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize geocoding service
    if 'geocoding_service' not in st.session_state:
        st.session_state.geocoding_service = GeocodingService()

    with st.sidebar:
        # ═══════════════════════════════════════
        # LOCATION SECTION WITH SEARCH
        # ═══════════════════════════════════════
        st.markdown("### Location")

        # Initialize selected location in session state
        if 'selected_location' not in st.session_state:
            st.session_state.selected_location = None

        # Initialize search results cache
        if 'location_search_results' not in st.session_state:
            st.session_state.location_search_results = []

        # Show currently selected location first
        if st.session_state.selected_location:
            st.success(f"📍 {st.session_state.selected_location.display_name}")
            st.info(
                f"🌐 {st.session_state.selected_location.latitude:.4f}, {st.session_state.selected_location.longitude:.4f}")

            if st.button("🔄 Change Location", key="clear_location"):
                st.session_state.selected_location = None
                st.session_state.location_search_results = []
                st.rerun()
        else:
            # Location search input
            location_query = st.text_input(
                "Search Location",
                placeholder="Search for a location...",
                label_visibility="collapsed",
                key="location_search",
                help="Start typing to search for locations"
            )

            # Search for locations when query changes
            if location_query and len(location_query) >= 2:
                # Only search if query changed
                if 'last_query' not in st.session_state or st.session_state.last_query != location_query:
                    with st.spinner("🔍 Searching..."):
                        locations = st.session_state.geocoding_service.search_locations(
                            location_query)
                        st.session_state.location_search_results = locations
                        st.session_state.last_query = location_query
                else:
                    locations = st.session_state.location_search_results

                if locations:
                    # Create a mapping of display names to location objects
                    # Use index to ensure unique keys
                    location_map = {
                        f"{loc.display_name}": loc for loc in locations}
                    location_options = [
                        "Select a location..."] + list(location_map.keys())

                    selected_key = st.selectbox(
                        "Select Location",
                        options=location_options,
                        label_visibility="collapsed",
                        key="location_selector",
                        index=0
                    )

                    # Store selected location when user makes a selection
                    if selected_key != "Select a location...":
                        selected_loc = location_map[selected_key]
                        if selected_loc:
                            st.session_state.selected_location = selected_loc
                            # Clear search state
                            st.session_state.location_search_results = []
                            if 'last_query' in st.session_state:
                                del st.session_state.last_query
                            st.rerun()
                else:
                    st.warning(
                        "No locations found. Try a different search term.")
            else:
                # Clear search results when query is too short
                if st.session_state.location_search_results:
                    st.session_state.location_search_results = []

        # ═══════════════════════════════════════
        # DATE & TIME RANGE SECTION
        # ═══════════════════════════════════════
        st.markdown("### Date & Time Range")

        # Date range picker
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        st.markdown("**Start Date & Time**")
        start_date = st.date_input(
            "Start Date",
            value=today,
            format="MM/DD/YYYY",
            label_visibility="collapsed",
            key="start_date_input",
            min_value=today
        )

        start_time = st.time_input(
            "Start Time",
            value=time(9, 0),
            label_visibility="collapsed",
            key="start_time_input",
            step=3600
        )

        st.markdown("**End Date & Time**")

        # end date must be >= start date; suggest +1 day
        suggested_end = start_date + timedelta(days=1)

        # if there is a prior selection, keep it but clamp to start_date+
        prev_end = st.session_state.get("end_date_input", suggested_end)
        end_default = max(prev_end, start_date)

        end_date = st.date_input(
            "End Date",
            value=end_default,
            format="MM/DD/YYYY",
            label_visibility="collapsed",
            key="end_date_input",
            min_value=start_date,
        )

        end_time = st.time_input(
            "End Time",
            value=st.session_state.get("end_time_input", time(17, 0)),
            label_visibility="collapsed",
            key="end_time_input",
            step=3600
        )

        # ═══════════════════════════════════════
        # ACTIVITY TYPE SECTION
        # ═══════════════════════════════════════
        st.markdown("### Activity Type")

        activity_options = [
            "🥾 Hiking",
            "🏖️ Beach day",
            "🚴 Cycling",
            "🎵 Outdoor concert",
            "🏕️ Camping",
            "🏄 Surfing",
            "📷 Photography",
            "🧺 Picnic",
            "🏃 Running",
            "🎣 Fishing"
        ]

        activity_type = st.selectbox(
            "Activity",
            options=activity_options,
            index=0,
            label_visibility="collapsed",
            key="activity_select"
        )

        # Custom activity input
        custom_activity = st.text_input(
            "Custom activity",
            placeholder="Custom activity (e.g., Wedding, Photo shoot)",
            label_visibility="collapsed",
            key="custom_activity_input"
        )

        # ═══════════════════════════════════════
        # WEATHER METRICS SECTION
        # ═══════════════════════════════════════
        # st.markdown("### Weather Metrics")

        # Initialize session state for checkboxes if not exists
        if 'metrics' not in st.session_state:
            st.session_state.metrics = {
                'temperature': True,
                'precipitation': True,
                'wind_speed': True,
                'humidity': True
            }

        

        # Update session state
        st.session_state.metrics['temperature'] = True
        st.session_state.metrics['precipitation'] = True
        st.session_state.metrics['wind_speed'] = True
        st.session_state.metrics['humidity'] = True

        # ═══════════════════════════════════════
        # ASSESS ACTIVITY BUTTON
        # ═══════════════════════════════════════
        assess_button = st.button("🚀 Assess Activity", type="primary",
                                  use_container_width=True, key="assess_activity_btn")

    # Return the collected form data as a dictionary
    # Clean up the emoji from activity type in the return value
    activity_value = activity_type.split(
        " ", 1)[1] if " " in activity_type else activity_type

    # Get location data from selected location
    location_data = {
        'name': st.session_state.selected_location.display_name if st.session_state.selected_location else None,
        'latitude': st.session_state.selected_location.latitude if st.session_state.selected_location else None,
        'longitude': st.session_state.selected_location.longitude if st.session_state.selected_location else None
    }

    # Combine date and time into datetime objects
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)

    return {
        'location': location_data,
        'start_datetime': start_datetime,
        'end_datetime': end_datetime,
        'activity': custom_activity if custom_activity else activity_value,
        'metrics': st.session_state.metrics,
        'assess_clicked': assess_button
    }
