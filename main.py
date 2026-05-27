import os
import sys

# ⚙️ Force Kivy to utilize the updated ANGLE system using Direct3D 11 backend drivers
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
os.environ['KIVY_ANGLE_PLATFORM'] = 'd3d11'

import requests
import json
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

# 🗺️ Import MapSource cleanly from the top-level package
from kivy_garden.mapview import MapView, MapMarker, MapSource

# 📡 Import Plyer GPS API wrapper for true hardware binding
from plyer import gps

# ⚠️ YOUR ACTIVE FIREBASE URL
FIREBASE_URL = "https://safep-caca1-default-rtdb.firebaseio.com/"

KV = '''
MDScreenManager:
    id: screen_manager
    LoginScreen:
    RegisterScreen:
    UserDashboard:
    BookTripScreen:
    PaymentScreen:
    LiveTrackingScreen:
    AdminDashboard:

<LoginScreen>:
    name: "login_screen"
    md_bg_color: 0, 0, 0, 1  # Deep Black
    
    MDBoxLayout:
        orientation: "vertical"
        padding: "32dp"
        spacing: "20dp"
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {"center_x": .5, "center_y": .5}
        
        MDLabel:
            text: "Safe Pass Tracker"
            font_style: "H4"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.86, 0.08, 0.24, 1  # Crimson Red
            size_hint_y: None
            height: "60dp"
            
        MDTextField:
            id: email_field
            hint_text: "Email Address"
            mode: "rectangle"
            line_color_focus: 0.86, 0.08, 0.24, 1
            hint_text_color_focus: 0.86, 0.08, 0.24, 1
            size_hint_y: None
            height: "50dp"
            
        MDTextField:
            id: password_field
            hint_text: "Password"
            password: True
            mode: "rectangle"
            line_color_focus: 0.86, 0.08, 0.24, 1
            hint_text_color_focus: 0.86, 0.08, 0.24, 1
            size_hint_y: None
            height: "50dp"
            
        MDRaisedButton:
            text: "Login"
            md_bg_color: 0.86, 0.08, 0.24, 1
            pos_hint: {"center_x": .5}
            size_hint_x: .8
            on_release: app.login_user(email_field.text, password_field.text)
                
        MDFlatButton:
            text: "Don't have an account? Sign Up"
            theme_text_color: "Custom"
            text_color: 0.86, 0.08, 0.24, 1
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = "register_screen"

<RegisterScreen>:
    name: "register_screen"
    md_bg_color: 0, 0, 0, 1
    
    MDBoxLayout:
        orientation: "vertical"
        padding: "32dp"
        spacing: "20dp"
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {"center_x": .5, "center_y": .5}
        
        MDLabel:
            text: "Create Account"
            font_style: "H5"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.86, 0.08, 0.24, 1
            size_hint_y: None
            height: "50dp"
            
        MDTextField:
            id: username_field
            hint_text: "Username"
            mode: "rectangle"
            line_color_focus: 0.86, 0.08, 0.24, 1
            size_hint_y: None
            height: "50dp"
            
        MDTextField:
            id: email_field
            hint_text: "Email Address"
            mode: "rectangle"
            line_color_focus: 0.86, 0.08, 0.24, 1
            size_hint_y: None
            height: "50dp"
            
        MDTextField:
            id: password_field
            hint_text: "Password"
            password: True
            mode: "rectangle"
            line_color_focus: 0.86, 0.08, 0.24, 1
            size_hint_y: None
            height: "50dp"
            
        MDRaisedButton:
            text: "Register"
            md_bg_color: 0.86, 0.08, 0.24, 1
            pos_hint: {"center_x": .5}
            size_hint_x: .8
            on_release: app.register_user(username_field.text, email_field.text, password_field.text)
                
        MDFlatButton:
            text: "Back to Login"
            theme_text_color: "Custom"
            text_color: 0.86, 0.08, 0.24, 1
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = "login_screen"

<UserDashboard>:
    name: "user_dashboard"
    md_bg_color: 0, 0, 0, 1
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "SafePass Dashboard"
            background_color: 0.1, 0.1, 0.1, 1
            specific_text_color: 0.86, 0.08, 0.24, 1
            elevation: 4
            right_action_items: [["logout", lambda x: app.process_logout()]]
            
        MDBoxLayout:
            orientation: "vertical"
            padding: "24dp"
            spacing: "24dp"
            
            MDLabel:
                id: dashboard_title
                text: "Welcome back!"
                font_style: "H6"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_y: None
                height: "40dp"
                
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                size_hint_x: .95
                size_hint_y: None
                height: "180dp"
                pos_hint: {"center_x": .5}
                md_bg_color: 0.1, 0.1, 0.1, 1
                radius: [12, 12, 12, 12]
                
                MDLabel:
                    text: "Plan Your Next Journey"
                    font_style: "Subtitle1"
                    theme_text_color: "Custom"
                    text_color: 0.86, 0.08, 0.24, 1
                    halign: "center"
                    
                MDLabel:
                    text: "Register destination coordinates securely and authorize live tracking channels cleanly."
                    font_style: "Body2"
                    theme_text_color: "Custom"
                    text_color: 0.7, 0.7, 0.7, 1
                    halign: "center"

                MDRaisedButton:
                    text: "Book A New Trip"
                    md_bg_color: 0.86, 0.08, 0.24, 1
                    pos_hint: {"center_x": .5}
                    on_release: root.manager.current = "book_trip_screen"
                    
            Widget:

<BookTripScreen>:
    name: "book_trip_screen"
    md_bg_color: 0, 0, 0, 1
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "New Booking"
            background_color: 0.1, 0.1, 0.1, 1
            specific_text_color: 0.86, 0.08, 0.24, 1
            right_action_items: [["logout", lambda x: app.process_logout()]]
            
        MDBoxLayout:
            orientation: "vertical"
            padding: "24dp"
            spacing: "16dp"
            
            MDLabel:
                text: "Trip Details"
                font_style: "H5"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.86, 0.08, 0.24, 1
                size_hint_y: None
                height: "30dp"
                
            MDTextField:
                id: pickup_field
                hint_text: "Starting Location / Pickup"
                mode: "rectangle"
                line_color_focus: 0.86, 0.08, 0.24, 1
                
            MDTextField:
                id: dropoff_field
                hint_text: "Destination / Drop-off"
                mode: "rectangle"
                line_color_focus: 0.86, 0.08, 0.24, 1
                
            MDTextField:
                id: scheduled_time
                hint_text: "Departure Time (e.g. 14:30)"
                mode: "rectangle"
                line_color_focus: 0.86, 0.08, 0.24, 1

            MDRaisedButton:
                text: "Proceed to Payment Verification"
                md_bg_color: 0.86, 0.08, 0.24, 1
                size_hint_x: 1
                on_release: app.submit_trip_form(pickup_field.text, dropoff_field.text, scheduled_time.text)
                
            MDFlatButton:
                text: "Cancel Booking"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.6
                pos_hint: {"center_x": .5}
                on_release: root.manager.current = "user_dashboard"

<PaymentScreen>:
    name: "payment_screen"
    md_bg_color: 0, 0, 0, 1
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Bank Settlement Gate"
            background_color: 0.1, 0.1, 0.1, 1
            specific_text_color: 0.86, 0.08, 0.24, 1
            right_action_items: [["logout", lambda x: app.process_logout()]]
            
        MDBoxLayout:
            orientation: "vertical"
            padding: "24dp"
            spacing: "20dp"
            
            MDLabel:
                text: "Manual Bank Transfer Details"
                font_style: "H6"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.86, 0.08, 0.24, 1
                
            MDCard:
                orientation: "vertical"
                padding: "20dp"
                spacing: "10dp"
                size_hint_y: None
                height: "160dp"
                md_bg_color: 0.1, 0.1, 0.1, 1
                radius: [8, 8, 8, 8]
                
                MDLabel:
                    text: "BANK: Providus Bank"
                    font_style: "Subtitle1"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                MDLabel:
                    text: "A/C NAME: SAFEPASS TECHNOLOGIES LTD"
                    font_style: "Subtitle1"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                MDLabel:
                    text: "A/C NO: 1309430532"
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: 0.86, 0.08, 0.24, 1
                MDLabel:
                    text: "AMOUNT DUE: ₦2,000"
                    font_style: "Subtitle2"
                    theme_text_color: "Custom"
                    text_color: 0.7, 0.7, 0.7, 1

            MDRaisedButton:
                text: "I Have Transferred - Start Trip"
                md_bg_color: 0.86, 0.08, 0.24, 1
                size_hint_x: 1
                size_hint_y: None
                height: "50dp"
                on_release: app.confirm_payment_and_start()

<LiveTrackingScreen>:
    name: "live_tracking_screen"
    md_bg_color: 0, 0, 0, 1
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            id: tracking_bar
            title: "Locating hardware coordinate grids..."
            background_color: 0.1, 0.1, 0.1, 1
            specific_text_color: 0.86, 0.08, 0.24, 1
            right_action_items: [["logout", lambda x: app.process_logout()]]
            
        MDBoxLayout:
            id: map_container
            orientation: "vertical"
            
        # 💬 Messenger layout inside User Viewport Screen
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: "160dp"
            padding: "8dp"
            spacing: "6dp"
            md_bg_color: 0.05, 0.05, 0.05, 1
            
            ScrollView:
                MDLabel:
                    id: user_chat_logs
                    text: "--- Safety Channel Active ---\\n"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "Caption"
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None
                    
            MDBoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: "45dp"
                spacing: "8dp"
                
                MDTextField:
                    id: user_message_input
                    hint_text: "Message Control Terminal..."
                    mode: "rectangle"
                    line_color_focus: 0.86, 0.08, 0.24, 1
                    
                MDRaisedButton:
                    text: "Send"
                    md_bg_color: 0.86, 0.08, 0.24, 1
                    on_release: app.send_message_payload(user_message_input.text, "User")

        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: "65dp"
            padding: "10dp"
            md_bg_color: 0.1, 0.1, 0.1, 1
            
            MDRaisedButton:
                text: "End Active Journey"
                md_bg_color: 0.86, 0.08, 0.24, 1
                size_hint_x: 1
                on_release: app.end_active_trip()

<AdminDashboard>:
    name: "admin_dashboard"
    md_bg_color: 0, 0, 0, 1
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            id: admin_topbar
            title: "SafePass HQ Command Terminal"
            background_color: 0.1, 0.1, 0.1, 1
            specific_text_color: 0.86, 0.08, 0.24, 1
            right_action_items: [["refresh", lambda x: app.refresh_admin_stream_nodes()], ["logout", lambda x: app.process_logout()]]
            
        MDBoxLayout:
            orientation: "horizontal"
            
            # Left Navigation Panel - Live Feeds list
            MDBoxLayout:
                orientation: "vertical"
                size_hint_x: 0.3
                md_bg_color: 0.05, 0.05, 0.05, 1
                padding: "10dp"
                spacing: "10dp"
                
                MDLabel:
                    text: "LIVE FEEDS"
                    font_style: "Button"
                    theme_text_color: "Custom"
                    text_color: 0.86, 0.08, 0.24, 1
                    size_hint_y: None
                    height: "30dp"
                    
                ScrollView:
                    MDBoxLayout:
                        id: live_users_box
                        orientation: "vertical"
                        spacing: "8dp"
                        size_hint_y: None
                        height: self.minimum_height

            # Right Viewport Panel - Dedicated Map and Chat
            MDBoxLayout:
                orientation: "vertical"
                size_hint_x: 0.7
                
                MDBoxLayout:
                    id: admin_map_container
                    orientation: "vertical"
                    
                # 💬 Administrative Control Terminal Messenger Layout
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "180dp"
                    padding: "8dp"
                    spacing: "6dp"
                    md_bg_color: 0.08, 0.08, 0.08, 1
                    
                    ScrollView:
                        MDLabel:
                            id: admin_chat_logs
                            text: "Select a live feed node to initialize communications...\\n"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            font_style: "Caption"
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None
                            
                    MDBoxLayout:
                        orientation: "horizontal"
                        size_hint_y: None
                        height: "45dp"
                        spacing: "8dp"
                        
                        MDTextField:
                            id: admin_message_input
                            hint_text: "Transmit message securely..."
                            mode: "rectangle"
                            line_color_focus: 0.86, 0.08, 0.24, 1
                            
                        MDRaisedButton:
                            text: "Transmit"
                            md_bg_color: 0.86, 0.08, 0.24, 1
                            on_release: app.send_message_payload(admin_message_input.text, "HQ_Admin")
                            
                        MDRaisedButton:
                            id: admin_terminate_btn
                            text: "TERMINATE TRIP"
                            md_bg_color: 0.5, 0, 0, 1
                            disabled: True
                            on_release: app.admin_terminate_selected_trip()
'''

class LoginScreen(MDScreen): pass
class RegisterScreen(MDScreen): pass
class UserDashboard(MDScreen): pass
class BookTripScreen(MDScreen): pass
class PaymentScreen(MDScreen): pass
class LiveTrackingScreen(MDScreen): pass
class AdminDashboard(MDScreen): pass

class SafePassTrackerApp(MDApp):
    dialog = None
    current_user_node = ""
    active_trip_id = ""
    map_view = None
    marker = None
    gps_configured = False
    
    # Administrative Scope Vectors
    selected_admin_user_node = ""
    selected_admin_trip_id = ""
    admin_map_view = None
    admin_marker = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.root_widget = Builder.load_string(KV)
        return self.root_widget

    def on_start(self):
        self.root.current = "login_screen"

    def show_alert(self, title, msg):
        self.dialog = MDDialog(
            title=title,
            text=msg,
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=[0.86, 0.08, 0.24, 1],
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

    def process_logout(self):
        self.stop_hardware_gps()
        Clock.unschedule(self.refresh_admin_stream_nodes)
        Clock.unschedule(self.poll_active_admin_session_data)
        Clock.unschedule(self.poll_chat_messages)
        self.current_user_node = ""
        self.active_trip_id = ""
        self.selected_admin_user_node = ""
        self.selected_admin_trip_id = ""
        if self.dialog:
            self.dialog.dismiss()
        self.root.current = "login_screen"

    def register_user(self, username, email, password):
        if not username or not email or not password:
            self.show_alert("Error", "All fields are required!")
            return

        email_clean_input = email.strip().lower()
        clean_email = email_clean_input.replace(".", "-")
        role = "admin" if username.lower().strip() == "admin" else "user"

        user_data = {
            "username": username.strip(),
            "email": email_clean_input,
            "password": password,
            "role": role
        }

        try:
            check_res = requests.get(f"{FIREBASE_URL}/users/{clean_email}.json")
            if check_res.json() is not None:
                self.show_alert("Error", "This email is already registered.")
                return

            requests.put(f"{FIREBASE_URL}/users/{clean_email}.json", json=user_data)
            self.show_alert("Success", "Account created successfully!")
            self.root.current = "login_screen"
        except Exception as e:
            self.show_alert("Connection Error", f"Could not connect: {e}")

    def login_user(self, email, password):
        if not email or not password:
            self.show_alert("Error", "Please fill in all fields.")
            return

        email_clean_input = email.strip().lower()
        self.current_user_node = email_clean_input.replace(".", "-")

        try:
            response = requests.get(f"{FIREBASE_URL}/users/{self.current_user_node}.json")
            user_data = response.json()

            if user_data and user_data.get("password") == password:
                role = user_data.get("role")
                if role == "admin":
                    self.root.current = "admin_dashboard"
                    self.refresh_admin_stream_nodes()
                    Clock.schedule_interval(lambda dt: self.refresh_admin_stream_nodes(), 8)
                else:
                    dash_screen = self.root.get_screen("user_dashboard")
                    dash_screen.ids.dashboard_title.text = f"Welcome, {user_data.get('username').upper()}\nRole: USER"
                    self.root.current = "user_dashboard"
            else:
                self.show_alert("Auth Error", "Invalid email or password.")
        except Exception as e:
            self.show_alert("Connection Error", f"Could not connect: {e}")

    def submit_trip_form(self, pickup, dropoff, dep_time):
        if not pickup or not dropoff or not dep_time:
            self.show_alert("Validation Error", "Please fill in all fields.")
            return

        trip_payload = {
            "pickup": pickup.strip(),
            "dropoff": dropoff.strip(),
            "departure_time": dep_time.strip(),
            "payment_status": "pending_manual_transfer",
            "sharing_active": False
        }

        try:
            response = requests.post(f"{FIREBASE_URL}/users/{self.current_user_node}/trips.json", json=trip_payload)
            if response.status_code == 200:
                self.active_trip_id = response.json().get("name")
                self.root.current = "payment_screen"
            else:
                self.show_alert("Storage Error", "Could not submit trip data.")
        except Exception as e:
            self.show_alert("Network Error", f"Failed connection layout pipeline: {e}")

    def confirm_payment_and_start(self):
        try:
            patch_url = f"{FIREBASE_URL}/users/{self.current_user_node}/trips/{self.active_trip_id}.json"
            requests.patch(patch_url, json={"payment_status": "user_confirmed_transfer", "sharing_active": True})

            initial_lat, initial_lon = 6.5244, 3.3792
            tracking_screen = self.root.get_screen("live_tracking_screen")
            container = tracking_screen.ids.map_container
            container.clear_widgets()

            google_maps_source = MapSource(
                url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                cache_key="google_maps_base",
                attribution="Google Maps Street View"
            )

            self.map_view = MapView(zoom=16, lat=initial_lat, lon=initial_lon, map_source=google_maps_source)
            self.marker = MapMarker(lat=initial_lat, lon=initial_lon)
            self.map_view.add_widget(self.marker)
            container.add_widget(self.map_view)

            self.root.current = "live_tracking_screen"
            self.start_hardware_gps()
            Clock.schedule_interval(self.poll_chat_messages, 2)
        except Exception as e:
            self.show_alert("Initialization Error", f"Could not bind tracking engines: {e}")

    def start_hardware_gps(self):
        try:
            if not self.gps_configured:
                gps.configure(on_location=self.on_location_changed, on_status=self.on_gps_status)
                self.gps_configured = True
            gps.start(minTime=1000, minDistance=1)
        except NotImplementedError:
            Clock.schedule_once(lambda dt: self.on_location_changed(lat=6.5244, lon=3.3792), 1)

    def stop_hardware_gps(self):
        try:
            gps.stop()
        except:
            pass

    def on_location_changed(self, **kwargs):
        lat, lon = kwargs.get("lat"), kwargs.get("lon")
        if not lat or not lon or not self.marker: return

        self.marker.lat, self.marker.lon = lat, lon
        self.map_view.center_on(lat, lon)

        try:
            patch_url = f"{FIREBASE_URL}/users/{self.current_user_node}/trips/{self.active_trip_id}.json"
            requests.patch(patch_url, json={"current_latitude": lat, "current_longitude": lon})
        except Exception as e: print(f"Cloud update sync variance caught: {e}")

        Clock.schedule_once(lambda dt: self.fetch_street_name_async(lat, lon, "user"), 0.1)

    def fetch_street_name_async(self, lat, lon, target_view="user"):
        try:
            headers = {"User-Agent": "SafePassTrackerApp/1.0"}
            geocode_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18"
            response = requests.get(geocode_url, headers=headers, timeout=4)
            if response.status_code == 200:
                data = response.json()
                address = data.get("address", {})
                street_name = address.get("road") or address.get("suburb") or address.get("city") or "Unknown Thoroughfare"
                
                if target_view == "user":
                    self.root.get_screen("live_tracking_screen").ids.tracking_bar.title = f"On: {street_name}"
                else:
                    self.root.get_screen("admin_dashboard").ids.admin_topbar.title = f"HQ Tracking Target Node | On: {street_name}"
        except Exception as e: print(f"Geocoding reverse handshake failed: {e}")

    def on_gps_status(self, general_status, status_message): pass

    # =========================================================================
    # 🏛️ ADMINISTRATIVE ENGINE SUBSYSTEMS
    # =========================================================================

    def refresh_admin_stream_nodes(self):
        if self.root.current != "admin_dashboard": return
        try:
            res = requests.get(f"{FIREBASE_URL}/users.json")
            users_data = res.json() or {}
            
            admin_screen = self.root.get_screen("admin_dashboard")
            live_container = admin_screen.ids.live_users_box
            live_container.clear_widgets()

            for node_key, package in users_data.items():
                trips = package.get("trips", {})
                for trip_id, details in trips.items():
                    if details.get("sharing_active") is True:
                        username = package.get("username", "Unknown User").upper()
                        btn = MDRaisedButton(
                            text=f"{username}\n({details.get('dropoff', 'Trip')})",
                            md_bg_color=[0.86, 0.08, 0.24, 1],
                            size_hint_x=1,
                            on_release=lambda x, u=node_key, t=trip_id: self.select_live_user_feed(u, t)
                        )
                        live_container.add_widget(btn)
        except Exception as e: print(f"Admin node synchronization failure: {e}")

    def select_live_user_feed(self, user_node, trip_id):
        self.selected_admin_user_node = user_node
        self.selected_admin_trip_id = trip_id
        
        admin_screen = self.root.get_screen("admin_dashboard")
        admin_screen.ids.admin_terminate_btn.disabled = False
        
        map_container = admin_screen.ids.admin_map_container
        map_container.clear_widgets()
        
        google_maps_source = MapSource(
            url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            cache_key="google_maps_admin"
        )
        
        self.admin_map_view = MapView(zoom=16, lat=6.5244, lon=3.3792, map_source=google_maps_source)
        self.admin_marker = MapMarker(lat=6.5244, lon=3.3792)
        self.admin_map_view.add_widget(self.admin_marker)
        map_container.add_widget(self.admin_map_view)

        Clock.unschedule(self.poll_active_admin_session_data)
        Clock.schedule_interval(self.poll_active_admin_session_data, 3)
        
        Clock.unschedule(self.poll_chat_messages)
        Clock.schedule_interval(self.poll_chat_messages, 2)

    def poll_active_admin_session_data(self, dt):
        if self.root.current != "admin_dashboard" or not self.selected_admin_user_node: return False
        try:
            url = f"{FIREBASE_URL}/users/{self.selected_admin_user_node}/trips/{self.selected_admin_trip_id}.json"
            trip_data = requests.get(url).json()
            
            if not trip_data or trip_data.get("sharing_active") is False:
                self.show_alert("Session Terminated", "The monitored feed has disconnected safely.")
                self.reset_admin_viewport()
                return False

            lat = trip_data.get("current_latitude")
            lon = trip_data.get("current_longitude")
            
            if lat and lon and self.admin_marker:
                self.admin_marker.lat, self.admin_marker.lon = lat, lon
                self.admin_map_view.center_on(lat, lon)
                Clock.schedule_once(lambda dt: self.fetch_street_name_async(lat, lon, "admin"), 0.1)
        except Exception as e: print(f"Admin tracking telemetry fetch skipped: {e}")

    def admin_terminate_selected_trip(self):
        if not self.selected_admin_user_node: return
        try:
            url = f"{FIREBASE_URL}/users/{self.selected_admin_user_node}/trips/{self.selected_admin_trip_id}.json"
            requests.patch(url, json={"sharing_active": False, "trip_status": "terminated_by_hq"})
            self.show_alert("Trip Terminated", "Command broadcast issued. Vector session halted.")
            self.reset_admin_viewport()
            self.refresh_admin_stream_nodes()
        except Exception as e: self.show_alert("Error", str(e))

    def reset_admin_viewport(self):
        self.selected_admin_user_node = ""
        self.selected_admin_trip_id = ""
        admin_screen = self.root.get_screen("admin_dashboard")
        admin_screen.ids.admin_map_container.clear_widgets()
        admin_screen.ids.admin_terminate_btn.disabled = True
        admin_screen.ids.admin_topbar.title = "SafePass HQ Command Terminal"
        admin_screen.ids.admin_chat_logs.text = "Select a live feed node to initialize communications...\n"

    # =========================================================================
    # 💬 REALTIME SECURE MESSAGING CONTROL
    # =========================================================================

    def send_message_payload(self, text, sender):
        if not text.strip(): return
        target_user = self.current_user_node if sender == "User" else self.selected_admin_user_node
        target_trip = self.active_trip_id if sender == "User" else self.selected_admin_trip_id
        
        if not target_user or not target_trip: return

        try:
            msg_url = f"{FIREBASE_URL}/users/{target_user}/trips/{target_trip}/messages.json"
            payload = {"sender": sender, "text": text.strip()}
            requests.post(msg_url, json=payload)
            
            if sender == "User":
                self.root.get_screen("live_tracking_screen").ids.user_message_input.text = ""
            else:
                self.root.get_screen("admin_dashboard").ids.admin_message_input.text = ""
            self.poll_chat_messages(None)
        except Exception as e: print(f"Message payload dropping failure: {e}")

    def poll_chat_messages(self, dt):
        target_user = self.current_user_node if self.root.current == "live_tracking_screen" else self.selected_admin_user_node
        target_trip = self.active_trip_id if self.root.current == "live_tracking_screen" else self.selected_admin_trip_id
        
        if not target_user or not target_trip: return

        try:
            msg_url = f"{FIREBASE_URL}/users/{target_user}/trips/{target_trip}/messages.json"
            messages = requests.get(msg_url).json() or {}
            
            chat_format = ""
            for msg_id, payload in messages.items():
                chat_format += f"[{payload.get('sender')}] : {payload.get('text')}\n"
                
            if self.root.current == "live_tracking_screen":
                self.root.get_screen("live_tracking_screen").ids.user_chat_logs.text = chat_format
            elif self.root.current == "admin_dashboard":
                self.root.get_screen("admin_dashboard").ids.admin_chat_logs.text = chat_format
        except Exception as e: pass

    # =========================================================================
    # USER DEACTIVATION SYSTEM
    # =========================================================================

    def end_active_trip(self):
        try:
            self.stop_hardware_gps()
            Clock.unschedule(self.poll_chat_messages)
            url = f"{FIREBASE_URL}/users/{self.current_user_node}/trips/{self.active_trip_id}.json"
            requests.patch(url, json={"sharing_active": False, "trip_status": "completed"})
            self.show_alert("Trip Completed", "Your safe-pass vector log has been successfully closed.")
            self.root.current = "user_dashboard"
        except Exception as e: self.show_alert("Error", f"Failed closing channel: {e}")

if __name__ == "__main__":
    SafePassTrackerApp().run()
