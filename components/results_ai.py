import streamlit as st
import streamlit.components.v1 as components
from typing import Optional, List


def render_ai_analysis_card(
    location: str = "San Francisco, CA",
    date: str = "June 15, 2025",
    activity: str = "hiking",
    suitable: bool = True,
    risk_level: str = "LOW",
    confidence_level: str = "high",
    temperature_range: str = "68-75°F",
    primary_concerns: List[str] = None,
    recommendation: str = None
):
    """
    Renders the AI Weather Analysis card using Tailwind CSS based on API assessment data

    Args:
        location: Location name
        date: Date string
        activity: Activity type
        suitable: Whether conditions are suitable (True/False)
        risk_level: Risk level (LOW, CAUTION, HIGH, EXTREME)
        confidence_level: Confidence level (high, medium, low)
        temperature_range: Temperature range string
        primary_concerns: List of primary concern strings
        recommendation: Main recommendation text from AI
    """

    # Map risk levels to condition text and colors
    # Risk levels from API: LOW, CAUTION, HIGH, EXTREME
    if suitable:
        if risk_level.upper() == "LOW":
            condition_text = "Excellent conditions"
            condition_color = "text-emerald-500"
            condition_icon = "✅"
        elif risk_level.upper() == "CAUTION":
            condition_text = "Good conditions with caution"
            condition_color = "text-blue-500"
            condition_icon = "ℹ️"
        elif risk_level.upper() == "HIGH":
            condition_text = "Proceed with caution"
            condition_color = "text-amber-500"
            condition_icon = "⚠️"
        else:  # EXTREME
            condition_text = "High risk conditions"
            condition_color = "text-red-500"
            condition_icon = "🚫"
    else:
        condition_text = "Not recommended"
        condition_color = "text-red-500"
        condition_icon = "❌"

    # Build recommendation section
    recommendation_html = ""
    if recommendation:
        recommendation_html = f"""
            <div class="flex items-start gap-3 my-4 bg-blue-500/10 rounded-lg p-4 border border-blue-500/20">
                <span class="text-blue-400 text-lg flex-shrink-0 mt-0.5">💡</span>
                <div>
                    <p class="text-blue-300 text-xs font-semibold uppercase mb-1">AI Recommendation</p>
                    <span class="text-white/90 text-[0.95rem] leading-relaxed">{recommendation}</span>
                </div>
            </div>
        """

    # Build primary concerns section
    concerns_html = ""
    if primary_concerns and len(primary_concerns) > 0:
        concerns_items = ""
        for concern in primary_concerns:
            concerns_items += f"""
                <div class="flex items-center gap-2 mb-2">
                    <span class="text-amber-400 text-sm">⚠️</span>
                    <span class="text-white/80 text-sm">{concern}</span>
                </div>
            """

        concerns_html = f"""
            <div class="my-4 bg-amber-500/10 rounded-lg p-4 border border-amber-500/20">
                <p class="text-amber-300 text-xs font-semibold uppercase mb-3">Primary Concerns</p>
                {concerns_items}
            </div>
        """

    # Risk level badge color mapping
    risk_badge_colors = {
        "low": ("bg-emerald-500/15", "border-emerald-500/40", "text-emerald-500", "🟢"),
        "caution": ("bg-yellow-500/15", "border-yellow-500/40", "text-yellow-500", "🟡"),
        "high": ("bg-orange-500/15", "border-orange-500/40", "text-orange-500", "🟠"),
        "extreme": ("bg-red-500/15", "border-red-500/40", "text-red-500", "🔴")
    }

    risk_key = risk_level.lower()
    risk_bg, risk_border, risk_text, risk_icon = risk_badge_colors.get(
        risk_key,
        ("bg-gray-500/15", "border-gray-500/40", "text-gray-500", "⚪")
    )

    # Confidence level badge colors
    confidence_badge_colors = {
        "high": ("bg-emerald-500/15", "border-emerald-500/40", "text-emerald-500"),
        "medium": ("bg-yellow-500/15", "border-yellow-500/40", "text-yellow-500"),
        "low": ("bg-red-500/15", "border-red-500/40", "text-red-500")
    }

    conf_key = confidence_level.lower()
    conf_bg, conf_border, conf_text = confidence_badge_colors.get(
        conf_key,
        ("bg-gray-500/15", "border-gray-500/40", "text-gray-500")
    )

    # Format display text
    risk_display = risk_level.upper()
    confidence_display = confidence_level.title()

    # Suitability text
    suitability_text = "✓ Suitable" if suitable else "✗ Not Suitable"
    suitability_color = "text-emerald-400" if suitable else "text-red-400"

    # Complete HTML card with Tailwind
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {{
                theme: {{
                    extend: {{
                        colors: {{
                            primary: {{
                                500: '#10b981',
                                600: '#059669',
                            }}
                        }}
                    }}
                }}
            }}
        </script>
    </head>
    <body class="m-0 p-0 font-sans antialiased">
        <div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-2xl p-8 shadow-xl">
            <!-- Header -->
            <div class="flex items-start gap-4 mb-6">
                <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-3 w-14 h-14 flex items-center justify-center text-3xl flex-shrink-0">
                    ✨
                </div>
                <div class="flex-1">
                    <h2 class="text-white text-3xl font-bold mb-2 leading-tight">
                        AI Weather Analysis
                    </h2>
                    <p class="text-white/60 text-sm leading-relaxed m-0">
                        Based on NASA Earth observation data • {location} • {date}
                    </p>
                </div>
            </div>
            
            <!-- Content -->
            <div class="mt-4">
                <!-- Condition Summary -->
                <div class="flex items-center gap-3 mb-4">
                    <span class="text-3xl">{condition_icon}</span>
                    <div>
                        <p class="text-white text-lg leading-tight">
                            <span class="{condition_color} font-bold">{condition_text}</span> 
                            <span class="text-white/60">for your {activity} activity</span>
                        </p>
                        <p class="text-white/60 text-sm mt-1">
                            Temperature: <span class="text-white font-medium">{temperature_range}</span> • 
                            <span class="{suitability_color} font-medium">{suitability_text}</span>
                        </p>
                    </div>
                </div>
                
                <!-- AI Recommendation -->
                {recommendation_html}
                
                <!-- Primary Concerns -->
                {concerns_html}
                
                <!-- Status Badges -->
                <div class="flex gap-3 mt-6 flex-wrap">
                    <div class="px-4 py-2 rounded-lg text-sm font-medium {risk_bg} border {risk_border} {risk_text} flex items-center gap-2">
                        <span>{risk_icon}</span>
                        <span>Risk: {risk_display}</span>
                    </div>
                    <div class="px-4 py-2 rounded-lg text-sm font-medium {conf_bg} border {conf_border} {conf_text}">
                        Confidence: {confidence_display}
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Use components.html for proper HTML rendering
    # Increased height to accommodate all content
    components.html(html_content, height=550)
