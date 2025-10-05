import streamlit as st
import streamlit.components.v1 as components


def render_header():
    """
    Renders the PixelCast header component with logo and subtitle using Tailwind CSS
    Similar to a React component: <Header />
    """

    # Header HTML structure with Tailwind classes
    header_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="m-0 p-0">
        <div class="flex items-center py-4 mb-2 border-b border-gray-200">
            <div class="flex items-center gap-3">
                <div class="bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-lg p-2 flex items-center justify-center w-9 h-9 text-xl">
                    🌍
                </div>
                <h1 class="text-2xl font-semibold text-gray-800 m-0 leading-none">
                    PixelCast
                </h1>
                <p class="text-sm text-gray-600 m-0 ml-4 pl-4 border-l border-gray-300">
                    Powered by NASA Open Dataset
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(header_html, height=80)
