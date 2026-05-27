from flask import Flask, render_template_string
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    # This HTML/JS structure runs locally inside your Android app shell
    html_dashboard = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SafePass Command Terminal</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        
        <style>
            body { 
                background-color: #000000; 
                color: #e50914; 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
                margin: 0; 
                padding: 15px; 
            }
            .header { 
                text-align: center; 
                border-bottom: 2px solid #e50914; 
                padding-bottom: 12px; 
                margin-bottom: 15px;
            }
            .status-box { 
                background: #121212; 
                padding: 12px; 
                border-radius: 6px; 
                margin-bottom: 15px; 
                border-left: 4px solid #e50914;
                font-size: 14px;
            }
            #map { 
                height: 65vh; 
                width: 100%; 
                border: 1px solid #e50914; 
                border-radius: 8px; 
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h2 style="margin: 0; letter-spacing: 1px;">SAFEPASS TERMINAL</h2>
            <small style="color: #666; font-weight: bold;">POWERED BY DTECH</small>
        </div>
        
        <div class="status-box">
            <span style="color: #888;">System Node:</span> <strong style="color: #fff;">Active Monitoring</strong>
        </div>

        <div id="map"></div>

        <script>
            // Initialize the map coordinate center
            var map = L.map('map', { zoomControl: false }).setView([9.0820, 8.6753], 6);
            
            // Apply a sleek, dark-mode map style that fits your crimson palette
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_dashboard)

def run_server():
    # Flask serves the assets locally inside the native app loop
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    while True:
        time.sleep(1)
