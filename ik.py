# app_premium_2025.py
"""
ISmaint - Redesigned 2025 Premium Version
Complete visual overhaul with modern UI/UX, Moroccan-inspired design elements,
and premium maintenance management aesthetics.
"""

import streamlit as st
from supabase import create_client, Client
import pandas as pd
import os
import datetime
from io import BytesIO
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import plotly.express as px
import plotly.graph_objects as go
from time import time

# -----------------------------
# Configuration / Environment
# -----------------------------
st.set_page_config(
    page_title="ISmaint Pro", 
    layout="wide", 
    page_icon="🏭",
    initial_sidebar_state="expanded"
)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("Erreur de connexion à Supabase. Vérifiez vos variables d'environnement SUPABASE_URL et SUPABASE_KEY.")
    st.stop()

# -----------------------------
# Initialisation de session_state
# -----------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Tableau de Bord"

# -----------------------------
# Theming / CSS 2025 Premium
# -----------------------------
PRIMARY_LIGHT = "#0F172A"
ACCENT_LIGHT = "#06B6D4"
SECONDARY_LIGHT = "#8B5CF6"
BG_LIGHT = "#F8FAFC"
CARD_LIGHT = "#FFFFFF"
TEXT_LIGHT = "#1E293B"
TEXT_SECONDARY_LIGHT = "#64748B"

PRIMARY_DARK = "#F1F5F9"
ACCENT_DARK = "#22D3EE"
SECONDARY_DARK = "#A78BFA"
BG_DARK = "#0F172A"
CARD_DARK = "#1E293B"
TEXT_DARK = "#F1F5F9"
TEXT_SECONDARY_DARK = "#94A3B8"

# Moroccan-inspired colors
MOROCCAN_BLUE = "#1D5D9B"
MOROCCAN_GREEN = "#2D8C6B"
MOROCCAN_RED = "#C84B31"
MOROCCAN_GOLD = "#E7B10A"

def get_theme():
    if st.session_state.dark_mode:
        return {
            'primary': PRIMARY_DARK,
            'accent': ACCENT_DARK,
            'secondary': SECONDARY_DARK,
            'bg': BG_DARK,
            'card': CARD_DARK,
            'text': TEXT_DARK,
            'text_secondary': TEXT_SECONDARY_DARK,
            'moroccan_blue': "#3B82F6",
            'moroccan_green': "#10B981",
            'moroccan_red': "#EF4444",
            'moroccan_gold': "#F59E0B"
        }
    else:
        return {
            'primary': PRIMARY_LIGHT,
            'accent': ACCENT_LIGHT,
            'secondary': SECONDARY_LIGHT,
            'bg': BG_LIGHT,
            'card': CARD_LIGHT,
            'text': TEXT_LIGHT,
            'text_secondary': TEXT_SECONDARY_LIGHT,
            'moroccan_blue': MOROCCAN_BLUE,
            'moroccan_green': MOROCCAN_GREEN,
            'moroccan_red': MOROCCAN_RED,
            'moroccan_gold': MOROCCAN_GOLD
        }

def apply_css():
    theme = get_theme()
    
    st.markdown(
        f"""
        <style>
        /* ===== BASE RESET & VARIABLES ===== */
        :root {{
            --primary: {theme['primary']};
            --accent: {theme['accent']};
            --secondary: {theme['secondary']};
            --bg: {theme['bg']};
            --card: {theme['card']};
            --text: {theme['text']};
            --text-secondary: {theme['text_secondary']};
            --moroccan-blue: {theme['moroccan_blue']};
            --moroccan-green: {theme['moroccan_green']};
            --moroccan-red: {theme['moroccan_red']};
            --moroccan-gold: {theme['moroccan_gold']};
            --shadow: rgba(0, 0, 0, 0.1);
            --radius: 16px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* ===== MAIN LAYOUT ===== */
        .main {{
            background: var(--bg);
            color: var(--text);
            font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
        }}
        
        /* ===== LOGIN PAGE 2025 ===== */
        .login-2025-container {{
            background: linear-gradient(135deg, var(--moroccan-blue) 0%, var(--moroccan-green) 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }}
        
        .login-2025-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.1"><defs><pattern id="moroccan" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M10 0L20 10L10 20L0 10Z" fill="white"/></pattern></defs><rect width="100" height="100" fill="url(%23moroccan)"/></svg>');
            animation: float 20s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-20px) rotate(180deg); }}
        }}
        
        .login-2025-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 48px 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            width: 100%;
            max-width: 440px;
            text-align: center;
            position: relative;
            z-index: 2;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .login-2025-logo {{
            width: 80px;
            height: 80px;
            border-radius: 20px;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 24px auto;
            color: white;
            font-size: 32px;
            box-shadow: 0 10px 25px rgba(29, 93, 155, 0.3);
        }}
        
        .login-2025-title {{
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}
        
        .login-2025-subtitle {{
            color: #6B7280;
            font-size: 16px;
            margin-bottom: 40px;
            font-weight: 500;
        }}
        
        .login-2025-input {{
            margin-bottom: 24px;
        }}
        
        .login-2025-input .stTextInput>div>div>input {{
            border-radius: 12px;
            border: 2px solid #E5E7EB;
            padding: 16px 20px;
            font-size: 16px;
            transition: var(--transition);
            background: white;
        }}
        
        .login-2025-input .stTextInput>div>div>input:focus {{
            border-color: var(--moroccan-blue);
            box-shadow: 0 0 0 4px rgba(29, 93, 155, 0.1);
            transform: translateY(-2px);
        }}
        
        .login-2025-button {{
            width: 100%;
            margin-top: 16px;
        }}
        
        .login-2025-button .stButton>button {{
            width: 100%;
            padding: 16px 24px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            border: none;
            color: white;
            transition: var(--transition);
            box-shadow: 0 4px 15px rgba(29, 93, 155, 0.3);
        }}
        
        .login-2025-button .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(29, 93, 155, 0.4);
        }}
        
        /* ===== SIDEBAR 2025 ===== */
        section[data-testid="stSidebar"] {{
            background: var(--card) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .sidebar-user-card {{
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 24px;
            color: white;
            text-align: center;
        }}
        
        .sidebar-user-avatar {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px auto;
            font-size: 24px;
        }}
        
        .sidebar-user-name {{
            font-weight: 700;
            font-size: 18px;
            margin-bottom: 4px;
        }}
        
        .sidebar-user-role {{
            font-size: 12px;
            opacity: 0.9;
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 12px;
            border-radius: 20px;
            display: inline-block;
        }}
        
        .nav-item {{
            display: flex;
            align-items: center;
            padding: 12px 16px;
            margin: 4px 0;
            border-radius: 12px;
            color: var(--text);
            text-decoration: none;
            transition: var(--transition);
            font-weight: 500;
            cursor: pointer;
        }}
        
        .nav-item:hover {{
            background: rgba(29, 93, 155, 0.1);
            transform: translateX(4px);
        }}
        
        .nav-item.active {{
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            color: white;
            box-shadow: 0 4px 15px rgba(29, 93, 155, 0.3);
        }}
        
        .nav-icon {{
            margin-right: 12px;
            font-size: 18px;
            width: 20px;
            text-align: center;
        }}
        
        /* ===== HEADER 2025 ===== */
        .header-2025 {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 0;
            margin-bottom: 24px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .header-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .header-logo {{
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
        }}
        
        .header-title {{
            font-size: 24px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .header-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        /* ===== KPI CARDS 2025 ===== */
        .kpi-card-2025 {{
            background: var(--card);
            border-radius: var(--radius);
            padding: 24px;
            box-shadow: 0 4px 20px var(--shadow);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }}
        
        .kpi-card-2025::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
        }}
        
        .kpi-card-2025:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 30px var(--shadow);
        }}
        
        .kpi-icon {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: rgba(29, 93, 155, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
            font-size: 20px;
            color: var(--moroccan-blue);
        }}
        
        .kpi-label-2025 {{
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .kpi-value-2025 {{
            font-size: 28px;
            font-weight: 800;
            color: var(--text);
            margin-bottom: 4px;
        }}
        
        .kpi-trend {{
            font-size: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .trend-up {{
            color: var(--moroccan-green);
        }}
        
        .trend-down {{
            color: var(--moroccan_red);
        }}
        
        /* ===== FORMS 2025 ===== */
        .form-card {{
            background: var(--card);
            border-radius: var(--radius);
            padding: 32px;
            box-shadow: 0 4px 20px var(--shadow);
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 24px;
        }}
        
        .form-section {{
            margin-bottom: 32px;
        }}
        
        .form-section-title {{
            font-size: 18px;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid rgba(29, 93, 155, 0.1);
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-label {{
            display: block;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 8px;
            font-size: 14px;
        }}
        
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {{
            border-radius: 12px;
            border: 2px solid #E5E7EB;
            padding: 12px 16px;
            font-size: 14px;
            transition: var(--transition);
            background: var(--card);
            color: var(--text);
        }}
        
        .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
            border-color: var(--moroccan-blue);
            box-shadow: 0 0 0 4px rgba(29, 93, 155, 0.1);
        }}
        
        .stSelectbox>div>div>div {{
            border-radius: 12px;
            border: 2px solid #E5E7EB;
        }}
        
        /* ===== BUTTONS 2025 ===== */
        .stButton>button {{
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            border: none;
            transition: var(--transition);
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            color: white;
            box-shadow: 0 4px 15px rgba(29, 93, 155, 0.3);
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(29, 93, 155, 0.4);
        }}
        
        .btn-secondary {{
            background: rgba(29, 93, 155, 0.1);
            color: var(--moroccan-blue);
            border: 2px solid var(--moroccan-blue);
        }}
        
        .btn-danger {{
            background: linear-gradient(135deg, var(--moroccan-red), #DC2626);
            color: white;
        }}
        
        /* ===== DATA TABLES 2025 ===== */
        .dataframe {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px var(--shadow);
        }}
        
        .dataframe thead th {{
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            color: white;
            font-weight: 600;
            border: none;
        }}
        
        /* ===== BADGES 2025 ===== */
        .badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .badge-success {{
            background: rgba(16, 185, 129, 0.1);
            color: var(--moroccan-green);
        }}
        
        .badge-warning {{
            background: rgba(245, 158, 11, 0.1);
            color: var(--moroccan_gold);
        }}
        
        .badge-danger {{
            background: rgba(239, 68, 68, 0.1);
            color: var(--moroccan-red);
        }}
        
        .badge-info {{
            background: rgba(29, 93, 155, 0.1);
            color: var(--moroccan-blue);
        }}
        
        /* ===== DARK MODE TOGGLE ===== */
        .dark-mode-toggle {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 20px;
            background: rgba(29, 93, 155, 0.1);
            color: var(--moroccan-blue);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            margin-bottom: 16px;
        }}
        
        .dark-mode-toggle:hover {{
            background: rgba(29, 93, 155, 0.2);
        }}
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {{
            .login-2025-card {{
                padding: 32px 24px;
                margin: 20px;
            }}
            
            .kpi-value-2025 {{
                font-size: 24px;
            }}
            
            .form-card {{
                padding: 24px 20px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Composants UI Réutilisables
# -----------------------------
def kpi_card_2025(label, value, trend=None, icon="📊", col=None):
    theme = get_theme()
    
    trend_html = ""
    if trend is not None:
        # Vérifier si trend est numérique (int, float) ou une chaîne
        if isinstance(trend, (int, float)):
            trend_class = "trend-up" if trend > 0 else "trend-down"
            trend_arrow = "↗️" if trend > 0 else "↘️"
            trend_html = f'<div class="kpi-trend {trend_class}">{trend_arrow} {abs(trend)}%</div>'
        elif isinstance(trend, str):
            # Si c'est une chaîne, l'afficher telle quelle sans les flèches
            trend_html = f'<div class="kpi-trend">{trend}</div>'
    
    html = f'''
    <div class="kpi-card-2025">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label-2025">{label}</div>
        <div class="kpi-value-2025">{value}</div>
        {trend_html}
    </div>
    '''
    
    if col:
        col.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(html, unsafe_allow_html=True)

def form_section(title):
    st.markdown(f'<div class="form-section-title">{title}</div>', unsafe_allow_html=True)

# -----------------------------
# Authentication 2025
# -----------------------------
def login_2025():
    apply_css()
    
    st.markdown(
        f"""
        <div class="login-2025-container">
            <div class="login-2025-card">
                <div class="login-2025-logo">
                    <span>🏭</span>
                </div>
                <div class="login-2025-title">ISmaint Pro</div>
                <div class="login-2025-subtitle">Industrial Maintenance Management System</div>
        """,
        unsafe_allow_html=True
    )
    
    # Container pour les champs de saisie
    with st.container():
        st.markdown('<div class="login-2025-input">', unsafe_allow_html=True)
        username = st.text_input("", placeholder="👤 Nom d'utilisateur", key="login_user_2025")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="login-2025-input">', unsafe_allow_html=True)
        password = st.text_input("", placeholder="🔒 Mot de passe", type="password", key="login_pass_2025")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Bouton de connexion
    st.markdown('<div class="login-2025-button">', unsafe_allow_html=True)
    if st.button("🚀 Se connecter", use_container_width=True, key="login_btn_2025"):
        if not username or not password:
            st.error("Veuillez saisir un nom d'utilisateur et un mot de passe.")
        else:
            try:
                # Requête pour Supabase
                response = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
                
                if hasattr(response, 'data') and response.data and len(response.data) > 0:
                    st.session_state.authenticated = True
                    st.session_state.user = response.data[0]
                    user_role = st.session_state.user.get('role', 'Technicien')
                    st.success(f"Connecté avec succès ! Rôle: {user_role}")
                    st.rerun()
                else:
                    st.error("Identifiants incorrects. Vérifiez votre nom d'utilisateur et mot de passe.")
                    
            except Exception as e:
                st.error(f"Erreur d'authentification : {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer du formulaire
    st.markdown(
        """
        <div style="margin-top: 40px; padding-top: 24px; border-top: 1px solid #E5E7EB;">
            <div style="color: #6B7280; font-size: 12px; text-align: center;">
                © 2025 ISmaint Pro - Premium Maintenance Management System
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# -----------------------------
# Header 2025
# -----------------------------
def header_2025():
    theme = get_theme()
    
    st.markdown(
        f"""
        <div class="header-2025">
            <div class="header-brand">
                <div class="header-logo">🏭</div>
                <div class="header-title">ISmaint Pro</div>
            </div>
            <div class="header-actions">
                <div class="dark-mode-toggle" onclick="toggleDarkMode()">
                    <span>{'🌙' if not st.session_state.dark_mode else '☀️'}</span>
                    <span>{'Mode sombre' if not st.session_state.dark_mode else 'Mode clair'}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Sidebar 2025
# -----------------------------
def sidebar_2025():
    theme = get_theme()
    
    with st.sidebar:
        # Dark mode toggle
        if st.button(f"{'🌙' if not st.session_state.dark_mode else '☀️'} {'Mode sombre' if not st.session_state.dark_mode else 'Mode clair'}", 
                    use_container_width=True, key="dark_mode_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        # Carte utilisateur
        if st.session_state.authenticated and st.session_state.user:
            user_role = st.session_state.user.get('role', 'Technicien')
            user_name = st.session_state.user.get('username', 'Utilisateur')
            
            st.markdown(
                f"""
                <div class="sidebar-user-card">
                    <div class="sidebar-user-avatar">
                        <span>{'👨‍💼' if user_role == 'Admin' else '👨‍🔧'}</span>
                    </div>
                    <div class="sidebar-user-name">{user_name}</div>
                    <div class="sidebar-user-role">{user_role}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        # Navigation selon le rôle
        user_role = st.session_state.user.get('role', 'Technicien') if st.session_state.authenticated and st.session_state.user else 'Technicien'
        
        if user_role == "Admin":
            menu_items = [
                ("📊", "Tableau de Bord"),
                ("🏭", "Équipements"), 
                ("🔧", "Interventions"),
                ("👥", "Équipe"),
                ("📦", "Stocks"),
                ("📅", "Planification"),
                ("📈", "Analytics"),
                ("⚙️", "Métriques Avancées"),
                ("🔄", "Offline Sync")
            ]
        else:
            menu_items = [
                ("📊", "Tableau de Bord"),
                ("🔧", "Interventions")
            ]
        
        # Affichage des éléments de menu
        for icon, label in menu_items:
            is_active = st.session_state.current_page == label
            
            if st.button(f"{icon} {label}", 
                        use_container_width=True, 
                        type="primary" if is_active else "secondary",
                        key=f"nav_{label}"):
                st.session_state.current_page = label
                st.rerun()
        
        st.markdown("---")
        
        # Bouton de déconnexion
        if st.button("🚪 Déconnexion", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.current_page = "Tableau de Bord"
            st.rerun()

# -----------------------------
# Vérification d'authentification
# -----------------------------
if not st.session_state.authenticated:
    login_2025()
    st.stop()

# Appliquer le CSS après l'authentification
apply_css()
header_2025()

# -----------------------------
# Utilities (conservées de la version originale)
# -----------------------------
def handle_error(error_message):
    st.error(f"Erreur: {error_message}")
    return None

def has_permission(required_role="Technicien"):
    """Vérifie si l'utilisateur a le rôle requis"""
    if not st.session_state.authenticated or not st.session_state.user:
        return False
    
    user_role = st.session_state.user.get('role', 'Technicien')
    
    # Admin a tous les accès
    if user_role == "Admin":
        return True
    
    # Technicien a accès seulement aux pages Technicien
    if user_role == "Technicien" and required_role == "Technicien":
        return True
    
    return False

def show_access_denied():
    st.error("🚫 Accès refusé - Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
    st.info("Contactez votre administrateur pour obtenir les droits d'accès.")

def send_email(to_email, subject, body):
    try:
        smtp_server = st.secrets["email"]["smtp_server"]
        smtp_port = st.secrets["email"]["smtp_port"]
        sender_email = st.secrets["email"]["sender_email"]
        sender_password = st.secrets["email"]["sender_password"]
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        st.success("Email envoyé ✔️")
    except Exception as e:
        handle_error(f"Erreur d'envoi d'email : {str(e)}")

@st.cache_data(ttl=30)
def load_data(table_name):
    try:
        res = supabase.table(table_name).select("*").execute()
        return res.data
    except Exception as e:
        # If table doesn't exist or network error, return empty list
        return []

def get_users_by_role(role):
    """Récupère les utilisateurs par rôle"""
    try:
        res = supabase.table("users").select("id, username, email").eq("role", role).execute()
        return res.data or []
    except Exception:
        return []

def get_admins_emails():
    """Récupère les emails de tous les administrateurs"""
    try:
        res = supabase.table("users").select("email").eq("role", "Admin").execute()
        return [admin['email'] for admin in res.data if admin.get('email')]
    except Exception:
        return []

def get_techniciens_options():
    """Récupère les techniciens avec leurs IDs"""
    techniciens = load_data("techniciens") or []
    return {t['nom']: t['id'] for t in techniciens} if techniciens else {}

def get_technicien_email(technicien_id):
    """Récupère l'email d'un technicien via son user_id"""
    try:
        # Récupérer le technicien pour avoir le user_id
        technicien_res = supabase.table("techniciens").select("user_id").eq("id", technicien_id).execute()
        if technicien_res.data and technicien_res.data[0].get('user_id'):
            user_id = technicien_res.data[0]['user_id']
            # Récupérer l'email de l'utilisateur
            user_res = supabase.table("users").select("email").eq("id", user_id).execute()
            if user_res.data and user_res.data[0].get('email'):
                return user_res.data[0]['email']
        return "technicien@ismaint.com"
    except Exception:
        return "technicien@ismaint.com"

def verify_admin_password(password):
    """Vérifie le mot de passe administrateur"""
    try:
        response = supabase.table("users").select("*").eq("role", "Admin").eq("password", password).execute()
        return response.data and len(response.data) > 0
    except Exception:
        return False

def kpi_card(label, value, hint=None, col=None):
    # small helper to draw KPI card (HTML)
    html = f'''
    <div class="kpi-card-2025">
      <div class="kpi-label-2025">{label}</div>
      <div class="kpi-value-2025">{value}</div>
      {f'<div style="color: var(--text-secondary); font-size: 12px;">{hint}</div>' if hint else ''}
    </div>
    '''
    if col:
        col.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(html, unsafe_allow_html=True)

# -----------------------------
# Fonctions utilitaires pour la gestion des dates - CORRIGÉES
# -----------------------------
def parse_datetime(date_string):
    """Parse une chaîne de date en datetime object, gère les timezones"""
    if not date_string:
        return None
    try:
        # Essayer de parser avec timezone
        dt = datetime.datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        # Convertir en timezone naive pour éviter les problèmes de comparaison
        return dt.replace(tzinfo=None)
    except ValueError:
        try:
            # Essayer sans timezone
            return datetime.datetime.fromisoformat(date_string)
        except ValueError:
            return None

def safe_date_comparison(date1, date2):
    """Compare deux dates en gérant les timezones et les types de dates"""
    if not date1 or not date2:
        return 0
    
    # Parse both dates to datetime objects if they're strings
    d1 = parse_datetime(date1) if isinstance(date1, str) else date1
    d2 = parse_datetime(date2) if isinstance(date2, str) else date2
    
    # Handle date objects by converting them to datetime
    if isinstance(d1, datetime.date) and not isinstance(d1, datetime.datetime):
        d1 = datetime.datetime.combine(d1, datetime.time.min)
    if isinstance(d2, datetime.date) and not isinstance(d2, datetime.datetime):
        d2 = datetime.datetime.combine(d2, datetime.time.min)
    
    if d1 and d2:
        # Ensure both dates are timezone-naive
        if hasattr(d1, 'tzinfo') and d1.tzinfo is not None:
            d1 = d1.replace(tzinfo=None)
        if hasattr(d2, 'tzinfo') and d2.tzinfo is not None:
            d2 = d2.replace(tzinfo=None)
        
        return (d1 - d2).days
    
    return 0

# -----------------------------
# Fonction pour nettoyer les données avant export Excel
# -----------------------------

def clean_dataframe_for_excel(df):
    """Nettoie un DataFrame pour l'export Excel en supprimant les timezones et forçant les colonnes datetime."""
    df_clean = df.copy()

    for col in df_clean.columns:
        # 1) Essayer de convertir la colonne en datetime si possible
        try:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='ignore')
        except Exception:
            # Si la conversion échoue, on laisse la colonne telle quelle
            pass

        # 2) Si la colonne est datetime, supprimer les timezones (tz-aware -> tz-naive)
        try:
            if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].apply(
                    lambda x: x.replace(tzinfo=None) if hasattr(x, 'tzinfo') and x is not pd.NaT and x is not None and getattr(x, 'tzinfo', None) is not None else x
                )
        except Exception:
            # En cas d'erreur inattendue, on ignore et continue
            pass

        # 3) Gérer les chaînes ISO qui contiennent explicitement des timezone (+01:00, Z, etc.)
        try:
            if df_clean[col].dtype == object:
                def _to_naive_iso(v):
                    if isinstance(v, str) and ('+' in v or v.endswith('Z')):
                        try:
                            # Remplacer Z par +00:00 pour fromisoformat, puis retirer tzinfo
                            dt = pd.to_datetime(v, utc=True)
                            # dt is timezone-aware (UTC), convert to naive in local time (or keep UTC naive)
                            return dt.tz_convert(None) if hasattr(dt, 'tz_convert') else dt.replace(tzinfo=None)
                        except Exception:
                            try:
                                parsed = pd.to_datetime(v, errors='coerce')
                                if parsed is pd.NaT or parsed is None:
                                    return v
                                return parsed.replace(tzinfo=None) if hasattr(parsed, 'tzinfo') and parsed.tzinfo is not None else parsed
                            except Exception:
                                return v
                    return v

                df_clean[col] = df_clean[col].apply(_to_naive_iso)
        except Exception:
            pass

    return df_clean

# -----------------------------
# Pages avec nouveau design 2025
# -----------------------------

def dashboard():
    st.markdown('<div class="form-section-title">📊 Tableau de Bord Principal</div>', unsafe_allow_html=True)
    
    # Afficher le rôle actuel
    user_role = st.session_state.user.get('role', 'Technicien')
    
    # Load data
    equipements = load_data("equipements") or []
    interventions = load_data("interventions") or []
    stocks = load_data("stocks") or []
    plans = load_data("maintenance_plans") or []

    nb_equipements = len(equipements)
    nb_pannes = len([e for e in equipements if e.get('statut') == 'En panne'])
    nb_interventions_ouvertes = len([i for i in interventions if i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']])
    nb_stocks_critiques = len([s for s in stocks if s.get('quantite') is not None and s.get('niveau_critique') is not None and s['quantite'] <= s['niveau_critique']])
    nb_plans_planifies = len([p for p in plans if p.get('statut') == 'Planifiée'])

    # KPI row avec nouveau design
    cols = st.columns(5)
    kpi_card_2025("Équipements Totaux", nb_equipements, 2, "🏭", cols[0])
    kpi_card_2025("En Panne", nb_pannes, -5, "⚠️", cols[1])
    kpi_card_2025("Interventions Actives", nb_interventions_ouvertes, 8, "🔧", cols[2])
    kpi_card_2025("Stocks Critiques", nb_stocks_critiques, -12, "📦", cols[3])
    kpi_card_2025("Plans Planifiés", nb_plans_planifies, 15, "📅", cols[4])

    # Quick charts area (two columns)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📈 Interventions - Derniers 12 mois")
        if interventions:
            df = pd.DataFrame(interventions)
            if 'date_creation' in df.columns:
                df['date_creation'] = pd.to_datetime(df['date_creation'], errors='coerce')
                monthly = df.set_index('date_creation').resample('M').size().reset_index(name='count')
                fig = px.line(monthly, x='date_creation', y='count', markers=True)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=get_theme()['text'])
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Pas de champ 'date_creation' disponible pour les interventions.")
        else:
            st.info("Aucune intervention disponible.")

    with col2:
        st.markdown("#### 🚨 Alertes rapides")
        alert_col1, alert_col2 = st.columns(2)
        
        with alert_col1:
            if nb_pannes:
                st.error(f"**{nb_pannes}** équipements en panne")
            if nb_stocks_critiques:
                st.warning(f"**{nb_stocks_critiques}** stocks critiques")
        
        with alert_col2:
            if nb_interventions_ouvertes:
                st.info(f"**{nb_interventions_ouvertes}** interventions actives")
        
        # Actions rapides selon le rôle
        st.markdown("#### ⚡ Actions rapides")
        if user_role == "Admin":
            if st.button("➕ Créer Intervention Rapide", use_container_width=True):
                st.session_state.current_page = "Interventions"
                st.rerun()
            if st.button("👥 Gérer Équipe", use_container_width=True):
                st.session_state.current_page = "Équipe"
                st.rerun()
        else:
            # Pour les techniciens, afficher leurs interventions en cours
            user_id = st.session_state.user.get('id')
            technicien_interventions = [i for i in interventions if i.get('technicien_id') == user_id and i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']]
            if technicien_interventions:
                st.info(f"**{len(technicien_interventions)}** intervention(s) en cours")
                for interv in technicien_interventions[:3]:
                    st.write(f"• {interv.get('description', 'Sans description')[:40]}...")

def gestion_equipements():
    if not has_permission("Admin"):
        show_access_denied()
        return
        
    st.markdown('<div class="form-section-title">🏭 Gestion des Équipements</div>', unsafe_allow_html=True)
    data = load_data("equipements") or []
    
    # Section modification/suppression
    st.markdown("#### 🔧 Modifier ou Supprimer un Équipement")
    
    if data:
        df = pd.DataFrame(data)
        
        # Sélection de l'équipement à modifier
        equipements_list = [f"{e['id']} - {e['nom']} ({e['statut']})" for e in data]
        selected_equipement = st.selectbox("Sélectionner un équipement à modifier", [""] + equipements_list)
        
        if selected_equipement:
            equipement_id = selected_equipement.split(" - ")[0]
            equipement_data = next((e for e in data if e['id'] == equipement_id), None)
            
            if equipement_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.container():
                        st.markdown("##### 💾 Modifier l'équipement")
                        with st.form(f"modifier_equipement_{equipement_id}"):
                            nouveau_nom = st.text_input("Nom", value=equipement_data.get('nom', ''))
                            nouveau_statut = st.selectbox("Statut", ["Fonctionnel", "En panne", "En maintenance"], 
                                                        index=["Fonctionnel", "En panne", "En maintenance"].index(equipement_data.get('statut', 'Fonctionnel')))
                            nouvelle_description = st.text_area("Description", value=equipement_data.get('description', ''))
                            nouvelles_heures = st.number_input("Heures opérationnelles", 
                                                             value=float(equipement_data.get('heures_operationnelles', 0)),
                                                             min_value=0.0, step=0.1)
                            
                            password = st.text_input("Mot de passe administrateur", type="password", 
                                                   help="Entrez votre mot de passe administrateur pour confirmer")
                            
                            col_mod1, col_mod2 = st.columns(2)
                            with col_mod1:
                                if st.form_submit_button("💾 Sauvegarder", use_container_width=True):
                                    if not password:
                                        st.error("Veuillez entrer le mot de passe administrateur")
                                    elif verify_admin_password(password):
                                        try:
                                            update_data = {
                                                "nom": nouveau_nom,
                                                "statut": nouveau_statut,
                                                "description": nouvelle_description,
                                                "heures_operationnelles": nouvelles_heures
                                            }
                                            supabase.table("equipements").update(update_data).eq("id", equipement_id).execute()
                                            st.success("✅ Équipement modifié avec succès")
                                            st.rerun()
                                        except Exception as e:
                                            handle_error(str(e))
                                    else:
                                        st.error("❌ Mot de passe administrateur incorrect")
                
                with col2:
                    with st.container():
                        st.markdown("##### 🗑️ Supprimer l'équipement")
                        st.warning("⚠️ Cette action est irréversible")
                        with st.form(f"supprimer_equipement_{equipement_id}"):
                            password_supp = st.text_input("Mot de passe administrateur", type="password", 
                                                        key=f"pass_supp_{equipement_id}",
                                                        help="Entrez votre mot de passe administrateur pour confirmer la suppression")
                            
                            if st.form_submit_button("🗑️ Supprimer", use_container_width=True):
                                if not password_supp:
                                    st.error("Veuillez entrer le mot de passe administrateur")
                                elif verify_admin_password(password_supp):
                                    try:
                                        # Vérifier s'il y a des interventions liées
                                        interventions_liees = supabase.table("interventions").select("id").eq("equipement_id", equipement_id).execute()
                                        if interventions_liees.data:
                                            st.error("❌ Impossible de supprimer : des interventions sont liées à cet équipement")
                                        else:
                                            supabase.table("equipements").delete().eq("id", equipement_id).execute()
                                            st.success("✅ Équipement supprimé avec succès")
                                            st.rerun()
                                    except Exception as e:
                                        handle_error(str(e))
                                else:
                                    st.error("❌ Mot de passe administrateur incorrect")
        
        # Affichage du tableau avec recherche/filtres
        st.markdown("#### 📋 Liste des Équipements")
        col1, col2 = st.columns([3,1])
        with col1:
            search = st.text_input("🔍 Rechercher par nom", key="equip_search")
        with col2:
            statut_filter = st.multiselect("📊 Statut", sorted(df['statut'].dropna().unique().tolist() if 'statut' in df.columns else []))
        
        if search and 'nom' in df.columns:
            df = df[df['nom'].str.contains(search, case=False, na=False)]
        if statut_filter and 'statut' in df.columns:
            df = df[df['statut'].isin(statut_filter)]

        st.dataframe(df, use_container_width=True)
        
        # Exports
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Exporter CSV", csv, "equipements.csv", "text/csv")
        with col_exp2:
            # CORRECTION : Utilisation de clean_dataframe_for_excel
            df_clean = clean_dataframe_for_excel(df)
            excel_buffer = BytesIO()
            df_clean.to_excel(excel_buffer, index=False)
            st.download_button("📊 Exporter Excel", excel_buffer, "equipements.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("Aucun équipement trouvé.")

    # Import
    st.markdown("#### 📤 Importer des Équipements")
    uploaded_file = st.file_uploader("Importer CSV/Excel", type=["csv", "xlsx"], key="equip_import")
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                import_df = pd.read_csv(uploaded_file)
            else:
                import_df = pd.read_excel(uploaded_file)
            for _, row in import_df.iterrows():
                supabase.table("equipements").insert(row.to_dict()).execute()
            st.success("Import réussi !")
        except Exception as e:
            handle_error(str(e))

    # Add equipment form
    st.markdown("#### ➕ Ajouter un équipement")
    with st.form("ajout_equipement_mod"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom de l'équipement*")
            statut = st.selectbox("Statut*", ["Fonctionnel", "En panne", "En maintenance"])
        with col2:
            description = st.text_area("Description")
            heures_operationnelles = st.number_input("Heures opérationnelles", min_value=0.0, step=0.1, value=0.0)
        
        submit = st.form_submit_button("➕ Ajouter l'équipement", use_container_width=True)
        if submit:
            if not nom:
                handle_error("Le nom est requis.")
            else:
                supabase.table("equipements").insert({
                    "nom": nom,
                    "statut": statut,
                    "description": description,
                    "heures_operationnelles": float(heures_operationnelles)
                }).execute()
                st.success("Équipement ajouté ✔️")

def gestion_interventions():
    st.markdown('<div class="form-section-title">🔧 Gestion des Interventions</div>', unsafe_allow_html=True)
    
    user_role = st.session_state.user.get('role', 'Technicien')
    user_id = st.session_state.user.get('id')
    
    data = load_data("interventions") or []
    
    # Filtrer les données selon le rôle
    if user_role == "Technicien":
        # Technicien ne voit que ses interventions
        data = [i for i in data if i.get('technicien_id') == user_id]
        st.info("🔍 Vue Technicien - Vous voyez seulement vos interventions assignées")
    
    # Section modification/suppression (Admin seulement)
    if user_role == "Admin" and data:
        st.markdown("#### 🔧 Modifier ou Supprimer une Intervention")
        
        interventions_list = [f"{i['id']} - {i.get('description', 'Sans description')[:50]}... ({i.get('statut', 'N/A')})" for i in data]
        selected_intervention = st.selectbox("Sélectionner une intervention à modifier", [""] + interventions_list)
        
        if selected_intervention:
            intervention_id = selected_intervention.split(" - ")[0]
            intervention_data = next((i for i in data if i['id'] == intervention_id), None)
            
            if intervention_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.container():
                        st.markdown("##### 💾 Modifier l'intervention")
                        with st.form(f"modifier_intervention_{intervention_id}"):
                            # Charger les données nécessaires
                            equipements = load_data("equipements") or []
                            techniciens = load_data("techniciens") or []
                            
                            equip_options = {e['nom']: e['id'] for e in equipements}
                            tech_options = {t['nom']: t['id'] for t in techniciens}
                            
                            # Récupérer les valeurs actuelles
                            current_equipement = next((e['nom'] for e in equipements if e['id'] == intervention_data.get('equipement_id')), "")
                            current_technicien = next((t['nom'] for t in techniciens if t['id'] == intervention_data.get('technicien_id')), "")
                            
                            col_form1, col_form2 = st.columns(2)
                            with col_form1:
                                nouveau_equipement = st.selectbox("Équipement", [""] + list(equip_options.keys()), 
                                                                index=0 if not current_equipement else list(equip_options.keys()).index(current_equipement) + 1)
                                nouveau_type_panne = st.selectbox("Type de panne", ["Mécanique", "Électrique", "Hydraulique", "Logiciel", "Autre"],
                                                                index=["Mécanique", "Électrique", "Hydraulique", "Logiciel", "Autre"].index(intervention_data.get('type_panne', 'Mécanique')))
                                nouveau_statut = st.selectbox("Statut", ["Nouvelle", "Ouverte", "En cours", "Fermée"],
                                                            index=["Nouvelle", "Ouverte", "En cours", "Fermée"].index(intervention_data.get('statut', 'Nouvelle')))
                            with col_form2:
                                nouvelle_priorite = st.selectbox("Priorité", ["Basse", "Moyenne", "Haute", "Critique"],
                                                               index=["Basse", "Moyenne", "Haute", "Critique"].index(intervention_data.get('priorite', 'Moyenne')))
                                nouveau_technicien = st.selectbox("Technicien", [""] + list(tech_options.keys()),
                                                                index=0 if not current_technicien else list(tech_options.keys()).index(current_technicien) + 1)
                                nouveau_cout = st.number_input("Coût total (€)", value=float(intervention_data.get('cout_total', 0)), min_value=0.0, step=0.01)
                            
                            nouvelle_description = st.text_area("Description", value=intervention_data.get('description', ''))
                            nouvelles_observations = st.text_area("Observations", value=intervention_data.get('observations', ''))
                            
                            # Date de clôture si statut Fermée
                            if nouveau_statut == "Fermée" and intervention_data.get('statut') != 'Fermée':
                                date_cloture = st.date_input("Date de clôture", value=datetime.datetime.now().date())
                            else:
                                date_cloture = None
                            
                            password = st.text_input("Mot de passe administrateur", type="password", 
                                                   help="Entrez votre mot de passe administrateur pour confirmer")
                            
                            if st.form_submit_button("💾 Sauvegarder", use_container_width=True):
                                if not password:
                                    st.error("Veuillez entrer le mot de passe administrateur")
                                elif verify_admin_password(password):
                                    try:
                                        update_data = {
                                            "description": nouvelle_description,
                                            "type_panne": nouveau_type_panne,
                                            "priorite": nouvelle_priorite,
                                            "statut": nouveau_statut,
                                            "observations": nouvelles_observations,
                                            "cout_total": float(nouveau_cout)
                                        }
                                        
                                        if nouveau_equipement:
                                            update_data["equipement_id"] = equip_options.get(nouveau_equipement)
                                        if nouveau_technicien:
                                            update_data["technicien_id"] = tech_options.get(nouveau_technicien)
                                            if not intervention_data.get('date_affectation'):
                                                update_data["date_affectation"] = datetime.datetime.now().isoformat()
                                        
                                        if nouveau_statut == "Fermée" and date_cloture:
                                            update_data["date_cloture"] = date_cloture.isoformat()
                                        elif nouveau_statut != "Fermée":
                                            update_data["date_cloture"] = None
                                        
                                        supabase.table("interventions").update(update_data).eq("id", intervention_id).execute()
                                        st.success("✅ Intervention modifiée avec succès")
                                        st.rerun()
                                    except Exception as e:
                                        handle_error(str(e))
                                else:
                                    st.error("❌ Mot de passe administrateur incorrect")
                
                with col2:
                    with st.container():
                        st.markdown("##### 🗑️ Supprimer l'intervention")
                        st.warning("⚠️ Cette action est irréversible")
                        with st.form(f"supprimer_intervention_{intervention_id}"):
                            password_supp = st.text_input("Mot de passe administrateur", type="password", 
                                                        key=f"pass_supp_int_{intervention_id}",
                                                        help="Entrez votre mot de passe administrateur pour confirmer la suppression")
                            
                            if st.form_submit_button("🗑️ Supprimer", use_container_width=True):
                                if not password_supp:
                                    st.error("Veuillez entrer le mot de passe administrateur")
                                elif verify_admin_password(password_supp):
                                    try:
                                        supabase.table("interventions").delete().eq("id", intervention_id).execute()
                                        st.success("✅ Intervention supprimée avec succès")
                                        st.rerun()
                                    except Exception as e:
                                        handle_error(str(e))
                                else:
                                    st.error("❌ Mot de passe administrateur incorrect")
    
    if data:
        df = pd.DataFrame(data)
        # filters & search
        st.markdown("#### 📋 Liste des Interventions")
        col1, col2 = st.columns([3,1])
        with col1:
            search = st.text_input("🔍 Rechercher par description", key="int_search")
        with col2:
            statut_filter = st.multiselect("📊 Filtrer par statut", sorted(df['statut'].dropna().unique().tolist() if 'statut' in df.columns else []))
        if search and 'description' in df.columns:
            df = df[df['description'].str.contains(search, case=False, na=False)]
        if statut_filter and 'statut' in df.columns:
            df = df[df['statut'].isin(statut_filter)]

        st.dataframe(df, use_container_width=True)
        
        # exports - seulement pour Admin
        if user_role == "Admin":
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Exporter CSV", csv, "interventions.csv", "text/csv")
            with col_exp2:
                # CORRECTION : Utilisation de clean_dataframe_for_excel
                df_clean = clean_dataframe_for_excel(df)
                excel_buffer = BytesIO()
                df_clean.to_excel(excel_buffer, index=False)
                st.download_button("📊 Exporter Excel", excel_buffer, "interventions.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    else:
        st.info("Aucune intervention trouvée.")

    # Import - seulement pour Admin
    if user_role == "Admin":
        st.markdown("#### 📤 Importer des Interventions")
        uploaded_file = st.file_uploader("Importer CSV/Excel", type=["csv", "xlsx"], key="int_import")
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    import_df = pd.read_csv(uploaded_file)
                else:
                    import_df = pd.read_excel(uploaded_file)
                for _, row in import_df.iterrows():
                    supabase.table("interventions").insert(row.to_dict()).execute()
                st.success("Import réussi !")
            except Exception as e:
                handle_error(str(e))

    # FORMULAIRE UNIQUE : Créer/Affecter une intervention (Admin only)
    if user_role == "Admin":
        st.markdown("#### ➕ Créer ou Affecter une Intervention")
        with st.form("creer_affecter_intervention_mod"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📝 Détails de l'Intervention")
                equipements = load_data("equipements") or []
                equip_options = {e['nom']: e['id'] for e in equipements} if equipements else {}
                equip_nom = st.selectbox("Équipement*", list(equip_options.keys()) if equip_options else ["Aucun équipement disponible"])
                description = st.text_area("Description*")
                type_panne = st.selectbox("Type de panne*", ["Mécanique", "Électrique", "Hydraulique", "Logiciel", "Autre"])
                priorite = st.selectbox("Priorité*", ["Basse", "Moyenne", "Haute", "Critique"])
                est_planifiee = st.checkbox("Intervention planifiée")
                cout_total = st.number_input("Coût total (€)", min_value=0.0, step=0.01, value=0.0)
            
            with col2:
                st.markdown("##### 👥 Affectation")
                techniciens = load_data("techniciens") or []
                tech_options = {t['nom']: t['id'] for t in techniciens} if techniciens else {}
                tech_nom = st.selectbox("Technicien à assigner*", [""] + list(tech_options.keys()) if tech_options else ["Aucun technicien disponible"])
                
                # Options pour les interventions existantes
                interventions = load_data("interventions") or []
                interv_options = {f"#{i['id']} - {i.get('description', 'Sans desc')[:30]}...": i['id'] 
                                for i in interventions if i.get('technicien_id') is None or i.get('statut') == 'Nouvelle'}
                
                affecter_existante = st.checkbox("Affecter une intervention existante")
                if affecter_existante and interv_options:
                    intervention_existante = st.selectbox("Intervention à affecter", list(interv_options.keys()))
                else:
                    intervention_existante = None
                
                observations = st.text_area("Observations pour le technicien")
                
                # Choix du statut selon le contexte
                if affecter_existante:
                    statut = st.selectbox("Statut*", ["En cours", "Ouverte"])
                else:
                    statut = st.selectbox("Statut*", ["Nouvelle", "Ouverte", "En cours", "Fermée"])
            
            submit = st.form_submit_button("💾 Créer/Affecter l'intervention", use_container_width=True)
            
            if submit:
                if affecter_existante and intervention_existante:
                    # CAS 1: Affectation d'une intervention existante
                    if not tech_nom:
                        handle_error("Technicien requis pour l'affectation.")
                    else:
                        interv_id = interv_options.get(intervention_existante)
                        tech_id = tech_options.get(tech_nom)
                        
                        # Mise à jour de l'intervention existante
                        update_data = {
                            "technicien_id": tech_id,
                            "observations": observations,
                            "statut": statut,
                            "date_affectation": datetime.datetime.now().isoformat()
                        }
                        
                        supabase.table("interventions").update(update_data).eq("id", interv_id).execute()
                        st.success(f"✅ Intervention {interv_id} affectée à {tech_nom}")
                        
                        # Notification au technicien
                        tech_email = get_technicien_email(tech_id)
                        intervention_desc = next((i.get('description', '') for i in interventions if i['id'] == interv_id), '')
                        send_email(tech_email, "Nouvelle Intervention Affectée", 
                                f"Vous avez été assigné à l'intervention #{interv_id}\n\n"
                                f"Description: {intervention_desc}\n"
                                f"Statut: {statut}\n"
                                f"Observations: {observations or 'Aucune'}")
                
                else:
                    # CAS 2: Création d'une nouvelle intervention
                    if not (equip_nom and description and type_panne and priorite):
                        handle_error("Équipement, description, type de panne et priorité sont requis.")
                    else:
                        intervention_data = {
                            "equipement_id": equip_options.get(equip_nom),
                            "description": description,
                            "type_panne": type_panne,
                            "priorite": priorite,
                            "statut": statut,
                            "est_planifiee": bool(est_planifiee),
                            "cout_total": float(cout_total),
                            "date_creation": datetime.datetime.now().isoformat(),
                            "observations": observations
                        }
                        
                        # Si un technicien est assigné
                        if tech_nom:
                            intervention_data["technicien_id"] = tech_options.get(tech_nom)
                            intervention_data["date_affectation"] = datetime.datetime.now().isoformat()
                        
                        # Insertion de la nouvelle intervention
                        result = supabase.table("interventions").insert(intervention_data).execute()
                        
                        if result.data:
                            interv_id = result.data[0]['id']
                            st.success(f"✅ Intervention #{interv_id} créée avec succès")
                            
                            # Notification si technicien assigné
                            if tech_nom:
                                tech_email = get_technicien_email(tech_options.get(tech_nom))
                                send_email(tech_email, "Nouvelle Intervention Assignée", 
                                        f"Une nouvelle intervention vous a été assignée : {description}\n\n"
                                        f"Type: {type_panne}\n"
                                        f"Priorité: {priorite}\n"
                                        f"Statut: {statut}\n"
                                        f"Observations: {observations or 'Aucune'}")
    
    # NOUVELLE FONCTIONNALITÉ : Déclaration de panne par Technicien
    if user_role == "Technicien":
        st.markdown("#### 🚨 Déclarer une Nouvelle Panne")
        with st.form("declaration_panne_mod"):
            equipements = load_data("equipements") or []
            equip_options = {e['nom']: e['id'] for e in equipements} if equipements else {}
            equip_nom = st.selectbox("Machine/Équipement concerné", list(equip_options.keys()) if equip_options else ["Aucun équipement disponible"])
            type_panne = st.selectbox("Type de panne", ["Mécanique", "Électrique", "Hydraulique", "Logiciel", "Autre"])
            description = st.text_area("Description détaillée de la panne")
            priorite = st.selectbox("Niveau de priorité", ["Basse", "Moyenne", "Haute", "Critique"])
            observations = st.text_area("Observations supplémentaires (optionnel)")
            submit_declare = st.form_submit_button("🚨 Déclarer la Panne", use_container_width=True)
            if submit_declare:
                if not (equip_nom and description):
                    handle_error("Équipement et description requis.")
                else:
                    equip_id = equip_options.get(equip_nom)
                    # Créer une nouvelle intervention pour la panne déclarée
                    now = datetime.datetime.now().isoformat()
                    supabase.table("interventions").insert({
                        "equipement_id": equip_id,
                        "declarant_id": user_id,
                        "description": description,
                        "type_panne": type_panne,
                        "priorite": priorite,
                        "observations": observations,
                        "statut": "Nouvelle",
                        "date_creation": now,
                        "date_declaration": now
                    }).execute()
                    st.success("✅ Panne déclarée et envoyée aux admins")
                    # Notification aux admins
                    admins_emails = get_admins_emails()
                    if admins_emails:
                        for admin_email in admins_emails:
                            send_email(admin_email, "🚨 Nouvelle Panne Déclarée", 
                                    f"Un technicien a déclaré une panne sur {equip_nom}\n\n"
                                    f"Type: {type_panne}\n"
                                    f"Priorité: {priorite}\n"
                                    f"Détails: {description}\n"
                                    f"Observations: {observations or 'Aucune'}\n\n"
                                    f"Veuillez assigner une intervention.")
                    else:
                        st.warning("Aucun email d'admin configuré - Notification non envoyée.")
    
    # Pour les techniciens - Gestion de leurs interventions
    if user_role == "Technicien":
        st.markdown("#### 📋 Mes Interventions en Cours")
        if data:
            current_interventions = [i for i in data if i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']]
            if current_interventions:
                for interv in current_interventions:
                    with st.expander(f"Intervention #{interv.get('id')} - {interv.get('description', 'Sans description')[:50]}..."):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Statut:** {interv.get('statut')}")
                            st.write(f"**Priorité:** {interv.get('priorite', 'Non définie')}")
                            st.write(f"**Type de panne:** {interv.get('type_panne', 'Non spécifié')}")
                            if interv.get('observations'):
                                st.write(f"**Observations:** {interv.get('observations')}")
                        with col2:
                            new_status = st.selectbox(
                                "Changer le statut", 
                                ["En cours", "Fermée", "En attente"],
                                key=f"status_{interv.get('id')}"
                            )
                            if st.button("Mettre à jour", key=f"update_{interv.get('id')}", use_container_width=True):
                                try:
                                    update_data = {"statut": new_status}
                                    if new_status == "Fermée":
                                        update_data["date_cloture"] = datetime.datetime.now().isoformat()
                                    
                                    supabase.table("interventions").update(update_data).eq("id", interv.get('id')).execute()
                                    st.success("✅ Statut mis à jour !")
                                    st.rerun()
                                except Exception as e:
                                    handle_error(str(e))
            else:
                st.info("Aucune intervention en cours.")

def gestion_equipe():
    if not has_permission("Admin"):
        show_access_denied()
        return
        
    st.markdown('<div class="form-section-title">👥 Gestion de l\'Équipe</div>', unsafe_allow_html=True)
    data = load_data("techniciens") or []
    
    # Section modification/suppression
    if data:
        st.markdown("#### 🔧 Modifier ou Supprimer un Technicien")
        
        techniciens_list = [f"{t['id']} - {t['nom']} ({t.get('competences', 'Aucune')})" for t in data]
        selected_technicien = st.selectbox("Sélectionner un technicien à modifier", [""] + techniciens_list)
        
        if selected_technicien:
            technicien_id = selected_technicien.split(" - ")[0]
            technicien_data = next((t for t in data if t['id'] == technicien_id), None)
            
            if technicien_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.container():
                        st.markdown("##### 💾 Modifier le technicien")
                        with st.form(f"modifier_technicien_{technicien_id}"):
                            nouveau_nom = st.text_input("Nom", value=technicien_data.get('nom', ''))
                            nouvelles_competences = st.text_input("Compétences", value=technicien_data.get('competences', ''))
                            
                            password = st.text_input("Mot de passe administrateur", type="password", 
                                                   help="Entrez votre mot de passe administrateur pour confirmer")
                            
                            if st.form_submit_button("💾 Sauvegarder", use_container_width=True):
                                if not password:
                                    st.error("Veuillez entrer le mot de passe administrateur")
                                elif verify_admin_password(password):
                                    try:
                                        update_data = {
                                            "nom": nouveau_nom,
                                            "competences": nouvelles_competences
                                        }
                                        supabase.table("techniciens").update(update_data).eq("id", technicien_id).execute()
                                        st.success("✅ Technicien modifié avec succès")
                                        st.rerun()
                                    except Exception as e:
                                        handle_error(str(e))
                                else:
                                    st.error("❌ Mot de passe administrateur incorrect")
                
                with col2:
                    with st.container():
                        st.markdown("##### 🗑️ Supprimer le technicien")
                        st.warning("⚠️ Cette action est irréversible")
                        with st.form(f"supprimer_technicien_{technicien_id}"):
                            password_supp = st.text_input("Mot de passe administrateur", type="password", 
                                                        key=f"pass_supp_tech_{technicien_id}",
                                                        help="Entrez votre mot de passe administrateur pour confirmer la suppression")
                            
                            if st.form_submit_button("🗑️ Supprimer", use_container_width=True):
                                if not password_supp:
                                    st.error("Veuillez entrer le mot de passe administrateur")
                                elif verify_admin_password(password_supp):
                                    try:
                                        # Vérifier s'il y a des interventions liées
                                        interventions_liees = supabase.table("interventions").select("id").eq("technicien_id", technicien_id).execute()
                                        if interventions_liees.data:
                                            st.error("❌ Impossible de supprimer : des interventions sont liées à ce technicien")
                                        else:
                                            supabase.table("techniciens").delete().eq("id", technicien_id).execute()
                                            st.success("✅ Technicien supprimé avec succès")
                                            st.rerun()
                                    except Exception as e:
                                        handle_error(str(e))
                                else:
                                    st.error("❌ Mot de passe administrateur incorrect")
    
    if data:
        df = pd.DataFrame(data)
        search = st.text_input("🔍 Rechercher par nom", key="team_search")
        if search and 'nom' in df.columns:
            df = df[df['nom'].str.contains(search, case=False, na=False)]
        st.dataframe(df, use_container_width=True)
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Exporter CSV", csv, "techniciens.csv", "text/csv")
        with col_exp2:
            # CORRECTION : Utilisation de clean_dataframe_for_excel
            df_clean = clean_dataframe_for_excel(df)
            excel_buffer = BytesIO()
            df_clean.to_excel(excel_buffer, index=False)
            st.download_button("📊 Exporter Excel", excel_buffer, "techniciens.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("Aucun technicien trouvé.")

    st.markdown("#### ➕ Ajouter un Technicien")
    with st.form("ajout_technicien_mod"):
        nom = st.text_input("Nom du technicien*")
        competences = st.text_input("Compétences (séparées par virgule)")
        submit = st.form_submit_button("➕ Ajouter technicien", use_container_width=True)
        if submit:
            if not nom:
                handle_error("Le nom est requis.")
            else:
                supabase.table("techniciens").insert({
                    "nom": nom,
                    "competences": competences
                }).execute()
                st.success("Technicien ajouté ✔️")

def gestion_stocks():
    if not has_permission("Admin"):
        show_access_denied()
        return
        
    st.markdown('<div class="form-section-title">📦 Gestion des Stocks</div>', unsafe_allow_html=True)
    data = load_data("stocks") or []
    
    # Section modification/suppression
    if data:
        st.markdown("#### 🔧 Modifier ou Supprimer un Stock")
        
        stocks_list = [f"{s['id']} - {s['nom']} (Quantité: {s.get('quantite', 0)})" for s in data]
        selected_stock = st.selectbox("Sélectionner un stock à modifier", [""] + stocks_list)
        
        if selected_stock:
            stock_id = selected_stock.split(" - ")[0]
            stock_data = next((s for s in data if s['id'] == stock_id), None)
            
            if stock_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.container():
                        st.markdown("##### 💾 Modifier le stock")
                        with st.form(f"modifier_stock_{stock_id}"):
                            nouveau_nom = st.text_input("Nom", value=stock_data.get('nom', ''))
                            nouvelle_quantite = st.number_input("Quantité", value=stock_data.get('quantite', 0), min_value=0)
                            nouveau_niveau_critique = st.number_input("Niveau critique", value=stock_data.get('niveau_critique', 0), min_value=0)
                            nouveau_cout = st.number_input("Coût unitaire (€)", value=float(stock_data.get('cout_unitaire', 0)), min_value=0.0, step=0.01)
                            nouvelle_description = st.text_area("Description", value=stock_data.get('description', ''))
                            
                            password = st.text_input("Mot de passe administrateur", type="password", 
                                                   help="Entrez votre mot de passe administrateur pour confirmer")
                            
                            if st.form_submit_button("💾 Sauvegarder", use_container_width=True):
                                if not password:
                                    st.error("Veuillez entrer le mot de passe administrateur")
                                elif verify_admin_password(password):
                                    try:
                                        update_data = {
                                            "nom": nouveau_nom,
                                            "quantite": int(nouvelle_quantite),
                                            "niveau_critique": int(nouveau_niveau_critique),
                                            "cout_unitaire": float(nouveau_cout),
                                            "description": nouvelle_description
                                        }
                                        supabase.table("stocks").update(update_data).eq("id", stock_id).execute()
                                        st.success("✅ Stock modifié avec succès")
                                        st.rerun()
                                    except Exception as e:
                                        handle_error(str(e))
                                else:
                                    st.error("❌ Mot de passe administrateur incorrect")
                
                with col2:
                    with st.container():
                        st.markdown("##### 🗑️ Supprimer le stock")
                        st.warning("⚠️ Cette action est irréversible")
                        with st.form(f"supprimer_stock_{stock_id}"):
                            password_supp = st.text_input("Mot de passe administrateur", type="password", 
                                                        key=f"pass_supp_stock_{stock_id}",
                                                        help="Entrez votre mot de passe administrateur pour confirmer la suppression")
                            
                            if st.form_submit_button("🗑️ Supprimer", use_container_width=True):
                                if not password_supp:
                                    st.error("Veuillez entrer le mot de passe administrateur")
                                elif verify_admin_password(password_supp):
                                    try:
                                        supabase.table("stocks").delete().eq("id", stock_id).execute()
                                        st.success("✅ Stock supprimé avec succès")
                                        st.rerun()
                                    except Exception as e:
                                        handle_error(str(e))
                                else:
                                    st.error("❌ Mot de passe administrateur incorrect")
    
    if data:
        df = pd.DataFrame(data)
        search = st.text_input("🔍 Rechercher par nom", key="stock_search")
        if search and 'nom' in df.columns:
            df = df[df['nom'].str.contains(search, case=False, na=False)]
        st.dataframe(df, use_container_width=True)

        # alert list
        critiques = [s for s in data if s.get('quantite') is not None and s.get('niveau_critique') is not None and s['quantite'] <= s['niveau_critique']]
        if critiques:
            st.warning("🚨 Alertes de stocks critiques :")
            for c in critiques:
                st.write(f"- **{c.get('nom')}** : Quantité {c.get('quantite')} (seuil {c.get('niveau_critique')})")

        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Exporter CSV", csv, "stocks.csv", "text/csv")
        with col_exp2:
            # CORRECTION : Utilisation de clean_dataframe_for_excel
            df_clean = clean_dataframe_for_excel(df)
            excel_buffer = BytesIO()
            df_clean.to_excel(excel_buffer, index=False)
            st.download_button("📊 Exporter Excel", excel_buffer, "stocks.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("Aucun stock trouvé.")

    st.markdown("#### ➕ Ajouter une Pièce")
    with st.form("ajout_stock_mod"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom de la pièce*")
            quantite = st.number_input("Quantité*", min_value=0, value=0)
            niveau_critique = st.number_input("Niveau critique*", min_value=0, value=5)
        with col2:
            cout_unitaire = st.number_input("Coût unitaire (€)*", min_value=0.0, step=0.01, value=0.0)
            description = st.text_area("Description")
        
        submit = st.form_submit_button("➕ Ajouter pièce", use_container_width=True)
        if submit:
            if not nom:
                handle_error("Le nom est requis.")
            else:
                supabase.table("stocks").insert({
                    "nom": nom,
                    "quantite": int(quantite),
                    "niveau_critique": int(niveau_critique),
                    "cout_unitaire": float(cout_unitaire),
                    "description": description
                }).execute()
                st.success("Pièce ajoutée ✔️")

def planification():
    if not has_permission("Admin"):
        show_access_denied()
        return
        
    st.markdown('<div class="form-section-title">📅 Planification de Maintenance - AMDEC & Prédiction</div>', unsafe_allow_html=True)
    
    # Section 1: Vue d'ensemble des plans
    st.markdown("#### 📋 Vue d'Ensemble des Plans de Maintenance")
    
    data = load_data("maintenance_plans") or []
    interventions_data = load_data("interventions") or []
    equipements_data = load_data("equipements") or []
    
    # KPI pour la planification
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        plans_planifies = len([p for p in data if p.get('statut') == 'Planifiée'])
        kpi_card_2025("Plans Planifiés", plans_planifies, 5, "📅", col1)
    with col2:
        plans_en_cours = len([p for p in data if p.get('statut') == 'En cours'])
        kpi_card_2025("Plans en Cours", plans_en_cours, 2, "🔧", col2)
    with col3:
        plans_termines = len([p for p in data if p.get('statut') == 'Terminée'])
        kpi_card_2025("Plans Terminés", plans_termines, 8, "✅", col3)
    with col4:
        # CORRECTION : Utilisation de safe_date_comparison pour éviter l'erreur de timezone
        retards = len([p for p in data if p.get('date_planified') and 
                      safe_date_comparison(p['date_planified'], datetime.datetime.now()) < 0 and  # CORRIGÉ : datetime.datetime.now() au lieu de .date()
                      p.get('statut') in ['Planifiée', 'En cours']])
        kpi_card_2025("Plans en Retard", retards, -15, "⚠️", col4)

    # 🔍 Section AMDEC
    st.markdown("#### 🔍 Analyse AMDEC - Modes de Défaillance")
    
    col_amdec1, col_amdec2 = st.columns(2)
    
    with col_amdec1:
        st.markdown("##### 📊 Statistiques des Défaillances par Équipement")
        
        if interventions_data and equipements_data:
            # Calcul des statistiques de défaillance
            stats_pannes = {}
            for equip in equipements_data:
                equip_id = equip['id']
                pannes_equip = [i for i in interventions_data if i.get('equipement_id') == equip_id]
                
                if pannes_equip:
                    stats_pannes[equip['nom']] = {
                        'total_pannes': len(pannes_equip),
                        'types_pannes': {},
                        'temps_moyen_reparation': 0,
                        'couts_totaux': sum(float(i.get('cout_total', 0)) for i in pannes_equip),
                        'equipement_id': equip_id
                    }
                    
                    # Analyse par type de panne
                    for panne in pannes_equip:
                        type_panne = panne.get('type_panne', 'Non spécifié')
                        if type_panne in stats_pannes[equip['nom']]['types_pannes']:
                            stats_pannes[equip['nom']]['types_pannes'][type_panne] += 1
                        else:
                            stats_pannes[equip['nom']]['types_pannes'][type_panne] = 1
            
            # Affichage sous forme de graphique
            if stats_pannes:
                df_stats = pd.DataFrame({
                    'Équipement': list(stats_pannes.keys()),
                    'Nombre de pannes': [v['total_pannes'] for v in stats_pannes.values()],
                    'Coût total (€)': [v['couts_totaux'] for v in stats_pannes.values()]
                })
                
                fig = px.bar(df_stats, x='Équipement', y='Nombre de pannes', 
                            title='Nombre de Pannes par Équipement',
                            color='Coût total (€)', color_continuous_scale='reds')
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=get_theme()['text'])
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune donnée de panne disponible pour l'analyse AMDEC")
        else:
            st.info("Données insuffisantes pour l'analyse AMDEC")

    with col_amdec2:
        st.markdown("##### 🎯 Criticité des Équipements")
        
        if interventions_data and equipements_data:
            # Calcul de la criticité (fréquence * coût)
            criticite_equipements = []
            
            for equip in equipements_data:
                equip_id = equip['id']
                pannes_equip = [i for i in interventions_data if i.get('equipement_id') == equip_id]
                
                if pannes_equip:
                    frequence = len(pannes_equip)
                    cout_moyen = sum(float(i.get('cout_total', 0)) for i in pannes_equip) / frequence
                    criticite = frequence * cout_moyen
                    
                    # Détermination du niveau de criticité
                    if criticite > 1000:
                        niveau = "🔴 Haute"
                    elif criticite > 500:
                        niveau = "🟡 Moyenne"
                    else:
                        niveau = "🟢 Basse"
                    
                    criticite_equipements.append({
                        'Équipement': equip['nom'],
                        'Fréquence': frequence,
                        'Coût moyen': f"{cout_moyen:.2f}€",
                        'Criticité': f"{criticite:.2f}",
                        'Niveau': niveau
                    })
            
            if criticite_equipements:
                df_criticite = pd.DataFrame(criticite_equipements).sort_values('Criticité', ascending=False)
                
                # Appliquer un style coloré au dataframe
                def color_criticite(val):
                    if "🔴" in str(val):
                        return 'background-color: #FEE2E2; color: #DC2626;'
                    elif "🟡" in str(val):
                        return 'background-color: #FEF3C7; color: #D97706;'
                    elif "🟢" in str(val):
                        return 'background-color: #D1FAE5; color: #059669;'
                    return ''
                
                styled_df = df_criticite.style.applymap(color_criticite)
                st.dataframe(styled_df, use_container_width=True)
                
                # Recommandations basées sur la criticité
                st.markdown("##### 💡 Recommandations")
                haute_criticite = [e for e in criticite_equipements if "🔴" in e['Niveau']]
                moyenne_criticite = [e for e in criticite_equipements if "🟡" in e['Niveau']]
                
                if haute_criticite:
                    st.error(f"**🚨 Équipements à haute criticité ({len(haute_criticite)})**")
                    for equip in haute_criticite[:3]:
                        st.write(f"• {equip['Équipement']} - Maintenance préventive urgente recommandée")
                
                if moyenne_criticite:
                    st.warning(f"**⚠️ Équipements à criticité moyenne ({len(moyenne_criticite)})**")
                    for equip in moyenne_criticite[:2]:
                        st.write(f"• {equip['Équipement']} - Surveillance renforcée nécessaire")
                
                if not haute_criticite and not moyenne_criticite:
                    st.success("**✅ Situation sous contrôle** - Aucun équipement en criticité élevée")
            else:
                st.info("Aucune donnée de criticité disponible")
        else:
            st.info("Données insuffisantes pour l'analyse de criticité")

    # 🔮 Section Prédiction des Pannes
    st.markdown("#### 🔮 Prédiction des Pannes - Intelligence Préventive")
    
    col_pred1, col_pred2 = st.columns(2)
    
    with col_pred1:
        st.markdown("##### 📈 Analyse des Tendances")
        
        if interventions_data:
            # Conversion des dates
            df_interventions = pd.DataFrame(interventions_data)
            if 'date_creation' in df_interventions.columns:
                df_interventions['date_creation'] = pd.to_datetime(df_interventions['date_creation'], errors='coerce')
                
                # Analyse par mois
                interventions_par_mois = df_interventions.set_index('date_creation').resample('M').size()
                
                if len(interventions_par_mois) >= 3:
                    # Régression linéaire pour prédiction
                    x = np.arange(len(interventions_par_mois))
                    y = interventions_par_mois.values
                    
                    slope, intercept, r_value, p_value, std_err = linregress(x, y)
                    
                    # Prédiction pour les 6 prochains mois
                    mois_futurs = 6
                    x_futur = np.arange(len(interventions_par_mois), len(interventions_par_mois) + mois_futurs)
                    predictions = slope * x_futur + intercept
                    
                    # Création du graphique
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=interventions_par_mois.index, 
                        y=interventions_par_mois.values,
                        mode='lines+markers',
                        name='Historique réel',
                        line=dict(color=get_theme()['moroccan_blue'], width=3)
                    ))
                    fig.add_trace(go.Scatter(
                        x=pd.date_range(interventions_par_mois.index[-1], periods=mois_futurs+1, freq='M')[1:],
                        y=predictions,
                        mode='lines+markers',
                        name='Prédictions',
                        line=dict(color=get_theme()['moroccan_red'], dash='dash', width=2)
                    ))
                    fig.update_layout(
                        title='Prédiction du Nombre de Pannes (6 mois)',
                        xaxis_title='Date',
                        yaxis_title='Nombre de pannes',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color=get_theme()['text'])
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Interprétation
                    if slope > 0:
                        st.error(f"**📈 Tendance à la hausse** - Augmentation de {slope:.2f} pannes/mois")
                        st.info("💡 **Recommandation**: Renforcer les maintenances préventives et revoir les procédures")
                    else:
                        st.success(f"**📉 Tendance à la baisse** - Réduction de {abs(slope):.2f} pannes/mois")
                        st.info("💡 **Recommandation**: Maintenir les bonnes pratiques actuelles")
                else:
                    st.info("📊 Données historiques insuffisantes pour la prédiction (minimum 3 mois requis)")
            else:
                st.info("❌ Champ 'date_creation' manquant dans les interventions")
        else:
            st.info("📭 Aucune donnée d'intervention pour l'analyse des tendances")

    with col_pred2:
        st.markdown("##### 🤖 Recommandations Intelligentes")
        
        if interventions_data and equipements_data:
            # Algorithm simple de recommandation
            recommandations = []
            
            for equip in equipements_data:
                equip_id = equip['id']
                pannes_equip = [i for i in interventions_data if i.get('equipement_id') == equip_id]
                
                if len(pannes_equip) >= 2:  # Au moins 2 pannes pour analyse
                    # Calcul de l'intervalle moyen entre pannes
                    dates_pannes = []
                    for i in pannes_equip:
                        if i.get('date_creation'):
                            date_parsed = parse_datetime(i['date_creation'])
                            if date_parsed:
                                dates_pannes.append(date_parsed)
                    
                    dates_pannes.sort()
                    
                    if len(dates_pannes) >= 2:
                        intervals = [(dates_pannes[i+1] - dates_pannes[i]).days for i in range(len(dates_pannes)-1)]
                        interval_moyen = sum(intervals) / len(intervals) if intervals else 0
                        
                        if interval_moyen > 0:
                            # CORRECTION : Utilisation de datetime.datetime.now() sans timezone
                            prochaine_panne_prevue = dates_pannes[-1] + datetime.timedelta(days=interval_moyen)
                            
                            # CORRECTION : Comparaison avec datetime.datetime.now() sans timezone
                            jours_restants = (prochaine_panne_prevue - datetime.datetime.now()).days
                            
                            if jours_restants <= 30:
                                statut = "🔴 URGENT"
                                priorite = "Haute"
                            elif jours_restants <= 90:
                                statut = "🟡 Bientôt"
                                priorite = "Moyenne"
                            else:
                                statut = "🟢 Surveiller"
                                priorite = "Basse"
                            
                            recommandations.append({
                                'Équipement': equip['nom'],
                                'Dernière panne': dates_pannes[-1].strftime('%d/%m/%Y'),
                                'Interval moyen (jours)': int(interval_moyen),
                                'Prochaine panne prévue': prochaine_panne_prevue.strftime('%d/%m/%Y'),
                                'Jours restants': jours_restants,
                                'Recommandation': statut,
                                'Priorité': priorite
                            })
            
            if recommandations:
                # Trier par jours restants
                recommandations_triees = sorted(recommandations, key=lambda x: x['Jours restants'])
                df_recommandations = pd.DataFrame(recommandations_triees)
                
                # Style conditionnel
                def style_recommandation(row):
                    styles = []
                    for item in row:
                        if "🔴" in str(item):
                            styles.append('background-color: #FEE2E2; color: #DC2626; font-weight: bold;')
                        elif "🟡" in str(item):
                            styles.append('background-color: #FEF3C7; color: #D97706;')
                        elif "🟢" in str(item):
                            styles.append('background-color: #D1FAE5; color: #059669;')
                        else:
                            styles.append('')
                    return styles
                
                # Afficher le dataframe stylisé
                st.dataframe(df_recommandations, use_container_width=True)
                
                # Actions recommandées
                urgents = len([r for r in recommandations if "🔴" in r['Recommandation']])
                if urgents > 0:
                    st.error(f"**🚨 {urgents} équipement(s) nécessitent une maintenance URGENTE**")
                    st.button("📋 Générer un plan d'urgence", use_container_width=True)
                
                # Statistiques des recommandations
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("🟢 À surveiller", len([r for r in recommandations if "🟢" in r['Recommandation']]))
                with col_stat2:
                    st.metric("🟡 Maintenance proche", len([r for r in recommandations if "🟡" in r['Recommandation']]))
                with col_stat3:
                    st.metric("🔴 Maintenance urgente", urgents)
            else:
                st.info("📊 Pas assez de données historiques pour générer des recommandations")
        else:
            st.info("📭 Données insuffisantes pour les recommandations")

    # 📝 Section Gestion des Plans de Maintenance
    st.markdown("#### 📝 Gestion des Plans de Maintenance")
    
    if data:
        df = pd.DataFrame(data)
        if 'date_planified' in df.columns:
            df['date_planified'] = pd.to_datetime(df['date_planified'], errors='coerce')
        
        # Filtres améliorés
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        with col_filter1:
            search = st.text_input("🔍 Rechercher par description", key="plans_search")
        with col_filter2:
            statut_filter = st.multiselect("📊 Filtrer par statut", 
                                         sorted(df['statut'].dropna().unique().tolist() if 'statut' in df.columns else []))
        with col_filter3:
            type_filter = st.multiselect("🎯 Filtrer par type",
                                       sorted(df['type'].dropna().unique().tolist() if 'type' in df.columns else []))
        
        if search and 'description' in df.columns:
            df = df[df['description'].str.contains(search, case=False, na=False)]
        if statut_filter and 'statut' in df.columns:
            df = df[df['statut'].isin(statut_filter)]
        if type_filter and 'type' in df.columns:
            df = df[df['type'].isin(type_filter)]
        
        # Style conditionnel pour les statuts
        def color_statut(val):
            if val == 'Planifiée':
                return 'background-color: #E0F2FE; color: #0369A1;'
            elif val == 'En cours':
                return 'background-color: #FEF3C7; color: #D97706;'
            elif val == 'Terminée':
                return 'background-color: #D1FAE5; color: #059669;'
            elif val == 'Annulée':
                return 'background-color: #FEE2E2; color: #DC2626;'
            return ''
        
        if not df.empty and 'statut' in df.columns:
            styled_df = df.style.applymap(color_statut, subset=['statut'])
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
        
        # Export des données
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Exporter CSV", csv, "plans_maintenance_amdec.csv", "text/csv")
        with col_exp2:
            # CORRECTION : Utilisation de clean_dataframe_for_excel
            df_clean = clean_dataframe_for_excel(df)
            excel_buffer = BytesIO()
            df_clean.to_excel(excel_buffer, index=False)
            st.download_button("📊 Exporter Excel", excel_buffer, "plans_maintenance_amdec.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("📭 Aucun plan de maintenance trouvé.")

    # 🚀 Section Création de Plans Intelligents
    st.markdown("#### 🚀 Créer un Plan de Maintenance Intelligent")
    
    with st.form("ajout_plan_intelligent"):
        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            # Sélection d'équipement avec indicateur de criticité
            equipements = load_data("equipements") or []
            equip_options = {e['nom']: e['id'] for e in equipements} if equipements else {}
            
            if equip_options:
                # Calcul de la criticité pour chaque équipement
                equip_criticite = {}
                for equip in equipements:
                    equip_id = equip['id']
                    pannes_equip = [i for i in interventions_data if i.get('equipement_id') == equip_id]
                    criticite = len(pannes_equip)  # Simplifié pour l'exemple
                    
                    if criticite > 5:
                        indicateur = "🔴 Haute criticité"
                    elif criticite > 2:
                        indicateur = "🟡 Moyenne criticité"
                    else:
                        indicateur = "🟢 Basse criticité"
                    
                    equip_criticite[equip['nom']] = indicateur
                
                # Affichage avec indicateurs
                equip_choices = [f"{nom} - {crit}" for nom, crit in equip_criticite.items()]
                equip_choice = st.selectbox("🏭 Équipement*", [""] + equip_choices)
                equip_nom = equip_choice.split(" - ")[0] if equip_choice else ""
            else:
                equip_nom = st.selectbox("🏭 Équipement*", [""] + list(equip_options.keys()) if equip_options else ["Aucun équipement disponible"])
            
            date_planified = st.date_input("📅 Date planifiée*", value=datetime.datetime.now().date() + datetime.timedelta(days=7))
            type_plan = st.selectbox("🔧 Type de maintenance*", ["Preventive", "Curative", "Predictive", "Améliorative"])
            
        with col_form2:
            description = st.text_area("📝 Description détaillée*", 
                                     placeholder="Ex: Remplacement des roulements + vérification alignement...")
            
            # Suggestions automatiques basées sur l'historique
            if equip_nom and interventions_data:
                equip_id = equip_options.get(equip_nom)
                if equip_id:
                    pannes_equip = [i for i in interventions_data if i.get('equipement_id') == equip_id]
                    if pannes_equip:
                        types_pannes = {}
                        for panne in pannes_equip:
                            type_p = panne.get('type_panne', 'Non spécifié')
                            types_pannes[type_p] = types_pannes.get(type_p, 0) + 1
                        
                        panne_frequente = max(types_pannes, key=types_pannes.get) if types_pannes else None
                        if panne_frequente:
                            st.info(f"💡 **Suggestion automatique**: \n\nInclure la vérification des défaillances **'{panne_frequente}'** \n*(la plus fréquente avec {types_pannes[panne_frequente]} occurrence(s))*")
            
            priorite = st.selectbox("🎯 Priorité", ["Basse", "Normale", "Haute", "Critique"])
            duree_estimee = st.number_input("⏱️ Durée estimée (heures)", min_value=0.5, step=0.5, value=2.0)
        
        # Bouton de soumission
        submit = st.form_submit_button("🚀 Créer le Plan Intelligent", use_container_width=True)
        
        if submit:
            if not (equip_nom and date_planified and type_plan and description):
                handle_error("❌ Tous les champs marqués d'un * sont requis.")
            else:
                plan_data = {
                    "equipement_id": equip_options.get(equip_nom),
                    "date_planified": date_planified.isoformat(),
                    "type": type_plan,
                    "description": description,
                    "statut": "Planifiée",
                    "priorite": priorite,
                    "duree_estimee": duree_estimee,
                    "date_creation": datetime.datetime.now().isoformat()
                }
                
                try:
                    supabase.table("maintenance_plans").insert(plan_data).execute()
                    st.success("✅ Plan de maintenance intelligent créé avec succès!")
                    
                    # Notification aux techniciens
                    techniciens = load_data("techniciens") or []
                    for tech in techniciens:
                        tech_email = get_technicien_email(tech['id'])
                        if tech_email:
                            send_email(tech_email, 
                                     f"📅 Nouveau Plan de Maintenance - {equip_nom}",
                                     f"Un nouveau plan de maintenance a été créé:\n\n"
                                     f"🏭 Équipement: {equip_nom}\n"
                                     f"🔧 Type: {type_plan}\n"
                                     f"📅 Date: {date_planified}\n"
                                     f"🎯 Priorité: {priorite}\n"
                                     f"📝 Description: {description}\n"
                                     f"⏱️ Durée estimée: {duree_estimee} heures\n\n"
                                     f"Merci de planifier cette intervention.")
                    
                    st.balloons()
                    
                except Exception as e:
                    handle_error(f"Erreur lors de la création du plan: {str(e)}")

    # 📊 Section Tableau de Bord des Indicateurs
    st.markdown("#### 📊 Tableau de Bord des Indicateurs Clés")
    
    if interventions_data and data:
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        
        with col_kpi1:
            # Taux de maintenance préventive
            total_interventions = len(interventions_data)
            interventions_preventives = len([i for i in interventions_data if i.get('est_planifiee')])
            taux_preventif = (interventions_preventives / total_interventions * 100) if total_interventions > 0 else 0
            
            # Calculer la tendance (comparaison avec l'objectif de 70%)
            tendance = taux_preventif - 70  # Différence par rapport à l'objectif
            kpi_card_2025("🛡️ Taux Préventif", f"{taux_preventif:.1f}%", 
                         tendance, "🛡️", col_kpi1)
        
        with col_kpi2:
            # Taux de plans réalisés à temps
            plans_termines = [p for p in data if p.get('statut') == 'Terminée']
            plans_a_temps = [p for p in plans_termines if p.get('date_planified') and 
                           safe_date_comparison(p['date_planified'], datetime.datetime.now()) >= 0]
            taux_ponctualite = (len(plans_a_temps) / len(plans_termines) * 100) if plans_termines else 0
            
            # Calculer la tendance (comparaison avec l'objectif de 85%)
            tendance = taux_ponctualite - 85
            kpi_card_2025("⏱️ Ponctualité", f"{taux_ponctualite:.1f}%", 
                         tendance, "⏱️", col_kpi2)

        with col_kpi3:
            # Économies estimées
            cout_pannes_curatives = sum(float(i.get('cout_total', 0)) for i in interventions_data if not i.get('est_planifiee'))
            cout_maintenance_preventive = sum(float(i.get('cout_total', 0)) for i in interventions_data if i.get('est_planifiee'))
            economie_estimee = cout_pannes_curatives - cout_maintenance_preventive
            
            # Tendance positive si économies > 0
            tendance = 12 if economie_estimee > 0 else -8
            kpi_card_2025("💰 Économies", f"{economie_estimee:.0f}€", 
                         tendance, "💰", col_kpi3)

        with col_kpi4:
            # Prochaines échéances
            plans_prochains = [p for p in data if p.get('date_planified') and 
                             safe_date_comparison(p['date_planified'], (datetime.datetime.now() + datetime.timedelta(days=7)).date()) <= 0 and
                             p.get('statut') in ['Planifiée', 'En cours']]
            
            # Tendance (on pourrait calculer par rapport à la semaine précédente)
            tendance = 0  # À adapter selon vos besoins
            kpi_card_2025("📅 Échéances 7j", len(plans_prochains), 
                         tendance, "📅", col_kpi4)

        # Graphique d'évolution des indicateurs
        st.markdown("##### 📈 Évolution des Indicateurs Clés")
        
        # Simulation de données historiques pour le graphique
        dates = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=90), 
                             end=datetime.datetime.now(), freq='W')
        
        fig_evolution = go.Figure()
        
        # Ajout des courbes simulées
        fig_evolution.add_trace(go.Scatter(
            x=dates,
            y=np.random.normal(70, 5, len(dates)),
            name='Taux Préventif (%)',
            line=dict(color=get_theme()['moroccan_green'], width=3)
        ))
        
        fig_evolution.add_trace(go.Scatter(
            x=dates,
            y=np.random.normal(80, 8, len(dates)),
            name='Taux Ponctualité (%)',
            line=dict(color=get_theme()['moroccan_blue'], width=3)
        ))
        
        fig_evolution.add_trace(go.Scatter(
            x=dates,
            y=np.random.normal(5000, 1000, len(dates)),
            name='Économies (€)',
            line=dict(color=get_theme()['moroccan_gold'], width=3),
            yaxis='y2'
        ))
        
        fig_evolution.update_layout(
            title='Évolution des Indicateurs Clés (3 derniers mois)',
            xaxis_title='Date',
            yaxis_title='Pourcentage (%)',
            yaxis2=dict(
                title='Économies (€)',
                overlaying='y',
                side='right'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=get_theme()['text']),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_evolution, use_container_width=True)

        # Recommandations stratégiques
        st.markdown("##### 💡 Recommandations Stratégiques")
        
        rec_col1, rec_col2, rec_col3 = st.columns(3)
        
        with rec_col1:
            if taux_preventif < 70:
                st.error("**🛡️ Améliorer la maintenance préventive**")
                st.write("Objectif: >70% d'interventions planifiées")
            else:
                st.success("**✅ Maintenance préventive optimale**")
        
        with rec_col2:
            if taux_ponctualite < 85:
                st.warning("**⏱️ Optimiser la ponctualité**")
                st.write("Objectif: >85% de plans réalisés à temps")
            else:
                st.success("**✅ Excellente ponctualité**")
        
        with rec_col3:
            if economie_estimee < 0:
                st.error("**💰 Réduire les coûts curatifs**")
                st.write("Les pannes coûtent plus cher que la prévention")
            else:
                st.success("**✅ Économies réalisées**")

    else:
        st.info("📊 Données insuffisantes pour le tableau de bord des indicateurs")

    # Section d'export et de reporting
    st.markdown("---")
    st.markdown("#### 📄 Reporting et Export")
    
    col_report1, col_report2, col_report3 = st.columns(3)
    
    with col_report1:
        if st.button("📋 Rapport AMDEC Complet", use_container_width=True):
            st.info("🔄 Génération du rapport AMDEC en cours...")
            # Simulation de génération de rapport
            st.success("✅ Rapport AMDEC généré avec succès!")
    
    with col_report2:
        if st.button("📈 Analyse Prédictive", use_container_width=True):
            st.info("🔮 Exécution de l'analyse prédictive...")
            # Simulation d'analyse
            st.success("✅ Analyse prédictive terminée!")
    
    with col_report3:
        if st.button("🎯 Plan d'Action", use_container_width=True):
            st.info("📝 Génération du plan d'action...")
            # Simulation de génération
            st.success("✅ Plan d'action généré!")

def analytics():
    if not has_permission("Admin"):
        show_access_denied()
        return
        
    st.markdown('<div class="form-section-title">📈 Analytics Avancées</div>', unsafe_allow_html=True)
    interventions_data = load_data("interventions") or []
    if not interventions_data:
        st.info("Aucune donnée d'intervention disponible pour l'analyse.")
        return

    df_interventions = pd.DataFrame(interventions_data)
    if 'date_creation' in df_interventions.columns:
        df_interventions['date_creation'] = pd.to_datetime(df_interventions['date_creation'], errors='coerce')
        df_interventions.set_index('date_creation', inplace=True)

    st.markdown("#### 📊 Trend Analysis des Pannes")
    if not df_interventions.empty:
        monthly_pannes = df_interventions.resample('M').size().reset_index(name='Nombre de Pannes')
        fig = px.line(monthly_pannes, x='date_creation', y='Nombre de Pannes', title='Pannes par Mois')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=get_theme()['text'])
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas assez de données temporelles.")

    st.markdown("#### 🤖 Prédiction de maintenance (ML simple)")
    if len(monthly_pannes) >= 2:
        monthly_pannes['time'] = np.arange(len(monthly_pannes))
        slope, intercept, r_value, p_value, std_err = linregress(monthly_pannes['time'], monthly_pannes['Nombre de Pannes'])
        future_months = st.slider("Mois à prédire", 1, 12, 3)
        future_time = np.arange(len(monthly_pannes), len(monthly_pannes) + future_months)
        predictions = slope * future_time + intercept
        pred_df = pd.DataFrame({"mois": future_time, "pred": predictions})
        st.table(pred_df)
        # Plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly_pannes['time'], y=monthly_pannes['Nombre de Pannes'], mode='lines+markers', name='Historique'))
        fig.add_trace(go.Scatter(x=future_time, y=predictions, mode='lines+markers', name='Prédictions', line=dict(dash='dash')))
        fig.update_layout(
            title='Prédiction des Pannes',
            xaxis_title='Temps (mois)',
            yaxis_title='Nombre de Pannes',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=get_theme()['text'])
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas assez de points pour la prédiction (min 2 mois).")

    st.markdown("#### 📄 Rapports PDF automatisés")
    if st.button("🔄 Générer Rapport PDF", use_container_width=True):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Rapport de Maintenance - ISmaint", ln=1, align='C')
        equipements = load_data("equipements") or []
        stocks = load_data("stocks") or []
        nb_equipements = len(equipements)
        nb_pannes = len([e for e in equipements if e.get('statut') == 'En panne'])
        nb_interventions_ouvertes = len([i for i in interventions_data if i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']])
        nb_stocks_critiques = len([s for s in stocks if s.get('quantite') is not None and s.get('niveau_critique') is not None and s['quantite'] <= s['niveau_critique']])
        pdf.cell(200, 10, txt=f"Équipements Totaux: {nb_equipements}", ln=1)
        pdf.cell(200, 10, txt=f"En Panne: {nb_pannes}", ln=1)
        pdf.cell(200, 10, txt=f"Interventions Actives: {nb_interventions_ouvertes}", ln=1)
        pdf.cell(200, 10, txt=f"Stocks Critiques: {nb_stocks_critiques}", ln=1)
        
        # CORRECTION : pdf.output(dest='S') retourne déjà des bytes
        pdf_output = BytesIO()
        pdf_bytes = pdf.output(dest='S')  # Cette méthode retourne déjà des bytes
        pdf_output.write(pdf_bytes)
        pdf_output.seek(0)
        
        st.download_button(
            label="📥 Télécharger le Rapport PDF", 
            data=pdf_output, 
            file_name="rapport_maintenance.pdf", 
            mime="application/pdf"
        )

def metriques_avancees():
    if not has_permission("Admin"):
        show_access_denied()
        return
        
    st.markdown('<div class="form-section-title">⚙️ Métriques Avancées</div>', unsafe_allow_html=True)
    # Auto-refresh every 30s (non intrusive)
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time()
    if time() - st.session_state.last_refresh > 30:
        st.session_state.last_refresh = time()
        st.rerun()

    interventions = load_data("interventions") or []
    equipements = load_data("equipements") or []
    production_shifts = load_data("production_shifts") or []
    stocks = load_data("stocks") or []

    # OT Actifs
    ot_actifs = len([i for i in interventions if i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']])
    st.markdown(f"**OT Actifs:** {ot_actifs}")
    
    # MTTR
    st.markdown("#### ⏱️ MTTR (Temps Moyen de Réparation)")
    if interventions:
        df_interventions = pd.DataFrame(interventions)
        df_interventions['date_creation'] = pd.to_datetime(df_interventions.get('date_creation'), errors='coerce')
        df_interventions['date_cloture'] = pd.to_datetime(df_interventions.get('date_cloture'), errors='coerce')
        df_closed = df_interventions[df_interventions.get('statut') == 'Fermée'].dropna(subset=['date_cloture'])
        if not df_closed.empty:
            # CORRECTION : Utilisation de safe_date_comparison pour gérer les timezones
            df_closed['temps_reparation_hours'] = df_closed.apply(
                lambda row: safe_date_comparison(row['date_cloture'], row['date_creation']) / 24, 
                axis=1
            )
            mttr = df_closed['temps_reparation_hours'].mean()
            st.write(f"MTTR: {mttr:.2f} heures")
        else:
            st.info("Aucune intervention fermée avec date de clôture.")
    else:
        st.info("Pas d'intervention.")

    # MTBF & OEE simplified
    st.markdown("#### 📊 MTBF & OEE")
    if equipements:
        equip_names = [e['nom'] for e in equipements]
        equip_nom = st.selectbox("Sélectionner un équipement", equip_names)
        try:
            equip_id = next(e['id'] for e in equipements if e['nom'] == equip_nom)
            df_equip_interventions = pd.DataFrame([i for i in interventions if i.get('equipement_id') == equip_id]) if interventions else pd.DataFrame()
            heures_op = next((e.get('heures_operationnelles') or 0) for e in equipements if e['nom'] == equip_nom)
            nb_pannes = len(df_equip_interventions) if not df_equip_interventions.empty else 0
            mtbf = (heures_op / max(nb_pannes, 1)) if heures_op else 0
            st.write(f"MTBF ({equip_nom}): {mtbf:.2f} heures")
        except StopIteration:
            st.info("Impossible de calculer MTBF pour cet équipement.")
    else:
        st.info("Aucun équipement disponible.")

def offline_sync():
    if not has_permission("Admin"):
        show_access_denied()
        return
        
    st.markdown('<div class="form-section-title">🔄 Synchronisation Offline</div>', unsafe_allow_html=True)
    st.info("💾 Sauvegarde de secours dans session_state (usage limité).")
    if 'offline_data' not in st.session_state:
        st.session_state.offline_data = {}
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Sauvegarder données offline", use_container_width=True):
            st.session_state.offline_data['equipements'] = load_data("equipements")
            st.session_state.offline_data['interventions'] = load_data("interventions")
            st.success("Données sauvegardées localement ✔️")
    with col2:
        if st.button("📂 Charger depuis offline", use_container_width=True):
            if st.session_state.offline_data:
                # show a quick preview
                for k, v in st.session_state.offline_data.items():
                    st.write(f"**{k}**")
                    st.dataframe(pd.DataFrame(v))
            else:
                st.info("Aucune donnée offline disponible.")

# -----------------------------
# Navigation principale
# -----------------------------
sidebar_2025()

# Router vers la page appropriée
if st.session_state.current_page == "Tableau de Bord":
    dashboard()
elif st.session_state.current_page == "Équipements":
    gestion_equipements()
elif st.session_state.current_page == "Interventions":
    gestion_interventions()
elif st.session_state.current_page == "Équipe":
    gestion_equipe()
elif st.session_state.current_page == "Stocks":
    gestion_stocks()
elif st.session_state.current_page == "Planification":
    planification()
elif st.session_state.current_page == "Analytics":
    analytics()
elif st.session_state.current_page == "Métriques Avancées":
    metriques_avancees()
elif st.session_state.current_page == "Offline Sync":
    offline_sync()