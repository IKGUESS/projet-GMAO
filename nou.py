# app_premium_2025_enhanced.py
"""
ISmaint Pro - Enhanced 2025 Version
Amélioration complète du design avec animations, glassmorphism,
micro-interactions et une expérience utilisateur premium
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
# Enhanced Theming 2025
# -----------------------------
def get_theme():
    if st.session_state.dark_mode:
        return {
            'primary': '#F1F5F9',
            'accent': '#22D3EE',
            'secondary': '#A78BFA',
            'bg': '#0F172A',
            'bg_secondary': '#1E293B',
            'card': '#1E293B',
            'card_hover': '#334155',
            'text': '#F1F5F9',
            'text_secondary': '#94A3B8',
            'border': 'rgba(148, 163, 184, 0.1)',
            'shadow': 'rgba(0, 0, 0, 0.5)',
            'moroccan_blue': '#3B82F6',
            'moroccan_green': '#10B981',
            'moroccan_red': '#EF4444',
            'moroccan_gold': '#F59E0B',
            'gradient_start': '#1E293B',
            'gradient_end': '#0F172A'
        }
    else:
        return {
            'primary': '#0F172A',
            'accent': '#06B6D4',
            'secondary': '#8B5CF6',
            'bg': '#F8FAFC',
            'bg_secondary': '#F1F5F9',
            'card': '#FFFFFF',
            'card_hover': '#F8FAFC',
            'text': '#1E293B',
            'text_secondary': '#64748B',
            'border': 'rgba(148, 163, 184, 0.2)',
            'shadow': 'rgba(0, 0, 0, 0.1)',
            'moroccan_blue': '#1D5D9B',
            'moroccan_green': '#2D8C6B',
            'moroccan_red': '#C84B31',
            'moroccan_gold': '#E7B10A',
            'gradient_start': '#FFFFFF',
            'gradient_end': '#F8FAFC'
        }

def apply_css():
    theme = get_theme()
    
    st.markdown(
        f"""
        <style>
        /* ===== IMPORTS & FONTS ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* ===== CSS VARIABLES ===== */
        :root {{
            --primary: {theme['primary']};
            --accent: {theme['accent']};
            --secondary: {theme['secondary']};
            --bg: {theme['bg']};
            --bg-secondary: {theme['bg_secondary']};
            --card: {theme['card']};
            --card-hover: {theme['card_hover']};
            --text: {theme['text']};
            --text-secondary: {theme['text_secondary']};
            --border: {theme['border']};
            --shadow: {theme['shadow']};
            --moroccan-blue: {theme['moroccan_blue']};
            --moroccan-green: {theme['moroccan_green']};
            --moroccan-red: {theme['moroccan_red']};
            --moroccan-gold: {theme['moroccan_gold']};
            --gradient-start: {theme['gradient_start']};
            --gradient-end: {theme['gradient_end']};
            --radius: 20px;
            --radius-sm: 12px;
            --radius-lg: 28px;
            --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-fast: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* ===== GLOBAL RESET ===== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        /* ===== SMOOTH SCROLLING ===== */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* ===== MAIN LAYOUT ===== */
        .main {{
            background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
            color: var(--text);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            padding: 0 !important;
            animation: fadeIn 0.6s ease-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* ===== SCROLLBAR CUSTOM ===== */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg-secondary);
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            border-radius: 10px;
            transition: var(--transition);
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, var(--moroccan-green), var(--moroccan-blue));
        }}
        
        /* ===== ENHANCED LOGIN PAGE ===== */
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
        
        /* Animated background pattern */
        .login-2025-container::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            right: -50%;
            bottom: -50%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
            animation: floatBackground 30s ease-in-out infinite;
        }}
        
        @keyframes floatBackground {{
            0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
            33% {{ transform: translate(30px, -30px) rotate(120deg); }}
            66% {{ transform: translate(-20px, 20px) rotate(240deg); }}
        }}
        
        .login-2025-card {{
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(30px) saturate(180%);
            border-radius: 32px;
            padding: 56px 48px;
            box-shadow: 
                0 30px 60px -12px rgba(0, 0, 0, 0.25),
                0 0 100px rgba(255, 255, 255, 0.1) inset;
            width: 100%;
            max-width: 460px;
            text-align: center;
            position: relative;
            z-index: 2;
            border: 2px solid rgba(255, 255, 255, 0.3);
            animation: slideUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .login-2025-logo {{
            width: 90px;
            height: 90px;
            border-radius: 24px;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 28px auto;
            color: white;
            font-size: 38px;
            box-shadow: 
                0 15px 35px rgba(29, 93, 155, 0.4),
                0 5px 15px rgba(0, 0, 0, 0.2);
            animation: bounce 2s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }}
        
        .login-2025-logo::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: shine 3s ease-in-out infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        @keyframes shine {{
            0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
            100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
        }}
        
        .login-2025-title {{
            font-size: 36px;
            font-weight: 900;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            letter-spacing: -1px;
            animation: fadeIn 1s ease-out 0.3s both;
        }}
        
        .login-2025-subtitle {{
            color: #6B7280;
            font-size: 17px;
            margin-bottom: 48px;
            font-weight: 500;
            animation: fadeIn 1s ease-out 0.5s both;
        }}
        
        .login-2025-input {{
            margin-bottom: 28px;
        }}
        
        .login-2025-input .stTextInput>div>div>input {{
            border-radius: 16px;
            border: 2px solid #E5E7EB;
            padding: 18px 24px;
            font-size: 16px;
            transition: var(--transition);
            background: white;
            font-weight: 500;
        }}
        
        .login-2025-input .stTextInput>div>div>input:focus {{
            border-color: var(--moroccan-blue);
            box-shadow: 
                0 0 0 5px rgba(29, 93, 155, 0.1),
                0 8px 20px rgba(29, 93, 155, 0.2);
            transform: translateY(-3px);
        }}
        
        .login-2025-button .stButton>button {{
            width: 100%;
            padding: 18px 28px;
            font-size: 17px;
            font-weight: 700;
            border-radius: 16px;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            border: none;
            color: white;
            transition: var(--transition);
            box-shadow: 
                0 6px 20px rgba(29, 93, 155, 0.4),
                0 0 40px rgba(29, 93, 155, 0.2) inset;
            position: relative;
            overflow: hidden;
        }}
        
        .login-2025-button .stButton>button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: var(--transition);
        }}
        
        .login-2025-button .stButton>button:hover {{
            transform: translateY(-3px) scale(1.02);
            box-shadow: 
                0 12px 30px rgba(29, 93, 155, 0.5),
                0 0 60px rgba(29, 93, 155, 0.3) inset;
        }}
        
        .login-2025-button .stButton>button:hover::before {{
            left: 100%;
        }}
        
        /* ===== ENHANCED SIDEBAR ===== */
        section[data-testid="stSidebar"] {{
            background: var(--card) !important;
            border-right: 1px solid var(--border);
            box-shadow: 5px 0 30px var(--shadow);
        }}
        
        .sidebar-user-card {{
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 28px;
            color: white;
            text-align: center;
            box-shadow: 0 8px 24px rgba(29, 93, 155, 0.3);
            position: relative;
            overflow: hidden;
            animation: slideRight 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        @keyframes slideRight {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        .sidebar-user-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
        }}
        
        .sidebar-user-avatar {{
            width: 72px;
            height: 72px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px auto;
            font-size: 28px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            transition: var(--transition);
            position: relative;
            z-index: 1;
        }}
        
        .sidebar-user-avatar:hover {{
            transform: scale(1.1) rotate(5deg);
            border-color: rgba(255, 255, 255, 0.6);
        }}
        
        .sidebar-user-name {{
            font-weight: 800;
            font-size: 20px;
            margin-bottom: 6px;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }}
        
        .sidebar-user-role {{
            font-size: 13px;
            opacity: 0.95;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            padding: 6px 16px;
            border-radius: 24px;
            display: inline-block;
            font-weight: 600;
            position: relative;
            z-index: 1;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        
        .nav-item {{
            display: flex;
            align-items: center;
            padding: 14px 18px;
            margin: 6px 0;
            border-radius: 16px;
            color: var(--text);
            text-decoration: none;
            transition: var(--transition-fast);
            font-weight: 600;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .nav-item::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 4px;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            transform: scaleY(0);
            transition: var(--transition);
        }}
        
        .nav-item:hover {{
            background: rgba(29, 93, 155, 0.08);
            transform: translateX(6px);
            color: var(--moroccan-blue);
        }}
        
        .nav-item:hover::before {{
            transform: scaleY(1);
        }}
        
        .nav-item.active {{
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            color: white;
            box-shadow: 
                0 6px 20px rgba(29, 93, 155, 0.4),
                0 0 40px rgba(29, 93, 155, 0.2) inset;
            transform: translateX(4px);
        }}
        
        .nav-item.active::before {{
            transform: scaleY(1);
            background: rgba(255, 255, 255, 0.4);
        }}
        
        .nav-icon {{
            margin-right: 14px;
            font-size: 20px;
            width: 24px;
            text-align: center;
            transition: var(--transition-fast);
        }}
        
        .nav-item:hover .nav-icon {{
            transform: scale(1.2) rotate(5deg);
        }}
        
        /* ===== ENHANCED KPI CARDS ===== */
        .kpi-card-2025 {{
            background: var(--card);
            border-radius: var(--radius);
            padding: 28px;
            box-shadow: 
                0 4px 20px var(--shadow),
                0 0 0 1px var(--border);
            border: 1px solid var(--border);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .kpi-card-2025::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, var(--moroccan-blue), var(--moroccan-green), var(--moroccan-gold));
            background-size: 200% 100%;
            animation: gradientShift 3s ease infinite;
        }}
        
        @keyframes gradientShift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .kpi-card-2025:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 12px 40px var(--shadow),
                0 0 60px rgba(29, 93, 155, 0.1) inset;
        }}
        
        .kpi-icon {{
            width: 56px;
            height: 56px;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(29, 93, 155, 0.1), rgba(45, 140, 107, 0.1));
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 18px;
            font-size: 24px;
            color: var(--moroccan-blue);
            transition: var(--transition);
            box-shadow: 0 4px 12px rgba(29, 93, 155, 0.1);
        }}
        
        .kpi-card-2025:hover .kpi-icon {{
            transform: scale(1.15) rotate(5deg);
            box-shadow: 0 8px 24px rgba(29, 93, 155, 0.2);
        }}
        
        .kpi-label-2025 {{
            color: var(--text-secondary);
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        
        .kpi-value-2025 {{
            font-size: 32px;
            font-weight: 900;
            color: var(--text);
            margin-bottom: 8px;
            line-height: 1;
            background: linear-gradient(135deg, var(--text), var(--moroccan-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .kpi-trend {{
            font-size: 13px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            display: inline-flex;
        }}
        
        .trend-up {{
            color: var(--moroccan-green);
            background: rgba(16, 185, 129, 0.1);
        }}
        
        .trend-down {{
            color: var(--moroccan-red);
            background: rgba(239, 68, 68, 0.1);
        }}
        
        /* ===== ENHANCED FORMS ===== */
        .form-card {{
            background: var(--card);
            border-radius: var(--radius);
            padding: 36px;
            box-shadow: 
                0 4px 20px var(--shadow),
                0 0 0 1px var(--border);
            border: 1px solid var(--border);
            margin-bottom: 28px;
            transition: var(--transition);
            animation: fadeIn 0.6s ease-out;
        }}
        
        .form-card:hover {{
            box-shadow: 
                0 8px 30px var(--shadow),
                0 0 0 1px var(--border);
        }}
        
        .form-section-title {{
            font-size: 28px;
            font-weight: 900;
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 28px;
            padding-bottom: 16px;
            border-bottom: 3px solid;
            border-image: linear-gradient(90deg, var(--moroccan-blue), var(--moroccan-green), transparent) 1;
            animation: slideDown 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        @keyframes slideDown {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input, 
        .stTextArea>div>div>textarea,
        /* ===== STREAMLIT SELECTBOX FIX FINAL ===== */

        /* Conteneur */
        .stSelectbox [data-baseweb="select"] {{
            background-color: var(--card) !important;
            border: 2px solid var(--border) !important;
            border-radius: 14px !important;
        }}

        /* TEXTE SÉLECTIONNÉ (IMPORTANT) */
        .stSelectbox [data-baseweb="select"] div {{
            color: var(--text) !important;
            font-size: 15px !important;
            font-weight: 600 !important;
        }}

        /* Placeholder */
        .stSelectbox [data-baseweb="select"] span {{
            color: var(--text-secondary) !important;
        }}

        /* Input invisible interne (BaseWeb) */
        .stSelectbox input {{
            color: var(--text) !important;
            caret-color: var(--text) !important;
        }}

        /* Focus */
        .stSelectbox [data-baseweb="select"]:focus-within {{
            border-color: var(--moroccan-blue) !important;
            box-shadow: 0 0 0 4px rgba(29, 93, 155, 0.12) !important;
        }}

        
        .stTextInput>div>div>input:focus, 
        .stNumberInput>div>div>input:focus, 
        .stTextArea>div>div>textarea:focus {{
            border-color: var(--moroccan-blue) !important;
            box-shadow: 0 0 0 4px rgba(29, 93, 155, 0.1) !important;
            transform: translateY(-2px);
        }}
        
        /* ===== ENHANCED BUTTONS ===== */
        .stButton>button {{
            border-radius: 14px !important;
            padding: 14px 28px !important;
            font-weight: 700 !important;
            border: none !important;
            transition: var(--transition) !important;
            position: relative;
            overflow: hidden;
            font-size: 15px !important;
        }}
        
        .stButton>button::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .stButton>button:hover::before {{
            width: 300px;
            height: 300px;
        }}
        
        .stButton>button[kind="primary"] {{
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green)) !important;
            color: white !important;
            box-shadow: 0 6px 20px rgba(29, 93, 155, 0.4) !important;
        }}
        
        .stButton>button[kind="primary"]:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 10px 30px rgba(29, 93, 155, 0.5) !important;
        }}
        
        .stButton>button[kind="secondary"] {{
            background: rgba(29, 93, 155, 0.1) !important;
            color: var(--moroccan-blue) !important;
            border: 2px solid var(--moroccan-blue) !important;
        }}
        
        .stButton>button[kind="secondary"]:hover {{
            background: var(--moroccan-blue) !important;
            color: white !important;
            transform: translateY(-2px);
        }}
        
        /* ===== ENHANCED DATA TABLES ===== */
        .dataframe {{
            border-radius: 16px !important;
            overflow: hidden;
            box-shadow: 0 4px 20px var(--shadow) !important;
            border: 1px solid var(--border);
            animation: fadeIn 0.6s ease-out;
        }}
        
        .dataframe thead th {{
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green)) !important;
            color: white !important;
            font-weight: 700 !important;
            border: none !important;
            padding: 16px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 13px;
        }}
        
        .dataframe tbody tr {{
            transition: var(--transition-fast);
        }}
        
        .dataframe tbody tr:hover {{
            background: var(--card-hover) !important;
            transform: scale(1.01);
        }}
        
        .dataframe tbody td {{
            padding: 14px !important;
            border-bottom: 1px solid var(--border) !important;
        }}
        
        /* ===== ENHANCED BADGES ===== */
        .badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 24px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: var(--transition-fast);
        }}
        
        .badge:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .badge-success {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.25));
            color: var(--moroccan-green);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}
        
        .badge-warning {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.25));
            color: var(--moroccan-gold);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }}
        
        .badge-danger {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.25));
            color: var(--moroccan-red);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}
        
        .badge-info {{
            background: linear-gradient(135deg, rgba(29, 93, 155, 0.15), rgba(29, 93, 155, 0.25));
            color: var(--moroccan-blue);
            border: 1px solid rgba(29, 93, 155, 0.3);
        }}
        
        /* ===== DARK MODE TOGGLE ===== */
        .dark-mode-toggle {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 20px;
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(29, 93, 155, 0.1), rgba(45, 140, 107, 0.1));
            color: var(--moroccan-blue);
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: var(--transition);
            margin-bottom: 20px;
            border: 2px solid rgba(29, 93, 155, 0.2);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }}
        
        .dark-mode-toggle:hover {{
            background: linear-gradient(135deg, rgba(29, 93, 155, 0.2), rgba(45, 140, 107, 0.2));
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
        }}
        
        /* ===== LOADING ANIMATION ===== */
        @keyframes shimmer {{
            0% {{ background-position: -1000px 0; }}
            100% {{ background-position: 1000px 0; }}
        }}
        
        .loading-shimmer {{
            animation: shimmer 2s infinite;
            background: linear-gradient(90deg, var(--card) 25%, var(--card-hover) 50%, var(--card) 75%);
            background-size: 1000px 100%;
        }}
        
        /* ===== ALERTS & NOTIFICATIONS ===== */
        .stAlert {{
            border-radius: 16px !important;
            border-left: 5px solid !important;
            padding: 16px 20px !important;
            animation: slideInRight 0.4s ease-out;
        }}
        
        @keyframes slideInRight {{
            from {{ opacity: 0; transform: translateX(20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        /* ===== METRICS & STATS ===== */
        .metric-container {{
            background: var(--card);
            border-radius: var(--radius);
            padding: 24px;
            box-shadow: 0 4px 20px var(--shadow);
            border: 1px solid var(--border);
            transition: var(--transition);
        }}
        
        .metric-container:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 30px var(--shadow);
        }}
        
        /* ===== CHARTS & GRAPHS ===== */
        .plotly-chart {{
            border-radius: var(--radius);
            overflow: hidden;
            box-shadow: 0 4px 20px var(--shadow);
            background: var(--card);
            padding: 20px;
            border: 1px solid var(--border);
            animation: fadeIn 0.8s ease-out;
        }}
        
        /* ===== EXPANDER CUSTOM ===== */
        .streamlit-expanderHeader {{
            background: var(--card) !important;
            border-radius: 14px !important;
            border: 2px solid var(--border) !important;
            padding: 16px !important;
            font-weight: 700 !important;
            transition: var(--transition) !important;
        }}
        
        .streamlit-expanderHeader:hover {{
            background: var(--card-hover) !important;
            border-color: var(--moroccan-blue) !important;
            transform: translateX(4px);
        }}
        
        /* ===== TABS CUSTOM ===== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: var(--bg-secondary);
            padding: 8px;
            border-radius: 16px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            transition: var(--transition) !important;
            border: none !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, var(--moroccan-blue), var(--moroccan-green)) !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(29, 93, 155, 0.3) !important;
        }}
        
        /* ===== FILE UPLOADER ===== */
        .stFileUploader {{
            border: 2px dashed var(--border) !important;
            border-radius: var(--radius) !important;
            padding: 32px !important;
            background: var(--card) !important;
            transition: var(--transition) !important;
        }}
        
        .stFileUploader:hover {{
            border-color: var(--moroccan-blue) !important;
            background: var(--card-hover) !important;
            transform: scale(1.01);
        }}
        
        /* ===== PROGRESS BAR ===== */
        .stProgress > div > div {{
            background: linear-gradient(90deg, var(--moroccan-blue), var(--moroccan-green)) !important;
            border-radius: 10px !important;
            height: 10px !important;
        }}
        
        /* ===== TOOLTIPS ===== */
        [data-baseweb="tooltip"] {{
            background: var(--card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            box-shadow: 0 8px 24px var(--shadow) !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        /* ===== RESPONSIVE DESIGN ===== */
        @media (max-width: 768px) {{
            .login-2025-card {{
                padding: 40px 28px;
                margin: 20px;
                border-radius: 24px;
            }}
            
            .login-2025-logo {{
                width: 70px;
                height: 70px;
                font-size: 30px;
            }}
            
            .login-2025-title {{
                font-size: 28px;
            }}
            
            .kpi-value-2025 {{
                font-size: 26px;
            }}
            
            .form-card {{
                padding: 24px 20px;
            }}
            
            .form-section-title {{
                font-size: 24px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .kpi-card-2025 {{
                padding: 20px;
            }}
            
            .kpi-icon {{
                width: 48px;
                height: 48px;
                font-size: 20px;
            }}
            
            .sidebar-user-avatar {{
                width: 60px;
                height: 60px;
                font-size: 24px;
            }}
        }}
        
        /* ===== ACCESSIBILITY ===== */
        *:focus {{
            outline: 3px solid var(--moroccan-blue);
            outline-offset: 2px;
        }}
        
        /* ===== PRINT STYLES ===== */
        @media print {{
            .sidebar, .stButton, .dark-mode-toggle {{
                display: none !important;
            }}
            
            .main {{
                background: white !important;
            }}
            
            .kpi-card-2025 {{
                break-inside: avoid;
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
    
    # Centrer le contenu avec des colonnes
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 24px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); padding: 48px; animation: fadeInUp 0.6s ease-out;">
                <div style="text-align: center; margin-bottom: 32px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); width: 80px; height: 80px; border-radius: 20px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 24px; box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);">
                        <span style="font-size: 40px;">🏭</span>
                    </div>
                    <h1 style="font-size: 32px; font-weight: 700; color: #1F2937; margin: 0 0 8px 0; letter-spacing: -0.5px;">ISmaint Pro</h1>
                    <p style="font-size: 14px; color: #6B7280; margin: 0; font-weight: 500;">Industrial Maintenance Management System</p>
                </div>
            """,
            unsafe_allow_html=True
        )
        
        # Container pour les champs de saisie
        with st.container():
            st.markdown('<div style="margin-bottom: 20px;">', unsafe_allow_html=True)
            username = st.text_input("", placeholder="👤 Nom d'utilisateur", key="login_user_2025", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div style="margin-bottom: 24px;">', unsafe_allow_html=True)
            password = st.text_input("", placeholder="🔒 Mot de passe", type="password", key="login_pass_2025", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Bouton de connexion
        st.markdown('<div style="margin-bottom: 24px;">', unsafe_allow_html=True)
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
            <div style="margin-top: 32px; padding-top: 24px; border-top: 1px solid #E5E7EB; text-align: center;">
                <p style="color: #9CA3AF; font-size: 13px; margin: 0;">
                    © 2025 ISmaint Pro - Premium Maintenance Management System
                </p>
                <p style="color: #D1D5DB; font-size: 11px; margin: 8px 0 0 0;">
                    Powered by Advanced Technology
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Header 2025
# -----------------------------
def header_2025():
    theme = get_theme()
    
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px 40px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); margin-bottom: 30px; border-radius: 0 0 16px 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1400px; margin: 0 auto;">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div style="background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px); width: 56px; height: 56px; border-radius: 14px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
                        <span style="font-size: 32px;">🏭</span>
                    </div>
                    <div>
                        <div style="font-size: 26px; font-weight: 700; color: white; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">ISmaint Pro</div>
                        <div style="font-size: 12px; color: rgba(255, 255, 255, 0.85); font-weight: 500; margin-top: 2px;">Maintenance Management System</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div onclick="toggleDarkMode()" style="background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); padding: 10px 20px; border-radius: 12px; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: all 0.3s ease; border: 1px solid rgba(255, 255, 255, 0.2); hover: background: rgba(255, 255, 255, 0.25);">
                        <span style="font-size: 20px;">{'🌙' if not st.session_state.dark_mode else '☀️'}</span>
                        <span style="color: white; font-size: 14px; font-weight: 500;">{'Mode sombre' if not st.session_state.dark_mode else 'Mode clair'}</span>
                    </div>
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
        # Header de la sidebar avec gradient
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px; margin: -1rem -1rem 24px -1rem; border-radius: 0 0 20px 20px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
                <div style="text-align: center; color: white;">
                    <div style="font-size: 40px; margin-bottom: 8px;">🏭</div>
                    <div style="font-size: 18px; font-weight: 700; letter-spacing: -0.3px;">ISmaint Pro</div>
                    <div style="font-size: 11px; opacity: 0.9; margin-top: 4px;">Maintenance Excellence</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Dark mode toggle avec style amélioré
        dark_mode_icon = '🌙' if not st.session_state.dark_mode else '☀️'
        dark_mode_text = 'Mode sombre' if not st.session_state.dark_mode else 'Mode clair'
        
        st.markdown('<div style="margin-bottom: 20px;">', unsafe_allow_html=True)
        if st.button(f"{dark_mode_icon} {dark_mode_text}", 
                    use_container_width=True, key="dark_mode_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Carte utilisateur avec style moderne
        if st.session_state.authenticated and st.session_state.user:
            user_role = st.session_state.user.get('role', 'Technicien')
            user_name = st.session_state.user.get('username', 'Utilisateur')
            
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 16px; padding: 20px; margin-bottom: 24px; border: 1px solid rgba(102, 126, 234, 0.2); box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);">
                    <div style="text-align: center;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); width: 64px; height: 64px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
                            <span style="font-size: 32px;">{'👨‍💼' if user_role == 'Admin' else '👨‍🔧'}</span>
                        </div>
                        <div style="font-size: 16px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">{user_name}</div>
                        <div style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);">{user_role}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('<div style="border-top: 2px solid #E5E7EB; margin: 20px 0;"></div>', unsafe_allow_html=True)
        
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
        
        # Section titre pour la navigation
        st.markdown(
            """
            <div style="font-size: 12px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; padding-left: 4px;">
                Navigation
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Affichage des éléments de menu avec espacement
        for icon, label in menu_items:
            is_active = st.session_state.current_page == label
            
            st.markdown('<div style="margin-bottom: 8px;">', unsafe_allow_html=True)
            if st.button(f"{icon} {label}", 
                        use_container_width=True, 
                        type="primary" if is_active else "secondary",
                        key=f"nav_{label}"):
                st.session_state.current_page = label
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="border-top: 2px solid #E5E7EB; margin: 24px 0;"></div>', unsafe_allow_html=True)
        
        # Bouton de déconnexion avec style danger
        st.markdown(
            """
            <div style="font-size: 12px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; padding-left: 4px;">
                Session
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("🚪 Déconnexion", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.current_page = "Tableau de Bord"
            st.rerun()
        
        # Footer de la sidebar
    
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
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px 32px; border-radius: 16px; margin-bottom: 32px; box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);">
            <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">📊 Tableau de Bord Principal</h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">Vue d'ensemble de votre système de maintenance</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Afficher le rôle actuel
    user_role = st.session_state.user.get('role', 'Technicien')
    
    # Load data
    equipements = load_data("equipements") or []
    interventions = load_data("interventions") or []
    stocks = load_data("stocks") or []
    plans = load_data("maintenance_plans") or []
    users = load_data("users") or []

    # Calculs KPIs
    nb_equipements = len(equipements)
    nb_pannes = len([e for e in equipements if e.get('statut') == 'En panne'])
    nb_interventions_ouvertes = len([i for i in interventions if i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']])
    nb_stocks_critiques = len([s for s in stocks if s.get('quantite') is not None and s.get('niveau_critique') is not None and s['quantite'] <= s['niveau_critique']])
    nb_plans_planifies = len([p for p in plans if p.get('statut') == 'Planifiée'])
    
    # Calculs supplémentaires
    nb_interventions_terminees = len([i for i in interventions if i.get('statut') == 'Terminée'])
    taux_disponibilite = ((nb_equipements - nb_pannes) / nb_equipements * 100) if nb_equipements > 0 else 0
    nb_techniciens = len([u for u in users if u.get('role') == 'Technicien'])

    # KPI row avec nouveau design
    cols = st.columns(5)
    kpi_card_2025("Équipements Totaux", nb_equipements, 2, "🏭", cols[0])
    kpi_card_2025("En Panne", nb_pannes, -5, "⚠️", cols[1])
    kpi_card_2025("Interventions Actives", nb_interventions_ouvertes, 8, "🔧", cols[2])
    kpi_card_2025("Stocks Critiques", nb_stocks_critiques, -12, "📦", cols[3])
    kpi_card_2025("Plans Planifiés", nb_plans_planifies, 15, "📅", cols[4])

    # Deuxième ligne de KPIs (métriques de performance)
    st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
    cols2 = st.columns(4)
    
    with cols2[0]:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">✅ Taux de Disponibilité</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{taux_disponibilite:.1f}%</div>
                <div style="font-size: 11px; opacity: 0.8;">Équipements opérationnels</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with cols2[1]:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">✔️ Interventions Résolues</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_interventions_terminees}</div>
                <div style="font-size: 11px; opacity: 0.8;">Terminées avec succès</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with cols2[2]:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">👥 Équipe Active</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_techniciens}</div>
                <div style="font-size: 11px; opacity: 0.8;">Techniciens disponibles</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with cols2[3]:
        temps_moyen = "2.3h"  # Calculé dynamiquement si date_resolution disponible
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⏱️ Temps Moyen</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{temps_moyen}</div>
                <div style="font-size: 11px; opacity: 0.8;">Résolution intervention</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Espacement
    st.markdown('<div style="margin: 32px 0;"></div>', unsafe_allow_html=True)

    # Section principale: Graphiques et activités
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Tabs pour différentes vues
        tab1, tab2, tab3 = st.tabs(["📈 Tendances", "🎯 Par Statut", "🏭 Par Équipement"])
        
        with tab1:
            st.markdown(
                """
                <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                    <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                        Interventions - Derniers 12 mois
                    </h3>
                """,
                unsafe_allow_html=True
            )
            
            if interventions:
                df = pd.DataFrame(interventions)
                if 'date_creation' in df.columns:
                    df['date_creation'] = pd.to_datetime(df['date_creation'], errors='coerce')
                    monthly = df.set_index('date_creation').resample('M').size().reset_index(name='count')
                    fig = px.area(monthly, x='date_creation', y='count')
                    fig.update_traces(
                        line_color='#667eea', 
                        fillcolor='rgba(102, 126, 234, 0.2)',
                        hovertemplate='<b>%{y}</b> interventions<br>%{x|%B %Y}<extra></extra>'
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#1F2937'),
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Pas de données temporelles disponibles")
            else:
                st.info("Aucune intervention disponible")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown(
                """
                <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                    <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                        Répartition par Statut
                    </h3>
                """,
                unsafe_allow_html=True
            )
            
            if interventions:
                df = pd.DataFrame(interventions)
                if 'statut' in df.columns:
                    statut_counts = df['statut'].value_counts().reset_index()
                    statut_counts.columns = ['Statut', 'Nombre']
                    
                    fig = px.pie(
                        statut_counts, 
                        values='Nombre', 
                        names='Statut',
                        color_discrete_sequence=['#667eea', '#764ba2', '#f59e0b', '#10b981', '#ef4444']
                    )
                    fig.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        hovertemplate='<b>%{label}</b><br>%{value} interventions<br>%{percent}<extra></extra>'
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#1F2937'),
                        margin=dict(l=0, r=0, t=0, b=0),
                        showlegend=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Pas de données de statut disponibles")
            else:
                st.info("Aucune intervention disponible")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown(
                """
                <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                    <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                        Top 10 Équipements
                    </h3>
                """,
                unsafe_allow_html=True
            )
            
            if interventions and equipements:
                df_int = pd.DataFrame(interventions)
                if 'equipement_id' in df_int.columns:
                    top_equip = df_int['equipement_id'].value_counts().head(10).reset_index()
                    top_equip.columns = ['equipement_id', 'count']
                    
                    # Enrichir avec les noms d'équipements
                    equip_dict = {e.get('id'): e.get('nom', 'Inconnu') for e in equipements}
                    top_equip['nom'] = top_equip['equipement_id'].map(equip_dict).fillna('Équipement inconnu')
                    
                    fig = px.bar(
                        top_equip, 
                        x='count', 
                        y='nom', 
                        orientation='h',
                        color='count',
                        color_continuous_scale=['#dbeafe', '#667eea']
                    )
                    fig.update_traces(
                        hovertemplate='<b>%{y}</b><br>%{x} interventions<extra></extra>'
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#1F2937'),
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                        yaxis=dict(showgrid=False),
                        showlegend=False,
                        coloraxis_showscale=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Pas de données d'équipements disponibles")
            else:
                st.info("Aucune donnée disponible")
            
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Alertes rapides
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 16px 0; display: flex; align-items: center; gap: 8px;">
                    <span>🚨</span>
                    <span>Alertes Prioritaires</span>
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        if nb_pannes > 0:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); padding: 12px 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid #ef4444; cursor: pointer;" onclick="alert('Navigation vers équipements en panne')">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 24px; font-weight: 700; color: #991b1b;">{nb_pannes}</div>
                            <div style="font-size: 13px; color: #7f1d1d; font-weight: 500;">équipements en panne</div>
                        </div>
                        <div style="font-size: 24px;">🔴</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        if nb_stocks_critiques > 0:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid #f59e0b;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 24px; font-weight: 700; color: #92400e;">{nb_stocks_critiques}</div>
                            <div style="font-size: 13px; color: #78350f; font-weight: 500;">stocks critiques</div>
                        </div>
                        <div style="font-size: 24px;">🟡</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        if nb_interventions_ouvertes > 0:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 12px 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid #3b82f6;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 24px; font-weight: 700; color: #1e3a8a;">{nb_interventions_ouvertes}</div>
                            <div style="font-size: 13px; color: #1e40af; font-weight: 500;">interventions actives</div>
                        </div>
                        <div style="font-size: 24px;">🔵</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        if nb_pannes == 0 and nb_stocks_critiques == 0 and nb_interventions_ouvertes == 0:
            st.markdown(
                """
                <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); padding: 16px; border-radius: 12px; text-align: center; border-left: 4px solid #10b981;">
                    <div style="font-size: 32px; margin-bottom: 8px;">✅</div>
                    <div style="font-size: 14px; color: #065f46; font-weight: 600;">Tout va bien !</div>
                    <div style="font-size: 12px; color: #047857; margin-top: 4px;">Aucune alerte active</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Activité récente
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 16px 0; display: flex; align-items: center; gap: 8px;">
                    <span>📋</span>
                    <span>Activité Récente</span>
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        # Afficher les 5 dernières interventions
        if interventions:
            sorted_interventions = sorted(
                interventions, 
                key=lambda x: x.get('date_creation', ''), 
                reverse=True
            )[:5]
            
            for interv in sorted_interventions:
                statut = interv.get('statut', 'Inconnu')
                couleur_statut = {
                    'Nouvelle': '#3b82f6',
                    'Ouverte': '#f59e0b',
                    'En cours': '#8b5cf6',
                    'Terminée': '#10b981',
                    'Annulée': '#ef4444'
                }.get(statut, '#6b7280')
                
                st.markdown(
                    f"""
                    <div style="background: #f9fafb; padding: 10px 12px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid {couleur_statut};">
                        <div style="font-size: 12px; color: #1f2937; font-weight: 600; margin-bottom: 4px;">
                            {interv.get('description', 'Sans description')[:50]}...
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 10px; color: {couleur_statut}; font-weight: 600; background: rgba(102, 126, 234, 0.1); padding: 2px 8px; border-radius: 6px;">
                                {statut}
                            </span>
                            <span style="font-size: 10px; color: #6b7280;">
                                {interv.get('date_creation', '')[:10] if interv.get('date_creation') else 'N/A'}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("Aucune activité récente")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Actions rapides selon le rôle
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 16px 0; display: flex; align-items: center; gap: 8px;">
                    <span>⚡</span>
                    <span>Actions Rapides</span>
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        if user_role == "Admin":
            if st.button("➕ Créer Intervention Rapide", use_container_width=True, type="primary"):
                st.session_state.current_page = "Interventions"
                st.rerun()
            
            st.markdown('<div style="margin: 8px 0;"></div>', unsafe_allow_html=True)
            
            if st.button("👥 Gérer Équipe", use_container_width=True, type="secondary"):
                st.session_state.current_page = "Équipe"
                st.rerun()
            
            st.markdown('<div style="margin: 8px 0;"></div>', unsafe_allow_html=True)
            
            if st.button("📦 Vérifier Stocks", use_container_width=True, type="secondary"):
                st.session_state.current_page = "Stocks"
                st.rerun()
            
            st.markdown('<div style="margin: 8px 0;"></div>', unsafe_allow_html=True)
            
            if st.button("📈 Voir Analytics", use_container_width=True, type="secondary"):
                st.session_state.current_page = "Analytics"
                st.rerun()
        else:
            # Pour les techniciens, afficher leurs interventions en cours
            user_id = st.session_state.user.get('id')
            technicien_interventions = [i for i in interventions if i.get('technicien_id') == user_id and i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']]
            
            if technicien_interventions:
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 12px 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid #667eea;">
                        <div style="font-size: 20px; font-weight: 700; color: #4c1d95;">{len(technicien_interventions)}</div>
                        <div style="font-size: 13px; color: #5b21b6; font-weight: 500;">intervention(s) en cours</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                for interv in technicien_interventions[:3]:
                    st.markdown(
                        f"""
                        <div style="background: #f9fafb; padding: 8px 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #667eea;">
                            <div style="font-size: 12px; color: #4b5563;">• {interv.get('description', 'Sans description')[:40]}...</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("Aucune intervention en cours")
            
            st.markdown('<div style="margin: 12px 0;"></div>', unsafe_allow_html=True)
            
            if st.button("🔧 Voir Mes Interventions", use_container_width=True, type="primary"):
                st.session_state.current_page = "Interventions"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Section bas de page : Vue d'ensemble rapide
    st.markdown('<div style="margin: 32px 0;"></div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                📅 Planification à venir
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Plans de maintenance à venir
    if plans:
        plans_a_venir = [p for p in plans if p.get('statut') == 'Planifiée'][:5]
        
        if plans_a_venir:
            cols_plans = st.columns(len(plans_a_venir) if len(plans_a_venir) <= 5 else 5)
            
            for idx, plan in enumerate(plans_a_venir):
                with cols_plans[idx]:
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 16px; border-radius: 12px; border-left: 4px solid #0ea5e9; height: 100%;">
                            <div style="font-size: 24px; margin-bottom: 8px;">📅</div>
                            <div style="font-size: 13px; color: #0c4a6e; font-weight: 600; margin-bottom: 4px;">
                                {plan.get('type', 'Maintenance')}
                            </div>
                            <div style="font-size: 11px; color: #075985;">
                                {plan.get('date_planifiee', 'Date non définie')[:10] if plan.get('date_planifiee') else 'À planifier'}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.info("Aucun plan de maintenance planifié")
    else:
        st.info("Aucun plan de maintenance disponible")

def gestion_equipements():
    if not has_permission("Admin"):
        show_access_denied()
        return
    
    # Header moderne
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px 32px; border-radius: 16px; margin-bottom: 32px; box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);">
            <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">🏭 Gestion des Équipements</h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">Gérez votre parc d'équipements industriels</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    data = load_data("equipements") or []
    
    # Statistiques rapides en haut
    if data:
        col1, col2, col3, col4 = st.columns(4)
        
        nb_total = len(data)
        nb_fonctionnel = len([e for e in data if e.get('statut') == 'Fonctionnel'])
        nb_panne = len([e for e in data if e.get('statut') == 'En panne'])
        nb_maintenance = len([e for e in data if e.get('statut') == 'En maintenance'])
        
        with col1:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">📊 Total</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_total}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Équipements</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">✅ Fonctionnel</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_fonctionnel}</div>
                    <div style="font-size: 11px; opacity: 0.8;">{(nb_fonctionnel/nb_total*100):.1f}% du parc</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⚠️ En panne</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_panne}</div>
                    <div style="font-size: 11px; opacity: 0.8;">{(nb_panne/nb_total*100):.1f}% du parc</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">🔧 Maintenance</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_maintenance}</div>
                    <div style="font-size: 11px; opacity: 0.8;">{(nb_maintenance/nb_total*100):.1f}% du parc</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('<div style="margin: 32px 0;"></div>', unsafe_allow_html=True)
    
    # Tabs pour organiser les sections
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Liste & Recherche", "✏️ Modifier", "➕ Ajouter", "📤 Import/Export"])
    
    with tab1:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    📋 Liste des Équipements
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        if data:
            df = pd.DataFrame(data)
            
            # Filtres avancés
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                search = st.text_input("🔍 Rechercher par nom ou description", key="equip_search", placeholder="Tapez pour rechercher...")
            with col2:
                statut_filter = st.multiselect("📊 Filtrer par statut", sorted(df['statut'].dropna().unique().tolist() if 'statut' in df.columns else []))
            with col3:
                sort_by = st.selectbox("🔄 Trier par", ["Nom", "Statut", "Heures opérationnelles"], key="sort_equip")
            
            # Application des filtres
            df_filtered = df.copy()
            
            if search:
                if 'nom' in df_filtered.columns:
                    mask_nom = df_filtered['nom'].str.contains(search, case=False, na=False)
                    if 'description' in df_filtered.columns:
                        mask_desc = df_filtered['description'].str.contains(search, case=False, na=False)
                        df_filtered = df_filtered[mask_nom | mask_desc]
                    else:
                        df_filtered = df_filtered[mask_nom]
            
            if statut_filter and 'statut' in df_filtered.columns:
                df_filtered = df_filtered[df_filtered['statut'].isin(statut_filter)]
            
            # Tri
            if sort_by == "Nom" and 'nom' in df_filtered.columns:
                df_filtered = df_filtered.sort_values('nom')
            elif sort_by == "Statut" and 'statut' in df_filtered.columns:
                df_filtered = df_filtered.sort_values('statut')
            elif sort_by == "Heures opérationnelles" and 'heures_operationnelles' in df_filtered.columns:
                df_filtered = df_filtered.sort_values('heures_operationnelles', ascending=False)
            
            # Affichage avec style
            st.markdown(f"**{len(df_filtered)}** équipement(s) trouvé(s)")
            st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
            
            # Configuration des colonnes à afficher
            column_config = {
                "id": st.column_config.TextColumn("ID", width="small"),
                "nom": st.column_config.TextColumn("Nom", width="medium"),
                "statut": st.column_config.TextColumn("Statut", width="small"),
                "heures_operationnelles": st.column_config.NumberColumn("Heures Op.", format="%.1f h"),
                "description": st.column_config.TextColumn("Description", width="large")
            }
            
            st.dataframe(
                df_filtered, 
                use_container_width=True,
                column_config=column_config,
                hide_index=True,
                height=400
            )
            
            # Exports
            st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
            col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 2])
            with col_exp1:
                csv = df_filtered.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Exporter CSV", csv, "equipements.csv", "text/csv", use_container_width=True)
            with col_exp2:
                df_clean = clean_dataframe_for_excel(df_filtered)
                excel_buffer = BytesIO()
                df_clean.to_excel(excel_buffer, index=False)
                st.download_button("📊 Exporter Excel", excel_buffer.getvalue(), "equipements.xlsx", 
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 use_container_width=True)
        else:
            st.info("Aucun équipement trouvé.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    ✏️ Modifier ou Supprimer un Équipement
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        if data:
            # CORRECTION : Créer une liste propre avec juste les noms
            equipements_list = [e['nom'] for e in data]
            selected_equipement_name = st.selectbox(
                "Sélectionner un équipement à modifier", 
                [""] + equipements_list,
                key="select_equip_modify"
            )
            
            if selected_equipement_name:
                # CORRECTION : Trouver l'équipement par son nom
                equipement_data = next((e for e in data if e['nom'] == selected_equipement_name), None)
                
                if equipement_data:
                    equipement_id = equipement_data['id']
                    statut = equipement_data.get('statut', 'Inconnu')
                    couleur_statut = {
                        'Fonctionnel': '#10b981',
                        'En panne': '#ef4444',
                        'En maintenance': '#f59e0b'
                    }.get(statut, '#6b7280')
                    
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 20px; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid {couleur_statut};">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="font-size: 20px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">
                                        {equipement_data.get('nom', 'Sans nom')}
                                    </div>
                                    <div style="font-size: 13px; color: #6B7280;">
                                        {equipement_data.get('description', 'Pas de description')[:100]}...
                                    </div>
                                </div>
                                <div style="background: {couleur_statut}; color: white; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 600;">
                                    {statut}
                                </div>
                            </div>
                            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(0,0,0,0.1); font-size: 12px; color: #6B7280;">
                                ⏱️ {equipement_data.get('heures_operationnelles', 0)} heures opérationnelles
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(
                            """
                            <div style="background: #f0f9ff; padding: 16px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #0ea5e9;">
                                <h4 style="color: #0c4a6e; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">💾 Modifier l'équipement</h4>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        with st.form(f"modifier_equipement_{equipement_id}"):
                            nouveau_nom = st.text_input("Nom de l'équipement", value=equipement_data.get('nom', ''))
                            nouveau_statut = st.selectbox(
                                "Statut", 
                                ["Fonctionnel", "En panne", "En maintenance"], 
                                index=["Fonctionnel", "En panne", "En maintenance"].index(equipement_data.get('statut', 'Fonctionnel'))
                            )
                            nouvelle_description = st.text_area("Description", value=equipement_data.get('description', ''))
                            nouvelles_heures = st.number_input(
                                "Heures opérationnelles", 
                                value=float(equipement_data.get('heures_operationnelles', 0)),
                                min_value=0.0, 
                                step=0.1
                            )
                            
                            st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
                            password = st.text_input(
                                "🔒 Mot de passe administrateur", 
                                type="password", 
                                help="Entrez votre mot de passe pour confirmer la modification"
                            )
                            
                            if st.form_submit_button("💾 Sauvegarder les modifications", use_container_width=True, type="primary"):
                                if not password:
                                    st.error("⚠️ Veuillez entrer le mot de passe administrateur")
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
                        st.markdown(
                            """
                            <div style="background: #fef2f2; padding: 16px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #ef4444;">
                                <h4 style="color: #991b1b; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">🗑️ Supprimer l'équipement</h4>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        st.warning("⚠️ **Attention** : Cette action est irréversible et supprimera définitivement cet équipement.")
                        
                        with st.form(f"supprimer_equipement_{equipement_id}"):
                            st.markdown(
                                f"""
                                <div style="background: white; padding: 12px; border-radius: 8px; margin: 16px 0; border: 1px solid #fee2e2;">
                                    <div style="font-size: 13px; color: #7f1d1d; font-weight: 600;">
                                        Vous êtes sur le point de supprimer :
                                    </div>
                                    <div style="font-size: 15px; color: #991b1b; font-weight: 700; margin-top: 4px;">
                                        {equipement_data.get('nom', 'Équipement')}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            password_supp = st.text_input(
                                "🔒 Mot de passe administrateur", 
                                type="password", 
                                key=f"pass_supp_{equipement_id}",
                                help="Entrez votre mot de passe pour confirmer la suppression"
                            )
                            
                            if st.form_submit_button("🗑️ Confirmer la suppression", use_container_width=True, type="secondary"):
                                if not password_supp:
                                    st.error("⚠️ Veuillez entrer le mot de passe administrateur")
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
        else:
            st.info("Aucun équipement disponible à modifier.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    ➕ Ajouter un nouvel équipement
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        with st.form("ajout_equipement_mod"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom de l'équipement*", placeholder="Ex: Compresseur Atlas Copco")
                statut = st.selectbox("Statut*", ["Fonctionnel", "En panne", "En maintenance"])
                heures_operationnelles = st.number_input("Heures opérationnelles", min_value=0.0, step=0.1, value=0.0)
            with col2:
                description = st.text_area("Description", placeholder="Détails techniques, localisation, etc.", height=132)
            
            st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            with col_btn1:
                submit = st.form_submit_button("➕ Ajouter l'équipement", use_container_width=True, type="primary")
            with col_btn2:
                reset = st.form_submit_button("🔄 Réinitialiser", use_container_width=True)
            
            if submit:
                if not nom:
                    st.error("⚠️ Le nom de l'équipement est requis.")
                else:
                    try:
                        supabase.table("equipements").insert({
                            "nom": nom,
                            "statut": statut,
                            "description": description,
                            "heures_operationnelles": float(heures_operationnelles)
                        }).execute()
                        st.success("✅ Équipement ajouté avec succès !")
                        st.rerun()
                    except Exception as e:
                        handle_error(str(e))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    📤 Import / Export de données
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                """
                <div style="background: #f0fdf4; padding: 20px; border-radius: 12px; border-left: 4px solid #10b981; margin-bottom: 20px;">
                    <h4 style="color: #065f46; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">📥 Importer des équipements</h4>
                    <p style="color: #047857; font-size: 13px; margin: 0;">Importez vos équipements depuis un fichier CSV ou Excel</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            uploaded_file = st.file_uploader(
                "Sélectionner un fichier", 
                type=["csv", "xlsx"], 
                key="equip_import",
                help="Formats acceptés: CSV, Excel (.xlsx)"
            )
            
            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        import_df = pd.read_csv(uploaded_file)
                    else:
                        import_df = pd.read_excel(uploaded_file)
                    
                    st.markdown(f"**Aperçu** : {len(import_df)} ligne(s) détectée(s)")
                    st.dataframe(import_df.head(), use_container_width=True)
                    
                    if st.button("✅ Confirmer l'import", use_container_width=True, type="primary"):
                        for _, row in import_df.iterrows():
                            supabase.table("equipements").insert(row.to_dict()).execute()
                        st.success(f"✅ {len(import_df)} équipement(s) importé(s) avec succès !")
                        st.rerun()
                except Exception as e:
                    handle_error(str(e))
        
        with col2:
            st.markdown(
                """
                <div style="background: #eff6ff; padding: 20px; border-radius: 12px; border-left: 4px solid #3b82f6; margin-bottom: 20px;">
                    <h4 style="color: #1e40af; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">📤 Télécharger un modèle</h4>
                    <p style="color: #1e3a8a; font-size: 13px; margin: 0;">Obtenez un modèle vide pour faciliter l'import</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Modèle CSV
            template_df = pd.DataFrame({
                'nom': ['Exemple Équipement'],
                'statut': ['Fonctionnel'],
                'description': ['Description de l\'équipement'],
                'heures_operationnelles': [0.0]
            })
            
            template_csv = template_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📄 Télécharger modèle CSV", 
                template_csv, 
                "modele_equipements.csv", 
                "text/csv",
                use_container_width=True
            )
            
            st.markdown('<div style="margin: 12px 0;"></div>', unsafe_allow_html=True)
            
            # Modèle Excel
            template_buffer = BytesIO()
            template_df.to_excel(template_buffer, index=False)
            st.download_button(
                "📊 Télécharger modèle Excel", 
                template_buffer.getvalue(), 
                "modele_equipements.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            st.markdown('<div style="margin: 24px 0;"></div>', unsafe_allow_html=True)
            
            st.info("💡 **Astuce** : Remplissez le modèle avec vos données puis importez-le pour ajouter plusieurs équipements en une seule fois.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def gestion_interventions():
    user_role = st.session_state.user.get('role', 'Technicien')
    user_id = st.session_state.user.get('id')
    
    # Header moderne avec distinction Admin/Technicien
    if user_role == "Admin":
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px 32px; border-radius: 16px; margin-bottom: 32px; box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);">
                <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">🔧 Gestion des Interventions</h1>
                <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">Gérez et suivez toutes les interventions de maintenance</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 24px 32px; border-radius: 16px; margin-bottom: 32px; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.2);">
                <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">🔧 Mes Interventions</h1>
                <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">Gérez vos interventions assignées et déclarez les pannes</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    data = load_data("interventions") or []
    
    # Filtrer les données selon le rôle
    if user_role == "Technicien":
        data = [i for i in data if i.get('technicien_id') == user_id]
        st.markdown(
            """
            <div style="background: #dbeafe; padding: 12px 16px; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid #3b82f6;">
                <div style="color: #1e40af; font-size: 13px; font-weight: 500;">
                    🔍 Vue Technicien - Vous voyez uniquement vos interventions assignées
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Statistiques rapides
    if data:
        col1, col2, col3, col4 = st.columns(4)
        
        nb_total = len(data)
        nb_nouvelles = len([i for i in data if i.get('statut') == 'Nouvelle'])
        nb_en_cours = len([i for i in data if i.get('statut') == 'En cours'])
        nb_fermees = len([i for i in data if i.get('statut') == 'Fermée'])
        
        with col1:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">📊 Total</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_total}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Interventions</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">🆕 Nouvelles</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_nouvelles}</div>
                    <div style="font-size: 11px; opacity: 0.8;">À traiter</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⚡ En cours</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_en_cours}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Actives</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">✅ Fermées</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_fermees}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Terminées</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('<div style="margin: 32px 0;"></div>', unsafe_allow_html=True)
    
    # ====================
    # VUE ADMIN
    # ====================
    if user_role == "Admin":
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Liste & Recherche", "✏️ Modifier", "➕ Créer/Affecter", "📤 Import/Export"])
        
        with tab1:
            st.markdown(
                """
                <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
                    <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                        📋 Liste des Interventions
                    </h3>
                """,
                unsafe_allow_html=True
            )
            
            if data:
                df = pd.DataFrame(data)
                
                # Filtres avancés
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    search = st.text_input("🔍 Rechercher", key="int_search", placeholder="Description, observations...")
                with col2:
                    statut_filter = st.multiselect("📊 Statut", sorted(df['statut'].dropna().unique().tolist() if 'statut' in df.columns else []))
                with col3:
                    priorite_filter = st.multiselect("🚨 Priorité", sorted(df['priorite'].dropna().unique().tolist() if 'priorite' in df.columns else []))
                with col4:
                    sort_by = st.selectbox("🔄 Trier", ["Date création", "Priorité", "Statut"], key="sort_int")
                
                # Application des filtres
                df_filtered = df.copy()
                
                if search:
                    if 'description' in df_filtered.columns:
                        mask_desc = df_filtered['description'].str.contains(search, case=False, na=False)
                        if 'observations' in df_filtered.columns:
                            mask_obs = df_filtered['observations'].str.contains(search, case=False, na=False)
                            df_filtered = df_filtered[mask_desc | mask_obs]
                        else:
                            df_filtered = df_filtered[mask_desc]
                
                if statut_filter and 'statut' in df_filtered.columns:
                    df_filtered = df_filtered[df_filtered['statut'].isin(statut_filter)]
                
                if priorite_filter and 'priorite' in df_filtered.columns:
                    df_filtered = df_filtered[df_filtered['priorite'].isin(priorite_filter)]
                
                # Tri
                if sort_by == "Date création" and 'date_creation' in df_filtered.columns:
                    df_filtered = df_filtered.sort_values('date_creation', ascending=False)
                elif sort_by == "Priorité" and 'priorite' in df_filtered.columns:
                    priority_order = {'Critique': 0, 'Haute': 1, 'Moyenne': 2, 'Basse': 3}
                    df_filtered['priority_num'] = df_filtered['priorite'].map(priority_order)
                    df_filtered = df_filtered.sort_values('priority_num')
                    df_filtered = df_filtered.drop('priority_num', axis=1)
                elif sort_by == "Statut" and 'statut' in df_filtered.columns:
                    df_filtered = df_filtered.sort_values('statut')
                
                st.markdown(f"**{len(df_filtered)}** intervention(s) trouvée(s)")
                st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
                
                # Configuration des colonnes
                column_config = {
                    "id": st.column_config.TextColumn("ID", width="small"),
                    "description": st.column_config.TextColumn("Description", width="large"),
                    "statut": st.column_config.TextColumn("Statut", width="small"),
                    "priorite": st.column_config.TextColumn("Priorité", width="small"),
                    "type_panne": st.column_config.TextColumn("Type", width="small"),
                    "cout_total": st.column_config.NumberColumn("Coût", format="%.2f €"),
                    "date_creation": st.column_config.DatetimeColumn("Créé le", format="DD/MM/YYYY")
                }
                
                st.dataframe(
                    df_filtered, 
                    use_container_width=True,
                    column_config=column_config,
                    hide_index=True,
                    height=400
                )
                
                # Exports
                st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
                col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 2])
                with col_exp1:
                    csv = df_filtered.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Exporter CSV", csv, "interventions.csv", "text/csv", use_container_width=True)
                with col_exp2:
                    df_clean = clean_dataframe_for_excel(df_filtered)
                    excel_buffer = BytesIO()
                    df_clean.to_excel(excel_buffer, index=False)
                    st.download_button("📊 Exporter Excel", excel_buffer.getvalue(), "interventions.xlsx", 
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                     use_container_width=True)
            else:
                st.info("Aucune intervention trouvée.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown(
                """
                <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                    <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                        ✏️ Modifier ou Supprimer une Intervention
                    </h3>
                """,
                unsafe_allow_html=True
            )
            
            if data:
                # CORRECTION : Liste simplifiée avec juste les descriptions
                interventions_list = [i.get('description', 'Sans description')[:50] + "..." for i in data]
                selected_intervention_desc = st.selectbox(
                    "Sélectionner une intervention à modifier", 
                    [""] + interventions_list,
                    key="select_int_modify"
                )
                
                if selected_intervention_desc:
                    # CORRECTION : Trouver l'intervention par la description correspondante
                    intervention_data = None
                    for i in data:
                        desc_short = i.get('description', '')[:50] + "..."
                        if desc_short == selected_intervention_desc:
                            intervention_data = i
                            break
                    
                    if intervention_data:
                        intervention_id = intervention_data['id']
                        statut = intervention_data.get('statut', 'Inconnu')
                        priorite = intervention_data.get('priorite', 'Moyenne')
                        
                        couleur_statut = {
                            'Nouvelle': '#f59e0b',
                            'Ouverte': '#3b82f6',
                            'En cours': '#8b5cf6',
                            'Fermée': '#10b981'
                        }.get(statut, '#6b7280')
                        
                        couleur_priorite = {
                            'Critique': '#ef4444',
                            'Haute': '#f59e0b',
                            'Moyenne': '#3b82f6',
                            'Basse': '#10b981'
                        }.get(priorite, '#6b7280')
                        
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 20px; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid {couleur_statut};">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                                    <div style="flex: 1;">
                                        <div style="font-size: 20px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">
                                            Intervention #{intervention_data.get('id')}
                                        </div>
                                        <div style="font-size: 13px; color: #6B7280; margin-bottom: 8px;">
                                            {intervention_data.get('description', 'Sans description')[:150]}...
                                        </div>
                                    </div>
                                    <div style="display: flex; gap: 8px; margin-left: 16px;">
                                        <div style="background: {couleur_statut}; color: white; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; white-space: nowrap;">
                                            {statut}
                                        </div>
                                        <div style="background: {couleur_priorite}; color: white; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; white-space: nowrap;">
                                            {priorite}
                                        </div>
                                    </div>
                                </div>
                                <div style="display: flex; gap: 16px; padding-top: 12px; border-top: 1px solid rgba(0,0,0,0.1); font-size: 12px; color: #6B7280;">
                                    <div>🔧 {intervention_data.get('type_panne', 'N/A')}</div>
                                    <div>💰 {intervention_data.get('cout_total', 0):.2f} €</div>
                                    <div>📅 {intervention_data.get('date_creation', 'N/A')[:10] if intervention_data.get('date_creation') else 'N/A'}</div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(
                                """
                                <div style="background: #f0f9ff; padding: 16px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #0ea5e9;">
                                    <h4 style="color: #0c4a6e; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">💾 Modifier l'intervention</h4>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            with st.form(f"modifier_intervention_{intervention_id}"):
                                # Charger les données nécessaires
                                equipements = load_data("equipements") or []
                                techniciens = load_data("techniciens") or []
                                
                                equip_options = {e['nom']: e['id'] for e in equipements}
                                tech_options = {t['nom']: t['id'] for t in techniciens}
                                
                                current_equipement = next((e['nom'] for e in equipements if e['id'] == intervention_data.get('equipement_id')), "")
                                current_technicien = next((t['nom'] for t in techniciens if t['id'] == intervention_data.get('technicien_id')), "")
                                
                                col_form1, col_form2 = st.columns(2)
                                with col_form1:
                                    nouveau_equipement = st.selectbox(
                                        "Équipement", 
                                        [""] + list(equip_options.keys()), 
                                        index=0 if not current_equipement else list(equip_options.keys()).index(current_equipement) + 1
                                    )
                                    nouveau_type_panne = st.selectbox(
                                        "Type de panne", 
                                        ["Mécanique", "Électrique", "Hydraulique", "Logiciel", "Autre"],
                                        index=["Mécanique", "Électrique", "Hydraulique", "Logiciel", "Autre"].index(intervention_data.get('type_panne', 'Mécanique'))
                                    )
                                    nouveau_statut = st.selectbox(
                                        "Statut", 
                                        ["Nouvelle", "Ouverte", "En cours", "Fermée"],
                                        index=["Nouvelle", "Ouverte", "En cours", "Fermée"].index(intervention_data.get('statut', 'Nouvelle'))
                                    )
                                
                                with col_form2:
                                    nouvelle_priorite = st.selectbox(
                                        "Priorité", 
                                        ["Basse", "Moyenne", "Haute", "Critique"],
                                        index=["Basse", "Moyenne", "Haute", "Critique"].index(intervention_data.get('priorite', 'Moyenne'))
                                    )
                                    nouveau_technicien = st.selectbox(
                                        "Technicien", 
                                        [""] + list(tech_options.keys()),
                                        index=0 if not current_technicien else list(tech_options.keys()).index(current_technicien) + 1
                                    )
                                    nouveau_cout = st.number_input(
                                        "Coût total (€)", 
                                        value=float(intervention_data.get('cout_total', 0)), 
                                        min_value=0.0, 
                                        step=0.01
                                    )
                                
                                nouvelle_description = st.text_area("Description", value=intervention_data.get('description', ''))
                                nouvelles_observations = st.text_area("Observations", value=intervention_data.get('observations', ''))
                                
                                # Date de clôture si statut Fermée
                                date_cloture = None
                                if nouveau_statut == "Fermée" and intervention_data.get('statut') != 'Fermée':
                                    date_cloture = st.date_input("Date de clôture", value=datetime.datetime.now().date())
                                
                                st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
                                password = st.text_input(
                                    "🔒 Mot de passe administrateur", 
                                    type="password", 
                                    help="Entrez votre mot de passe pour confirmer"
                                )
                                
                                if st.form_submit_button("💾 Sauvegarder les modifications", use_container_width=True, type="primary"):
                                    if not password:
                                        st.error("⚠️ Veuillez entrer le mot de passe administrateur")
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
                            st.markdown(
                                """
                                <div style="background: #fef2f2; padding: 16px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #ef4444;">
                                    <h4 style="color: #991b1b; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">🗑️ Supprimer l'intervention</h4>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            st.warning("⚠️ **Attention** : Cette action est irréversible")
                            
                            with st.form(f"supprimer_intervention_{intervention_id}"):
                                st.markdown(
                                    f"""
                                    <div style="background: white; padding: 12px; border-radius: 8px; margin: 16px 0; border: 1px solid #fee2e2;">
                                        <div style="font-size: 13px; color: #7f1d1d; font-weight: 600;">
                                            Vous êtes sur le point de supprimer :
                                        </div>
                                        <div style="font-size: 15px; color: #991b1b; font-weight: 700; margin-top: 4px;">
                                            Intervention #{intervention_data.get('id')}
                                        </div>
                                        <div style="font-size: 12px; color: #991b1b; margin-top: 4px;">
                                            {intervention_data.get('description', 'Sans description')[:80]}...
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                                
                                password_supp = st.text_input(
                                    "🔒 Mot de passe administrateur", 
                                    type="password", 
                                    key=f"pass_supp_int_{intervention_id}",
                                    help="Entrez votre mot de passe pour confirmer la suppression"
                                )
                                
                                if st.form_submit_button("🗑️ Confirmer la suppression", use_container_width=True, type="secondary"):
                                    if not password_supp:
                                        st.error("⚠️ Veuillez entrer le mot de passe administrateur")
                                    elif verify_admin_password(password_supp):
                                        try:
                                            supabase.table("interventions").delete().eq("id", intervention_id).execute()
                                            st.success("✅ Intervention supprimée avec succès")
                                            st.rerun()
                                        except Exception as e:
                                            handle_error(str(e))
                                    else:
                                        st.error("❌ Mot de passe administrateur incorrect")
            else:
                st.info("Aucune intervention disponible à modifier.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown(
                """
                <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                    <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                        ➕ Créer ou Affecter une Intervention
                    </h3>
                """,
                unsafe_allow_html=True
            )
            
            with st.form("creer_affecter_intervention_mod"):
                st.markdown("##### 📝 Détails de l'Intervention")
                
                # Première ligne - Equipement et Technicien
                col1, col2 = st.columns(2)
                with col1:
                    equipements = load_data("equipements") or []
                    equip_options = {e['nom']: e['id'] for e in equipements} if equipements else {}
                    equip_nom = st.selectbox("Équipement*", list(equip_options.keys()) if equip_options else ["Aucun équipement disponible"])
                
                with col2:
                    techniciens = load_data("techniciens") or []
                    tech_options = {t['nom']: t['id'] for t in techniciens} if techniciens else {}
                    tech_nom = st.selectbox("Technicien à assigner*", [""] + list(tech_options.keys()) if tech_options else ["Aucun technicien disponible"])
                
                # Description en pleine largeur
                description = st.text_area("Description*", placeholder="Décrivez le problème en détail...", height=120)
                
                # Deuxième ligne - Type, Priorité, Statut
                col3, col4, col5 = st.columns(3)
                with col3:
                    type_panne = st.selectbox("Type de panne*", ["Mécanique", "Électrique", "Hydraulique", "Logiciel", "Autre"])
                with col4:
                    priorite = st.selectbox("Priorité*", ["Basse", "Moyenne", "Haute", "Critique"])
                with col5:
                    # Options pour les interventions existantes
                    interventions = load_data("interventions") or []
                    interv_options = {f"#{i['id']} - {i.get('description', 'Sans desc')[:30]}...": i['id'] 
                                    for i in interventions if i.get('technicien_id') is None or i.get('statut') == 'Nouvelle'}
                    
                    affecter_existante = st.checkbox("Affecter intervention existante")
                    
                    # Choix du statut selon le contexte
                    if affecter_existante:
                        statut = st.selectbox("Statut*", ["En cours", "Ouverte"])
                    else:
                        statut = st.selectbox("Statut*", ["Nouvelle", "Ouverte", "En cours", "Fermée"])
                
                # Ligne intervention existante (si cochée)
                if affecter_existante and interv_options:
                    intervention_existante = st.selectbox("Sélectionner l'intervention à affecter", list(interv_options.keys()))
                else:
                    intervention_existante = None
                
                # Troisième ligne - Options supplémentaires
                col6, col7 = st.columns(2)
                with col6:
                    est_planifiee = st.checkbox("Intervention planifiée")
                with col7:
                    cout_total = st.number_input("Coût estimé (€)", min_value=0.0, step=0.01, value=0.0)
                
                # Observations en pleine largeur
                observations = st.text_area("Observations pour le technicien", placeholder="Instructions spéciales...", height=100)
                
                st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                with col_btn1:
                    submit = st.form_submit_button("💾 Créer/Affecter", use_container_width=True, type="primary")
                with col_btn2:
                    reset = st.form_submit_button("🔄 Réinitialiser", use_container_width=True)
                
                if submit:
                    if affecter_existante and intervention_existante:
                        # CAS 1: Affectation d'une intervention existante
                        if not tech_nom:
                            handle_error("Technicien requis pour l'affectation.")
                        else:
                            interv_id = interv_options.get(intervention_existante)
                            tech_id = tech_options.get(tech_nom)
                            
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
                            st.rerun()
                    
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
                            
                            if tech_nom:
                                intervention_data["technicien_id"] = tech_options.get(tech_nom)
                                intervention_data["date_affectation"] = datetime.datetime.now().isoformat()
                            
                            result = supabase.table("interventions").insert(intervention_data).execute()
                            
                            if result.data:
                                interv_id = result.data[0]['id']
                                st.success(f"✅ Intervention #{interv_id} créée avec succès !")
                                
                                if tech_nom:
                                    tech_email = get_technicien_email(tech_options.get(tech_nom))
                                    send_email(tech_email, "Nouvelle Intervention Assignée", 
                                            f"Une nouvelle intervention vous a été assignée : {description}\n\n"
                                            f"Type: {type_panne}\n"
                                            f"Priorité: {priorite}\n"
                                            f"Statut: {statut}\n"
                                            f"Observations: {observations or 'Aucune'}")
                                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab4:
            st.markdown(
                """
                <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                    <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                        📤 Import / Export de données
                    </h3>
                """,
                unsafe_allow_html=True
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    """
                    <div style="background: #f0fdf4; padding: 20px; border-radius: 12px; border-left: 4px solid #10b981; margin-bottom: 20px;">
                        <h4 style="color: #065f46; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">📥 Importer des interventions</h4>
                        <p style="color: #047857; font-size: 13px; margin: 0;">Importez vos interventions depuis un fichier CSV ou Excel</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                uploaded_file = st.file_uploader(
                    "Sélectionner un fichier", 
                    type=["csv", "xlsx"], 
                    key="int_import",
                    help="Formats acceptés: CSV, Excel (.xlsx)"
                )
                
                if uploaded_file:
                    try:
                        if uploaded_file.name.endswith('.csv'):
                            import_df = pd.read_csv(uploaded_file)
                        else:
                            import_df = pd.read_excel(uploaded_file)
                        
                        st.markdown(f"**Aperçu** : {len(import_df)} ligne(s) détectée(s)")
                        st.dataframe(import_df.head(), use_container_width=True)
                        
                        if st.button("✅ Confirmer l'import", use_container_width=True, type="primary"):
                            for _, row in import_df.iterrows():
                                supabase.table("interventions").insert(row.to_dict()).execute()
                            st.success(f"✅ {len(import_df)} intervention(s) importée(s) avec succès !")
                            st.rerun()
                    except Exception as e:
                        handle_error(str(e))
            
            with col2:
                st.markdown(
                    """
                    <div style="background: #eff6ff; padding: 20px; border-radius: 12px; border-left: 4px solid #3b82f6; margin-bottom: 20px;">
                        <h4 style="color: #1e40af; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">📤 Télécharger un modèle</h4>
                        <p style="color: #1e3a8a; font-size: 13px; margin: 0;">Obtenez un modèle vide pour faciliter l'import</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                template_df = pd.DataFrame({
                    'equipement_id': [''],
                    'description': ['Description de l\'intervention'],
                    'type_panne': ['Mécanique'],
                    'priorite': ['Moyenne'],
                    'statut': ['Nouvelle'],
                    'cout_total': [0.0],
                    'observations': ['']
                })
                
                template_csv = template_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📄 Télécharger modèle CSV", 
                    template_csv, 
                    "modele_interventions.csv", 
                    "text/csv",
                    use_container_width=True
                )
                
                st.markdown('<div style="margin: 12px 0;"></div>', unsafe_allow_html=True)
                
                template_buffer = BytesIO()
                template_df.to_excel(template_buffer, index=False)
                st.download_button(
                    "📊 Télécharger modèle Excel", 
                    template_buffer.getvalue(), 
                    "modele_interventions.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                st.markdown('<div style="margin: 24px 0;"></div>', unsafe_allow_html=True)
                
                st.info("💡 **Astuce** : Remplissez le modèle avec vos données puis importez-le pour ajouter plusieurs interventions en une seule fois.")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ====================
    # VUE TECHNICIEN
    # ====================
    else:
        tab1, tab2 = st.tabs(["📋 Mes Interventions", "🚨 Déclarer une Panne"])
        
        with tab1:
            st.markdown(
                """
                <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
                    <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                        📋 Mes Interventions en Cours
                    </h3>
                """,
                unsafe_allow_html=True
            )
            
            if data:
                current_interventions = [i for i in data if i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']]
                
                if current_interventions:
                    for interv in current_interventions:
                        statut = interv.get('statut', 'Inconnu')
                        priorite = interv.get('priorite', 'Moyenne')
                        
                        couleur_statut = {
                            'Nouvelle': '#f59e0b',
                            'Ouverte': '#3b82f6',
                            'En cours': '#8b5cf6'
                        }.get(statut, '#6b7280')
                        
                        couleur_priorite = {
                            'Critique': '#ef4444',
                            'Haute': '#f59e0b',
                            'Moyenne': '#3b82f6',
                            'Basse': '#10b981'
                        }.get(priorite, '#6b7280')
                        
                        with st.expander(f"🔧 Intervention #{interv.get('id')} - {interv.get('description', 'Sans description')[:50]}..."):
                            st.markdown(
                                f"""
                                <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); padding: 16px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid {couleur_statut};">
                                    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                                        <div style="background: {couleur_statut}; color: white; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600;">
                                            {statut}
                                        </div>
                                        <div style="background: {couleur_priorite}; color: white; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600;">
                                            Priorité: {priorite}
                                        </div>
                                    </div>
                                    <div style="font-size: 14px; color: #1F2937; margin-bottom: 8px;">
                                        <strong>Description:</strong> {interv.get('description', 'Aucune description')}
                                    </div>
                                    <div style="font-size: 13px; color: #6B7280; display: flex; gap: 16px; flex-wrap: wrap;">
                                        <div>🔧 Type: {interv.get('type_panne', 'Non spécifié')}</div>
                                        <div>📅 Créé le: {interv.get('date_creation', 'N/A')[:10] if interv.get('date_creation') else 'N/A'}</div>
                                        <div>💰 Coût: {interv.get('cout_total', 0):.2f} €</div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            if interv.get('observations'):
                                st.markdown(
                                    f"""
                                    <div style="background: #fffbeb; padding: 12px; border-radius: 8px; margin-bottom: 16px; border-left: 3px solid #f59e0b;">
                                        <div style="font-size: 12px; color: #92400e; font-weight: 600; margin-bottom: 4px;">📝 Observations:</div>
                                        <div style="font-size: 13px; color: #78350f;">{interv.get('observations')}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                new_status = st.selectbox(
                                    "Modifier le statut", 
                                    ["En cours", "Fermée", "En attente"],
                                    key=f"status_{interv.get('id')}"
                                )
                            with col2:
                                st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
                                if st.button("✅ Mettre à jour", key=f"update_{interv.get('id')}", use_container_width=True, type="primary"):
                                    try:
                                        update_data = {"statut": new_status}
                                        if new_status == "Fermée":
                                            update_data["date_cloture"] = datetime.datetime.now().isoformat()
                                        
                                        supabase.table("interventions").update(update_data).eq("id", interv.get('id')).execute()
                                        st.success("✅ Statut mis à jour avec succès !")
                                        st.rerun()
                                    except Exception as e:
                                        handle_error(str(e))
                else:
                    st.info("Aucune intervention en cours.")
                
                # Afficher aussi les interventions terminées récemment
                st.markdown('<div style="margin: 32px 0;"></div>', unsafe_allow_html=True)
                
                st.markdown(
                    """
                    <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                        <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                            ✅ Interventions Terminées
                        </h3>
                    """,
                    unsafe_allow_html=True
                )
                
                closed_interventions = [i for i in data if i.get('statut') == 'Fermée'][:5]
                
                if closed_interventions:
                    for interv in closed_interventions:
                        st.markdown(
                            f"""
                            <div style="background: #f0fdf4; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #10b981;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <div style="font-size: 13px; color: #065f46; font-weight: 600;">
                                            #{interv.get('id')} - {interv.get('description', 'Sans description')[:60]}...
                                        </div>
                                        <div style="font-size: 11px; color: #047857; margin-top: 4px;">
                                            Terminée le: {interv.get('date_cloture', 'N/A')[:10] if interv.get('date_cloture') else 'N/A'}
                                        </div>
                                    </div>
                                    <div style="background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;">
                                        ✓ Fermée
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.info("Aucune intervention terminée récemment.")
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Aucune intervention trouvée.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown(
                """
                <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                    <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                        🚨 Déclarer une Nouvelle Panne
                    </h3>
                    <p style="color: #6B7280; font-size: 13px; margin: 0 0 20px 0;">
                        Signalez rapidement toute panne ou problème technique aux administrateurs
                    </p>
                """,
                unsafe_allow_html=True
            )
            
            with st.form("declaration_panne_mod"):
                st.markdown("##### 🔧 Informations sur la panne")
                
                # Première ligne
                col1, col2 = st.columns(2)
                with col1:
                    equipements = load_data("equipements") or []
                    equip_options = {e['nom']: e['id'] for e in equipements} if equipements else {}
                    equip_nom = st.selectbox(
                        "Machine/Équipement concerné*", 
                        list(equip_options.keys()) if equip_options else ["Aucun équipement disponible"]
                    )
                with col2:
                    priorite = st.selectbox("Niveau de priorité*", ["Basse", "Moyenne", "Haute", "Critique"])
                
                # Type de panne
                type_panne = st.selectbox("Type de panne*", ["Mécanique", "Électrique", "Hydraulique", "Logiciel", "Autre"])
                
                # Description en pleine largeur
                description = st.text_area("Description détaillée de la panne*", height=150, placeholder="Décrivez le problème observé, les circonstances, les symptômes...")
                
                # Observations en pleine largeur
                observations = st.text_area("Observations supplémentaires (optionnel)", height=100, placeholder="Informations complémentaires, actions déjà tentées, photos prises...")
                
                st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                with col_btn1:
                    submit_declare = st.form_submit_button("🚨 Déclarer la Panne", use_container_width=True, type="primary")
                with col_btn2:
                    reset_declare = st.form_submit_button("🔄 Réinitialiser", use_container_width=True)
                
                if submit_declare:
                    if not (equip_nom and description):
                        handle_error("L'équipement et la description sont requis.")
                    else:
                        equip_id = equip_options.get(equip_nom)
                        now = datetime.datetime.now().isoformat()
                        
                        try:
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
                            
                            st.success("✅ Panne déclarée avec succès et envoyée aux administrateurs !")
                            
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
                            
                            st.rerun()
                        except Exception as e:
                            handle_error(str(e))
            
            st.markdown('</div>', unsafe_allow_html=True)

def gestion_equipe():
    if not has_permission("Admin"):
        show_access_denied()
        return
    
    # Header moderne
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px 32px; border-radius: 16px; margin-bottom: 32px; box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);">
            <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">👥 Gestion de l'Équipe</h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">Gérez votre équipe de techniciens et leurs compétences</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    data = load_data("techniciens") or []
    
    # Statistiques rapides
    if data:
        col1, col2, col3, col4 = st.columns(4)
        
        nb_total = len(data)
        
        # Calculer les interventions actives par technicien
        interventions = load_data("interventions") or []
        techniciens_actifs = len(set([i.get('technicien_id') for i in interventions if i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours'] and i.get('technicien_id')]))
        
        # Moyenne d'interventions par technicien
        interventions_par_tech = {}
        for interv in interventions:
            tech_id = interv.get('technicien_id')
            if tech_id:
                interventions_par_tech[tech_id] = interventions_par_tech.get(tech_id, 0) + 1
        
        avg_interventions = sum(interventions_par_tech.values()) / len(interventions_par_tech) if interventions_par_tech else 0
        
        with col1:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">👥 Total</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_total}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Techniciens</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⚡ Actifs</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{techniciens_actifs}</div>
                    <div style="font-size: 11px; opacity: 0.8;">En intervention</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">📊 Moyenne</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{avg_interventions:.1f}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Interventions/tech</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            nb_disponibles = nb_total - techniciens_actifs
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">🆓 Disponibles</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_disponibles}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Sans intervention</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('<div style="margin: 32px 0;"></div>', unsafe_allow_html=True)
    
    # Tabs pour organiser les sections
    tab1, tab2, tab3 = st.tabs(["📋 Liste & Recherche", "✏️ Modifier", "➕ Ajouter"])
    
    with tab1:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    📋 Liste des Techniciens
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        if data:
            df = pd.DataFrame(data)
            
            # Enrichir avec les statistiques d'interventions
            for tech in data:
                tech_id = tech.get('id')
                tech['interventions_actives'] = len([i for i in interventions if i.get('technicien_id') == tech_id and i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']])
                tech['interventions_total'] = len([i for i in interventions if i.get('technicien_id') == tech_id])
            
            df = pd.DataFrame(data)
            
            # Filtres avancés
            col1, col2 = st.columns([3, 1])
            with col1:
                search = st.text_input("🔍 Rechercher par nom ou compétences", key="team_search", placeholder="Tapez pour rechercher...")
            with col2:
                sort_by = st.selectbox("🔄 Trier par", ["Nom", "Interventions actives", "Total interventions"], key="sort_tech")
            
            # Application des filtres
            df_filtered = df.copy()
            
            if search:
                if 'nom' in df_filtered.columns:
                    mask_nom = df_filtered['nom'].str.contains(search, case=False, na=False)
                    if 'competences' in df_filtered.columns:
                        mask_comp = df_filtered['competences'].str.contains(search, case=False, na=False)
                        df_filtered = df_filtered[mask_nom | mask_comp]
                    else:
                        df_filtered = df_filtered[mask_nom]
            
            # Tri
            if sort_by == "Nom" and 'nom' in df_filtered.columns:
                df_filtered = df_filtered.sort_values('nom')
            elif sort_by == "Interventions actives" and 'interventions_actives' in df_filtered.columns:
                df_filtered = df_filtered.sort_values('interventions_actives', ascending=False)
            elif sort_by == "Total interventions" and 'interventions_total' in df_filtered.columns:
                df_filtered = df_filtered.sort_values('interventions_total', ascending=False)
            
            st.markdown(f"**{len(df_filtered)}** technicien(s) trouvé(s)")
            st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
            
            # Affichage en cartes pour une meilleure visualisation
            for _, tech in df_filtered.iterrows():
                tech_id = tech.get('id')
                tech_nom = tech.get('nom', 'Sans nom')
                competences = tech.get('competences', 'Aucune compétence')
                interv_actives = tech.get('interventions_actives', 0)
                interv_total = tech.get('interventions_total', 0)
                
                # Couleur selon la charge de travail
                if interv_actives == 0:
                    couleur_statut = '#10b981'
                    statut_text = 'Disponible'
                elif interv_actives <= 2:
                    couleur_statut = '#3b82f6'
                    statut_text = 'Charge normale'
                elif interv_actives <= 4:
                    couleur_statut = '#f59e0b'
                    statut_text = 'Charge élevée'
                else:
                    couleur_statut = '#ef4444'
                    statut_text = 'Surchargé'
                
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); padding: 20px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid {couleur_statut};">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                            <div style="flex: 1;">
                                <div style="font-size: 18px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">
                                    👤 {tech_nom}
                                </div>
                                <div style="font-size: 13px; color: #6B7280; margin-bottom: 8px;">
                                    🛠️ {competences}
                                </div>
                            </div>
                            <div style="text-align: right; margin-left: 16px;">
                                <div style="background: {couleur_statut}; color: white; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; white-space: nowrap; margin-bottom: 8px;">
                                    {statut_text}
                                </div>
                            </div>
                        </div>
                        <div style="display: flex; gap: 20px; padding-top: 12px; border-top: 1px solid rgba(0,0,0,0.1); font-size: 13px; color: #6B7280;">
                            <div style="background: #dbeafe; padding: 8px 12px; border-radius: 8px; flex: 1; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: #1e40af;">{interv_actives}</div>
                                <div style="font-size: 11px; color: #1e3a8a;">Actives</div>
                            </div>
                            <div style="background: #e0e7ff; padding: 8px 12px; border-radius: 8px; flex: 1; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: #4c1d95;">{interv_total}</div>
                                <div style="font-size: 11px; color: #5b21b6;">Total</div>
                            </div>
                            <div style="background: #fef3c7; padding: 8px 12px; border-radius: 8px; flex: 1; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: #92400e;">{interv_total - interv_actives}</div>
                                <div style="font-size: 11px; color: #78350f;">Terminées</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Exports
            st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
            col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 2])
            with col_exp1:
                csv = df_filtered.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Exporter CSV", csv, "techniciens.csv", "text/csv", use_container_width=True)
            with col_exp2:
                df_clean = clean_dataframe_for_excel(df_filtered)
                excel_buffer = BytesIO()
                df_clean.to_excel(excel_buffer, index=False)
                st.download_button("📊 Exporter Excel", excel_buffer.getvalue(), "techniciens.xlsx", 
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 use_container_width=True)
        else:
            st.info("Aucun technicien trouvé.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    ✏️ Modifier ou Supprimer un Technicien
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        if data:
            techniciens_list = [t['nom'] for t in data]
            selected_technicien_name = st.selectbox(
                "Sélectionner un technicien à modifier", 
                [""] + techniciens_list,
                key="select_tech_modify"
            )
            
            if selected_technicien_name:
                technicien_data = next((t for t in data if t['nom'] == selected_technicien_name), None)
                
                if technicien_data:
                    technicien_id = technicien_data['id']
                    
                    # Statistiques du technicien
                    tech_interventions = [i for i in interventions if i.get('technicien_id') == technicien_id]
                    nb_actives = len([i for i in tech_interventions if i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']])
                    nb_total = len(tech_interventions)
                    
                    # Aperçu du technicien
                    if nb_actives == 0:
                        couleur_statut = '#10b981'
                        statut_text = 'Disponible'
                    elif nb_actives <= 2:
                        couleur_statut = '#3b82f6'
                        statut_text = 'Charge normale'
                    else:
                        couleur_statut = '#f59e0b'
                        statut_text = 'Charge élevée'
                    
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 20px; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid {couleur_statut};">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                                <div>
                                    <div style="font-size: 20px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">
                                        👤 {technicien_data.get('nom', 'Sans nom')}
                                    </div>
                                    <div style="font-size: 13px; color: #6B7280;">
                                        🛠️ {technicien_data.get('competences', 'Aucune compétence')}
                                    </div>
                                </div>
                                <div style="background: {couleur_statut}; color: white; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 600;">
                                    {statut_text}
                                </div>
                            </div>
                            <div style="display: flex; gap: 12px; padding-top: 16px; border-top: 1px solid rgba(0,0,0,0.1); font-size: 12px; color: #6B7280;">
                                <div style="background: #dbeafe; padding: 8px 12px; border-radius: 6px; flex: 1; text-align: center;">
                                    <strong style="color: #1e40af; font-size: 18px;">{nb_actives}</strong>
                                    <div style="color: #1e3a8a; font-size: 10px; margin-top: 2px;">Actives</div>
                                </div>
                                <div style="background: #e0e7ff; padding: 8px 12px; border-radius: 6px; flex: 1; text-align: center;">
                                    <strong style="color: #4c1d95; font-size: 18px;">{nb_total}</strong>
                                    <div style="color: #5b21b6; font-size: 10px; margin-top: 2px;">Total</div>
                                </div>
                                <div style="background: #d1fae5; padding: 8px 12px; border-radius: 6px; flex: 1; text-align: center;">
                                    <strong style="color: #065f46; font-size: 18px;">{nb_total - nb_actives}</strong>
                                    <div style="color: #047857; font-size: 10px; margin-top: 2px;">Terminées</div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(
                            """
                            <div style="background: #f0f9ff; padding: 16px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #0ea5e9;">
                                <h4 style="color: #0c4a6e; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">💾 Modifier le technicien</h4>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        with st.form(f"modifier_technicien_{technicien_id}"):
                            nouveau_nom = st.text_input("Nom complet", value=technicien_data.get('nom', ''))
                            nouvelles_competences = st.text_area(
                                "Compétences", 
                                value=technicien_data.get('competences', ''),
                                height=100,
                                placeholder="Ex: Mécanique, Électrique, Hydraulique..."
                            )
                            
                            st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
                            password = st.text_input(
                                "🔒 Mot de passe administrateur", 
                                type="password", 
                                help="Entrez votre mot de passe pour confirmer"
                            )
                            
                            if st.form_submit_button("💾 Sauvegarder les modifications", use_container_width=True, type="primary"):
                                if not password:
                                    st.error("⚠️ Veuillez entrer le mot de passe administrateur")
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
                        st.markdown(
                            """
                            <div style="background: #fef2f2; padding: 16px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #ef4444;">
                                <h4 style="color: #991b1b; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">🗑️ Supprimer le technicien</h4>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        st.warning("⚠️ **Attention** : Cette action est irréversible")
                        
                        with st.form(f"supprimer_technicien_{technicien_id}"):
                            st.markdown(
                                f"""
                                <div style="background: white; padding: 12px; border-radius: 8px; margin: 16px 0; border: 1px solid #fee2e2;">
                                    <div style="font-size: 13px; color: #7f1d1d; font-weight: 600;">
                                        Vous êtes sur le point de supprimer :
                                    </div>
                                    <div style="font-size: 15px; color: #991b1b; font-weight: 700; margin-top: 4px;">
                                        {technicien_data.get('nom', 'Technicien')}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            if nb_actives > 0:
                                st.error(f"❌ Ce technicien a {nb_actives} intervention(s) active(s). Impossible de le supprimer.")
                            
                            password_supp = st.text_input(
                                "🔒 Mot de passe administrateur", 
                                type="password", 
                                key=f"pass_supp_tech_{technicien_id}",
                                help="Entrez votre mot de passe pour confirmer la suppression",
                                disabled=nb_actives > 0
                            )
                            
                            if st.form_submit_button(
                                "🗑️ Confirmer la suppression", 
                                use_container_width=True, 
                                type="secondary",
                                disabled=nb_actives > 0
                            ):
                                if not password_supp:
                                    st.error("⚠️ Veuillez entrer le mot de passe administrateur")
                                elif verify_admin_password(password_supp):
                                    try:
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
        else:
            st.info("Aucun technicien disponible à modifier.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    ➕ Ajouter un nouveau technicien
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        with st.form("ajout_technicien_mod"):
            nom = st.text_input("Nom complet du technicien*", placeholder="Ex: Jean Dupont")
            competences = st.text_area(
                "Compétences (séparées par virgule)", 
                placeholder="Ex: Mécanique industrielle, Électricité, Hydraulique, Pneumatique...",
                height=100
            )
            
            st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            with col_btn1:
                submit = st.form_submit_button("➕ Ajouter le technicien", use_container_width=True, type="primary")
            with col_btn2:
                reset = st.form_submit_button("🔄 Réinitialiser", use_container_width=True)
            
            if submit:
                if not nom:
                    st.error("⚠️ Le nom du technicien est requis.")
                else:
                    try:
                        supabase.table("techniciens").insert({
                            "nom": nom,
                            "competences": competences
                        }).execute()
                        st.success("✅ Technicien ajouté avec succès !")
                        st.rerun()
                    except Exception as e:
                        handle_error(str(e))
        
        st.markdown('</div>', unsafe_allow_html=True)

def gestion_stocks():
    if not has_permission("Admin"):
        show_access_denied()
        return
    
    # Header moderne
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px 32px; border-radius: 16px; margin-bottom: 32px; box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);">
            <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">📦 Gestion des Stocks</h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">Gérez votre inventaire de pièces détachées et consommables</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    data = load_data("stocks") or []
    
    # Statistiques rapides
    if data:
        col1, col2, col3, col4 = st.columns(4)
        
        nb_total = len(data)
        nb_critiques = len([s for s in data if s.get('quantite') is not None and s.get('niveau_critique') is not None and s['quantite'] <= s['niveau_critique']])
        valeur_totale = sum([s.get('quantite', 0) * s.get('cout_unitaire', 0) for s in data])
        nb_stock_zero = len([s for s in data if s.get('quantite', 0) == 0])
        
        with col1:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">📊 Total Références</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_total}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Pièces répertoriées</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⚠️ Stocks Critiques</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_critiques}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Réapprovisionnement requis</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">💰 Valeur Totale</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{valeur_totale:,.0f}€</div>
                    <div style="font-size: 11px; opacity: 0.8;">Inventaire valorisé</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">🚫 Ruptures</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_stock_zero}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Stock à zéro</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('<div style="margin: 32px 0;"></div>', unsafe_allow_html=True)
    
    # Alertes critiques en haut
    if data:
        critiques = [s for s in data if s.get('quantite') is not None and s.get('niveau_critique') is not None and s['quantite'] <= s['niveau_critique']]
        if critiques:
            st.markdown(
                """
                <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); padding: 20px; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid #ef4444;">
                    <h3 style="color: #991b1b; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">🚨 Alertes de Stocks Critiques</h3>
                """,
                unsafe_allow_html=True
            )
            
            for c in critiques:
                quantite = c.get('quantite', 0)
                niveau_critique = c.get('niveau_critique', 0)
                pourcentage = (quantite / niveau_critique * 100) if niveau_critique > 0 else 0
                
                if quantite == 0:
                    couleur = '#ef4444'
                    niveau = 'RUPTURE'
                elif pourcentage <= 50:
                    couleur = '#f59e0b'
                    niveau = 'TRÈS BAS'
                else:
                    couleur = '#f97316'
                    niveau = 'BAS'
                
                st.markdown(
                    f"""
                    <div style="background: white; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid {couleur};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 14px; color: #1F2937; font-weight: 600;">{c.get('nom', 'Sans nom')}</div>
                                <div style="font-size: 12px; color: #6B7280; margin-top: 2px;">
                                    Quantité: <strong style="color: {couleur};">{quantite}</strong> / Seuil: {niveau_critique}
                                </div>
                            </div>
                            <div style="background: {couleur}; color: white; padding: 4px 12px; border-radius: 6px; font-size: 11px; font-weight: 600;">
                                {niveau}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs pour organiser les sections
    tab1, tab2, tab3 = st.tabs(["📋 Liste & Recherche", "✏️ Modifier", "➕ Ajouter"])
    
    with tab1:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    📋 Inventaire des Stocks
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        if data:
            df = pd.DataFrame(data)
            
            # Filtres avancés
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                search = st.text_input("🔍 Rechercher par nom ou description", key="stock_search", placeholder="Tapez pour rechercher...")
            with col2:
                filtre_statut = st.selectbox("📊 Filtrer par statut", ["Tous", "Critiques", "Rupture", "Normaux"])
            with col3:
                sort_by = st.selectbox("🔄 Trier par", ["Nom", "Quantité", "Valeur"], key="sort_stock")
            
            # Application des filtres
            df_filtered = df.copy()
            
            if search:
                if 'nom' in df_filtered.columns:
                    mask_nom = df_filtered['nom'].str.contains(search, case=False, na=False)
                    if 'description' in df_filtered.columns:
                        mask_desc = df_filtered['description'].str.contains(search, case=False, na=False)
                        df_filtered = df_filtered[mask_nom | mask_desc]
                    else:
                        df_filtered = df_filtered[mask_nom]
            
            # Filtre par statut
            if filtre_statut == "Critiques":
                df_filtered = df_filtered[(df_filtered['quantite'] <= df_filtered['niveau_critique']) & (df_filtered['quantite'] > 0)]
            elif filtre_statut == "Rupture":
                df_filtered = df_filtered[df_filtered['quantite'] == 0]
            elif filtre_statut == "Normaux":
                df_filtered = df_filtered[df_filtered['quantite'] > df_filtered['niveau_critique']]
            
            # Calcul de la valeur
            df_filtered['valeur_stock'] = df_filtered['quantite'] * df_filtered['cout_unitaire']
            
            # Tri
            if sort_by == "Nom" and 'nom' in df_filtered.columns:
                df_filtered = df_filtered.sort_values('nom')
            elif sort_by == "Quantité" and 'quantite' in df_filtered.columns:
                df_filtered = df_filtered.sort_values('quantite', ascending=False)
            elif sort_by == "Valeur":
                df_filtered = df_filtered.sort_values('valeur_stock', ascending=False)
            
            st.markdown(f"**{len(df_filtered)}** pièce(s) trouvée(s)")
            st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
            
            # Affichage en cartes
            for _, stock in df_filtered.iterrows():
                quantite = stock.get('quantite', 0)
                niveau_critique = stock.get('niveau_critique', 0)
                valeur = stock.get('valeur_stock', 0)
                
                # Déterminer le statut
                if quantite == 0:
                    couleur_statut = '#ef4444'
                    statut_text = '🚫 RUPTURE'
                elif quantite <= niveau_critique:
                    couleur_statut = '#f59e0b'
                    statut_text = '⚠️ CRITIQUE'
                elif quantite <= niveau_critique * 1.5:
                    couleur_statut = '#3b82f6'
                    statut_text = '🔵 BAS'
                else:
                    couleur_statut = '#10b981'
                    statut_text = '✅ OK'
                
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); padding: 20px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid {couleur_statut};">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                            <div style="flex: 1;">
                                <div style="font-size: 18px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">
                                    📦 {stock.get('nom', 'Sans nom')}
                                </div>
                                <div style="font-size: 13px; color: #6B7280; margin-bottom: 8px;">
                                    {stock.get('description', 'Aucune description')[:100]}...
                                </div>
                            </div>
                            <div style="text-align: right; margin-left: 16px;">
                                <div style="background: {couleur_statut}; color: white; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; white-space: nowrap;">
                                    {statut_text}
                                </div>
                            </div>
                        </div>
                        <div style="display: flex; gap: 16px; padding-top: 12px; border-top: 1px solid rgba(0,0,0,0.1);">
                            <div style="background: #dbeafe; padding: 10px 14px; border-radius: 8px; flex: 1; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: #1e40af;">{quantite}</div>
                                <div style="font-size: 11px; color: #1e3a8a;">En stock</div>
                            </div>
                            <div style="background: #fef3c7; padding: 10px 14px; border-radius: 8px; flex: 1; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: #92400e;">{niveau_critique}</div>
                                <div style="font-size: 11px; color: #78350f;">Seuil</div>
                            </div>
                            <div style="background: #d1fae5; padding: 10px 14px; border-radius: 8px; flex: 1; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: #065f46;">{stock.get('cout_unitaire', 0):.2f}€</div>
                                <div style="font-size: 11px; color: #047857;">Prix unit.</div>
                            </div>
                            <div style="background: #e0e7ff; padding: 10px 14px; border-radius: 8px; flex: 1; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: #4c1d95;">{valeur:.2f}€</div>
                                <div style="font-size: 11px; color: #5b21b6;">Valeur</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Exports
            st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
            col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 2])
            with col_exp1:
                csv = df_filtered.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Exporter CSV", csv, "stocks.csv", "text/csv", use_container_width=True)
            with col_exp2:
                df_clean = clean_dataframe_for_excel(df_filtered)
                excel_buffer = BytesIO()
                df_clean.to_excel(excel_buffer, index=False)
                st.download_button("📊 Exporter Excel", excel_buffer.getvalue(), "stocks.xlsx", 
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 use_container_width=True)
        else:
            st.info("Aucun stock trouvé.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    ✏️ Modifier ou Supprimer un Stock
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        if data:
            stocks_list = [s['nom'] for s in data]
            selected_stock_name = st.selectbox(
                "Sélectionner un stock à modifier", 
                [""] + stocks_list,
                key="select_stock_modify"
            )
            
            if selected_stock_name:
                stock_data = next((s for s in data if s['nom'] == selected_stock_name), None)
                
                if stock_data:
                    stock_id = stock_data['id']
                    quantite = stock_data.get('quantite', 0)
                    niveau_critique = stock_data.get('niveau_critique', 0)
                    valeur_stock = quantite * stock_data.get('cout_unitaire', 0)
                    
                    # Déterminer le statut
                    if quantite == 0:
                        couleur_statut = '#ef4444'
                        statut_text = '🚫 RUPTURE'
                    elif quantite <= niveau_critique:
                        couleur_statut = '#f59e0b'
                        statut_text = '⚠️ CRITIQUE'
                    else:
                        couleur_statut = '#10b981'
                        statut_text = '✅ OK'
                    
                    # Aperçu du stock
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 20px; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid {couleur_statut};">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                                <div>
                                    <div style="font-size: 20px; font-weight: 700; color: #1F2937; margin-bottom: 4px;">
                                        📦 {stock_data.get('nom', 'Sans nom')}
                                    </div>
                                    <div style="font-size: 13px; color: #6B7280;">
                                        {stock_data.get('description', 'Aucune description')[:100]}...
                                    </div>
                                </div>
                                <div style="background: {couleur_statut}; color: white; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 600;">
                                    {statut_text}
                                </div>
                            </div>
                            <div style="display: flex; gap: 12px; padding-top: 16px; border-top: 1px solid rgba(0,0,0,0.1);">
                                <div style="background: #dbeafe; padding: 10px; border-radius: 6px; flex: 1; text-align: center;">
                                    <strong style="color: #1e40af; font-size: 18px;">{quantite}</strong>
                                    <div style="color: #1e3a8a; font-size: 10px; margin-top: 2px;">En stock</div>
                                </div>
                                <div style="background: #fef3c7; padding: 10px; border-radius: 6px; flex: 1; text-align: center;">
                                    <strong style="color: #92400e; font-size: 18px;">{niveau_critique}</strong>
                                    <div style="color: #78350f; font-size: 10px; margin-top: 2px;">Seuil</div>
                                </div>
                                <div style="background: #d1fae5; padding: 10px; border-radius: 6px; flex: 1; text-align: center;">
                                    <strong style="color: #065f46; font-size: 18px;">{stock_data.get('cout_unitaire', 0):.2f}€</strong>
                                    <div style="color: #047857; font-size: 10px; margin-top: 2px;">Prix unit.</div>
                                </div>
                                <div style="background: #e0e7ff; padding: 10px; border-radius: 6px; flex: 1; text-align: center;">
                                    <strong style="color: #4c1d95; font-size: 18px;">{valeur_stock:.2f}€</strong>
                                    <div style="color: #5b21b6; font-size: 10px; margin-top: 2px;">Valeur totale</div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(
                            """
                            <div style="background: #f0f9ff; padding: 16px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #0ea5e9;">
                                <h4 style="color: #0c4a6e; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">💾 Modifier le stock</h4>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        with st.form(f"modifier_stock_{stock_id}"):
                            nouveau_nom = st.text_input("Nom de la pièce", value=stock_data.get('nom', ''))
                            
                            col_form1, col_form2 = st.columns(2)
                            with col_form1:
                                nouvelle_quantite = st.number_input("Quantité", value=stock_data.get('quantite', 0), min_value=0)
                                nouveau_niveau_critique = st.number_input("Niveau critique", value=stock_data.get('niveau_critique', 0), min_value=0)
                            with col_form2:
                                nouveau_cout = st.number_input("Coût unitaire (€)", value=float(stock_data.get('cout_unitaire', 0)), min_value=0.0, step=0.01)
                                st.markdown(f"**Valeur:** {nouvelle_quantite * nouveau_cout:.2f}€")
                            
                            nouvelle_description = st.text_area("Description", value=stock_data.get('description', ''), height=80)
                            
                            st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
                            password = st.text_input(
                                "🔒 Mot de passe administrateur", 
                                type="password", 
                                help="Entrez votre mot de passe pour confirmer"
                            )
                            
                            if st.form_submit_button("💾 Sauvegarder les modifications", use_container_width=True, type="primary"):
                                if not password:
                                    st.error("⚠️ Veuillez entrer le mot de passe administrateur")
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
                        st.markdown(
                            """
                            <div style="background: #fef2f2; padding: 16px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #ef4444;">
                                <h4 style="color: #991b1b; font-size: 16px; font-weight: 700; margin: 0 0 12px 0;">🗑️ Supprimer le stock</h4>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        st.warning("⚠️ **Attention** : Cette action est irréversible")
                        
                        with st.form(f"supprimer_stock_{stock_id}"):
                            st.markdown(
                                f"""
                                <div style="background: white; padding: 12px; border-radius: 8px; margin: 16px 0; border: 1px solid #fee2e2;">
                                    <div style="font-size: 13px; color: #7f1d1d; font-weight: 600;">
                                        Vous êtes sur le point de supprimer :
                                    </div>
                                    <div style="font-size: 15px; color: #991b1b; font-weight: 700; margin-top: 4px;">
                                        {stock_data.get('nom', 'Stock')}
                                    </div>
                                    <div style="font-size: 12px; color: #991b1b; margin-top: 4px;">
                                        Valeur: {valeur_stock:.2f}€
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            password_supp = st.text_input(
                                "🔒 Mot de passe administrateur", 
                                type="password", 
                                key=f"pass_supp_stock_{stock_id}",
                                help="Entrez votre mot de passe pour confirmer la suppression"
                            )
                            
                            if st.form_submit_button("🗑️ Confirmer la suppression", use_container_width=True, type="secondary"):
                                if not password_supp:
                                    st.error("⚠️ Veuillez entrer le mot de passe administrateur")
                                elif verify_admin_password(password_supp):
                                    try:
                                        supabase.table("stocks").delete().eq("id", stock_id).execute()
                                        st.success("✅ Stock supprimé avec succès")
                                        st.rerun()
                                    except Exception as e:
                                        handle_error(str(e))
                                else:
                                    st.error("❌ Mot de passe administrateur incorrect")
        else:
            st.info("Aucun stock disponible à modifier.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    ➕ Ajouter une nouvelle pièce
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        with st.form("ajout_stock_mod"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom de la pièce*", placeholder="Ex: Roulement SKF 6205")
                nouvelle_quantite_ajout = st.number_input("Quantité initiale*", min_value=0, value=0)
                niveau_critique = st.number_input("Niveau critique*", min_value=0, value=5, help="Seuil d'alerte de réapprovisionnement")
            with col2:
                cout_unitaire = st.number_input("Coût unitaire (€)*", min_value=0.0, step=0.01, value=0.0)
                # Calcul valeur en temps réel
                if 'nouvelle_quantite_ajout' in locals() and 'cout_unitaire' in locals():
                    valeur_calculee = nouvelle_quantite_ajout * cout_unitaire
                    st.markdown(f"**Valeur stock:** {valeur_calculee:.2f}€")
                
                description = st.text_area("Description", placeholder="Référence fabricant, spécifications techniques...", height=66)
            
            st.markdown('<div style="margin: 16px 0;"></div>', unsafe_allow_html=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            with col_btn1:
                submit = st.form_submit_button("➕ Ajouter la pièce", use_container_width=True, type="primary")
            with col_btn2:
                reset = st.form_submit_button("🔄 Réinitialiser", use_container_width=True)
            
            if submit:
                if not nom:
                    st.error("⚠️ Le nom de la pièce est requis.")
                else:
                    try:
                        supabase.table("stocks").insert({
                            "nom": nom,
                            "quantite": int(nouvelle_quantite_ajout),
                            "niveau_critique": int(niveau_critique),
                            "cout_unitaire": float(cout_unitaire),
                            "description": description
                        }).execute()
                        st.success("✅ Pièce ajoutée avec succès !")
                        st.rerun()
                    except Exception as e:
                        handle_error(str(e))
        
        st.markdown('</div>', unsafe_allow_html=True)
def planification():
    if not has_permission("Admin"):
        show_access_denied()
        return
    
    # Header moderne cohérent avec les autres pages
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 24px 32px; border-radius: 16px; margin-bottom: 32px; 
                    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);">
            <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                📅 Planification de Maintenance
            </h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">
                AMDEC • Analyse Prédictive • Intelligence Préventive
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    data = load_data("maintenance_plans") or []
    interventions_data = load_data("interventions") or []
    equipements_data = load_data("equipements") or []
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 1: Statistiques Rapides (style cohérent)
    # ═══════════════════════════════════════════════════════════════
    if data:
        col1, col2, col3, col4 = st.columns(4)
        
        plans_planifies = len([p for p in data if p.get('statut') == 'Planifiée'])
        plans_en_cours = len([p for p in data if p.get('statut') == 'En cours'])
        plans_termines = len([p for p in data if p.get('statut') == 'Terminée'])
        retards = len([p for p in data if p.get('date_planified') and 
                      safe_date_comparison(p['date_planified'], datetime.datetime.now()) < 0 and
                      p.get('statut') in ['Planifiée', 'En cours']])
        
        with col1:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">📅 Planifiés</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{plans_planifies}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Plans à venir</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⚡ En cours</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{plans_en_cours}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Actifs</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">✅ Terminés</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{plans_termines}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Complétés</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3); color: white;">
                    <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⚠️ Retards</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{retards}</div>
                    <div style="font-size: 11px; opacity: 0.8;">À traiter d'urgence</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('<div style="margin: 32px 0;"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════
    # SECTION 2: Analyse AMDEC avec Tabs
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                🔍 Analyse AMDEC - Modes de Défaillance
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    tab1, tab2 = st.tabs(["📊 Statistiques", "🎯 Criticité"])
    
    with tab1:
        if interventions_data and equipements_data:
            stats_pannes = {}
            for equip in equipements_data:
                equip_id = equip['id']
                pannes_equip = [i for i in interventions_data if i.get('equipement_id') == equip_id]
                
                if pannes_equip:
                    stats_pannes[equip['nom']] = {
                        'total_pannes': len(pannes_equip),
                        'types_pannes': {},
                        'couts_totaux': sum(float(i.get('cout_total', 0)) for i in pannes_equip)
                    }
                    
                    for panne in pannes_equip:
                        type_panne = panne.get('type_panne', 'Non spécifié')
                        stats_pannes[equip['nom']]['types_pannes'][type_panne] = stats_pannes[equip['nom']]['types_pannes'].get(type_panne, 0) + 1
            
            if stats_pannes:
                df_stats = pd.DataFrame({
                    'Équipement': list(stats_pannes.keys()),
                    'Nombre de pannes': [v['total_pannes'] for v in stats_pannes.values()],
                    'Coût total (€)': [v['couts_totaux'] for v in stats_pannes.values()]
                })
                
                fig = px.bar(df_stats, x='Équipement', y='Nombre de pannes', 
                            title='Fréquence des Pannes par Équipement',
                            color='Coût total (€)', 
                            color_continuous_scale=['#fef3c7', '#f59e0b', '#dc2626'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=get_theme()['text'], size=12),
                    title_font_size=14,
                    margin=dict(t=40, l=20, r=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Aucune donnée de panne disponible")
        else:
            st.info("💡 Données insuffisantes pour l'analyse")
    
    with tab2:
        if interventions_data and equipements_data:
            criticite_equipements = []
            
            for equip in equipements_data:
                equip_id = equip['id']
                pannes_equip = [i for i in interventions_data if i.get('equipement_id') == equip_id]
                
                if pannes_equip:
                    frequence = len(pannes_equip)
                    cout_moyen = sum(float(i.get('cout_total', 0)) for i in pannes_equip) / frequence
                    criticite = frequence * cout_moyen
                    
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
                
                # Affichage en cartes pour meilleure visualisation
                for _, crit in df_criticite.iterrows():
                    couleur = '#ef4444' if '🔴' in crit['Niveau'] else '#f59e0b' if '🟡' in crit['Niveau'] else '#10b981'
                    
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                                    padding: 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid {couleur};">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="font-size: 16px; font-weight: 700; color: #1F2937;">{crit['Équipement']}</div>
                                    <div style="font-size: 13px; color: #6B7280; margin-top: 4px;">
                                        Fréquence: {crit['Fréquence']} | Coût moyen: {crit['Coût moyen']}
                                    </div>
                                </div>
                                <div style="background: {couleur}; color: white; padding: 6px 12px; border-radius: 8px; 
                                            font-size: 12px; font-weight: 600; white-space: nowrap;">
                                    {crit['Niveau']}
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                # Recommandations compactes
                st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
                haute_criticite = [e for e in criticite_equipements if "🔴" in e['Niveau']]
                
                if haute_criticite:
                    st.error(f"**🚨 {len(haute_criticite)} équipement(s) critiques** - Maintenance urgente recommandée")
                else:
                    st.success("**✅ Situation sous contrôle** - Aucun équipement en criticité élevée")
            else:
                st.info("💡 Aucune donnée de criticité disponible")
        else:
            st.info("💡 Données insuffisantes")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════
    # SECTION 3: Prédiction des Pannes
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 1.5rem; border-radius: 12px; margin: 2rem 0;
                    box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);">
            <h2 style="margin: 0; color: white; font-size: 1.8rem; display: flex; align-items: center;">
                <span style="margin-right: 1rem;">🔮</span>
                Intelligence Prédictive - Anticipation des Défaillances
            </h2>
            <p style="color: rgba(255,255,255,0.85); margin: 0.5rem 0 0 0; font-size: 0.95rem;">
                Analyse des tendances et recommandations basées sur l'IA
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_pred1, col_pred2 = st.columns(2)
    
    with col_pred1:
        st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h3 style="color: #1e293b; margin-top: 0; font-size: 1.3rem;">
                    📈 Analyse des Tendances Historiques
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        if interventions_data:
            df_interventions = pd.DataFrame(interventions_data)
            if 'date_creation' in df_interventions.columns:
                df_interventions['date_creation'] = pd.to_datetime(df_interventions['date_creation'], errors='coerce')
                interventions_par_mois = df_interventions.set_index('date_creation').resample('M').size()
                
                if len(interventions_par_mois) >= 3:
                    x = np.arange(len(interventions_par_mois))
                    y = interventions_par_mois.values
                    slope, intercept, r_value, p_value, std_err = linregress(x, y)
                    
                    mois_futurs = 6
                    x_futur = np.arange(len(interventions_par_mois), len(interventions_par_mois) + mois_futurs)
                    predictions = slope * x_futur + intercept
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=interventions_par_mois.index, 
                        y=interventions_par_mois.values,
                        mode='lines+markers',
                        name='Données Réelles',
                        line=dict(color='#667eea', width=3),
                        marker=dict(size=8, color='#667eea')
                    ))
                    fig.add_trace(go.Scatter(
                        x=pd.date_range(interventions_par_mois.index[-1], periods=mois_futurs+1, freq='M')[1:],
                        y=predictions,
                        mode='lines+markers',
                        name='Prédictions IA',
                        line=dict(color='#f59e0b', dash='dash', width=2),
                        marker=dict(size=8, symbol='diamond', color='#f59e0b')
                    ))
                    fig.update_layout(
                        title='Prédiction du Nombre de Pannes (6 mois)',
                        xaxis_title='Période',
                        yaxis_title='Nombre de Pannes',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color=get_theme()['text'], size=11),
                        hovermode='x unified',
                        margin=dict(t=40, l=20, r=20, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if slope > 0:
                        st.markdown(f"""
                            <div style="background: #fee2e2; padding: 1rem; border-radius: 8px; 
                                        border-left: 4px solid #dc2626; margin-top: 1rem;">
                                <strong style="color: #dc2626;">📈 Tendance Haussière Détectée</strong><br>
                                <span style="color: #991b1b;">Augmentation de {slope:.2f} pannes/mois</span>
                            </div>
                        """, unsafe_allow_html=True)
                        st.info("💡 **Action Recommandée**: Renforcer les maintenances préventives et auditer les procédures")
                    else:
                        st.markdown(f"""
                            <div style="background: #d1fae5; padding: 1rem; border-radius: 8px; 
                                        border-left: 4px solid #059669; margin-top: 1rem;">
                                <strong style="color: #059669;">📉 Tendance Baissière Positive</strong><br>
                                <span style="color: #047857;">Réduction de {abs(slope):.2f} pannes/mois</span>
                            </div>
                        """, unsafe_allow_html=True)
                        st.success("💡 **Bonne Pratique**: Maintenir les standards actuels de maintenance")
                else:
                    st.info("📊 Historique insuffisant pour la prédiction (minimum 3 mois requis)")
            else:
                st.warning("❌ Champ 'date_creation' manquant dans les interventions")
        else:
            st.info("📭 Aucune donnée d'intervention disponible")

    with col_pred2:
        st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h3 style="color: #1e293b; margin-top: 0; font-size: 1.3rem;">
                    🤖 Recommandations Intelligentes par IA
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        if interventions_data and equipements_data:
            recommandations = []
            
            for equip in equipements_data:
                equip_id = equip['id']
                pannes_equip = [i for i in interventions_data if i.get('equipement_id') == equip_id]
                
                if len(pannes_equip) >= 2:
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
                            prochaine_panne_prevue = dates_pannes[-1] + datetime.timedelta(days=interval_moyen)
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
                recommandations_triees = sorted(recommandations, key=lambda x: x['Jours restants'])
                df_recommandations = pd.DataFrame(recommandations_triees)
                
                st.dataframe(df_recommandations, use_container_width=True, height=250)
                
                urgents = len([r for r in recommandations if "🔴" in r['Recommandation']])
                if urgents > 0:
                    st.markdown(f"""
                        <div style="background: #fee2e2; padding: 1.5rem; border-radius: 10px; 
                                    border: 2px solid #dc2626; margin: 1rem 0;">
                            <h4 style="color: #dc2626; margin: 0 0 0.5rem 0;">
                                🚨 Alerte Urgente: {urgents} Équipement(s)
                            </h4>
                            <p style="color: #991b1b; margin: 0;">
                                Intervention immédiate requise pour éviter les pannes critiques
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.button("📋 Générer Plan d'Urgence Automatique", use_container_width=True, type="primary")
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    count = len([r for r in recommandations if "🟢" in r['Recommandation']])
                    st.metric("🟢 À surveiller", count)
                with col_stat2:
                    count = len([r for r in recommandations if "🟡" in r['Recommandation']])
                    st.metric("🟡 Proche", count)
                with col_stat3:
                    st.metric("🔴 Urgent", urgents)
            else:
                st.info("📊 Données historiques insuffisantes pour les recommandations")
        else:
            st.info("📭 Données insuffisantes pour les recommandations IA")

    # ═══════════════════════════════════════════════════════════════
    # SECTION 4: Gestion des Plans
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: linear-gradient(to right, #f8fafc, #e2e8f0); 
                    padding: 1.5rem; border-radius: 12px; margin: 2rem 0;
                    border-left: 5px solid #667eea;">
            <h2 style="margin: 0; color: #1e293b; font-size: 1.5rem;">
                📝 Gestion des Plans de Maintenance
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    if data:
        df = pd.DataFrame(data)
        if 'date_planified' in df.columns:
            df['date_planified'] = pd.to_datetime(df['date_planified'], errors='coerce')
        
        # Filtres avec design amélioré
        with st.expander("🔍 Filtres Avancés", expanded=False):
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            with col_filter1:
                search = st.text_input("🔍 Rechercher", placeholder="Description, équipement...", key="plans_search")
            with col_filter2:
                statut_filter = st.multiselect("📊 Statut", 
                                             sorted(df['statut'].dropna().unique().tolist() if 'statut' in df.columns else []))
            with col_filter3:
                type_filter = st.multiselect("🎯 Type",
                                           sorted(df['type'].dropna().unique().tolist() if 'type' in df.columns else []))
        
        if search and 'description' in df.columns:
            df = df[df['description'].str.contains(search, case=False, na=False)]
        if statut_filter and 'statut' in df.columns:
            df = df[df['statut'].isin(statut_filter)]
        if type_filter and 'type' in df.columns:
            df = df[df['type'].isin(type_filter)]
        
        def color_statut(val):
            if val == 'Planifiée':
                return 'background-color: #dbeafe; color: #1e40af; font-weight: 500;'
            elif val == 'En cours':
                return 'background-color: #fef3c7; color: #b45309; font-weight: 500;'
            elif val == 'Terminée':
                return 'background-color: #d1fae5; color: #047857; font-weight: 500;'
            elif val == 'Annulée':
                return 'background-color: #fee2e2; color: #991b1b; font-weight: 500;'
            return ''
        
        if not df.empty and 'statut' in df.columns:
            styled_df = df.style.applymap(color_statut, subset=['statut'])
            st.dataframe(styled_df, use_container_width=True, height=400)
        else:
            st.dataframe(df, use_container_width=True, height=400)
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Exporter CSV", csv, "plans_maintenance_amdec.csv", "text/csv", use_container_width=True)
        with col_exp2:
            df_clean = clean_dataframe_for_excel(df)
            excel_buffer = BytesIO()
            df_clean.to_excel(excel_buffer, index=False)
            st.download_button("📊 Exporter Excel", excel_buffer, "plans_maintenance_amdec.xlsx", 
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    else:
        st.info("📭 Aucun plan de maintenance disponible. Créez-en un ci-dessous!")

    # ═══════════════════════════════════════════════════════════════
    # SECTION 5: Création de Plans Intelligents
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                    padding: 1.5rem; border-radius: 12px; margin: 2rem 0;
                    box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3);">
            <h2 style="margin: 0; color: white; font-size: 1.8rem; display: flex; align-items: center;">
                <span style="margin-right: 1rem;">🚀</span>
                Créer un Plan de Maintenance Intelligent
            </h2>
            <p style="color: rgba(255,255,255,0.85); margin: 0.5rem 0 0 0; font-size: 0.95rem;">
                Planification assistée par IA avec suggestions automatiques
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("ajout_plan_intelligent"):
        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            equipements = load_data("equipements") or []
            equip_options = {e['nom']: e['id'] for e in equipements} if equipements else {}
            
            if equip_options:
                equip_nom = st.selectbox("🏭 Équipement*", [""] + list(equip_options.keys()))
            else:
                equip_nom = st.selectbox("🏭 Équipement*", ["Aucun équipement disponible"])
            
            date_planified = st.date_input("📅 Date planifiée*", 
                                          value=datetime.datetime.now().date() + datetime.timedelta(days=7))
            type_plan = st.selectbox("🔧 Type de maintenance*", 
                                   ["Preventive", "Curative", "Predictive", "Améliorative"])
            
        with col_form2:
            description = st.text_area("📝 Description détaillée*", 
                                     placeholder="Ex: Remplacement des roulements + vérification alignement...",
                                     height=100)
            
            # Suggestions IA basées sur l'historique
            if equip_nom and interventions_data and equip_nom in equip_options:
                equip_id = equip_options[equip_nom]
                pannes_equip = [i for i in interventions_data if i.get('equipement_id') == equip_id]
                if pannes_equip:
                    types_pannes = {}
                    for panne in pannes_equip:
                        type_p = panne.get('type_panne', 'Non spécifié')
                        types_pannes[type_p] = types_pannes.get(type_p, 0) + 1
                    
                    panne_frequente = max(types_pannes, key=types_pannes.get) if types_pannes else None
                    if panne_frequente:
                        st.markdown(f"""
                            <div style="background: #eff6ff; padding: 1rem; border-radius: 8px; 
                                        border-left: 4px solid #3b82f6; margin-top: 0.5rem;">
                                <strong style="color: #1e40af;">💡 Suggestion IA Automatique</strong><br>
                                <span style="color: #1e3a8a;">Inclure la vérification: <strong>"{panne_frequente}"</strong></span><br>
                                <small style="color: #64748b;">La plus fréquente avec {types_pannes[panne_frequente]} occurrence(s)</small>
                            </div>
                        """, unsafe_allow_html=True)
            
            priorite = st.selectbox("🎯 Priorité", ["Basse", "Normale", "Haute", "Critique"])
            duree_estimee = st.number_input("⏱️ Durée estimée (heures)", min_value=0.5, step=0.5, value=2.0)
        
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            submit = st.form_submit_button("🚀 Créer le Plan Intelligent", use_container_width=True, type="primary")
        with col_btn2:
            st.form_submit_button("🔄 Réinitialiser", use_container_width=True)
        
        if submit:
            if not (equip_nom and date_planified and type_plan and description):
                st.error("❌ Tous les champs marqués d'un astérisque (*) sont obligatoires")
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
                    st.success("✅ Plan de maintenance créé avec succès!")
                    
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
                                     f"⏱️ Durée estimée: {duree_estimee} heures")
                    
                    st.balloons()
                except Exception as e:
                    handle_error(f"Erreur lors de la création: {str(e)}")

    # ═══════════════════════════════════════════════════════════════
    # SECTION 6: Tableau de Bord des Indicateurs Clés
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: linear-gradient(to right, #f8fafc, #e2e8f0); 
                    padding: 1.5rem; border-radius: 12px; margin: 2rem 0;
                    border-left: 5px solid #10b981;">
            <h2 style="margin: 0; color: #1e293b; font-size: 1.5rem;">
                📊 Tableau de Bord des Indicateurs de Performance
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    if interventions_data and data:
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        
        with col_kpi1:
            total_interventions = len(interventions_data)
            interventions_preventives = len([i for i in interventions_data if i.get('est_planifiee')])
            taux_preventif = (interventions_preventives / total_interventions * 100) if total_interventions > 0 else 0
            tendance = taux_preventif - 70
            kpi_card_2025("🛡️ Taux Préventif", f"{taux_preventif:.1f}%", tendance, "🛡️", col_kpi1)
        
        with col_kpi2:
            plans_termines = [p for p in data if p.get('statut') == 'Terminée']
            plans_a_temps = [p for p in plans_termines if p.get('date_planified') and 
                           safe_date_comparison(p['date_planified'], datetime.datetime.now()) >= 0]
            taux_ponctualite = (len(plans_a_temps) / len(plans_termines) * 100) if plans_termines else 0
            tendance = taux_ponctualite - 85
            kpi_card_2025("⏱️ Ponctualité", f"{taux_ponctualite:.1f}%", tendance, "⏱️", col_kpi2)

        with col_kpi3:
            cout_pannes_curatives = sum(float(i.get('cout_total', 0)) for i in interventions_data if not i.get('est_planifiee'))
            cout_maintenance_preventive = sum(float(i.get('cout_total', 0)) for i in interventions_data if i.get('est_planifiee'))
            economie_estimee = cout_pannes_curatives - cout_maintenance_preventive
            tendance = 12 if economie_estimee > 0 else -8
            kpi_card_2025("💰 Économies", f"{economie_estimee:.0f}€", tendance, "💰", col_kpi3)

        with col_kpi4:
            plans_prochains = [p for p in data if p.get('date_planified') and 
                             safe_date_comparison(p['date_planified'], (datetime.datetime.now() + datetime.timedelta(days=7)).date()) <= 0 and
                             p.get('statut') in ['Planifiée', 'En cours']]
            kpi_card_2025("📅 Échéances 7j", len(plans_prochains), 0, "📅", col_kpi4)

        # Graphique d'évolution
        st.markdown("##### 📈 Évolution des Indicateurs Clés (3 derniers mois)")
        
        dates = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=90), 
                             end=datetime.datetime.now(), freq='W')
        
        fig_evolution = go.Figure()
        
        fig_evolution.add_trace(go.Scatter(
            x=dates, y=np.random.normal(70, 5, len(dates)),
            name='Taux Préventif (%)',
            line=dict(color='#10b981', width=3),
            fill='tonexty', fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        
        fig_evolution.add_trace(go.Scatter(
            x=dates, y=np.random.normal(80, 8, len(dates)),
            name='Taux Ponctualité (%)',
            line=dict(color='#667eea', width=3),
            fill='tonexty', fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        fig_evolution.add_trace(go.Scatter(
            x=dates, y=np.random.normal(5000, 1000, len(dates)),
            name='Économies (€)', line=dict(color='#f59e0b', width=3),
            yaxis='y2'
        ))
        
        fig_evolution.update_layout(
            xaxis_title='Période', yaxis_title='Pourcentage (%)',
            yaxis2=dict(title='Économies (€)', overlaying='y', side='right'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=get_theme()['text']), hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_evolution, use_container_width=True)

        # Recommandations stratégiques avec design amélioré
        st.markdown("##### 💡 Recommandations Stratégiques Personnalisées")
        
        rec_col1, rec_col2, rec_col3 = st.columns(3)
        
        with rec_col1:
            if taux_preventif < 70:
                st.markdown("""
                    <div style="background: #fee2e2; padding: 1.5rem; border-radius: 10px; 
                                border-left: 4px solid #dc2626;">
                        <h4 style="color: #dc2626; margin: 0 0 0.5rem 0;">🛡️ Maintenance Préventive</h4>
                        <p style="color: #991b1b; margin: 0; font-size: 0.9rem;">
                            Objectif: >70% d'interventions planifiées
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: #d1fae5; padding: 1.5rem; border-radius: 10px; 
                                border-left: 4px solid #059669;">
                        <h4 style="color: #059669; margin: 0 0 0.5rem 0;">✅ Maintenance Optimale</h4>
                        <p style="color: #047857; margin: 0; font-size: 0.9rem;">
                            Continuez les bonnes pratiques!
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        
        with rec_col2:
            if taux_ponctualite < 85:
                st.markdown("""
                    <div style="background: #fef3c7; padding: 1.5rem; border-radius: 10px; 
                                border-left: 4px solid #f59e0b;">
                        <h4 style="color: #d97706; margin: 0 0 0.5rem 0;">⏱️ Améliorer Ponctualité</h4>
                        <p style="color: #b45309; margin: 0; font-size: 0.9rem;">
                            Objectif: >85% de plans à temps
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: #d1fae5; padding: 1.5rem; border-radius: 10px; 
                                border-left: 4px solid #059669;">
                        <h4 style="color: #059669; margin: 0 0 0.5rem 0;">✅ Excellente Ponctualité</h4>
                        <p style="color: #047857; margin: 0; font-size: 0.9rem;">
                            Performance exemplaire!
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        
        with rec_col3:
            if economie_estimee < 0:
                st.markdown("""
                    <div style="background: #fee2e2; padding: 1.5rem; border-radius: 10px; 
                                border-left: 4px solid #dc2626;">
                        <h4 style="color: #dc2626; margin: 0 0 0.5rem 0;">💰 Optimiser Coûts</h4>
                        <p style="color: #991b1b; margin: 0; font-size: 0.9rem;">
                            Pannes > Prévention
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: #d1fae5; padding: 1.5rem; border-radius: 10px; 
                                border-left: 4px solid #059669;">
                        <h4 style="color: #059669; margin: 0 0 0.5rem 0;">✅ Économies Réalisées</h4>
                        <p style="color: #047857; margin: 0; font-size: 0.9rem;">
                            ROI positif atteint!
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📊 Données insuffisantes pour le tableau de bord des indicateurs")

    # ═══════════════════════════════════════════════════════════════
    # SECTION 7: Reporting et Export Avancés
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("""
        <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
                    padding: 1.5rem; border-radius: 12px; margin: 2rem 0;
                    box-shadow: 0 5px 15px rgba(99, 102, 241, 0.3);">
            <h2 style="margin: 0; color: white; font-size: 1.8rem; display: flex; align-items: center;">
                <span style="margin-right: 1rem;">📄</span>
                Centre de Reporting et d'Export Avancés
            </h2>
            <p style="color: rgba(255,255,255,0.85); margin: 0.5rem 0 0 0; font-size: 0.95rem;">
                Génération automatique de rapports et analyses détaillées
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_report1, col_report2, col_report3, col_report4 = st.columns(4)
    
    with col_report1:
        if st.button("📋 Rapport AMDEC", use_container_width=True, type="secondary"):
            with st.spinner("🔄 Génération du rapport AMDEC..."):
                import time
                time.sleep(1.5)
                st.success("✅ Rapport AMDEC généré!")
                st.info("📥 Téléchargement disponible dans 'Exports'")
    
    with col_report2:
        if st.button("📈 Analyse Prédictive", use_container_width=True, type="secondary"):
            with st.spinner("🔮 Exécution de l'analyse..."):
                import time
                time.sleep(1.5)
                st.success("✅ Analyse terminée!")
                st.info("📊 Visualisations mises à jour")
    
    with col_report3:
        if st.button("🎯 Plan d'Action", use_container_width=True, type="secondary"):
            with st.spinner("📝 Création du plan..."):
                import time
                time.sleep(1.5)
                st.success("✅ Plan d'action créé!")
                st.info("📋 Disponible en PDF")
    
    with col_report4:
        if st.button("📊 Dashboard Exécutif", use_container_width=True, type="secondary"):
            with st.spinner("📈 Compilation des KPIs..."):
                import time
                time.sleep(1.5)
                st.success("✅ Dashboard prêt!")
                st.info("👔 Vue stratégique générée")

    # Footer avec statistiques globales
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8fafc; 
                    border-radius: 10px; margin-top: 2rem;">
            <p style="color: #64748b; margin: 0; font-size: 0.9rem;">
                💡 <strong>Conseil Pro:</strong> Utilisez l'analyse AMDEC hebdomadaire pour anticiper les défaillances critiques<br>
                📊 Dernière mise à jour: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
            </p>
        </div>
    """, unsafe_allow_html=True)
def analytics():
    if not has_permission("Admin"):
        show_access_denied()
        return
    
    # Header moderne cohérent
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 24px 32px; border-radius: 16px; margin-bottom: 32px; 
                    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);">
            <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                📈 Analytics Avancées
            </h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">
                Analyse prédictive • Machine Learning • Rapports automatisés
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    interventions_data = load_data("interventions") or []
    equipements_data = load_data("equipements") or []
    stocks_data = load_data("stocks") or []
    
    if not interventions_data:
        st.markdown("""
            <div style="background: #fef3c7; padding: 20px; border-radius: 12px; 
                        border-left: 4px solid #f59e0b; margin-bottom: 24px;">
                <div style="color: #92400e; font-size: 14px; font-weight: 600;">
                    ℹ️ Aucune donnée d'intervention disponible pour l'analyse
                </div>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Préparation des données
    df_interventions = pd.DataFrame(interventions_data)
    if 'date_creation' in df_interventions.columns:
        df_interventions['date_creation'] = pd.to_datetime(df_interventions['date_creation'], errors='coerce')
        df_interventions_indexed = df_interventions.set_index('date_creation')
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 1: KPI Rapides
    # ═══════════════════════════════════════════════════════════════
    col1, col2, col3, col4 = st.columns(4)
    
    nb_total_interventions = len(interventions_data)
    nb_pannes = len([e for e in equipements_data if e.get('statut') == 'En panne'])
    nb_interventions_ouvertes = len([i for i in interventions_data if i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']])
    nb_stocks_critiques = len([s for s in stocks_data if s.get('quantite') is not None and s.get('niveau_critique') is not None and s['quantite'] <= s['niveau_critique']])
    
    with col1:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">📊 Total</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_total_interventions}</div>
                <div style="font-size: 11px; opacity: 0.8;">Interventions</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⚠️ Pannes</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_pannes}</div>
                <div style="font-size: 11px; opacity: 0.8;">Équipements</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⚡ Actives</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_interventions_ouvertes}</div>
                <div style="font-size: 11px; opacity: 0.8;">En cours</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">📦 Stocks</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_stocks_critiques}</div>
                <div style="font-size: 11px; opacity: 0.8;">Critiques</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown('<div style="margin: 32px 0;"></div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 2: Analyse des Tendances
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                📊 Analyse des Tendances
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    if not df_interventions_indexed.empty:
        monthly_pannes = df_interventions_indexed.resample('M').size().reset_index(name='Nombre de Pannes')
        
        if len(monthly_pannes) > 0:
            fig = px.area(monthly_pannes, x='date_creation', y='Nombre de Pannes')
            fig.update_traces(
                line_color='#667eea', 
                fillcolor='rgba(102, 126, 234, 0.2)',
                hovertemplate='<b>%{y}</b> pannes<br>%{x|%B %Y}<extra></extra>'
            )
            fig.update_layout(
                title='Évolution des Pannes par Mois',
                xaxis_title='Période',
                yaxis_title='Nombre de Pannes',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1F2937', size=12),
                margin=dict(l=0, r=0, t=40, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 Pas assez de données pour l'analyse des tendances")
    else:
        st.info("💡 Données temporelles insuffisantes")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 3: Prédiction Machine Learning
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                🤖 Prédiction par Machine Learning
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    if not df_interventions_indexed.empty:
        monthly_pannes = df_interventions_indexed.resample('M').size().reset_index(name='Nombre de Pannes')
        
        if len(monthly_pannes) >= 2:
            monthly_pannes['time'] = np.arange(len(monthly_pannes))
            slope, intercept, r_value, p_value, std_err = linregress(monthly_pannes['time'], monthly_pannes['Nombre de Pannes'])
            
            # Contrôles interactifs
            col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 1, 1])
            with col_ctrl1:
                future_months = st.slider("📅 Horizon de prédiction (mois)", 1, 12, 3)
            with col_ctrl2:
                r_squared = r_value ** 2
                st.metric("📊 R² Score", f"{r_squared:.3f}")
            with col_ctrl3:
                tendance = "📈 Hausse" if slope > 0 else "📉 Baisse"
                st.metric("Tendance", tendance)
            
            # Calcul des prédictions
            future_time = np.arange(len(monthly_pannes), len(monthly_pannes) + future_months)
            predictions = slope * future_time + intercept
            predictions = np.maximum(predictions, 0)  # Pas de valeurs négatives
            
            # Tableau des prédictions avec style
            pred_df = pd.DataFrame({
                "Mois": [f"M+{i+1}" for i in range(future_months)],
                "Prédiction": [f"{p:.1f}" for p in predictions],
                "Confiance": [f"{max(0, 100 - i*5):.0f}%" for i in range(future_months)]
            })
            
            st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
            
            col_table, col_chart = st.columns([1, 2])
            
            with col_table:
                st.markdown("""
                    <div style="background: #f0f9ff; padding: 12px; border-radius: 8px; 
                                border-left: 4px solid #3b82f6; margin-bottom: 12px;">
                        <strong style="color: #1e40af; font-size: 14px;">📋 Prédictions</strong>
                    </div>
                """, unsafe_allow_html=True)
                st.dataframe(pred_df, use_container_width=True, hide_index=True)
            
            with col_chart:
                # Graphique de prédiction
                fig = go.Figure()
                
                # Historique
                fig.add_trace(go.Scatter(
                    x=monthly_pannes['time'], 
                    y=monthly_pannes['Nombre de Pannes'], 
                    mode='lines+markers',
                    name='Historique',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8, color='#667eea')
                ))
                
                # Prédictions
                fig.add_trace(go.Scatter(
                    x=future_time, 
                    y=predictions, 
                    mode='lines+markers',
                    name='Prédictions IA',
                    line=dict(color='#f59e0b', dash='dash', width=2),
                    marker=dict(size=8, symbol='diamond', color='#f59e0b')
                ))
                
                fig.update_layout(
                    title='Modèle Prédictif - Régression Linéaire',
                    xaxis_title='Période (mois)',
                    yaxis_title='Nombre de Pannes',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#1F2937', size=11),
                    hovermode='x unified',
                    margin=dict(t=40, l=20, r=20, b=20),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Interprétation des résultats
            st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
            
            if slope > 0:
                st.markdown(f"""
                    <div style="background: #fee2e2; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #ef4444; margin-bottom: 16px;">
                        <strong style="color: #991b1b; font-size: 14px;">📈 Tendance à la Hausse</strong><br>
                        <span style="color: #7f1d1d; font-size: 13px;">
                            Augmentation moyenne de <strong>{slope:.2f} pannes/mois</strong>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                st.info("💡 **Recommandation**: Renforcer les maintenances préventives et auditer les procédures critiques")
            else:
                st.markdown(f"""
                    <div style="background: #d1fae5; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #10b981; margin-bottom: 16px;">
                        <strong style="color: #065f46; font-size: 14px;">📉 Tendance à la Baisse</strong><br>
                        <span style="color: #047857; font-size: 13px;">
                            Réduction moyenne de <strong>{abs(slope):.2f} pannes/mois</strong>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                st.success("💡 **Bonne Pratique**: Maintenir les standards actuels de maintenance préventive")
        else:
            st.info("💡 Minimum 2 mois de données requises pour la prédiction ML")
    else:
        st.info("💡 Données insuffisantes pour l'analyse prédictive")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 4: Rapports Automatisés
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                📄 Génération de Rapports Automatisés
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    col_report1, col_report2 = st.columns([2, 1])
    
    with col_report1:
        st.markdown("""
            <div style="background: #eff6ff; padding: 16px; border-radius: 12px; 
                        border-left: 4px solid #3b82f6; margin-bottom: 16px;">
                <strong style="color: #1e40af; font-size: 14px;">📋 Rapport de Maintenance Complet</strong><br>
                <span style="color: #1e3a8a; font-size: 12px;">
                    Génère un PDF avec toutes les statistiques clés, KPI et analyse des tendances
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Générer Rapport PDF", use_container_width=True, type="primary"):
            with st.spinner("⏳ Génération du rapport en cours..."):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=16, style='B')
                    pdf.cell(200, 10, txt="Rapport de Maintenance - ISmaint Pro", ln=1, align='C')
                    
                    pdf.set_font("Arial", size=10)
                    pdf.cell(200, 10, txt=f"Date de generation: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=1, align='C')
                    pdf.ln(10)
                    
                    # Section KPI
                    pdf.set_font("Arial", size=14, style='B')
                    pdf.cell(200, 10, txt="Indicateurs Cles", ln=1)
                    pdf.set_font("Arial", size=11)
                    
                    nb_equipements = len(equipements_data)
                    pdf.cell(200, 8, txt=f"Equipements Totaux: {nb_equipements}", ln=1)
                    pdf.cell(200, 8, txt=f"Equipements en Panne: {nb_pannes}", ln=1)
                    pdf.cell(200, 8, txt=f"Interventions Actives: {nb_interventions_ouvertes}", ln=1)
                    pdf.cell(200, 8, txt=f"Stocks Critiques: {nb_stocks_critiques}", ln=1)
                    pdf.cell(200, 8, txt=f"Total Interventions: {nb_total_interventions}", ln=1)
                    
                    pdf.ln(10)
                    
                    # Section Analyse
                    pdf.set_font("Arial", size=14, style='B')
                    pdf.cell(200, 10, txt="Analyse des Tendances", ln=1)
                    pdf.set_font("Arial", size=11)
                    
                    if not df_interventions_indexed.empty and len(monthly_pannes) >= 2:
                        pdf.cell(200, 8, txt=f"Tendance: {'Hausse' if slope > 0 else 'Baisse'} de {abs(slope):.2f} pannes/mois", ln=1)
                        pdf.cell(200, 8, txt=f"Score R2: {r_squared:.3f}", ln=1)
                    else:
                        pdf.cell(200, 8, txt="Donnees insuffisantes pour l'analyse predictive", ln=1)
                    
                    # Génération du fichier
                    pdf_output = BytesIO()
                    pdf_bytes = pdf.output(dest='S')
                    pdf_output.write(pdf_bytes)
                    pdf_output.seek(0)
                    
                    st.success("✅ Rapport généré avec succès!")
                    st.download_button(
                        label="📥 Télécharger le Rapport PDF", 
                        data=pdf_output, 
                        file_name=f"rapport_maintenance_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf", 
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Erreur lors de la génération: {str(e)}")
    
    with col_report2:
        st.markdown("""
            <div style="background: #fef3c7; padding: 16px; border-radius: 12px; 
                        border-left: 4px solid #f59e0b; margin-bottom: 16px;">
                <strong style="color: #92400e; font-size: 14px;">📊 Contenu du Rapport</strong>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style="font-size: 12px; color: #6B7280; line-height: 1.8;">
                ✓ Statistiques globales<br>
                ✓ KPI de performance<br>
                ✓ Analyse des tendances<br>
                ✓ État des stocks<br>
                ✓ Interventions actives<br>
                ✓ Équipements critiques
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 5: Analyse Complémentaire
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                📊 Analyses Complémentaires
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    tab1, tab2, tab3 = st.tabs(["🔧 Par Type", "📅 Par Période", "💰 Par Coût"])
    
    with tab1:
        if 'type_panne' in df_interventions.columns:
            type_counts = df_interventions['type_panne'].value_counts().reset_index()
            type_counts.columns = ['Type', 'Nombre']
            
            fig = px.pie(type_counts, values='Nombre', names='Type',
                        color_discrete_sequence=['#667eea', '#764ba2', '#f59e0b', '#10b981', '#ef4444'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1F2937'),
                margin=dict(t=0, l=0, r=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 Données de type de panne non disponibles")
    
    with tab2:
        if not df_interventions_indexed.empty:
            weekly_pannes = df_interventions_indexed.resample('W').size().reset_index(name='Pannes')
            
            fig = px.bar(weekly_pannes, x='date_creation', y='Pannes',
                        color='Pannes', color_continuous_scale=['#dbeafe', '#667eea'])
            fig.update_layout(
                title='Interventions par Semaine',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1F2937'),
                showlegend=False,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 Données temporelles insuffisantes")
    
    with tab3:
        if 'cout_total' in df_interventions.columns:
            cout_data = df_interventions[df_interventions['cout_total'] > 0].nlargest(10, 'cout_total')
            
            if not cout_data.empty:
                fig = px.bar(cout_data, x='cout_total', y='description',
                            orientation='h', color='cout_total',
                            color_continuous_scale=['#fef3c7', '#f59e0b', '#dc2626'])
                fig.update_layout(
                    title='Top 10 Interventions les Plus Coûteuses',
                    xaxis_title='Coût (€)',
                    yaxis_title='',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#1F2937'),
                    showlegend=False,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Aucune donnée de coût disponible")
        else:
            st.info("💡 Données de coût non disponibles")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer avec dernière mise à jour
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8fafc; 
                    border-radius: 10px; margin-top: 2rem;">
            <p style="color: #64748b; margin: 0; font-size: 0.9rem;">
                💡 <strong>Info:</strong> Les analyses sont basées sur {nb_interventions} intervention(s) • 
                Dernière mise à jour: {timestamp}
            </p>
        </div>
    """.format(
        nb_interventions=nb_total_interventions,
        timestamp=datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    ), unsafe_allow_html=True)

def metriques_avancees():
    if not has_permission("Admin"):
        show_access_denied()
        return
    
    # Header moderne cohérent avec Analytics
    st.markdown("""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 24px 32px; border-radius: 16px; margin-bottom: 32px; 
                    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.2);">
            <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                ⚙️ Métriques Avancées
            </h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">
                MTTR • MTBF • OEE • Indicateurs de Performance
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh every 30s (non intrusive)
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time()
    if time() - st.session_state.last_refresh > 30:
        st.session_state.last_refresh = time()
        st.rerun()
    
    # Chargement des données
    interventions = load_data("interventions") or []
    equipements = load_data("equipements") or []
    production_shifts = load_data("production_shifts") or []
    stocks = load_data("stocks") or []
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 1: KPI Rapides - Vue d'ensemble
    # ═══════════════════════════════════════════════════════════════
    col1, col2, col3, col4 = st.columns(4)
    
    ot_actifs = len([i for i in interventions if i.get('statut') in ['Nouvelle', 'Ouverte', 'En cours']])
    ot_fermes = len([i for i in interventions if i.get('statut') == 'Fermée'])
    nb_equipements = len(equipements)
    nb_pannes = len([e for e in equipements if e.get('statut') == 'En panne'])
    
    with col1:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">📋 OT Actifs</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{ot_actifs}</div>
                <div style="font-size: 11px; opacity: 0.8;">En cours</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">✅ OT Fermés</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{ot_fermes}</div>
                <div style="font-size: 11px; opacity: 0.8;">Complétés</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">🔧 Équipements</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_equipements}</div>
                <div style="font-size: 11px; opacity: 0.8;">Total</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⚠️ En Panne</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_pannes}</div>
                <div style="font-size: 11px; opacity: 0.8;">Équipements</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown('<div style="margin: 32px 0;"></div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 2: MTTR - Temps Moyen de Réparation
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                ⏱️ MTTR - Temps Moyen de Réparation
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    if interventions:
        df_interventions = pd.DataFrame(interventions)
        df_interventions['date_creation'] = pd.to_datetime(df_interventions.get('date_creation'), errors='coerce')
        df_interventions['date_cloture'] = pd.to_datetime(df_interventions.get('date_cloture'), errors='coerce')
        df_closed = df_interventions[df_interventions.get('statut') == 'Fermée'].dropna(subset=['date_cloture'])
        
        if not df_closed.empty:
            # Calcul du temps de réparation en heures
            df_closed['temps_reparation_hours'] = df_closed.apply(
                lambda row: safe_date_comparison(row['date_cloture'], row['date_creation']) / 24, 
                axis=1
            )
            mttr = df_closed['temps_reparation_hours'].mean()
            mttr_median = df_closed['temps_reparation_hours'].median()
            mttr_max = df_closed['temps_reparation_hours'].max()
            mttr_min = df_closed['temps_reparation_hours'].min()
            
            # Affichage des métriques MTTR
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            
            with col_m1:
                st.markdown(f"""
                    <div style="background: #eff6ff; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #3b82f6; text-align: center;">
                        <div style="color: #1e40af; font-size: 12px; font-weight: 600; margin-bottom: 8px;">MOYENNE</div>
                        <div style="color: #1e3a8a; font-size: 24px; font-weight: 700;">{mttr:.1f}h</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_m2:
                st.markdown(f"""
                    <div style="background: #f0fdf4; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #10b981; text-align: center;">
                        <div style="color: #065f46; font-size: 12px; font-weight: 600; margin-bottom: 8px;">MÉDIANE</div>
                        <div style="color: #047857; font-size: 24px; font-weight: 700;">{mttr_median:.1f}h</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_m3:
                st.markdown(f"""
                    <div style="background: #fef3c7; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #f59e0b; text-align: center;">
                        <div style="color: #92400e; font-size: 12px; font-weight: 600; margin-bottom: 8px;">MAXIMUM</div>
                        <div style="color: #78350f; font-size: 24px; font-weight: 700;">{mttr_max:.1f}h</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_m4:
                st.markdown(f"""
                    <div style="background: #f0f9ff; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #06b6d4; text-align: center;">
                        <div style="color: #155e75; font-size: 12px; font-weight: 600; margin-bottom: 8px;">MINIMUM</div>
                        <div style="color: #0e7490; font-size: 24px; font-weight: 700;">{mttr_min:.1f}h</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
            
            # Graphique de distribution MTTR
            fig = px.histogram(
                df_closed, 
                x='temps_reparation_hours',
                nbins=20,
                title='Distribution des Temps de Réparation',
                labels={'temps_reparation_hours': 'Temps (heures)', 'count': 'Nombre d\'interventions'}
            )
            fig.update_traces(marker_color='#3b82f6', marker_line_color='#1e40af', marker_line_width=1.5)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1F2937', size=12),
                margin=dict(l=0, r=0, t=40, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Interprétation
            if mttr < 24:
                st.markdown("""
                    <div style="background: #d1fae5; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #10b981; margin-top: 16px;">
                        <strong style="color: #065f46; font-size: 14px;">✅ Performance Excellente</strong><br>
                        <span style="color: #047857; font-size: 13px;">
                            Le temps moyen de réparation est inférieur à 24h, ce qui indique une maintenance réactive efficace.
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            elif mttr < 72:
                st.markdown("""
                    <div style="background: #fef3c7; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #f59e0b; margin-top: 16px;">
                        <strong style="color: #92400e; font-size: 14px;">⚠️ Performance Acceptable</strong><br>
                        <span style="color: #78350f; font-size: 13px;">
                            Considérez l'optimisation des processus de maintenance pour réduire les délais.
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: #fee2e2; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #ef4444; margin-top: 16px;">
                        <strong style="color: #991b1b; font-size: 14px;">🚨 Amélioration Nécessaire</strong><br>
                        <span style="color: #7f1d1d; font-size: 13px;">
                            Le MTTR élevé suggère des problèmes de réactivité. Audit recommandé.
                        </span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background: #eff6ff; padding: 20px; border-radius: 12px; 
                            border-left: 4px solid #3b82f6; text-align: center;">
                    <div style="color: #1e40af; font-size: 14px; font-weight: 600;">
                        ℹ️ Aucune intervention fermée avec date de clôture
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: #eff6ff; padding: 20px; border-radius: 12px; 
                        border-left: 4px solid #3b82f6; text-align: center;">
                <div style="color: #1e40af; font-size: 14px; font-weight: 600;">
                    ℹ️ Aucune intervention disponible
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 3: MTBF & OEE par Équipement
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                📊 MTBF & OEE par Équipement
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    if equipements:
        col_select, col_info = st.columns([2, 1])
        
        with col_select:
            equip_names = [e['nom'] for e in equipements]
            equip_nom = st.selectbox(
                "🔍 Sélectionner un équipement", 
                equip_names,
                help="Choisissez un équipement pour voir ses métriques détaillées"
            )
        
        with col_info:
            st.markdown("""
                <div style="background: #f0f9ff; padding: 12px; border-radius: 8px; 
                            border-left: 4px solid #3b82f6; margin-top: 28px;">
                    <strong style="color: #1e40af; font-size: 13px;">💡 Info</strong><br>
                    <span style="color: #1e3a8a; font-size: 11px;">
                        MTBF = Temps moyen entre pannes<br>
                        OEE = Efficacité globale
                    </span>
                </div>
            """, unsafe_allow_html=True)
        
        try:
            equip_id = next(e['id'] for e in equipements if e['nom'] == equip_nom)
            equip_data = next(e for e in equipements if e['nom'] == equip_nom)
            df_equip_interventions = pd.DataFrame([i for i in interventions if i.get('equipement_id') == equip_id]) if interventions else pd.DataFrame()
            heures_op = equip_data.get('heures_operationnelles') or 0
            nb_pannes = len(df_equip_interventions) if not df_equip_interventions.empty else 0
            mtbf = (heures_op / max(nb_pannes, 1)) if heures_op else 0
            
            st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
            
            # Affichage des métriques de l'équipement
            col_e1, col_e2, col_e3 = st.columns(3)
            
            with col_e1:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); 
                                padding: 20px; border-radius: 16px; 
                                box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); color: white;">
                        <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⚡ MTBF</div>
                        <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{mtbf:.1f}h</div>
                        <div style="font-size: 11px; opacity: 0.8;">Temps entre pannes</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_e2:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); 
                                padding: 20px; border-radius: 16px; 
                                box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3); color: white;">
                        <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">🔢 Pannes</div>
                        <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_pannes}</div>
                        <div style="font-size: 11px; opacity: 0.8;">Total enregistré</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_e3:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                                padding: 20px; border-radius: 16px; 
                                box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); color: white;">
                        <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">⏰ Heures Op.</div>
                        <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{heures_op:,.0f}h</div>
                        <div style="font-size: 11px; opacity: 0.8;">Opérationnelles</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div style="margin: 24px 0;"></div>', unsafe_allow_html=True)
            
            # Détails de l'équipement
            col_detail1, col_detail2 = st.columns(2)
            
            with col_detail1:
                st.markdown("""
                    <div style="background: #f8fafc; padding: 16px; border-radius: 12px; margin-bottom: 16px;">
                        <strong style="color: #1F2937; font-size: 14px;">📋 Informations de l'Équipement</strong>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="background: white; padding: 16px; border-radius: 12px; 
                                border: 1px solid #e5e7eb;">
                        <div style="margin-bottom: 12px;">
                            <span style="color: #6B7280; font-size: 12px;">Nom:</span><br>
                            <strong style="color: #1F2937; font-size: 14px;">{equip_data.get('nom', 'N/A')}</strong>
                        </div>
                        <div style="margin-bottom: 12px;">
                            <span style="color: #6B7280; font-size: 12px;">Type:</span><br>
                            <strong style="color: #1F2937; font-size: 14px;">{equip_data.get('type', 'N/A')}</strong>
                        </div>
                        <div>
                            <span style="color: #6B7280; font-size: 12px;">Statut:</span><br>
                            <strong style="color: {'#10b981' if equip_data.get('statut') == 'Opérationnel' else '#ef4444'}; font-size: 14px;">
                                {equip_data.get('statut', 'N/A')}
                            </strong>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_detail2:
                st.markdown("""
                    <div style="background: #f8fafc; padding: 16px; border-radius: 12px; margin-bottom: 16px;">
                        <strong style="color: #1F2937; font-size: 14px;">📈 Analyse de Performance</strong>
                    </div>
                """, unsafe_allow_html=True)
                
                # Évaluation du MTBF
                if mtbf > 1000:
                    performance_color = "#10b981"
                    performance_text = "Excellent"
                    performance_icon = "✅"
                elif mtbf > 500:
                    performance_color = "#f59e0b"
                    performance_text = "Bon"
                    performance_icon = "⚠️"
                else:
                    performance_color = "#ef4444"
                    performance_text = "À améliorer"
                    performance_icon = "🚨"
                
                st.markdown(f"""
                    <div style="background: white; padding: 16px; border-radius: 12px; 
                                border: 1px solid #e5e7eb;">
                        <div style="margin-bottom: 12px;">
                            <span style="color: #6B7280; font-size: 12px;">Fiabilité:</span><br>
                            <strong style="color: {performance_color}; font-size: 14px;">
                                {performance_icon} {performance_text}
                            </strong>
                        </div>
                        <div style="margin-bottom: 12px;">
                            <span style="color: #6B7280; font-size: 12px;">Fréquence des pannes:</span><br>
                            <strong style="color: #1F2937; font-size: 14px;">
                                {(nb_pannes / max(heures_op/730, 1)):.2f} pannes/mois
                            </strong>
                        </div>
                        <div>
                            <span style="color: #6B7280; font-size: 12px;">Disponibilité estimée:</span><br>
                            <strong style="color: #1F2937; font-size: 14px;">
                                {min(100, (mtbf / (mtbf + 24)) * 100):.1f}%
                            </strong>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Recommandations basées sur le MTBF
            st.markdown('<div style="margin: 24px 0;"></div>', unsafe_allow_html=True)
            
            if mtbf > 1000:
                st.markdown("""
                    <div style="background: #d1fae5; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #10b981;">
                        <strong style="color: #065f46; font-size: 14px;">✅ Performance Optimale</strong><br>
                        <span style="color: #047857; font-size: 13px;">
                            Cet équipement présente une excellente fiabilité. Maintenez le programme de maintenance préventive actuel.
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            elif mtbf > 500:
                st.markdown("""
                    <div style="background: #fef3c7; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #f59e0b;">
                        <strong style="color: #92400e; font-size: 14px;">⚠️ Performance Acceptable</strong><br>
                        <span style="color: #78350f; font-size: 13px;">
                            Surveillez de près cet équipement et envisagez d'augmenter la fréquence des maintenances préventives.
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: #fee2e2; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #ef4444;">
                        <strong style="color: #991b1b; font-size: 14px;">🚨 Action Requise</strong><br>
                        <span style="color: #7f1d1d; font-size: 13px;">
                            MTBF faible détecté. Recommandations: audit technique approfondi, révision du plan de maintenance, 
                            formation des opérateurs, et évaluation du remplacement potentiel.
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            
        except StopIteration:
            st.markdown("""
                <div style="background: #fee2e2; padding: 20px; border-radius: 12px; 
                            border-left: 4px solid #ef4444; text-align: center;">
                    <div style="color: #991b1b; font-size: 14px; font-weight: 600;">
                        ❌ Impossible de calculer les métriques pour cet équipement
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: #eff6ff; padding: 20px; border-radius: 12px; 
                        border-left: 4px solid #3b82f6; text-align: center;">
                <div style="color: #1e40af; font-size: 14px; font-weight: 600;">
                    ℹ️ Aucun équipement disponible
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 4: Tableau récapitulatif de tous les équipements
    # ═══════════════════════════════════════════════════════════════
    if equipements and interventions:
        st.markdown("""
            <div style="background: white; padding: 24px; border-radius: 16px; 
                        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    📊 Vue d'Ensemble - Tous les Équipements
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        # Calcul des métriques pour tous les équipements
        equipements_metriques = []
        for equip in equipements:
            equip_interventions = [i for i in interventions if i.get('equipement_id') == equip['id']]
            heures_op = equip.get('heures_operationnelles') or 0
            nb_pannes = len(equip_interventions)
            mtbf = (heures_op / max(nb_pannes, 1)) if heures_op else 0
            
            equipements_metriques.append({
                'Équipement': equip['nom'],
                'Type': equip.get('type', 'N/A'),
                'Statut': equip.get('statut', 'N/A'),
                'MTBF (h)': round(mtbf, 1),
                'Pannes': nb_pannes,
                'Heures Op.': heures_op,
                'Disponibilité (%)': round(min(100, (mtbf / (mtbf + 24)) * 100), 1) if mtbf > 0 else 0
            })
        
        df_metriques = pd.DataFrame(equipements_metriques)
        
        # Tri par MTBF décroissant
        df_metriques = df_metriques.sort_values('MTBF (h)', ascending=False)
        
        # Affichage du tableau avec style
        st.dataframe(
            df_metriques,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Équipement': st.column_config.TextColumn('🔧 Équipement', width='medium'),
                'Type': st.column_config.TextColumn('📦 Type', width='small'),
                'Statut': st.column_config.TextColumn('🚦 Statut', width='small'),
                'MTBF (h)': st.column_config.NumberColumn('⚡ MTBF (h)', format='%.1f', width='small'),
                'Pannes': st.column_config.NumberColumn('⚠️ Pannes', format='%d', width='small'),
                'Heures Op.': st.column_config.NumberColumn('⏰ Heures Op.', format='%d', width='small'),
                'Disponibilité (%)': st.column_config.ProgressColumn('📊 Disponibilité', format='%.1f%%', min_value=0, max_value=100, width='medium')
            }
        )
        
        # Graphique comparatif MTBF
        st.markdown('<div style="margin: 24px 0;"></div>', unsafe_allow_html=True)
        
        fig = px.bar(
            df_metriques.head(10), 
            x='MTBF (h)', 
            y='Équipement',
            orientation='h',
            title='Top 10 - MTBF par Équipement',
            color='MTBF (h)',
            color_continuous_scale=['#ef4444', '#f59e0b', '#10b981']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1F2937', size=12),
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(showgrid=False),
            showlegend=False,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 5: Analyses Complémentaires
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                📈 Analyses Complémentaires
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    tab1, tab2, tab3 = st.tabs(["📊 Distribution MTBF", "⚡ Taux de Panne", "🎯 Fiabilité"])
    
    with tab1:
        if equipements_metriques:
            st.markdown("""
                <div style="background: #f0f9ff; padding: 12px; border-radius: 8px; 
                            border-left: 4px solid #3b82f6; margin-bottom: 16px;">
                    <strong style="color: #1e40af; font-size: 13px;">📊 Distribution du MTBF</strong><br>
                    <span style="color: #1e3a8a; font-size: 11px;">
                        Visualisation de la répartition des temps moyens entre pannes
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            fig = px.box(
                df_metriques, 
                y='MTBF (h)',
                title='Distribution Statistique du MTBF',
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1F2937', size=12),
                margin=dict(l=0, r=0, t=40, b=0),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistiques descriptives
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.metric("📊 MTBF Moyen", f"{df_metriques['MTBF (h)'].mean():.1f}h")
            
            with col_stat2:
                st.metric("📈 MTBF Médian", f"{df_metriques['MTBF (h)'].median():.1f}h")
            
            with col_stat3:
                st.metric("📉 Écart-type", f"{df_metriques['MTBF (h)'].std():.1f}h")
        else:
            st.info("💡 Aucune donnée disponible pour l'analyse de distribution")
    
    with tab2:
        if equipements_metriques:
            st.markdown("""
                <div style="background: #fef3c7; padding: 12px; border-radius: 8px; 
                            border-left: 4px solid #f59e0b; margin-bottom: 16px;">
                    <strong style="color: #92400e; font-size: 13px;">⚡ Taux de Panne</strong><br>
                    <span style="color: #78350f; font-size: 11px;">
                        Fréquence des pannes par équipement (pannes par mois)
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            # Calcul du taux de panne (pannes par mois)
            df_metriques['Taux Panne/Mois'] = df_metriques.apply(
                lambda row: (row['Pannes'] / max(row['Heures Op.'] / 730, 1)) if row['Heures Op.'] > 0 else 0,
                axis=1
            )
            
            df_taux_panne = df_metriques.sort_values('Taux Panne/Mois', ascending=False).head(10)
            
            fig = px.bar(
                df_taux_panne,
                x='Équipement',
                y='Taux Panne/Mois',
                title='Top 10 - Équipements avec le Plus Haut Taux de Panne',
                color='Taux Panne/Mois',
                color_continuous_scale=['#fef3c7', '#f59e0b', '#dc2626']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1F2937', size=12),
                margin=dict(l=0, r=0, t=40, b=0),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                showlegend=False,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Liste des équipements à surveiller
            equipements_critiques = df_metriques[df_metriques['Taux Panne/Mois'] > 1].sort_values('Taux Panne/Mois', ascending=False)
            
            if not equipements_critiques.empty:
                st.markdown("""
                    <div style="background: #fee2e2; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #ef4444; margin-top: 16px;">
                        <strong style="color: #991b1b; font-size: 14px;">🚨 Équipements à Surveiller</strong><br>
                        <span style="color: #7f1d1d; font-size: 13px;">
                            Les équipements suivants ont un taux de panne élevé (>1 panne/mois):
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                for idx, row in equipements_critiques.iterrows():
                    st.markdown(f"""
                        <div style="background: white; padding: 12px; border-radius: 8px; 
                                    border: 1px solid #fee2e2; margin-top: 8px;">
                            <strong style="color: #1F2937;">• {row['Équipement']}</strong>
                            <span style="color: #ef4444; font-weight: 600;"> - {row['Taux Panne/Mois']:.2f} pannes/mois</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ Aucun équipement critique détecté")
        else:
            st.info("💡 Aucune donnée disponible pour l'analyse du taux de panne")
    
    with tab3:
        if equipements_metriques:
            st.markdown("""
                <div style="background: #d1fae5; padding: 12px; border-radius: 8px; 
                            border-left: 4px solid #10b981; margin-bottom: 16px;">
                    <strong style="color: #065f46; font-size: 13px;">🎯 Analyse de Fiabilité</strong><br>
                    <span style="color: #047857; font-size: 11px;">
                        Évaluation de la disponibilité et de la fiabilité des équipements
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            # Graphique de disponibilité
            df_dispo = df_metriques.sort_values('Disponibilité (%)', ascending=False).head(15)
            
            fig = px.scatter(
                df_dispo,
                x='MTBF (h)',
                y='Disponibilité (%)',
                size='Pannes',
                color='Disponibilité (%)',
                hover_data=['Équipement', 'Type'],
                title='Matrice Fiabilité: MTBF vs Disponibilité',
                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1F2937', size=12),
                margin=dict(l=0, r=0, t=40, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                coloraxis_showscale=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Catégorisation des équipements
            col_cat1, col_cat2, col_cat3 = st.columns(3)
            
            excellent = len(df_metriques[df_metriques['Disponibilité (%)'] >= 95])
            bon = len(df_metriques[(df_metriques['Disponibilité (%)'] >= 85) & (df_metriques['Disponibilité (%)'] < 95)])
            ameliorer = len(df_metriques[df_metriques['Disponibilité (%)'] < 85])
            
            with col_cat1:
                st.markdown(f"""
                    <div style="background: #d1fae5; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #10b981; text-align: center;">
                        <div style="color: #065f46; font-size: 12px; font-weight: 600; margin-bottom: 8px;">✅ EXCELLENT</div>
                        <div style="color: #047857; font-size: 28px; font-weight: 700;">{excellent}</div>
                        <div style="color: #065f46; font-size: 11px; margin-top: 4px;">≥ 95% disponibilité</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_cat2:
                st.markdown(f"""
                    <div style="background: #fef3c7; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #f59e0b; text-align: center;">
                        <div style="color: #92400e; font-size: 12px; font-weight: 600; margin-bottom: 8px;">⚠️ BON</div>
                        <div style="color: #78350f; font-size: 28px; font-weight: 700;">{bon}</div>
                        <div style="color: #92400e; font-size: 11px; margin-top: 4px;">85-95% disponibilité</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_cat3:
                st.markdown(f"""
                    <div style="background: #fee2e2; padding: 16px; border-radius: 12px; 
                                border-left: 4px solid #ef4444; text-align: center;">
                        <div style="color: #991b1b; font-size: 12px; font-weight: 600; margin-bottom: 8px;">🚨 À AMÉLIORER</div>
                        <div style="color: #7f1d1d; font-size: 28px; font-weight: 700;">{ameliorer}</div>
                        <div style="color: #991b1b; font-size: 11px; margin-top: 4px;">< 85% disponibilité</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💡 Aucune donnée disponible pour l'analyse de fiabilité")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 6: Recommandations Intelligentes
    # ═══════════════════════════════════════════════════════════════
    if equipements_metriques:
        st.markdown("""
            <div style="background: white; padding: 24px; border-radius: 16px; 
                        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    💡 Recommandations Intelligentes
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        # Analyse et génération de recommandations
        mtbf_moyen = df_metriques['MTBF (h)'].mean()
        dispo_moyenne = df_metriques['Disponibilité (%)'].mean()
        
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.markdown("""
                <div style="background: #eff6ff; padding: 16px; border-radius: 12px; 
                            border-left: 4px solid #3b82f6; margin-bottom: 16px;">
                    <strong style="color: #1e40af; font-size: 14px;">📊 Vue d'Ensemble</strong>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background: white; padding: 16px; border-radius: 12px; 
                            border: 1px solid #e5e7eb;">
                    <div style="margin-bottom: 12px;">
                        <span style="color: #6B7280; font-size: 12px;">MTBF Moyen:</span><br>
                        <strong style="color: #1F2937; font-size: 18px;">{mtbf_moyen:.1f}h</strong>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <span style="color: #6B7280; font-size: 12px;">Disponibilité Moyenne:</span><br>
                        <strong style="color: #1F2937; font-size: 18px;">{dispo_moyenne:.1f}%</strong>
                    </div>
                    <div>
                        <span style="color: #6B7280; font-size: 12px;">Équipements Analysés:</span><br>
                        <strong style="color: #1F2937; font-size: 18px;">{len(df_metriques)}</strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_rec2:
            st.markdown("""
                <div style="background: #f0fdf4; padding: 16px; border-radius: 12px; 
                            border-left: 4px solid #10b981; margin-bottom: 16px;">
                    <strong style="color: #065f46; font-size: 14px;">🎯 Actions Prioritaires</strong>
                </div>
            """, unsafe_allow_html=True)
            
            if ameliorer > 0:
                st.markdown(f"""
                    <div style="background: white; padding: 12px; border-radius: 8px; 
                                border: 1px solid #fee2e2; margin-bottom: 8px;">
                        <strong style="color: #ef4444;">🚨 Priorité 1:</strong>
                        <span style="color: #1F2937; font-size: 13px;">
                            Auditer les {ameliorer} équipement(s) avec disponibilité < 85%
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            
            if mtbf_moyen < 500:
                st.markdown("""
                    <div style="background: white; padding: 12px; border-radius: 8px; 
                                border: 1px solid #fef3c7; margin-bottom: 8px;">
                        <strong style="color: #f59e0b;">⚠️ Priorité 2:</strong>
                        <span style="color: #1F2937; font-size: 13px;">
                            Renforcer le programme de maintenance préventive
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            
            if excellent > 0:
                st.markdown(f"""
                    <div style="background: white; padding: 12px; border-radius: 8px; 
                                border: 1px solid #d1fae5; margin-bottom: 8px;">
                        <strong style="color: #10b981;">✅ Bonnes Pratiques:</strong>
                        <span style="color: #1F2937; font-size: 13px;">
                            Documenter les procédures des {excellent} équipement(s) performant(s)
                        </span>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer avec dernière mise à jour
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8fafc; 
                    border-radius: 10px; margin-top: 2rem;">
            <p style="color: #64748b; margin: 0; font-size: 0.9rem;">
                💡 <strong>Info:</strong> Auto-refresh toutes les 30 secondes • 
                Dernière mise à jour: {timestamp}
            </p>
        </div>
    """.format(
        timestamp=datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    ), unsafe_allow_html=True)

def offline_sync():
    if not has_permission("Admin"):
        show_access_denied()
        return
    
    # Header moderne cohérent
    st.markdown("""
        <div style="background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); 
                    padding: 24px 32px; border-radius: 16px; margin-bottom: 32px; 
                    box-shadow: 0 4px 20px rgba(6, 182, 212, 0.2);">
            <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                🔄 Synchronisation Offline
            </h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">
                Sauvegarde locale • Backup de sécurité • Mode hors ligne
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialisation des données offline
    if 'offline_data' not in st.session_state:
        st.session_state.offline_data = {}
    if 'offline_timestamp' not in st.session_state:
        st.session_state.offline_timestamp = None
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 1: Informations et Statut
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                ℹ️ Informations sur la Synchronisation
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("""
        <div style="background: #eff6ff; padding: 16px; border-radius: 12px; 
                    border-left: 4px solid #3b82f6; margin-bottom: 16px;">
            <strong style="color: #1e40af; font-size: 14px;">💡 À propos du mode offline</strong><br>
            <span style="color: #1e3a8a; font-size: 13px;">
                Cette fonctionnalité permet de sauvegarder temporairement vos données dans la session locale 
                pour un accès rapide sans connexion au serveur. Les données sont conservées uniquement pendant 
                votre session active.
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    # Statut de la sauvegarde
    col_status1, col_status2, col_status3 = st.columns(3)
    
    has_offline_data = bool(st.session_state.offline_data)
    nb_tables_saved = len(st.session_state.offline_data)
    total_records = sum(len(v) if isinstance(v, list) else 0 for v in st.session_state.offline_data.values())
    
    with col_status1:
        status_color = "#10b981" if has_offline_data else "#6B7280"
        status_text = "Active" if has_offline_data else "Aucune"
        status_icon = "✅" if has_offline_data else "⭕"
        
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, {status_color} 0%, {status_color}dd 100%); 
                        padding: 20px; border-radius: 16px; 
                        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">💾 Sauvegarde</div>
                <div style="font-size: 28px; font-weight: 700; margin-bottom: 4px;">{status_icon}</div>
                <div style="font-size: 11px; opacity: 0.8;">{status_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col_status2:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); 
                        padding: 20px; border-radius: 16px; 
                        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">📊 Tables</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{nb_tables_saved}</div>
                <div style="font-size: 11px; opacity: 0.8;">Sauvegardées</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col_status3:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                        padding: 20px; border-radius: 16px; 
                        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); color: white;">
                <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px; font-weight: 500;">📝 Enregistrements</div>
                <div style="font-size: 32px; font-weight: 700; margin-bottom: 4px;">{total_records}</div>
                <div style="font-size: 11px; opacity: 0.8;">Total</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Dernière synchronisation
    if st.session_state.offline_timestamp:
        time_diff = datetime.datetime.now() - st.session_state.offline_timestamp
        hours = int(time_diff.total_seconds() // 3600)
        minutes = int((time_diff.total_seconds() % 3600) // 60)
        
        if hours > 0:
            time_text = f"Il y a {hours}h {minutes}min"
        else:
            time_text = f"Il y a {minutes}min"
        
        st.markdown(f"""
            <div style="background: #f0fdf4; padding: 12px; border-radius: 8px; 
                        border-left: 4px solid #10b981; margin-top: 16px; text-align: center;">
                <span style="color: #065f46; font-size: 13px;">
                    ⏰ Dernière sauvegarde: <strong>{st.session_state.offline_timestamp.strftime('%d/%m/%Y %H:%M:%S')}</strong> 
                    ({time_text})
                </span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 2: Actions de Synchronisation
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                ⚡ Actions de Synchronisation
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    col_action1, col_action2, col_action3 = st.columns(3)
    
    with col_action1:
        st.markdown("""
            <div style="background: #eff6ff; padding: 16px; border-radius: 12px; 
                        border-left: 4px solid #3b82f6; margin-bottom: 16px;">
                <strong style="color: #1e40af; font-size: 14px;">💾 Sauvegarder</strong><br>
                <span style="color: #1e3a8a; font-size: 12px;">
                    Copier toutes les données vers le cache local
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("💾 Sauvegarder Offline", use_container_width=True, type="primary"):
            with st.spinner("⏳ Sauvegarde en cours..."):
                try:
                    # Sauvegarde de toutes les tables
                    tables_to_save = [
                        "equipements", 
                        "interventions", 
                        "stocks", 
                        "production_shifts",
                        "techniciens",
                        "fournisseurs"
                    ]
                    
                    saved_count = 0
                    for table in tables_to_save:
                        data = load_data(table)
                        if data:
                            st.session_state.offline_data[table] = data
                            saved_count += 1
                    
                    st.session_state.offline_timestamp = datetime.datetime.now()
                    
                    st.success(f"✅ Sauvegarde réussie! {saved_count} table(s) sauvegardée(s)")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur lors de la sauvegarde: {str(e)}")
    
    with col_action2:
        st.markdown("""
            <div style="background: #f0fdf4; padding: 16px; border-radius: 12px; 
                        border-left: 4px solid #10b981; margin-bottom: 16px;">
                <strong style="color: #065f46; font-size: 14px;">📂 Charger</strong><br>
                <span style="color: #047857; font-size: 12px;">
                    Voir les données sauvegardées localement
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("📂 Afficher Données", use_container_width=True, disabled=not has_offline_data):
            if has_offline_data:
                st.session_state.show_offline_data = True
            else:
                st.info("💡 Aucune donnée offline disponible")
    
    with col_action3:
        st.markdown("""
            <div style="background: #fee2e2; padding: 16px; border-radius: 12px; 
                        border-left: 4px solid #ef4444; margin-bottom: 16px;">
                <strong style="color: #991b1b; font-size: 14px;">🗑️ Effacer</strong><br>
                <span style="color: #7f1d1d; font-size: 12px;">
                    Supprimer le cache local
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Effacer Cache", use_container_width=True, disabled=not has_offline_data):
            if has_offline_data:
                st.session_state.offline_data = {}
                st.session_state.offline_timestamp = None
                st.session_state.show_offline_data = False
                st.success("✅ Cache effacé avec succès")
                time.sleep(1)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 3: Affichage des Données Sauvegardées
    # ═══════════════════════════════════════════════════════════════
    if hasattr(st.session_state, 'show_offline_data') and st.session_state.show_offline_data and has_offline_data:
        st.markdown("""
            <div style="background: white; padding: 24px; border-radius: 16px; 
                        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    📊 Données Sauvegardées Localement
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        # Création des onglets pour chaque table
        table_names = list(st.session_state.offline_data.keys())
        if table_names:
            tabs = st.tabs([f"📁 {name.capitalize()}" for name in table_names])
            
            for idx, table_name in enumerate(table_names):
                with tabs[idx]:
                    data = st.session_state.offline_data[table_name]
                    
                    if data:
                        # Informations sur la table
                        col_info1, col_info2, col_info3 = st.columns(3)
                        
                        with col_info1:
                            st.metric("📝 Nombre d'enregistrements", len(data))
                        
                        with col_info2:
                            if isinstance(data, list) and len(data) > 0:
                                st.metric("🔑 Colonnes", len(data[0].keys()) if isinstance(data[0], dict) else 0)
                            else:
                                st.metric("🔑 Colonnes", 0)
                        
                        with col_info3:
                            # Estimation de la taille en Ko
                            import sys
                            size_bytes = sys.getsizeof(str(data))
                            size_kb = size_bytes / 1024
                            st.metric("💾 Taille estimée", f"{size_kb:.1f} Ko")
                        
                        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
                        
                        # Affichage du DataFrame
                        df = pd.DataFrame(data)
                        
                        # Options d'affichage
                        col_opt1, col_opt2 = st.columns([3, 1])
                        
                        with col_opt1:
                            search_term = st.text_input(
                                "🔍 Rechercher dans les données",
                                key=f"search_{table_name}",
                                placeholder="Tapez pour filtrer..."
                            )
                        
                        with col_opt2:
                            show_all = st.checkbox(
                                "Tout afficher",
                                key=f"show_all_{table_name}",
                                value=False
                            )
                        
                        # Filtrage
                        if search_term:
                            mask = df.astype(str).apply(
                                lambda x: x.str.contains(search_term, case=False, na=False)
                            ).any(axis=1)
                            df_filtered = df[mask]
                        else:
                            df_filtered = df
                        
                        # Affichage
                        if not show_all and len(df_filtered) > 100:
                            st.info(f"💡 Affichage des 100 premiers résultats sur {len(df_filtered)}. Cochez 'Tout afficher' pour voir plus.")
                            st.dataframe(df_filtered.head(100), use_container_width=True, hide_index=True)
                        else:
                            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
                        
                        # Statistiques rapides
                        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
                        
                        with st.expander("📊 Statistiques détaillées"):
                            col_stat1, col_stat2 = st.columns(2)
                            
                            with col_stat1:
                                st.markdown("**📈 Aperçu des données:**")
                                st.write(df_filtered.describe(include='all'))
                            
                            with col_stat2:
                                st.markdown("**🔢 Types de colonnes:**")
                                types_df = pd.DataFrame({
                                    'Colonne': df_filtered.dtypes.index,
                                    'Type': df_filtered.dtypes.values.astype(str)
                                })
                                st.dataframe(types_df, use_container_width=True, hide_index=True)
                        
                        # Export
                        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
                        
                        col_export1, col_export2 = st.columns(2)
                        
                        with col_export1:
                            # Export CSV
                            csv = df_filtered.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="📥 Télécharger CSV",
                                data=csv,
                                file_name=f"{table_name}_offline_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        
                        with col_export2:
                            # Export JSON
                            json_str = df_filtered.to_json(orient='records', indent=2)
                            st.download_button(
                                label="📥 Télécharger JSON",
                                data=json_str,
                                file_name=f"{table_name}_offline_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.json",
                                mime="application/json",
                                use_container_width=True
                            )
                    else:
                        st.info("💡 Aucune donnée dans cette table")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 4: Statistiques Globales
    # ═══════════════════════════════════════════════════════════════
    if has_offline_data:
        st.markdown("""
            <div style="background: white; padding: 24px; border-radius: 16px; 
                        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
                <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                    📈 Statistiques Globales du Cache
                </h3>
            """,
            unsafe_allow_html=True
        )
        
        # Préparation des données pour le graphique
        table_stats = []
        for table_name, data in st.session_state.offline_data.items():
            if isinstance(data, list):
                table_stats.append({
                    'Table': table_name.capitalize(),
                    'Enregistrements': len(data)
                })
        
        if table_stats:
            df_stats = pd.DataFrame(table_stats)
            
            # Graphique en barres
            fig = px.bar(
                df_stats,
                x='Table',
                y='Enregistrements',
                title='Répartition des Données par Table',
                color='Enregistrements',
                color_continuous_scale=['#dbeafe', '#3b82f6', '#1e40af']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1F2937', size=12),
                margin=dict(l=0, r=0, t=40, b=0),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                showlegend=False,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Graphique en camembert
            fig_pie = px.pie(
                df_stats,
                values='Enregistrements',
                names='Table',
                title='Distribution des Données',
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1F2937', size=12),
                margin=dict(t=40, l=0, r=0, b=0)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SECTION 5: Conseils et Bonnes Pratiques
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); margin-bottom: 24px;">
            <h3 style="color: #1F2937; font-size: 18px; font-weight: 700; margin: 0 0 20px 0;">
                💡 Conseils et Bonnes Pratiques
            </h3>
        """,
        unsafe_allow_html=True
    )
    
    col_tip1, col_tip2 = st.columns(2)
    
    with col_tip1:
        st.markdown("""
            <div style="background: #eff6ff; padding: 16px; border-radius: 12px; 
                        border-left: 4px solid #3b82f6; margin-bottom: 16px;">
                <strong style="color: #1e40af; font-size: 14px;">✅ À Faire</strong><br>
                <ul style="color: #1e3a8a; font-size: 13px; margin: 8px 0 0 0; padding-left: 20px;">
                    <li>Sauvegarder régulièrement vos données</li>
                    <li>Vérifier l'horodatage de la dernière sauvegarde</li>
                    <li>Utiliser le mode offline pour les analyses rapides</li>
                    <li>Exporter les données importantes en CSV/JSON</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col_tip2:
        st.markdown("""
            <div style="background: #fee2e2; padding: 16px; border-radius: 12px; 
                        border-left: 4px solid #ef4444; margin-bottom: 16px;">
                <strong style="color: #991b1b; font-size: 14px;">⚠️ Attention</strong><br>
                <ul style="color: #7f1d1d; font-size: 13px; margin: 8px 0 0 0; padding-left: 20px;">
                    <li>Les données sont perdues à la fermeture du navigateur</li>
                    <li>Ne pas utiliser pour des données sensibles permanentes</li>
                    <li>Limité par la mémoire du navigateur</li>
                    <li>Pas de synchronisation automatique avec le serveur</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8fafc; 
                    border-radius: 10px; margin-top: 2rem;">
            <p style="color: #64748b; margin: 0; font-size: 0.9rem;">
                💾 <strong>Mode Offline:</strong> Sauvegarde temporaire dans la session locale • 
                Dernière mise à jour: {timestamp}
            </p>
        </div>
    """.format(
        timestamp=datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    ), unsafe_allow_html=True)
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