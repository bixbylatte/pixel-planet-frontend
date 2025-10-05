import streamlit as st
import streamlit.components.v1 as components
from typing import Optional, List, Any


def render_ai_analysis_card(
    location: str = "San Francisco, CA",
    date: str = "June 15, 2025",
    activity: str = "hiking",
    suitable: bool = True,
    risk_level: str = "LOW",
    temperature_range: str = "68-75°F",
    primary_concerns: List[str] = None,
    recommendation: str = None,
    alternatives: Optional[List[Any]] = None,
):
    """
    Renders the AI Weather Analysis card using Tailwind CSS based on API assessment data.
    Includes embedded Alternative Windows.
    """

    # --- Initialize safe defaults for all dynamic variables ---
    recommendation_html = ""
    concerns_html = ""
    risk_bg = "bg-gray-500/15"
    risk_border = "border-gray-500/40"
    risk_text = "text-gray-500"
    risk_icon = "⚪"

    # --- Default icons and condition colors ---
    condition_icon = "ℹ️"
    condition_color = "text-white/80"
    condition_text = "Conditions unavailable"

    # --- Define condition text based on suitability and risk level ---
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
        else:
            condition_text = "High risk conditions"
            condition_color = "text-red-500"
            condition_icon = "🚫"
    else:
        condition_text = "Not recommended"
        condition_color = "text-red-500"
        condition_icon = "❌"

    # --- Build AI recommendation section ---
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

    # --- Build primary concerns section ---
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

    # --- Risk badge style mapping ---
    risk_badge_colors = {
        "low": ("bg-emerald-500/15", "border-emerald-500/40", "text-emerald-500", "🟢"),
        "caution": ("bg-yellow-500/15", "border-yellow-500/40", "text-yellow-500", "🟡"),
        "high": ("bg-orange-500/15", "border-orange-500/40", "text-orange-500", "🟠"),
        "extreme": ("bg-red-500/15", "border-red-500/40", "text-red-500", "🔴"),
    }

    key = risk_level.lower()
    if key in risk_badge_colors:
        risk_bg, risk_border, risk_text, risk_icon = risk_badge_colors[key]

    # --- Confidence badge (optional) ---
    confidence_badge_colors = {
        "high": ("bg-emerald-500/15", "border-emerald-500/40", "text-emerald-500"),
        "medium": ("bg-yellow-500/15", "border-yellow-500/40", "text-yellow-500"),
        "low": ("bg-red-500/15", "border-red-500/40", "text-red-500"),
    }

    # --- Suitability text and color ---
    if suitable:
        suitability_text = "✓ Suitable"
        suitability_color = "text-emerald-400"
    else:
        suitability_text = "✗ Not Suitable"
        suitability_color = "text-red-400"

    # --- Build Alternative Windows Section ---
    alt_html = ""
    if isinstance(alternatives, list) and alternatives:
        alt_cards = []
        for w in alternatives:
            if isinstance(w, dict):
                s = w.get("start", "—")
                e = w.get("end", "—")
                r = w.get("reason", "")
                alt_cards.append(f"""
                    <div class="rounded-xl border border-slate-600/40 bg-slate-700/40 p-4">
                        <div class="text-white/90 text-sm font-semibold">{s} → {e}</div>
                        <div class="text-white/60 text-sm mt-1">{r}</div>
                    </div>
                """)
            else:
                alt_cards.append(f"""
                    <div class="rounded-xl border border-slate-600/40 bg-slate-700/40 p-4">
                        <div class="text-white/80 text-sm">{w}</div>
                    </div>
                """)
        alt_html = f"""
            <div class="mt-6">
                <h3 class="text-white text-sm font-semibold flex items-center gap-2">
                    <span>🗓️</span><span>Alternative Windows</span>
                </h3>
                <div class="mt-3 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
                    {''.join(alt_cards)}
                </div>
            </div>
        """

    # --- HTML Card ---
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
                            primary: {{ 500:'#10b981', 600:'#059669' }}
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
                <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-3 w-14 h-14 flex items-center justify-center text-3xl flex-shrink-0">✨</div>
                <div class="flex-1">
                    <h2 class="text-white text-3xl font-bold mb-2 leading-tight">AI Weather Analysis</h2>
                    <p class="text-white/60 text-sm leading-relaxed m-0">
                        Based on NASA POWER observation data • {location} • {date}
                    </p>
                </div>
            </div>

            <!-- Content -->
            <div class="mt-4">
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

                {recommendation_html}
                {concerns_html}
                {alt_html}

                <div class="flex gap-3 mt-6 flex-wrap">
                    <div class="px-4 py-2 rounded-lg text-sm font-medium {risk_bg} border {risk_border} {risk_text} flex items-center gap-2">
                        <span>{risk_icon}</span>
                        <span>Risk: {risk_level.upper()}</span>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(html_content, height=800)
