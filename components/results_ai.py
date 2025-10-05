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
    # defaults
    recommendation_html = ""
    concerns_html = ""
    risk_bg = "bg-gray-500/15"
    risk_border = "border-gray-500/40"
    risk_text = "text-gray-600"
    risk_icon = "⚪"

    condition_icon = "ℹ️"
    condition_color = "text-slate-700"
    condition_text = "Conditions unavailable"

    risk = str(risk_level).upper().strip()
    RISK_MAP = {
        "LOW":       ("Excellent conditions",          "text-emerald-600", "✅"),
        "CAUTION":   ("Good conditions with caution",  "text-blue-600",    "ℹ️"),
        "MODERATE":  ("Moderate risk conditions",      "text-amber-600",   "⚠️"),
        "HIGH":      ("High risk – plan carefully",    "text-orange-600",  "🟠"),
        "EXTREME":   ("Extreme risk – reconsider",     "text-red-600",     "🚫"),
    }

    if not suitable:
        condition_text, condition_color, condition_icon = ("Not recommended", "text-red-600", "❌")
    else:
        condition_text, condition_color, condition_icon = RISK_MAP.get(
            risk, ("Mixed signals", "text-blue-600", "ℹ️")
        )

    if recommendation:
        recommendation_html = f"""
            <div class="flex items-start gap-3 my-4 bg-blue-50 rounded-lg p-4 border border-blue-200">
                <span class="text-blue-600 text-lg flex-shrink-0 mt-0.5">💡</span>
                <div>
                    <p class="text-blue-700 text-xs font-semibold uppercase mb-1">AI Recommendation</p>
                    <span class="text-slate-800 text-[0.95rem] leading-relaxed">{recommendation}</span>
                </div>
            </div>
        """

    if primary_concerns and len(primary_concerns) > 0:
        concerns_items = ""
        for concern in primary_concerns:
            concerns_items += f"""
                <div class="flex items-center gap-2 mb-2">
                    <span class="text-amber-600 text-sm">⚠️</span>
                    <span class="text-slate-700 text-sm">{concern}</span>
                </div>
            """
        concerns_html = f"""
            <div class="my-4 bg-amber-50 rounded-lg p-4 border border-amber-200">
                <p class="text-amber-700 text-xs font-semibold uppercase mb-3">Primary Concerns</p>
                {concerns_items}
            </div>
        """

    risk_badge_colors = {
        "low":      ("bg-emerald-500/10", "border-emerald-500/30", "text-emerald-700", "🟢"),
        "caution":  ("bg-yellow-500/10",  "border-yellow-500/30",  "text-yellow-700",  "🟡"),
        "moderate": ("bg-amber-500/10",   "border-amber-500/30",   "text-amber-700",   "⚠️"),
        "high":     ("bg-orange-500/10",  "border-orange-500/30",  "text-orange-700",  "🟠"),
        "extreme":  ("bg-red-500/10",     "border-red-500/30",     "text-red-700",     "🔴"),
    }
    risk_bg, risk_border, risk_text, risk_icon = risk_badge_colors.get(
        risk.lower(), ("bg-blue-500/10", "border-blue-500/30", "text-blue-700", "ℹ️")
    )

    suitability_text = "✓ Suitable" if suitable else "✗ Not Suitable"
    suitability_color = "text-emerald-700" if suitable else "text-red-700"

    alt_html = ""
    if isinstance(alternatives, list) and alternatives:
        cards = []
        for w in alternatives:
            if isinstance(w, dict):
                s = w.get("start", "—"); e = w.get("end", "—"); r = w.get("reason", "")
                cards.append(f"""
                    <div class="rounded-xl border border-slate-200 bg-white p-4">
                        <div class="text-slate-900 text-sm font-semibold">{s} → {e}</div>
                        <div class="text-slate-600 text-sm mt-1">{r}</div>
                    </div>
                """)
            else:
                cards.append(f"""
                    <div class="rounded-xl border border-slate-200 bg-white p-4">
                        <div class="text-slate-700 text-sm">{w}</div>
                    </div>
                """)
        alt_html = f"""
            <div class="mt-6">
                <h3 class="text-slate-900 text-sm font-semibold flex items-center gap-2">
                    <span>🗓️</span><span>Alternative Windows</span>
                </h3>
                <div class="mt-3 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
                    {''.join(cards)}
                </div>
            </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {{
                theme: {{
                    extend: {{
                        colors: {{ primary: {{ 500:'#10b981', 600:'#059669' }} }}
                    }}
                }}
            }}
        </script>
    </head>
    <body class="m-0 p-0 font-sans antialiased">
        <div class="bg-gradient-to-br from-white to-slate-50 rounded-2xl p-8 shadow-xl border border-slate-200">
            <!-- Header -->
            <div class="flex items-start gap-4 mb-6">
                <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-3 w-14 h-14 flex items-center justify-center text-3xl flex-shrink-0 text-white">✨</div>
                <div class="flex-1">
                    <h2 class="text-slate-900 text-3xl font-bold mb-2 leading-tight">AI Weather Analysis</h2>
                    <p class="text-slate-600 text-sm leading-relaxed m-0">
                        Based on NASA Open Dataset • {location} • {date}
                    </p>
                </div>
            </div>

            <!-- Content -->
            <div class="mt-4">
                <div class="flex items-center gap-3 mb-4">
                    <span class="text-3xl">{condition_icon}</span>
                    <div>
                        <p class="text-slate-900 text-lg leading-tight">
                            <span class="{condition_color} font-bold">{condition_text}</span>
                            <span class="text-slate-600">for your {activity} activity</span>
                        </p>
                        <p class="text-slate-600 text-sm mt-1">
                            Temperature: <span class="text-slate-900 font-medium">{temperature_range}</span> •
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
    components.html(html_content, height=850, scrolling=True)
