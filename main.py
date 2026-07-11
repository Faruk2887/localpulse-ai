#!/usr/bin/env python3
"""
LocalPulse AI - iOS & Android Mobile App
Full international location support
"""

import os, sys, json, threading, requests
from datetime import datetime

# Kivy config
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty, DictProperty
from kivy.core.clipboard import Clipboard
from kivy.utils import platform

# KivyMD for Material Design
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.chip import MDChip
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, ThreeLineListItem, OneLineAvatarListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.progressindicator import MDCircularProgressIndicator

# Colors
PRIMARY = [0.31, 0.27, 0.90, 1]
ACCENT = [0.06, 0.73, 0.51, 1]
DANGER = [0.94, 0.27, 0.27, 1]
WARNING = [0.96, 0.62, 0.04, 1]
DARK = [0.12, 0.16, 0.22, 1]
LIGHT = [0.98, 0.98, 0.98, 1]
WHITE = [1, 1, 1, 1]
GRAY = [0.42, 0.45, 0.50, 1]

# ============================================
# INTERNATIONAL LOCATIONS
# ============================================

LOCATIONS = {
    '🇺🇸 United States': {
        'flag': '🇺🇸',
        'cities': {
            'New York, NY': {'lat': 40.7128, 'lon': -74.0060, 'geo': 'US-NY'},
            'Los Angeles, CA': {'lat': 34.0522, 'lon': -118.2437, 'geo': 'US-CA'},
            'Chicago, IL': {'lat': 41.8781, 'lon': -87.6298, 'geo': 'US-IL'},
            'Houston, TX': {'lat': 29.7604, 'lon': -95.3698, 'geo': 'US-TX'},
            'Miami, FL': {'lat': 25.7617, 'lon': -80.1918, 'geo': 'US-FL'},
            'San Francisco, CA': {'lat': 37.7749, 'lon': -122.4194, 'geo': 'US-CA'},
            'Seattle, WA': {'lat': 47.6062, 'lon': -122.3321, 'geo': 'US-WA'},
            'Boston, MA': {'lat': 42.3601, 'lon': -71.0589, 'geo': 'US-MA'},
            'Austin, TX': {'lat': 30.2672, 'lon': -97.7431, 'geo': 'US-TX'},
            'Denver, CO': {'lat': 39.7392, 'lon': -104.9903, 'geo': 'US-CO'},
        }
    },
    '🇬🇧 United Kingdom': {
        'flag': '🇬🇧',
        'cities': {
            'London, England': {'lat': 51.5074, 'lon': -0.1278, 'geo': 'GB-ENG'},
            'Manchester, England': {'lat': 53.4808, 'lon': -2.2426, 'geo': 'GB-ENG'},
            'Birmingham, England': {'lat': 52.4862, 'lon': -1.8904, 'geo': 'GB-ENG'},
            'Liverpool, England': {'lat': 53.4084, 'lon': -2.9916, 'geo': 'GB-ENG'},
            'Edinburgh, Scotland': {'lat': 55.9533, 'lon': -3.1883, 'geo': 'GB-SCT'},
            'Glasgow, Scotland': {'lat': 55.8642, 'lon': -4.2518, 'geo': 'GB-SCT'},
            'Cardiff, Wales': {'lat': 51.4816, 'lon': -3.1791, 'geo': 'GB-WLS'},
            'Belfast, N. Ireland': {'lat': 54.5973, 'lon': -5.9301, 'geo': 'GB-NIR'},
        }
    },
    '🇨🇦 Canada': {
        'flag': '🇨🇦',
        'cities': {
            'Toronto, ON': {'lat': 43.6532, 'lon': -79.3832, 'geo': 'CA-ON'},
            'Vancouver, BC': {'lat': 49.2827, 'lon': -123.1207, 'geo': 'CA-BC'},
            'Montreal, QC': {'lat': 45.5017, 'lon': -73.5673, 'geo': 'CA-QC'},
            'Calgary, AB': {'lat': 51.0447, 'lon': -114.0719, 'geo': 'CA-AB'},
            'Ottawa, ON': {'lat': 45.4215, 'lon': -75.6972, 'geo': 'CA-ON'},
        }
    },
    '🇦🇺 Australia': {
        'flag': '🇦🇺',
        'cities': {
            'Sydney, NSW': {'lat': -33.8688, 'lon': 151.2093, 'geo': 'AU-NSW'},
            'Melbourne, VIC': {'lat': -37.8136, 'lon': 144.9631, 'geo': 'AU-VIC'},
            'Brisbane, QLD': {'lat': -27.4698, 'lon': 153.0251, 'geo': 'AU-QLD'},
            'Perth, WA': {'lat': -31.9505, 'lon': 115.8605, 'geo': 'AU-WA'},
            'Adelaide, SA': {'lat': -34.9285, 'lon': 138.6007, 'geo': 'AU-SA'},
        }
    },
    '🇩🇪 Germany': {
        'flag': '🇩🇪',
        'cities': {
            'Berlin': {'lat': 52.5200, 'lon': 13.4050, 'geo': 'DE-BE'},
            'Munich': {'lat': 48.1351, 'lon': 11.5820, 'geo': 'DE-BY'},
            'Hamburg': {'lat': 53.5511, 'lon': 9.9937, 'geo': 'DE-HH'},
            'Frankfurt': {'lat': 50.1109, 'lon': 8.6821, 'geo': 'DE-HE'},
        }
    },
    '🇫🇷 France': {
        'flag': '🇫🇷',
        'cities': {
            'Paris': {'lat': 48.8566, 'lon': 2.3522, 'geo': 'FR-IDF'},
            'Lyon': {'lat': 45.7640, 'lon': 4.8357, 'geo': 'FR-ARA'},
            'Marseille': {'lat': 43.2965, 'lon': 5.3698, 'geo': 'FR-PAC'},
        }
    },
    '🇪🇸 Spain': {
        'flag': '🇪🇸',
        'cities': {
            'Madrid': {'lat': 40.4168, 'lon': -3.7038, 'geo': 'ES-MD'},
            'Barcelona': {'lat': 41.3874, 'lon': 2.1686, 'geo': 'ES-CT'},
            'Valencia': {'lat': 39.4699, 'lon': -0.3763, 'geo': 'ES-VC'},
        }
    },
    '🇮🇹 Italy': {
        'flag': '🇮🇹',
        'cities': {
            'Rome': {'lat': 41.9028, 'lon': 12.4964, 'geo': 'IT-62'},
            'Milan': {'lat': 45.4642, 'lon': 9.1900, 'geo': 'IT-25'},
            'Naples': {'lat': 40.8518, 'lon': 14.2681, 'geo': 'IT-72'},
        }
    },
    '🇯🇵 Japan': {
        'flag': '🇯🇵',
        'cities': {
            'Tokyo': {'lat': 35.6762, 'lon': 139.6503, 'geo': 'JP-13'},
            'Osaka': {'lat': 34.6937, 'lon': 135.5023, 'geo': 'JP-27'},
        }
    },
    '🇧🇷 Brazil': {
        'flag': '🇧🇷',
        'cities': {
            'São Paulo': {'lat': -23.5505, 'lon': -46.6333, 'geo': 'BR-SP'},
            'Rio de Janeiro': {'lat': -22.9068, 'lon': -43.1729, 'geo': 'BR-RJ'},
        }
    },
    '🇮🇳 India': {
        'flag': '🇮🇳',
        'cities': {
            'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'geo': 'IN-MH'},
            'Delhi': {'lat': 28.7041, 'lon': 77.1025, 'geo': 'IN-DL'},
            'Bangalore': {'lat': 12.9716, 'lon': 77.5946, 'geo': 'IN-KA'},
        }
    },
    '🇦🇪 UAE': {
        'flag': '🇦🇪',
        'cities': {
            'Dubai': {'lat': 25.2048, 'lon': 55.2708, 'geo': 'AE-DU'},
            'Abu Dhabi': {'lat': 24.4539, 'lon': 54.3773, 'geo': 'AE-AZ'},
        }
    },
    '🇸🇬 Singapore': {
        'flag': '🇸🇬',
        'cities': {
            'Singapore': {'lat': 1.3521, 'lon': 103.8198, 'geo': 'SG-01'},
        }
    },
    '🇳🇬 Nigeria': {
        'flag': '🇳🇬',
        'cities': {
            'Lagos': {'lat': 6.5244, 'lon': 3.3792, 'geo': 'NG-LA'},
            'Abuja': {'lat': 9.0765, 'lon': 7.3986, 'geo': 'NG-FC'},
        }
    },
    '🇿🇦 South Africa': {
        'flag': '🇿🇦',
        'cities': {
            'Johannesburg': {'lat': -26.2041, 'lon': 28.0473, 'geo': 'ZA-GT'},
            'Cape Town': {'lat': -33.9249, 'lon': 18.4241, 'geo': 'ZA-WC'},
        }
    },
}

BUSINESS_TYPES = [
    {'name': 'Bakery', 'icon': '🎂'},
    {'name': 'Plumber', 'icon': '🔧'},
    {'name': 'Barber', 'icon': '💈'},
    {'name': 'Restaurant', 'icon': '🍽️'},
    {'name': 'Dentist', 'icon': '🦷'},
    {'name': 'Mechanic', 'icon': '🔧'},
    {'name': 'Electrician', 'icon': '⚡'},
    {'name': 'Cleaner', 'icon': '🧹'},
    {'name': 'Photographer', 'icon': '📸'},
    {'name': 'Tutor', 'icon': '📚'},
    {'name': 'Fitness Trainer', 'icon': '💪'},
    {'name': 'Pet Groomer', 'icon': '🐕'},
    {'name': 'HVAC Technician', 'icon': '❄️'},
    {'name': 'Locksmith', 'icon': '🔐'},
    {'name': 'Landscaper', 'icon': '🌿'},
]

# ============================================
# API HANDLER
# ============================================

class LocalPulseAPI:
    @staticmethod
    def scan(business_type, location, country, callback):
        def _scan():
            try:
                # Try live API first
                response = requests.post(
                    "https://api.localpulse.ai/v1/scan-intl",
                    json={
                        'business_type': business_type.lower(),
                        'city': location,
                        'country': country,
                    },
                    timeout=15
                )
                if response.status_code == 200:
                    data = response.json()
                    Clock.schedule_once(lambda dt: callback(True, data))
                    return
            except:
                pass
            
            # Fallback to demo data
            data = generate_demo_alerts(business_type, location)
            Clock.schedule_once(lambda dt: callback(True, data))
        
        threading.Thread(target=_scan, daemon=True).start()


def generate_demo_alerts(business_type, location):
    """Generate realistic demo alerts for any business type"""
    templates = {
        'Bakery': [
            ('URGENT', '🚨 Wedding cake emergency!', 'Need custom wedding cake. Baker cancelled!', 'Reddit', '$350'),
            ('OPPORTUNITY', '🎂 Birthday cake request', 'Looking for nut-free birthday cake for child', 'Facebook', '$95'),
            ('TREND', '📈 Sourdough trending', '47 searches for "sourdough near me" today', 'Google', '$180'),
        ],
        'Plumber': [
            ('URGENT', '🚨 Burst pipe!', 'Water flooding basement. Need plumber NOW', 'Nextdoor', '$500'),
            ('OPPORTUNITY', '🔧 Water heater install', 'Looking for reliable plumber for installation', 'Reddit', '$800'),
        ],
        'Restaurant': [
            ('OPPORTUNITY', '🍽️ Group dinner', 'Best restaurant for party of 12 this Friday', 'Facebook', '$600'),
            ('TREND', '📈 Brunch trending', '200+ searches for weekend brunch', 'Google', '$400'),
        ],
        'Barber': [
            ('OPPORTUNITY', '💈 Skin fade needed', 'Looking for barber who does good skin fades', 'Reddit', '$45'),
        ],
        'Dentist': [
            ('URGENT', '🦷 Toothache emergency', 'Severe tooth pain. Need emergency dentist', 'Nextdoor', '$300'),
        ],
        'Mechanic': [
            ('URGENT', '🚗 Car won\'t start', 'Need mechanic. Car broke down on highway', 'Facebook', '$400'),
        ],
    }
    
    alerts = templates.get(business_type, templates['Bakery'])
    return {
        'timestamp': datetime.now().isoformat(),
        'alerts': [
            {
                'type': a[0], 'headline': a[1], 'text': a[2],
                'source': f'{a[3]} - {location}', 'time': 'Just now',
                'value': a[4],
                'response': f'Hi! I saw your post about needing {business_type.lower()} services. I\'m local and available to help right away!'
            } for a in alerts
        ],
        'total_alerts': len(alerts),
        'business_type': business_type,
        'location': location,
    }


# ============================================
# SCREENS
# ============================================

class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.next_screen, 2)
    
    def next_screen(self, dt):
        app = MDApp.get_running_app()
        self.manager.current = 'dashboard' if app.user_email else 'onboarding'


class OnboardingScreen(Screen):
    pass


class SignupScreen(Screen):
    def signup(self):
        app = MDApp.get_running_app()
        app.user_email = self.ids.email.text or 'user@demo.com'
        app.user_plan = 'free_trial'
        self.manager.current = 'dashboard'
        Snackbar(text="🎉 Welcome! 7-day Pro trial activated!").open()


class LoginScreen(Screen):
    def login(self):
        app = MDApp.get_running_app()
        app.user_email = self.ids.email.text or 'user@demo.com'
        self.manager.current = 'dashboard'


class DashboardScreen(Screen):
    alerts = ListProperty([])
    scanning = BooleanProperty(False)
    
    def on_enter(self):
        app = MDApp.get_running_app()
        self.ids.biz_label.text = f"{app.business_icon} {app.business_type}"
        self.ids.loc_label.text = f"📍 {app.current_city}"
        self.ids.country_label.text = app.current_country.split()[0]
        self.scan()
    
    def scan(self):
        self.scanning = True
        app = MDApp.get_running_app()
        
        def callback(success, data):
            self.scanning = False
            if success:
                self.alerts = data.get('alerts', [])
                self.ids.alerts_list.clear_widgets()
                for alert in self.alerts:
                    self.ids.alerts_list.add_widget(self.build_alert_card(alert))
                Snackbar(text=f"✅ Found {len(self.alerts)} opportunities!").open()
        
        LocalPulseAPI.scan(app.business_type, app.current_city, app.current_country, callback)
    
    def build_alert_card(self, alert):
        color = DANGER if alert['type'] == 'URGENT' else WARNING if alert['type'] == 'OPPORTUNITY' else PRIMARY
        
        card = MDCard(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(170),
            md_bg_color=WHITE,
            elevation=3,
            radius=dp(16),
        )
        
        # Badge + Value
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32))
        badge = MDChip(
            text=alert['type'],
            color=WHITE,
            md_bg_color=color,
            size_hint=(None, None),
            size=(dp(100), dp(30)),
        )
        value = MDLabel(
            text=f"💰 {alert.get('value', 'N/A')}",
            theme_text_color='Custom',
            text_color=DARK,
            halign='right',
        )
        header.add_widget(badge)
        header.add_widget(value)
        
        # Headline
        headline = MDLabel(
            text=alert['headline'],
            bold=True,
            theme_text_color='Custom',
            text_color=DARK,
            size_hint_y=None,
            height=dp(30),
        )
        
        # Text
        desc = MDLabel(
            text=alert['text'],
            theme_text_color='Custom',
            text_color=GRAY,
            size_hint_y=None,
            height=dp(35),
        )
        
        # Source + Time
        footer = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(24))
        footer.add_widget(MDLabel(text=f"📱 {alert['source']}", theme_text_color='Custom', text_color=[0.6,0.6,0.6,1], font_style='caption'))
        footer.add_widget(MDLabel(text=f"⏰ {alert.get('time','')}", theme_text_color='Custom', text_color=[0.6,0.6,0.6,1], font_style='caption', halign='right'))
        
        # Action button
        btn = MDRaisedButton(
            text='📋  COPY RESPONSE',
            md_bg_color=PRIMARY,
            size_hint=(1, None),
            height=dp(36),
            on_release=lambda x, a=alert: self.copy_response(a),
        )
        
        card.add_widget(header)
        card.add_widget(headline)
        card.add_widget(desc)
        card.add_widget(footer)
        card.add_widget(btn)
        
        return card
    
    def copy_response(self, alert):
        Clipboard.copy(alert.get('response', ''))
        Snackbar(text="✅ Response copied to clipboard!").open()
    
    def show_biz_menu(self):
        menu_items = [
            {
                'text': f"{b['icon']}  {b['name']}",
                'viewclass': 'OneLineListItem',
                'on_release': lambda x=b: self.select_biz(x)
            } for b in BUSINESS_TYPES
        ]
        MDDropdownMenu(caller=self.ids.biz_btn, items=menu_items, width_mult=3).open()
    
    def select_biz(self, biz):
        app = MDApp.get_running_app()
        app.business_type = biz['name']
        app.business_icon = biz['icon']
        self.ids.biz_label.text = f"{biz['icon']} {biz['name']}"
        self.scan()
    
    def show_country_menu(self):
        menu_items = [
            {
                'text': country,
                'viewclass': 'OneLineListItem',
                'on_release': lambda x=c: self.select_country(c)
            } for c in LOCATIONS.keys()
        ]
        MDDropdownMenu(caller=self.ids.country_btn, items=menu_items, width_mult=4).open()
    
    def select_country(self, country):
        app = MDApp.get_running_app()
        app.current_country = country
        cities = list(LOCATIONS[country]['cities'].keys())
        app.current_city = cities[0]
        self.ids.loc_label.text = f"📍 {app.current_city}"
        self.ids.country_label.text = country.split()[0]
        self.scan()
    
    def show_city_menu(self):
        app = MDApp.get_running_app()
        cities = list(LOCATIONS[app.current_country]['cities'].keys())
        menu_items = [
            {
                'text': f"📍 {c}",
                'viewclass': 'OneLineListItem',
                'on_release': lambda x=c: self.select_city(x)
            } for c in cities
        ]
        MDDropdownMenu(caller=self.ids.loc_btn, items=menu_items, width_mult=4).open()
    
    def select_city(self, city):
        app = MDApp.get_running_app()
        app.current_city = city
        self.ids.loc_label.text = f"📍 {city}"
        self.scan()


class UpgradeScreen(Screen):
    def subscribe(self, plan):
        MDDialog(
            title="Subscribe to Pro",
            text=f"You selected {plan} plan.\nGoogle Play / App Store billing will open.",
            buttons=[MDFlatButton(text="OK")],
        ).open()


class SettingsScreen(Screen):
    pass


# ============================================
# MAIN APP
# ============================================

class LocalPulseApp(MDApp):
    user_email = StringProperty(None)
    user_plan = StringProperty('free')
    business_type = StringProperty('Bakery')
    business_icon = StringProperty('🎂')
    current_country = StringProperty('🇺🇸 United States')
    current_city = StringProperty('New York, NY')
    notifications = BooleanProperty(True)
    sounds = BooleanProperty(True)
    
    def build(self):
        self.title = "LocalPulse AI"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"
        
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(OnboardingScreen(name='onboarding'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(UpgradeScreen(name='upgrade'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm
    
    def on_start(self):
        self.init_ads()
    
    def init_ads(self):
        try:
            from kivmob import KivMob
            self.ads = KivMob("ca-app-pub-3940256099942544~3347511713")  # Test ID
            self.ads.new_banner("ca-app-pub-3940256099942544/6300978111")
            self.ads.request_banner()
            self.ads.show_banner()
        except:
            pass  # Ads disabled in development


# ============================================
# KV LAYOUT (simplified for brevity)
# ============================================

KV = '''
#:import dp kivy.metrics.dp
#:import PRIMARY __main__.PRIMARY
#:import ACCENT __main__.ACCENT
#:import DANGER __main__.DANGER
#:import DARK __main__.DARK
#:import WHITE __main__.WHITE
#:import GRAY __main__.GRAY

<SplashScreen>:
    name: 'splash'
    BoxLayout:
        orientation: 'vertical'
        md_bg_color: PRIMARY
        Image:
            source: 'assets/icon.png'
            size_hint: None, None
            size: dp(120), dp(120)
            pos_hint: {'center_x': 0.5}
        MDLabel:
            text: 'LocalPulse AI'
            font_style: 'h4'
            bold: True
            halign: 'center'
            theme_text_color: 'Custom'
            text_color: WHITE
        MDCircularProgressIndicator:
            size_hint: None, None
            size: dp(40), dp(40)
            pos_hint: {'center_x': 0.5}

<OnboardingScreen>:
    name: 'onboarding'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(16)
        md_bg_color: WHITE
        Widget: size_hint_y: 0.15
        Image:
            source: 'assets/icon.png'
            size_hint: None, None
            size: dp(180), dp(180)
            pos_hint: {'center_x': 0.5}
        MDLabel:
            text: 'Find Local Customers\\nInstantly'
            font_style: 'h4'
            bold: True
            halign: 'center'
        MDLabel:
            text: 'AI alerts when people nearby need your services'
            halign: 'center'
            theme_text_color: 'Custom'
            text_color: GRAY
        Widget: size_hint_y: 0.1
        MDRaisedButton:
            text: 'START FREE TRIAL'
            md_bg_color: PRIMARY
            size_hint_x: 0.8
            pos_hint: {'center_x': 0.5}
            on_release: app.root.current = 'signup'
        MDFlatButton:
            text: 'Sign In'
            pos_hint: {'center_x': 0.5}
            on_release: app.root.current = 'login'

<SignupScreen>:
    name: 'signup'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(12)
        md_bg_color: WHITE
        MDTopAppBar:
            title: 'Create Account'
        MDLabel:
            text: 'Start 7-Day Free Trial'
            font_style: 'h5'
            bold: True
            halign: 'center'
        MDTextField:
            id: email
            hint_text: 'Email'
            mode: 'rectangle'
        MDTextField:
            id: password
            hint_text: 'Password'
            mode: 'rectangle'
            password: True
        MDRaisedButton:
            text: 'CREATE FREE ACCOUNT'
            md_bg_color: PRIMARY
            size_hint_x: 0.8
            pos_hint: {'center_x': 0.5}
            on_release: root.signup()

<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(12)
        md_bg_color: WHITE
        MDTopAppBar:
            title: 'Sign In'
        MDLabel:
            text: 'Welcome Back'
            font_style: 'h5'
            bold: True
            halign: 'center'
        MDTextField:
            id: email
            hint_text: 'Email'
            mode: 'rectangle'
        MDTextField:
            id: password
            hint_text: 'Password'
            mode: 'rectangle'
            password: True
        MDRaisedButton:
            text: 'SIGN IN'
            md_bg_color: PRIMARY
            size_hint_x: 0.8
            pos_hint: {'center_x': 0.5}
            on_release: root.login()

<DashboardScreen>:
    name: 'dashboard'
    BoxLayout:
        orientation: 'vertical'
        md_bg_color: [0.95, 0.95, 0.95, 1]
        
        MDTopAppBar:
            title: 'LocalPulse AI'
            right_action_items: [['crown', lambda x: setattr(app.root, 'current', 'upgrade')], ['cog', lambda x: setattr(app.root, 'current', 'settings')]]
        
        # Business + Location selectors
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(48)
            padding: dp(8)
            spacing: dp(6)
            
            MDRaisedButton:
                id: biz_btn
                text: ''
                md_bg_color: PRIMARY
                size_hint_x: 0.1
                on_release: root.show_biz_menu()
                MDLabel:
                    id: biz_label
                    text: '🎂 Bakery'
                    theme_text_color: 'Custom'
                    text_color: WHITE
                    bold: True
            
            MDRaisedButton:
                id: country_btn
                text: ''
                md_bg_color: DARK
                size_hint_x: 0.1
                on_release: root.show_country_menu()
                MDLabel:
                    id: country_label
                    text: '🇺🇸'
                    theme_text_color: 'Custom'
                    text_color: WHITE
            
            MDRaisedButton:
                id: loc_btn
                text: ''
                md_bg_color: DARK
                size_hint_x: 0.1
                on_release: root.show_city_menu()
                MDLabel:
                    id: loc_label
                    text: '📍 NYC'
                    theme_text_color: 'Custom'
                    text_color: WHITE
                    font_style: 'caption'
        
        # Scan button
        MDRaisedButton:
            text: '🔍  SCAN FOR LEADS'
            md_bg_color: ACCENT
            size_hint_y: None
            height: dp(44)
            on_release: root.scan()
        
        # Alerts
        ScrollView:
            MDList:
                id: alerts_list
                padding: dp(8)
                spacing: dp(8)
        
        # Ad banner placeholder
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            md_bg_color: [0.88, 0.88, 0.88, 1]
            MDLabel:
                text: 'AdSense Banner'
                halign: 'center'
                theme_text_color: 'Custom'
                text_color: [0.5,0.5,0.5,1]
                font_style: 'caption'

<UpgradeScreen>:
    name: 'upgrade'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(12)
        md_bg_color: [0.95,0.95,0.95,1]
        MDTopAppBar:
            title: 'Upgrade to Pro'
        ScrollView:
            GridLayout:
                cols: 1
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height
                
                MDCard:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(8)
                    size_hint_y: None
                    height: dp(220)
                    md_bg_color: WHITE
                    radius: dp(16)
                    MDLabel:
                        text: '⭐ STARTER'
                        font_style: 'h6'
                        bold: True
                    MDLabel:
                        text: '\$49/month'
                        font_style: 'h4'
                        bold: True
                        theme_text_color: 'Custom'
                        text_color: PRIMARY
                    MDLabel:
                        text: '• 10 alerts/day\\n• 1 business type\\n• Email alerts\\n• 5-mile radius'
                    MDRaisedButton:
                        text: 'SUBSCRIBE'
                        md_bg_color: PRIMARY
                        on_release: root.subscribe('starter')
                
                MDCard:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(8)
                    size_hint_y: None
                    height: dp(260)
                    md_bg_color: WHITE
                    radius: dp(16)
                    MDLabel:
                        text: '👑 PROFESSIONAL'
                        font_style: 'h6'
                        bold: True
                        theme_text_color: 'Custom'
                        text_color: PRIMARY
                    MDLabel:
                        text: '\$99/month'
                        font_style: 'h4'
                        bold: True
                        theme_text_color: 'Custom'
                        text_color: PRIMARY
                    MDLabel:
                        text: '• Unlimited alerts\\n• 3 business types\\n• SMS + Email\\n• AI templates\\n• 25-mile radius\\n• Competitor tracking'
                    MDRaisedButton:
                        text: 'SUBSCRIBE - BEST VALUE'
                        md_bg_color: ACCENT
                        on_release: root.subscribe('pro')

<SettingsScreen>:
    name: 'settings'
    BoxLayout:
        orientation: 'vertical'
        md_bg_color: [0.95,0.95,0.95,1]
        MDTopAppBar:
            title: 'Settings'
        ScrollView:
            MDList:
                ThreeLineListItem:
                    text: 'Push Notifications'
                    secondary_text: 'Get instant lead alerts'
                    Widget:
                    MDCheckbox:
                        active: True
                ThreeLineListItem:
                    text: 'Alert Sounds'
                    secondary_text: 'Sound for urgent alerts'
                    Widget:
                    MDCheckbox:
                        active: True
                OneLineListItem:
                    text: '📧  Change Email'
                OneLineListItem:
                    text: '💳  Manage Subscription'
                OneLineListItem:
                    text: '🌍  Change Default Location'
                OneLineListItem:
                    text: '📄  Privacy Policy'
                OneLineListItem:
                    text: '📝  Terms of Service'
                OneLineListItem:
                    text: '⭐  Rate the App'
                OneLineListItem:
                    text: '🚪  Log Out'
'''

from kivy.lang import Builder
Builder.load_string(KV)

if __name__ == '__main__':
    LocalPulseApp().run()
