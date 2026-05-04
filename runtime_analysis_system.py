import streamlit as st
import json
import random
import hashlib
import datetime
import time
import uuid
import re
import subprocess
import os
import tempfile
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="JavaLens - Runtime Analysis Platform",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background-color: #FAFAFA;
    color: #262626;
}

.stApp {
    background-color: #FAFAFA;
}

section[data-testid="stSidebar"] {
    display: none !important;
    width: 0 !important;
}

[data-testid="collapsedControl"] {
    display: none !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

div[data-testid="stVerticalBlock"] > div:first-child {
    padding: 0;
}

header[data-testid="stHeader"] {
    background: transparent;
    height: 0;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    font-size: 14px;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: 'Inter', sans-serif;
}

.stTextInput > div > div > input {
    border-radius: 8px;
    border: 1px solid #DBDBDB;
    background: #FAFAFA;
    padding: 12px 14px;
    font-size: 14px;
    font-family: 'Inter', sans-serif;
    transition: border-color 0.2s;
}

.stTextInput > div > div > input:focus {
    border-color: #A8A8A8;
    box-shadow: none;
    outline: none;
}

.stSelectbox > div > div {
    border-radius: 8px;
    border: 1px solid #DBDBDB;
}

.stTextArea > div > div > textarea {
    border-radius: 8px;
    border: 1px solid #DBDBDB;
    font-family: 'Inter', sans-serif;
}

.stSlider > div {
    padding: 0;
}

div[data-testid="metric-container"] {
    background: white;
    border: 1px solid #DBDBDB;
    border-radius: 12px;
    padding: 16px;
}

.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

.stAlert {
    border-radius: 12px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid #DBDBDB;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 0;
    padding: 12px 20px;
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #8E8E8E;
    border-bottom: 2px solid transparent;
    background: transparent;
}

.stTabs [aria-selected="true"] {
    color: #262626;
    border-bottom: 2px solid #262626;
    background: transparent;
}

.stExpander {
    border: 1px solid #DBDBDB;
    border-radius: 12px;
    overflow: hidden;
}

hr {
    border-color: #DBDBDB;
    margin: 0;
}

.appview-container {
    background: #FAFAFA;
}

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: #FAFAFA;
}

::-webkit-scrollbar-thumb {
    background: #DBDBDB;
    border-radius: 3px;
}

.nav-bar {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid #DBDBDB;
    padding: 0 20px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.nav-brand {
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
}

.nav-actions {
    display: flex;
    align-items: center;
    gap: 16px;
}

.nav-icon-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: transparent;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 20px;
    transition: background 0.2s;
    color: #262626;
}

.nav-icon-btn:hover {
    background: #F0F0F0;
}

.avatar-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 14px;
    cursor: pointer;
    border: 2px solid transparent;
    transition: border-color 0.2s;
}

.avatar-circle:hover {
    border-color: #262626;
}

.tab-nav {
    display: flex;
    align-items: center;
    gap: 4px;
    background: transparent;
}

.tab-nav-item {
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    color: #8E8E8E;
    text-decoration: none;
    letter-spacing: 0.5px;
}

.tab-nav-item.active {
    background: #F0F0F0;
    color: #262626;
}

.tab-nav-item:hover {
    background: #F5F5F5;
    color: #262626;
}

.main-content {
    max-width: 1280px;
    margin: 0 auto;
    padding: 24px 20px;
}

.card {
    background: white;
    border: 1px solid #DBDBDB;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    transition: box-shadow 0.2s;
}

.card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid #F0F0F0;
}

.card-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 700;
    color: white;
    flex-shrink: 0;
}

.card-avatar-blue {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-avatar-green {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.card-avatar-red {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.card-avatar-orange {
    background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
}

.card-avatar-teal {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.card-avatar-purple {
    background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
}

.card-title {
    font-size: 15px;
    font-weight: 700;
    color: #262626;
    line-height: 1.2;
}

.card-subtitle {
    font-size: 12px;
    color: #8E8E8E;
    margin-top: 2px;
}

.card-action-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 14px;
    border-top: 1px solid #F0F0F0;
    margin-top: 14px;
}

.card-action-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #8E8E8E;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: color 0.2s;
    background: none;
    border: none;
    padding: 4px 0;
}

.card-action-btn:hover {
    color: #262626;
}

.primary-btn {
    background: #0095F6;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
    width: 100%;
}

.primary-btn:hover {
    background: #1877F2;
}

.secondary-btn {
    background: #EFEFEF;
    color: #262626;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
    width: 100%;
}

.secondary-btn:hover {
    background: #DBDBDB;
}

.badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.badge-blue {
    background: #E8F4FD;
    color: #0095F6;
}

.badge-green {
    background: #E6F9F1;
    color: #00B06B;
}

.badge-red {
    background: #FEE8E8;
    color: #ED4956;
}

.badge-orange {
    background: #FFF3E0;
    color: #FF8C00;
}

.badge-purple {
    background: #F3E5F5;
    color: #AB47BC;
}

.badge-gray {
    background: #F5F5F5;
    color: #8E8E8E;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
}

.stat-card {
    background: white;
    border: 1px solid #DBDBDB;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}

.stat-number {
    font-size: 28px;
    font-weight: 800;
    color: #262626;
    line-height: 1;
    margin-bottom: 6px;
}

.stat-label {
    font-size: 12px;
    color: #8E8E8E;
    font-weight: 500;
    letter-spacing: 0.5px;
}

.stories-row {
    display: flex;
    gap: 12px;
    overflow-x: auto;
    padding-bottom: 4px;
    margin-bottom: 24px;
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.stories-row::-webkit-scrollbar {
    display: none;
}

.story-item {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    cursor: pointer;
}

.story-ring {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    padding: 3px;
    background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045);
    transition: transform 0.2s;
}

.story-ring:hover {
    transform: scale(1.05);
}

.story-inner {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    border: 3px solid white;
}

.story-label {
    font-size: 11px;
    font-weight: 500;
    color: #262626;
    text-align: center;
    max-width: 70px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.login-wrapper {
    min-height: 100vh;
    background: #FAFAFA;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.login-box {
    background: white;
    border: 1px solid #DBDBDB;
    border-radius: 4px;
    padding: 40px;
    width: 100%;
    max-width: 380px;
}

.login-brand {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 28px;
}

.login-divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 16px 0;
    color: #8E8E8E;
    font-size: 13px;
    font-weight: 600;
}

.login-divider::before,
.login-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #DBDBDB;
}

.activity-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid #F5F5F5;
}

.activity-item:last-child {
    border-bottom: none;
}

.activity-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.activity-content {
    flex: 1;
}

.activity-text {
    font-size: 13px;
    color: #262626;
    line-height: 1.5;
}

.activity-text strong {
    font-weight: 700;
}

.activity-time {
    font-size: 11px;
    color: #8E8E8E;
    margin-top: 2px;
}

.code-block {
    background: #1a1a2e;
    border-radius: 10px;
    padding: 18px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 13px;
    color: #E8E8E8;
    overflow-x: auto;
    line-height: 1.7;
    border: 1px solid #2d2d4e;
}

.code-block .kw { color: #C678DD; }
.code-block .str { color: #98C379; }
.code-block .cm { color: #5C6370; font-style: italic; }
.code-block .num { color: #D19A66; }
.code-block .cls { color: #E5C07B; }
.code-block .fn { color: #61AFEF; }

.defect-card {
    background: white;
    border: 1px solid #DBDBDB;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    border-left: 4px solid #ED4956;
    transition: box-shadow 0.2s;
}

.defect-card:hover {
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.defect-card.medium {
    border-left-color: #FD8D14;
}

.defect-card.low {
    border-left-color: #0095F6;
}

.defect-card.resolved {
    border-left-color: #00B06B;
    opacity: 0.8;
}

.defect-title {
    font-size: 14px;
    font-weight: 700;
    color: #262626;
    margin-bottom: 6px;
}

.defect-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 10px;
}

.defect-desc {
    font-size: 13px;
    color: #8E8E8E;
    line-height: 1.5;
}

.progress-bar-wrapper {
    background: #EFEFEF;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    margin: 6px 0;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #0095F6, #1877F2);
    transition: width 0.5s ease;
}

.gauge-wrapper {
    text-align: center;
    padding: 10px 0;
}

.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}

.tag {
    background: #F5F5F5;
    border: 1px solid #DBDBDB;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 12px;
    color: #262626;
    font-weight: 500;
}

.notification-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #ED4956;
    display: inline-block;
    margin-left: 4px;
    vertical-align: middle;
}

.hero-section {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 32px;
    color: white;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-title {
    font-size: 28px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 10px;
    position: relative;
}

.hero-subtitle {
    font-size: 15px;
    color: rgba(255,255,255,0.7);
    line-height: 1.6;
    max-width: 500px;
    position: relative;
}

.hero-stat-row {
    display: flex;
    gap: 32px;
    margin-top: 24px;
    position: relative;
}

.hero-stat {
    text-align: center;
}

.hero-stat-num {
    font-size: 28px;
    font-weight: 800;
    color: white;
}

.hero-stat-lbl {
    font-size: 11px;
    color: rgba(255,255,255,0.6);
    margin-top: 2px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.timeline-item {
    display: flex;
    gap: 16px;
    padding-bottom: 20px;
    position: relative;
}

.timeline-item:not(:last-child)::after {
    content: '';
    position: absolute;
    left: 19px;
    top: 40px;
    bottom: 0;
    width: 2px;
    background: #EFEFEF;
}

.timeline-dot {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
    position: relative;
    z-index: 1;
}

.timeline-content {
    flex: 1;
    padding-top: 6px;
}

.timeline-title {
    font-size: 14px;
    font-weight: 700;
    color: #262626;
}

.timeline-sub {
    font-size: 12px;
    color: #8E8E8E;
    margin-top: 2px;
}

.search-bar {
    background: #EFEFEF;
    border-radius: 8px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    color: #8E8E8E;
    font-size: 14px;
    cursor: text;
}

.compare-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.compare-panel {
    background: white;
    border: 1px solid #DBDBDB;
    border-radius: 12px;
    padding: 16px;
}

.compare-panel-header {
    font-size: 13px;
    font-weight: 700;
    color: #262626;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.pulse-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #00B06B;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

.three-d-container {
    width: 100%;
    height: 350px;
    border-radius: 12px;
    overflow: hidden;
}

.mini-chart-row {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}

.mini-chart {
    flex: 1;
    background: white;
    border: 1px solid #DBDBDB;
    border-radius: 12px;
    padding: 16px;
}

.mini-chart-title {
    font-size: 12px;
    font-weight: 600;
    color: #8E8E8E;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.mini-chart-value {
    font-size: 24px;
    font-weight: 800;
    color: #262626;
}

.mini-chart-change {
    font-size: 12px;
    font-weight: 600;
    margin-top: 4px;
}

.positive { color: #00B06B; }
.negative { color: #ED4956; }
.neutral { color: #8E8E8E; }

.table-wrapper {
    background: white;
    border: 1px solid #DBDBDB;
    border-radius: 12px;
    overflow: hidden;
}

.table-header-row {
    display: grid;
    padding: 12px 16px;
    background: #FAFAFA;
    border-bottom: 1px solid #DBDBDB;
    font-size: 11px;
    font-weight: 700;
    color: #8E8E8E;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

.table-row {
    display: grid;
    padding: 14px 16px;
    border-bottom: 1px solid #F5F5F5;
    font-size: 13px;
    color: #262626;
    transition: background 0.1s;
    align-items: center;
}

.table-row:hover {
    background: #FAFAFA;
}

.table-row:last-child {
    border-bottom: none;
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #F0F0F0;
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 600;
    color: #262626;
    cursor: pointer;
    transition: background 0.2s;
    border: 1px solid #DBDBDB;
}

.chip:hover {
    background: #EFEFEF;
}

.chip.active {
    background: #262626;
    color: white;
    border-color: #262626;
}

.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 0;
}

.input-field-styled {
    background: #FAFAFA;
    border: 1px solid #DBDBDB;
    border-radius: 8px;
    padding: 12px 14px;
    width: 100%;
    font-size: 14px;
    font-family: 'Inter', sans-serif;
    color: #262626;
    transition: border-color 0.2s;
    outline: none;
}

.input-field-styled:focus {
    border-color: #A8A8A8;
}

.floating-action {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: #0095F6;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: 0 4px 20px rgba(0, 149, 246, 0.4);
    cursor: pointer;
    z-index: 999;
    transition: transform 0.2s, box-shadow 0.2s;
}

.floating-action:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 28px rgba(0, 149, 246, 0.5);
}

.section-title {
    font-size: 16px;
    font-weight: 700;
    color: #262626;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title-action {
    margin-left: auto;
    font-size: 13px;
    font-weight: 600;
    color: #0095F6;
    cursor: pointer;
}

.section-title-action:hover {
    color: #1877F2;
}

.empty-state {
    text-align: center;
    padding: 40px 20px;
    color: #8E8E8E;
}

.empty-state-icon {
    font-size: 48px;
    margin-bottom: 16px;
}

.empty-state-title {
    font-size: 20px;
    font-weight: 700;
    color: #262626;
    margin-bottom: 8px;
}

.empty-state-text {
    font-size: 14px;
    line-height: 1.6;
    max-width: 300px;
    margin: 0 auto;
}

.register-box {
    background: white;
    border: 1px solid #DBDBDB;
    border-radius: 4px;
    padding: 24px 40px;
    width: 100%;
    max-width: 380px;
    margin-top: 12px;
}

.role-selector {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin: 12px 0;
}

.role-option {
    border: 2px solid #DBDBDB;
    border-radius: 10px;
    padding: 14px 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    background: white;
}

.role-option:hover {
    border-color: #A8A8A8;
}

.role-option.selected {
    border-color: #0095F6;
    background: #E8F4FD;
}

.role-icon {
    font-size: 24px;
    margin-bottom: 6px;
}

.role-label {
    font-size: 11px;
    font-weight: 700;
    color: #262626;
    letter-spacing: 0.3px;
}

.highlight-number {
    font-size: 42px;
    font-weight: 900;
    background: linear-gradient(135deg, #0095F6 0%, #1877F2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}

.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

.grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.stButton > button[kind="primary"] {
    background: #0095F6;
    color: white;
    border: none;
    padding: 10px 20px;
    font-weight: 700;
    border-radius: 8px;
}

.stButton > button[kind="primary"]:hover {
    background: #1877F2;
    color: white;
}

.stButton > button[kind="secondary"] {
    background: #EFEFEF;
    color: #262626;
    border: none;
    padding: 10px 20px;
    font-weight: 700;
    border-radius: 8px;
}

.stButton > button[kind="secondary"]:hover {
    background: #DBDBDB;
}

.footer-box {
    background: white;
    border: 1px solid #DBDBDB;
    border-radius: 4px;
    padding: 16px 40px;
    width: 100%;
    max-width: 380px;
    text-align: center;
    margin-top: 10px;
}

.footer-box-text {
    font-size: 14px;
    color: #262626;
}

.footer-box-link {
    font-weight: 700;
    color: #0095F6;
    cursor: pointer;
}

.waterfall-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 0;
    border-bottom: 1px solid #F5F5F5;
    font-size: 13px;
    color: #262626;
}

.waterfall-bar {
    height: 20px;
    border-radius: 4px;
    min-width: 4px;
}

.log-entry {
    font-family: 'Courier New', monospace;
    font-size: 12px;
    padding: 6px 12px;
    border-radius: 4px;
    margin-bottom: 4px;
    line-height: 1.5;
}

.log-info { background: #F0F8FF; color: #1877F2; border-left: 3px solid #0095F6; }
.log-warn { background: #FFF8E8; color: #B8620A; border-left: 3px solid #FD8D14; }
.log-error { background: #FFF0F0; color: #CC0000; border-left: 3px solid #ED4956; }
.log-success { background: #F0FFF6; color: #006B3C; border-left: 3px solid #00B06B; }

.two-col-layout {
    display: grid;
    grid-template-columns: 1fr 360px;
    gap: 24px;
    align-items: start;
}

.right-rail {
    position: sticky;
    top: 80px;
}

.suggested-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
}

.suggested-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 700;
    color: white;
    flex-shrink: 0;
}

.suggested-name {
    font-size: 13px;
    font-weight: 700;
    color: #262626;
    flex: 1;
}

.suggested-sub {
    font-size: 12px;
    color: #8E8E8E;
}

.follow-btn {
    font-size: 13px;
    font-weight: 700;
    color: #0095F6;
    cursor: pointer;
    background: none;
    border: none;
    padding: 0;
}

.follow-btn:hover {
    color: #1877F2;
}

.status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
}

.status-green { background: #00B06B; }
.status-yellow { background: #FD8D14; }
.status-red { background: #ED4956; }
.status-gray { background: #DBDBDB; }

.scroll-feed {
    max-height: 70vh;
    overflow-y: auto;
    padding-right: 4px;
}

</style>
""", unsafe_allow_html=True)

if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "analyst@javalens.io": {
            "password": hashlib.sha256("analyst123".encode()).hexdigest(),
            "name": "Sarah Mitchell",
            "role": "Software Analyst",
            "username": "sarah_analyst",
            "bio": "Senior Software Analyst | Runtime Behavior Expert",
            "joined": "2025-01-15",
            "projects": 12,
            "analyses": 87,
            "defects": 234
        },
        "dev@javalens.io": {
            "password": hashlib.sha256("dev123".encode()).hexdigest(),
            "name": "Marcus Chen",
            "role": "Java Developer",
            "username": "marcus_dev",
            "bio": "Java Developer | Backend Systems",
            "joined": "2025-02-01",
            "projects": 8,
            "analyses": 54,
            "defects": 142
        },
        "admin@javalens.io": {
            "password": hashlib.sha256("admin123".encode()).hexdigest(),
            "name": "Elena Rodriguez",
            "role": "System Administrator",
            "username": "elena_admin",
            "bio": "System Administrator | Platform Manager",
            "joined": "2024-12-01",
            "projects": 30,
            "analyses": 200,
            "defects": 500
        }
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "projects" not in st.session_state:
    st.session_state.projects = []
if "defects" not in st.session_state:
    st.session_state.defects = []
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = []
if "execution_results" not in st.session_state:
    st.session_state.execution_results = []
if "patches" not in st.session_state:
    st.session_state.patches = []
if "notifications_count" not in st.session_state:
    st.session_state.notifications_count = 3
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None
if "system_config" not in st.session_state:
    st.session_state.system_config = {
        "java_version": "OpenJDK 17",
        "exec_timeout": 30,
        "memory_limit": 512,
        "log_level": "INFO",
        "defect_categories": ["Null Handling", "Arithmetic Errors", "Invalid Input", "Execution Order"],
        "active_categories": ["Null Handling", "Arithmetic Errors", "Invalid Input"],
        "max_iterations": 100
    }

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_audit_log(action, user=None, details=""):
    user_name = user or (st.session_state.current_user.get("name", "System") if st.session_state.current_user else "System")
    st.session_state.audit_logs.append({
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_name,
        "action": action,
        "details": details,
        "level": "INFO"
    })

def generate_sample_projects():
    if not st.session_state.projects:
        sample_projects = [
            {
                "id": str(uuid.uuid4())[:8],
                "name": "FinanceCore Analyzer",
                "description": "Runtime analysis for financial transaction processing engine",
                "status": "Active",
                "java_version": "OpenJDK 17",
                "defect_categories": ["Null Handling", "Arithmetic Errors"],
                "executions": 24,
                "defects_found": 18,
                "patches_applied": 12,
                "created_at": "2026-04-10",
                "last_run": "2026-05-03 14:30",
                "owner": "sarah_analyst",
                "language": "Java 17",
                "exec_timeout": 30,
                "memory_limit": 512
            },
            {
                "id": str(uuid.uuid4())[:8],
                "name": "HealthAPI Runtime Check",
                "description": "Healthcare API endpoint behavior analysis and validation",
                "status": "Completed",
                "java_version": "OpenJDK 11",
                "defect_categories": ["Invalid Input", "Execution Order"],
                "executions": 56,
                "defects_found": 31,
                "patches_applied": 28,
                "created_at": "2026-03-15",
                "last_run": "2026-04-28 09:15",
                "owner": "marcus_dev",
                "language": "Java 11",
                "exec_timeout": 45,
                "memory_limit": 256
            },
            {
                "id": str(uuid.uuid4())[:8],
                "name": "EcommerceOrder Engine",
                "description": "E-commerce order processing runtime defect detection",
                "status": "In Progress",
                "java_version": "OpenJDK 21",
                "defect_categories": ["Null Handling", "Arithmetic Errors", "Invalid Input"],
                "executions": 11,
                "defects_found": 7,
                "patches_applied": 3,
                "created_at": "2026-05-01",
                "last_run": "2026-05-04 08:00",
                "owner": "sarah_analyst",
                "language": "Java 21",
                "exec_timeout": 60,
                "memory_limit": 1024
            }
        ]
        st.session_state.projects = sample_projects

        sample_defects = [
            {"id": "D001", "project_id": sample_projects[0]["id"], "project": "FinanceCore Analyzer", "type": "NullPointerException", "severity": "Critical", "status": "Open", "method": "calculateInterest()", "line": 142, "description": "Variable 'account' may be null when rate is applied in compound interest scenario", "detected_at": "2026-05-03 14:31", "notes": "", "patch_id": "P001"},
            {"id": "D002", "project_id": sample_projects[0]["id"], "project": "FinanceCore Analyzer", "type": "ArithmeticException", "severity": "High", "status": "Resolved", "method": "divideBalance()", "line": 89, "description": "Division by zero when account balance is exactly zero", "detected_at": "2026-04-28 10:05", "notes": "Fixed with null-guard and zero-check", "patch_id": "P002"},
            {"id": "D003", "project_id": sample_projects[1]["id"], "project": "HealthAPI Runtime Check", "type": "InvalidInputException", "severity": "Medium", "status": "Open", "method": "parsePatientAge()", "line": 67, "description": "Negative age values are accepted without validation causing downstream failures", "detected_at": "2026-04-25 16:45", "notes": "", "patch_id": "P003"},
            {"id": "D004", "project_id": sample_projects[1]["id"], "project": "HealthAPI Runtime Check", "type": "ExecutionOrderFault", "severity": "Low", "status": "Resolved", "method": "initializeSession()", "line": 201, "description": "Session token generated before authentication verification completes", "detected_at": "2026-04-20 11:30", "notes": "Reordered initialization sequence", "patch_id": "P004"},
            {"id": "D005", "project_id": sample_projects[2]["id"], "project": "EcommerceOrder Engine", "type": "NullPointerException", "severity": "Critical", "status": "Open", "method": "processPayment()", "line": 315, "description": "Payment gateway object null when fallback provider not configured", "detected_at": "2026-05-04 08:01", "notes": "", "patch_id": "P005"},
            {"id": "D006", "project_id": sample_projects[0]["id"], "project": "FinanceCore Analyzer", "type": "OverflowException", "severity": "High", "status": "Open", "method": "computeTotal()", "line": 55, "description": "Integer overflow when summing large transaction batches", "detected_at": "2026-05-02 09:22", "notes": "", "patch_id": "P006"},
            {"id": "D007", "project_id": sample_projects[1]["id"], "project": "HealthAPI Runtime Check", "type": "InvalidInputException", "severity": "Medium", "status": "Resolved", "method": "validateDosage()", "line": 130, "description": "Boundary value 0.0 accepted as valid dosage causing null medication event", "detected_at": "2026-04-10 14:00", "notes": "Added boundary check", "patch_id": "P007"},
        ]
        st.session_state.defects = sample_defects

        sample_patches = [
            {"id": "P001", "defect_id": "D001", "type": "Null Guard", "description": "Add null check before accessing account object", "code": "if (account != null) {\n    rate = account.getInterestRate();\n} else {\n    throw new IllegalStateException(\"Account cannot be null\");\n}", "status": "Pending", "confidence": 92},
            {"id": "P002", "defect_id": "D002", "type": "Zero Guard", "description": "Prevent division by zero in balance calculation", "code": "if (balance == 0.0) return 0.0;\nreturn totalInterest / balance;", "status": "Applied", "confidence": 98},
            {"id": "P003", "defect_id": "D003", "type": "Input Validation", "description": "Add validation for negative age values", "code": "if (age < 0 || age > 150) {\n    throw new IllegalArgumentException(\"Invalid age: \" + age);\n}", "status": "Pending", "confidence": 87},
            {"id": "P004", "defect_id": "D004", "type": "Execution Order Fix", "description": "Reorder authentication before session initialization", "code": "verifyAuthentication(credentials);\nString token = generateSessionToken();\ninitializeUserSession(token);", "status": "Applied", "confidence": 95},
            {"id": "P005", "defect_id": "D005", "type": "Null Guard", "description": "Add fallback when payment gateway is null", "code": "PaymentGateway gw = getPaymentGateway();\nif (gw == null) {\n    gw = getFallbackGateway();\n    if (gw == null) throw new RuntimeException(\"No gateway available\");\n}", "status": "Pending", "confidence": 89},
            {"id": "P006", "defect_id": "D006", "type": "Overflow Prevention", "description": "Use long type to prevent integer overflow in summation", "code": "long total = 0L;\nfor (Transaction t : batch) {\n    total = Math.addExact(total, t.getAmount());\n}", "status": "Pending", "confidence": 94},
            {"id": "P007", "defect_id": "D007", "type": "Boundary Check", "description": "Reject zero and negative dosage values", "code": "if (dosage <= 0.0) {\n    throw new IllegalArgumentException(\"Dosage must be positive: \" + dosage);\n}", "status": "Applied", "confidence": 96},
        ]
        st.session_state.patches = sample_patches

        sample_executions = [
            {"id": "E001", "project": "FinanceCore Analyzer", "timestamp": "2026-05-03 14:30", "status": "Completed", "inputs_generated": 50, "defects_found": 4, "exceptions": 2, "duration_ms": 1240, "memory_mb": 128, "traces": 892},
            {"id": "E002", "project": "HealthAPI Runtime Check", "timestamp": "2026-04-28 09:15", "status": "Completed", "inputs_generated": 100, "defects_found": 6, "exceptions": 3, "duration_ms": 2150, "memory_mb": 96, "traces": 1450},
            {"id": "E003", "project": "EcommerceOrder Engine", "timestamp": "2026-05-04 08:00", "status": "Running", "inputs_generated": 30, "defects_found": 2, "exceptions": 1, "duration_ms": 980, "memory_mb": 200, "traces": 560},
            {"id": "E004", "project": "FinanceCore Analyzer", "timestamp": "2026-04-30 16:00", "status": "Completed", "inputs_generated": 75, "defects_found": 8, "exceptions": 5, "duration_ms": 1890, "memory_mb": 140, "traces": 1100},
        ]
        st.session_state.execution_results = sample_executions

        add_audit_log("System Initialized", "System", "Sample data loaded")

generate_sample_projects()

class RuntimeConfiguration:
    def __init__(self, defect_categories, execution_limit, memory_limit=512, timeout=30):
        self.defect_categories = defect_categories
        self.execution_limit = execution_limit
        self.memory_limit = memory_limit
        self.timeout = timeout

    def validateConfiguration(self):
        return self.execution_limit > 0 and self.memory_limit > 0 and self.timeout > 0

class JavaExecutionManager:
    def compileCode(self, source):
        has_class = "class " in source
        has_main = "main" in source or "void" in source
        return has_class and len(source) > 10

    def executeCode(self, source, inputs=None):
        if not source or len(source) < 5:
            return {"status": "fail", "error": "Source code is empty", "output": "", "traces": [], "exceptions": []}
        errors = []
        warnings = []
        traces = []
        if "/ 0" in source or "/0" in source:
            errors.append({"type": "ArithmeticException", "message": "Division by zero detected", "line": source.count('\n', 0, source.find('/0')) + 1 if '/0' in source else 0, "severity": "Critical"})
        if ".length" in source and "null" in source:
            errors.append({"type": "NullPointerException", "message": "Potential null dereference on object access", "line": random.randint(5, 50), "severity": "High"})
        if "Integer.parseInt" in source or "Long.parseLong" in source:
            warnings.append({"type": "ParseException", "message": "Unhandled parse exception risk on numeric conversion", "line": random.randint(3, 30), "severity": "Medium"})
        if "new " in source:
            traces.append("Object instantiation detected")
        if "for" in source or "while" in source:
            traces.append("Loop construct detected - boundary analysis applied")
        if "if" in source:
            traces.append("Conditional branch detected - path coverage tracked")
        method_count = source.count("void ") + source.count("int ") + source.count("String ")
        traces.append(f"{method_count} method signatures identified")
        traces.append("Execution trace captured: " + str(random.randint(50, 500)) + " steps")
        status = "fail" if errors else "success"
        return {
            "status": status,
            "errors": errors,
            "warnings": warnings,
            "traces": traces,
            "output": "Program executed successfully" if status == "success" else "Execution terminated with errors",
            "execution_time_ms": random.randint(200, 2000),
            "memory_used_mb": random.randint(32, 256)
        }

class RuntimeInputGenerator:
    def generateRandomInput(self, count=10):
        inputs = []
        for _ in range(count):
            inputs.append({
                "type": random.choice(["int", "String", "double", "boolean", "long"]),
                "value": random.choice([
                    random.randint(-1000, 1000),
                    random.uniform(-100.0, 100.0),
                    ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3, 10))),
                    None,
                    True, False
                ])
            })
        return inputs

    def generateBoundaryInput(self):
        return [
            {"type": "int", "value": 0, "label": "Zero"},
            {"type": "int", "value": 1, "label": "Min positive"},
            {"type": "int", "value": -1, "label": "Min negative"},
            {"type": "int", "value": 2147483647, "label": "INT_MAX"},
            {"type": "int", "value": -2147483648, "label": "INT_MIN"},
            {"type": "String", "value": "", "label": "Empty string"},
            {"type": "String", "value": None, "label": "Null string"},
            {"type": "double", "value": 0.0, "label": "Zero double"},
            {"type": "double", "value": float('inf'), "label": "Positive infinity"},
            {"type": "double", "value": float('nan'), "label": "NaN"},
        ]

class ExecutionMonitor:
    def captureTrace(self, execution_result):
        return {
            "traces": execution_result.get("traces", []),
            "memory": execution_result.get("memory_used_mb", 0),
            "duration": execution_result.get("execution_time_ms", 0),
            "status": execution_result.get("status", "unknown")
        }

    def recordException(self, execution_result):
        errors = execution_result.get("errors", [])
        return errors if errors else []

class Defect:
    def classifyDefect(self, error):
        if not error:
            return "No Defect"
        severity_map = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        return error.get("type", "Unknown Defect")

    def assignSeverity(self, defect_type):
        severity_map = {
            "NullPointerException": "Critical",
            "ArithmeticException": "Critical",
            "OverflowException": "High",
            "ParseException": "Medium",
            "InvalidInputException": "Medium",
            "ExecutionOrderFault": "Low"
        }
        return severity_map.get(defect_type, "Medium")

class BehaviorInferenceEngine:
    def inferBehavior(self, execution_result):
        if execution_result.get("status") == "success":
            return {"inference": "Expected Behavior", "confidence": random.uniform(85, 99), "anomalies": []}
        errors = execution_result.get("errors", [])
        anomalies = [e.get("type", "Unknown") for e in errors]
        return {
            "inference": "Unexpected Behavior",
            "confidence": random.uniform(70, 92),
            "anomalies": anomalies,
            "expected_pattern": "Normal termination without exceptions",
            "observed_pattern": f"Terminated with {len(errors)} exception(s)"
        }

class PatchRecommendation:
    def generatePatch(self, defect_type, context=""):
        patches = {
            "NullPointerException": {
                "type": "Null Guard",
                "code": "if (object != null) {\n    // safe access\n    object.method();\n} else {\n    throw new IllegalArgumentException(\"Object cannot be null\");\n}",
                "explanation": "Add null-check before object access to prevent NullPointerException",
                "confidence": 91
            },
            "ArithmeticException": {
                "type": "Zero Guard",
                "code": "if (divisor == 0) {\n    throw new ArithmeticException(\"Division by zero\");\n}\nresult = numerator / divisor;",
                "explanation": "Validate divisor before performing division operation",
                "confidence": 97
            },
            "OverflowException": {
                "type": "Safe Math",
                "code": "try {\n    long result = Math.addExact(a, b);\n} catch (ArithmeticException e) {\n    // handle overflow\n    result = Long.MAX_VALUE;\n}",
                "explanation": "Use Math.addExact() for safe arithmetic with overflow detection",
                "confidence": 89
            },
            "ParseException": {
                "type": "Safe Parse",
                "code": "try {\n    int value = Integer.parseInt(input);\n} catch (NumberFormatException e) {\n    value = defaultValue;\n    logger.warn(\"Invalid input: \" + input);\n}",
                "explanation": "Wrap parsing in try-catch to handle malformed input gracefully",
                "confidence": 93
            },
            "InvalidInputException": {
                "type": "Input Validation",
                "code": "if (input == null || input.isEmpty() || !isValid(input)) {\n    throw new IllegalArgumentException(\"Invalid input provided: \" + input);\n}",
                "explanation": "Validate input before processing to prevent downstream failures",
                "confidence": 86
            },
            "ExecutionOrderFault": {
                "type": "Sequence Fix",
                "code": "// Corrected execution sequence:\ninitialize();\nauthenticate(credentials);\nsetupResources();\nprocess();",
                "explanation": "Reorder execution steps to respect dependency constraints",
                "confidence": 84
            }
        }
        return patches.get(defect_type, {
            "type": "General Fix",
            "code": "// Add appropriate error handling\ntry {\n    // original code\n} catch (Exception e) {\n    logger.error(\"Unexpected error\", e);\n    throw new RuntimeException(e);\n}",
            "explanation": "Wrap in general exception handler as fallback",
            "confidence": 72
        })

class ResultComparator:
    def compareResults(self, old_result, new_result):
        if not old_result or not new_result:
            return {"changed": False, "details": "Insufficient data"}
        old_errors = len(old_result.get("errors", []))
        new_errors = len(new_result.get("errors", []))
        improvement = old_errors - new_errors
        return {
            "changed": old_result != new_result,
            "previous_errors": old_errors,
            "current_errors": new_errors,
            "improvement": improvement,
            "improved": improvement > 0,
            "improvement_pct": round((improvement / max(old_errors, 1)) * 100, 1),
            "details": f"Reduced defects from {old_errors} to {new_errors}"
        }

class AuditLogger:
    def recordActivity(self, activity, user=None, level="INFO", details=""):
        add_audit_log(activity, user, details)

    def retrieveLogs(self):
        return st.session_state.audit_logs

class ArtifactExporter:
    def exportReport(self, project_name, defects, execution_results):
        lines = []
        lines.append(f"JAVA RUNTIME ANALYSIS REPORT")
        lines.append(f"{'='*60}")
        lines.append(f"Project: {project_name}")
        lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"")
        lines.append(f"SUMMARY")
        lines.append(f"{'-'*40}")
        lines.append(f"Total Defects Found: {len(defects)}")
        open_defects = [d for d in defects if d.get('status') == 'Open']
        resolved_defects = [d for d in defects if d.get('status') == 'Resolved']
        lines.append(f"Open Defects: {len(open_defects)}")
        lines.append(f"Resolved Defects: {len(resolved_defects)}")
        lines.append(f"Total Executions: {len(execution_results)}")
        lines.append(f"")
        lines.append(f"DEFECT DETAILS")
        lines.append(f"{'-'*40}")
        for d in defects:
            lines.append(f"[{d.get('severity', 'N/A')}] {d.get('id', '')} - {d.get('type', '')} in {d.get('method', '')}")
            lines.append(f"  Status: {d.get('status', '')}")
            lines.append(f"  Description: {d.get('description', '')}")
            lines.append(f"  Detected: {d.get('detected_at', '')}")
            lines.append(f"")
        lines.append(f"")
        lines.append(f"EXECUTION HISTORY")
        lines.append(f"{'-'*40}")
        for e in execution_results:
            lines.append(f"{e.get('id', '')} | {e.get('timestamp', '')} | {e.get('status', '')} | Defects: {e.get('defects_found', 0)}")
        return "\n".join(lines)

    def exportLogs(self, logs):
        lines = ["AUDIT LOG EXPORT", "="*60]
        for log in logs:
            lines.append(f"[{log.get('timestamp','')}] [{log.get('level','INFO')}] {log.get('user','')} | {log.get('action','')} | {log.get('details','')}")
        return "\n".join(lines)

exec_manager = JavaExecutionManager()
input_gen = RuntimeInputGenerator()
monitor = ExecutionMonitor()
defect_cls = Defect()
infer_engine = BehaviorInferenceEngine()
patch_rec = PatchRecommendation()
comparator = ResultComparator()
audit_logger = AuditLogger()
exporter = ArtifactExporter()

def show_auth_page():
    if st.session_state.auth_mode == "login":
        show_login()
    else:
        show_register()

def show_login():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='login-box'>
            <div class='login-brand'>JavaLens</div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("<div style='background:white;border:1px solid #DBDBDB;border-radius:4px;padding:32px 32px 24px;'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:32px;font-weight:800;text-align:center;letter-spacing:-1.5px;color:#1a1a2e;margin-bottom:24px;'>JavaLens</div>", unsafe_allow_html=True)

            email = st.text_input("Email or Username", placeholder="Enter your email", key="login_email", label_visibility="collapsed")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            password = st.text_input("Password", placeholder="Password", type="password", key="login_password", label_visibility="collapsed")
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            if st.button("Log In", use_container_width=True, type="primary", key="login_btn"):
                if email and password:
                    user_data = st.session_state.users_db.get(email)
                    if user_data and user_data["password"] == hash_password(password):
                        st.session_state.logged_in = True
                        st.session_state.current_user = {**user_data, "email": email}
                        add_audit_log("User Login", user_data["name"], f"Role: {user_data['role']}")
                        st.success("Welcome back!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
                else:
                    st.warning("Please enter your email and password.")

            st.markdown("""
            <div class='login-divider'>OR</div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style='text-align:center;font-size:13px;color:#262626;'>
                <strong>Don't have an account?</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("Create New Account", use_container_width=True, key="goto_register"):
                st.session_state.auth_mode = "register"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background:white;border:1px solid #DBDBDB;border-radius:4px;padding:16px;text-align:center;margin-top:10px;font-size:14px;color:#262626;'>
            Part of the <strong>JavaLens</strong> Runtime Analysis Platform
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='text-align:center;margin-top:24px;font-size:11px;color:#8E8E8E;'>Java Runtime Analysis Platform &copy; 2026 JavaLens</div>", unsafe_allow_html=True)

def show_register():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

        with st.container():
            st.markdown("<div style='background:white;border:1px solid #DBDBDB;border-radius:4px;padding:28px 32px 24px;'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:26px;font-weight:800;text-align:center;letter-spacing:-1.5px;color:#1a1a2e;margin-bottom:4px;'>JavaLens</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;font-size:14px;color:#8E8E8E;margin-bottom:20px;'>Sign up to start analyzing Java runtime behavior</div>", unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                first_name = st.text_input("First Name", placeholder="First name", key="reg_first")
            with col_b:
                last_name = st.text_input("Last Name", placeholder="Last name", key="reg_last")

            username = st.text_input("Username", placeholder="Username", key="reg_username")
            email = st.text_input("Email", placeholder="Email address", key="reg_email")
            password = st.text_input("Password", placeholder="Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", placeholder="Confirm password", type="password", key="reg_confirm")

            st.markdown("<div style='font-size:12px;font-weight:700;color:#8E8E8E;letter-spacing:0.5px;text-transform:uppercase;margin:12px 0 8px;'>Select Role</div>", unsafe_allow_html=True)
            role = st.selectbox("Role", ["Software Analyst", "Java Developer", "System Administrator"], key="reg_role", label_visibility="collapsed")

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            if st.button("Sign Up", use_container_width=True, type="primary", key="register_btn"):
                if all([first_name, last_name, username, email, password, confirm_password]):
                    if password != confirm_password:
                        st.error("Passwords do not match.")
                    elif email in st.session_state.users_db:
                        st.error("An account with this email already exists.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        new_user = {
                            "password": hash_password(password),
                            "name": f"{first_name} {last_name}",
                            "role": role,
                            "username": username,
                            "bio": f"{role} | JavaLens Platform",
                            "joined": datetime.datetime.now().strftime("%Y-%m-%d"),
                            "projects": 0,
                            "analyses": 0,
                            "defects": 0
                        }
                        st.session_state.users_db[email] = new_user
                        add_audit_log("User Registration", f"{first_name} {last_name}", f"Role: {role}")
                        st.success("Account created successfully! Please log in.")
                        time.sleep(1)
                        st.session_state.auth_mode = "login"
                        st.rerun()
                else:
                    st.warning("Please fill in all fields.")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        with st.container():
            st.markdown("<div style='background:white;border:1px solid #DBDBDB;border-radius:4px;padding:16px;text-align:center;font-size:14px;'>", unsafe_allow_html=True)
            st.markdown("<div style='color:#262626;'>Already have an account?</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            if st.button("Log In", use_container_width=True, key="goto_login"):
                st.session_state.auth_mode = "login"
                st.rerun()

def render_navbar():
    user = st.session_state.current_user
    role = user.get("role", "")
    name = user.get("name", "User")
    initials = "".join([n[0] for n in name.split()[:2]]).upper()

    if role == "Software Analyst":
        pages = ["Dashboard", "Projects", "Execute Analysis", "Defect Analysis", "Behavior Inference", "Patch Generator", "Reports & Export"]
    elif role == "Java Developer":
        pages = ["Dashboard", "Submit Code", "Review Defects", "Apply Patches", "Compare Results", "Export Code"]
    else:
        pages = ["Dashboard", "System Config", "User Management", "Audit Logs", "Resource Monitor", "System Reports"]

    col_brand, col_nav, col_actions = st.columns([2, 6, 2])

    with col_brand:
        st.markdown("""
        <div style='display:flex;align-items:center;height:60px;padding-left:8px;'>
            <span style='font-size:24px;font-weight:900;letter-spacing:-1px;color:#1a1a2e;'>JavaLens</span>
        </div>
        """, unsafe_allow_html=True)

    with col_nav:
        nav_cols = st.columns(len(pages))
        for i, pg in enumerate(pages):
            with nav_cols[i]:
                is_active = st.session_state.current_page == pg
                btn_style = "background:#F0F0F0;color:#262626;border:none;border-radius:8px;padding:6px 10px;font-size:12px;font-weight:700;cursor:pointer;width:100%;" if is_active else "background:transparent;color:#8E8E8E;border:none;border-radius:8px;padding:6px 10px;font-size:12px;font-weight:600;cursor:pointer;width:100%;"
                if st.button(pg, key=f"nav_btn_{pg}", use_container_width=True):
                    st.session_state.current_page = pg
                    st.rerun()

    with col_actions:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            notif_label = f"Alerts ({st.session_state.notifications_count})" if st.session_state.notifications_count > 0 else "Alerts"
            if st.button("", key="notif_btn", help=notif_label):
                st.session_state.notifications_count = 0
        with col_b:
            st.markdown(f"""
            <div style='display:flex;align-items:center;justify-content:center;height:38px;'>
                <div class='avatar-circle'>{initials}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            if st.button("Exit", key="logout_btn"):
                add_audit_log("User Logout", name, "Session ended")
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.session_state.auth_mode = "login"
                st.rerun()

    st.markdown("<hr style='margin:0;border-color:#DBDBDB;'>", unsafe_allow_html=True)

def page_dashboard():
    user = st.session_state.current_user
    role = user.get("role", "")
    name = user.get("name", "")

    projects = st.session_state.projects
    defects = st.session_state.defects
    executions = st.session_state.execution_results

    total_projects = len(projects)
    total_defects = len(defects)
    open_defects = len([d for d in defects if d.get("status") == "Open"])
    resolved_defects = len([d for d in defects if d.get("status") == "Resolved"])
    total_executions = len(executions)
    total_patches = len(st.session_state.patches)
    applied_patches = len([p for p in st.session_state.patches if p.get("status") == "Applied"])

    hour = datetime.datetime.now().hour
    greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 17 else "Good evening")

    st.markdown(f"""
    <div class='hero-section'>
        <div class='hero-title'>{greeting}, {name.split()[0]}!</div>
        <div class='hero-subtitle'>Your Java runtime analysis platform. Monitor defects, generate patches, and improve code quality.</div>
        <div class='hero-stat-row'>
            <div class='hero-stat'>
                <div class='hero-stat-num'>{total_projects}</div>
                <div class='hero-stat-lbl'>Projects</div>
            </div>
            <div class='hero-stat'>
                <div class='hero-stat-num'>{total_executions}</div>
                <div class='hero-stat-lbl'>Executions</div>
            </div>
            <div class='hero-stat'>
                <div class='hero-stat-num'>{total_defects}</div>
                <div class='hero-stat-lbl'>Defects</div>
            </div>
            <div class='hero-stat'>
                <div class='hero-stat-num'>{applied_patches}</div>
                <div class='hero-stat-lbl'>Patches</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    story_items = [
        ("FinanceCore", "FinanceCore Analyzer"),
        ("HealthAPI", "HealthAPI Runtime Check"),
        ("EcomOrder", "EcommerceOrder Engine"),
        ("DataFlow", None),
        ("AuthService", None),
        ("CacheLayer", None),
    ]
    story_cols = st.columns(len(story_items))
    for i, (label, proj_name) in enumerate(story_items):
        with story_cols[i]:
            st.markdown(f"""
            <div style='display:flex;flex-direction:column;align-items:center;gap:4px;margin-bottom:4px;'>
                <div style='width:60px;height:60px;border-radius:50%;padding:3px;background:linear-gradient(135deg,#833ab4,#fd1d1d,#fcb045);'>
                    <div style='width:100%;height:100%;border-radius:50%;background:white;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:800;color:#1a1a2e;border:3px solid white;'>{label[0]}</div>
                </div>
                <div style='font-size:11px;font-weight:500;color:#262626;text-align:center;max-width:70px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("", key=f"story_{label}", use_container_width=True, help=f"Go to {label}"):
                if proj_name:
                    proj = next((p for p in st.session_state.projects if p["name"] == proj_name), None)
                    if proj:
                        st.session_state.selected_project = proj
                st.session_state.current_page = "Projects"
                st.rerun()

    col_main, col_rail = st.columns([2.2, 1])

    with col_main:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number' style='color:#0095F6'>{total_projects}</div>
                <div class='stat-label'>Projects</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number' style='color:#ED4956'>{open_defects}</div>
                <div class='stat-label'>Open Defects</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number' style='color:#00B06B'>{resolved_defects}</div>
                <div class='stat-label'>Resolved</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number' style='color:#FD8D14'>{total_executions}</div>
                <div class='stat-label'>Executions</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        severity_counts = {}
        for d in defects:
            sev = d.get("severity", "Unknown")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        defect_types = {}
        for d in defects:
            dt = d.get("type", "Unknown")
            defect_types[dt] = defect_types.get(dt, 0) + 1

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'><div class='card-avatar card-avatar-blue'>D</div><div><div class='card-title'>Defect Severity Distribution</div><div class='card-subtitle'>All projects combined</div></div></div>", unsafe_allow_html=True)
            if severity_counts:
                colors_map = {"Critical": "#ED4956", "High": "#FD8D14", "Medium": "#0095F6", "Low": "#00B06B"}
                fig = go.Figure(data=[go.Pie(
                    labels=list(severity_counts.keys()),
                    values=list(severity_counts.values()),
                    hole=0.6,
                    marker_colors=[colors_map.get(k, "#DBDBDB") for k in severity_counts.keys()],
                    textinfo='label+percent',
                    textfont_size=12
                )])
                fig.update_layout(
                    showlegend=False,
                    margin=dict(l=0, r=0, t=10, b=10),
                    height=200,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        with chart_col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'><div class='card-avatar card-avatar-green'>T</div><div><div class='card-title'>Defect Types</div><div class='card-subtitle'>Breakdown by exception category</div></div></div>", unsafe_allow_html=True)
            if defect_types:
                fig2 = go.Figure(go.Bar(
                    x=list(defect_types.values()),
                    y=list(defect_types.keys()),
                    orientation='h',
                    marker_color='#0095F6',
                    marker_line_width=0
                ))
                fig2.update_layout(
                    margin=dict(l=0, r=0, t=10, b=10),
                    height=200,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'><div class='card-avatar card-avatar-teal'>E</div><div><div class='card-title'>Execution Timeline</div><div class='card-subtitle'>Defects detected over recent executions</div></div></div>", unsafe_allow_html=True)

        x_data = [e.get("timestamp", "")[:10] for e in executions]
        y_defects = [e.get("defects_found", 0) for e in executions]
        y_exceptions = [e.get("exceptions", 0) for e in executions]

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=x_data, y=y_defects, mode='lines+markers', name='Defects Found',
                                  line=dict(color='#ED4956', width=2.5), marker=dict(size=8)))
        fig3.add_trace(go.Scatter(x=x_data, y=y_exceptions, mode='lines+markers', name='Exceptions',
                                  line=dict(color='#FD8D14', width=2.5), marker=dict(size=8)))
        fig3.update_layout(
            margin=dict(l=0, r=0, t=10, b=10),
            height=220,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", y=1.1, x=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#F5F5F5')
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Recent Activity</div>", unsafe_allow_html=True)

        activity_icons = {"NullPointerException": "", "ArithmeticException": "", "InvalidInput": "", "Resolved": "", "Patch": ""}
        recent_defects = sorted(defects, key=lambda d: d.get("detected_at", ""), reverse=True)[:5]
        for d in recent_defects:
            sev_color_map = {"Critical": "#ED4956", "High": "#FD8D14", "Medium": "#0095F6", "Low": "#00B06B"}
            clr = sev_color_map.get(d.get("severity", ""), "#8E8E8E")
            status_badge = "badge-green" if d.get("status") == "Resolved" else "badge-red"
            st.markdown(f"""
            <div class='activity-item'>
                <div class='activity-icon' style='background:{clr}22;'>
                    <span style='font-size:18px;'></span>
                </div>
                <div class='activity-content'>
                    <div class='activity-text'>
                        <strong>{d.get('type','')}</strong> detected in <strong>{d.get('project','')}</strong>
                        &nbsp;<span class='badge {status_badge}'>{d.get('status','')}</span>
                    </div>
                    <div class='activity-time'>{d.get('detected_at','')} &bull; {d.get('method','')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_rail:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:14px;'>Active Projects</div>", unsafe_allow_html=True)
        for p in projects[:3]:
            status_color = "#00B06B" if p.get("status") == "Completed" else ("#0095F6" if p.get("status") == "Active" else "#FD8D14")
            pct = int((p.get("patches_applied", 0) / max(p.get("defects_found", 1), 1)) * 100)
            st.markdown(f"""
            <div class='suggested-item'>
                <div class='suggested-avatar' style='background:linear-gradient(135deg,#667eea,#764ba2)'>
                    {p.get('name','')[0]}
                </div>
                <div>
                    <div class='suggested-name'>{p.get('name','')}</div>
                    <div class='suggested-sub'>{p.get('defects_found',0)} defects | {p.get('executions',0)} runs</div>
                    <div class='progress-bar-wrapper' style='width:140px;margin-top:4px;'>
                        <div class='progress-bar-fill' style='width:{pct}%;background:{status_color};'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:14px;'>System Health</div>", unsafe_allow_html=True)

        metrics = [("CPU Usage", 34, "#0095F6"), ("Memory", 58, "#00B06B"), ("Analysis Queue", 72, "#FD8D14"), ("Patch Success Rate", 86, "#00B06B")]
        for label, val, color in metrics:
            st.markdown(f"""
            <div style='margin-bottom:14px;'>
                <div style='display:flex;justify-content:space-between;font-size:12px;font-weight:600;color:#262626;margin-bottom:4px;'>
                    <span>{label}</span><span style='color:{color};'>{val}%</span>
                </div>
                <div class='progress-bar-wrapper'>
                    <div class='progress-bar-fill' style='width:{val}%;background:{color};'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:14px;'>Quick Stats</div>", unsafe_allow_html=True)

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round((resolved_defects / max(total_defects, 1)) * 100, 1),
            title={'text': "Resolution Rate", 'font': {'size': 12, 'color': '#8E8E8E'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "#00B06B"},
                'bgcolor': "white",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 40], 'color': '#FEE8E8'},
                    {'range': [40, 70], 'color': '#FFF3E0'},
                    {'range': [70, 100], 'color': '#E6F9F1'}
                ]
            },
            number={'suffix': '%', 'font': {'size': 24, 'color': '#262626'}}
        ))
        fig_gauge.update_layout(
            height=180,
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

def page_projects():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    col_hdr, col_btn = st.columns([3, 1])
    with col_hdr:
        st.markdown("<div class='section-title'>Analysis Projects</div>", unsafe_allow_html=True)
    with col_btn:
        if st.button("+ New Project", use_container_width=True, type="primary", key="new_proj_btn"):
            st.session_state.show_new_project = True

    if st.session_state.get("show_new_project"):
        with st.expander("Create New Analysis Project", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                proj_name = st.text_input("Project Name", placeholder="e.g., PaymentService Analyzer", key="new_proj_name")
                proj_desc = st.text_area("Description", placeholder="Describe what this project analyzes...", key="new_proj_desc", height=80)
                java_ver = st.selectbox("Java Version", ["OpenJDK 8", "OpenJDK 11", "OpenJDK 17", "OpenJDK 21"], key="new_proj_java")
            with c2:
                defect_cats = st.multiselect("Defect Categories", ["Null Handling", "Arithmetic Errors", "Invalid Input", "Execution Order", "Resource Leaks"], default=["Null Handling", "Arithmetic Errors"], key="new_proj_cats")
                exec_timeout = st.slider("Execution Timeout (seconds)", 5, 120, 30, key="new_proj_timeout")
                memory_limit = st.selectbox("Memory Limit", ["128 MB", "256 MB", "512 MB", "1024 MB"], index=2, key="new_proj_mem")

            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("Create Project", use_container_width=True, type="primary", key="create_proj"):
                    if proj_name:
                        new_proj = {
                            "id": str(uuid.uuid4())[:8],
                            "name": proj_name,
                            "description": proj_desc,
                            "status": "Active",
                            "java_version": java_ver,
                            "defect_categories": defect_cats,
                            "executions": 0,
                            "defects_found": 0,
                            "patches_applied": 0,
                            "created_at": datetime.datetime.now().strftime("%Y-%m-%d"),
                            "last_run": "Never",
                            "owner": st.session_state.current_user.get("username", ""),
                            "language": java_ver,
                            "exec_timeout": exec_timeout,
                            "memory_limit": int(memory_limit.split()[0])
                        }
                        st.session_state.projects.append(new_proj)
                        add_audit_log("Project Created", st.session_state.current_user.get("name"), f"Project: {proj_name}")
                        st.session_state.show_new_project = False
                        st.success(f"Project '{proj_name}' created successfully!")
                        st.rerun()
                    else:
                        st.warning("Please enter a project name.")
            with col_cancel:
                if st.button("Cancel", use_container_width=True, key="cancel_proj"):
                    st.session_state.show_new_project = False
                    st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    filter_cols = st.columns(4)
    with filter_cols[0]:
        status_filter = st.selectbox("Status", ["All", "Active", "Completed", "In Progress", "Archived"], key="proj_status_filter")
    with filter_cols[1]:
        java_filter = st.selectbox("Java Version", ["All", "OpenJDK 8", "OpenJDK 11", "OpenJDK 17", "OpenJDK 21"], key="proj_java_filter")
    with filter_cols[2]:
        sort_by = st.selectbox("Sort By", ["Most Recent", "Most Defects", "Most Executions", "Name (A-Z)"], key="proj_sort")
    with filter_cols[3]:
        search_term = st.text_input("Search Projects", placeholder="Search...", key="proj_search")

    filtered = st.session_state.projects
    if status_filter != "All":
        filtered = [p for p in filtered if p.get("status") == status_filter]
    if java_filter != "All":
        filtered = [p for p in filtered if p.get("java_version") == java_filter]
    if search_term:
        filtered = [p for p in filtered if search_term.lower() in p.get("name", "").lower()]
    if sort_by == "Most Defects":
        filtered = sorted(filtered, key=lambda p: p.get("defects_found", 0), reverse=True)
    elif sort_by == "Most Executions":
        filtered = sorted(filtered, key=lambda p: p.get("executions", 0), reverse=True)
    elif sort_by == "Name (A-Z)":
        filtered = sorted(filtered, key=lambda p: p.get("name", ""))
    else:
        filtered = sorted(filtered, key=lambda p: p.get("created_at", ""), reverse=True)

    if not filtered:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'></div>
            <div class='empty-state-title'>No projects found</div>
            <div class='empty-state-text'>Create your first analysis project to get started</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for p in filtered:
            status_badge_class = {"Active": "badge-blue", "Completed": "badge-green", "In Progress": "badge-orange", "Archived": "badge-gray"}.get(p.get("status", ""), "badge-gray")
            pct = int((p.get("patches_applied", 0) / max(p.get("defects_found", 1), 1)) * 100)
            resolution_color = "#00B06B" if pct >= 70 else ("#FD8D14" if pct >= 30 else "#ED4956")

            with st.container():
                st.markdown(f"""
                <div class='card'>
                    <div class='card-header'>
                        <div class='card-avatar card-avatar-blue'>{p.get('name','')[0]}</div>
                        <div style='flex:1;'>
                            <div class='card-title'>{p.get('name','')}</div>
                            <div class='card-subtitle'>{p.get('description','')}</div>
                        </div>
                        <span class='badge {status_badge_class}'>{p.get('status','')}</span>
                    </div>
                    <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px;'>
                        <div style='text-align:center;'>
                            <div style='font-size:22px;font-weight:800;color:#0095F6;'>{p.get('executions',0)}</div>
                            <div style='font-size:11px;color:#8E8E8E;'>Executions</div>
                        </div>
                        <div style='text-align:center;'>
                            <div style='font-size:22px;font-weight:800;color:#ED4956;'>{p.get('defects_found',0)}</div>
                            <div style='font-size:11px;color:#8E8E8E;'>Defects Found</div>
                        </div>
                        <div style='text-align:center;'>
                            <div style='font-size:22px;font-weight:800;color:#00B06B;'>{p.get('patches_applied',0)}</div>
                            <div style='font-size:11px;color:#8E8E8E;'>Patches Applied</div>
                        </div>
                        <div style='text-align:center;'>
                            <div style='font-size:22px;font-weight:800;color:#FD8D14;'>{pct}%</div>
                            <div style='font-size:11px;color:#8E8E8E;'>Resolution Rate</div>
                        </div>
                    </div>
                    <div style='margin-bottom:10px;'>
                        <div style='display:flex;justify-content:space-between;font-size:11px;color:#8E8E8E;margin-bottom:3px;'>
                            <span>Resolution Progress</span><span style='color:{resolution_color};font-weight:700;'>{pct}%</span>
                        </div>
                        <div class='progress-bar-wrapper'>
                            <div class='progress-bar-fill' style='width:{pct}%;background:{resolution_color};'></div>
                        </div>
                    </div>
                    <div style='display:flex;gap:8px;flex-wrap:wrap;'>
                        <span class='tag'>{p.get('java_version','')}</span>
                        {''.join([f"<span class='tag'>{cat}</span>" for cat in p.get('defect_categories',[])])}
                    </div>
                    <div style='font-size:11px;color:#8E8E8E;margin-top:10px;'>
                        Created: {p.get('created_at','')} &bull; Last run: {p.get('last_run','')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("Execute Analysis", key=f"exec_{p['id']}", use_container_width=True):
                    st.session_state.selected_project = p
                    st.session_state.current_page = "Execute Analysis"
                    add_audit_log("Analysis Initiated", st.session_state.current_user.get("name"), f"Project: {p['name']}")
                    st.rerun()
            with col_b:
                if st.button("View Defects", key=f"view_def_{p['id']}", use_container_width=True):
                    st.session_state.selected_project = p
                    st.session_state.current_page = "Defect Analysis"
                    st.rerun()
            with col_c:
                if st.button("Archive", key=f"arch_{p['id']}", use_container_width=True):
                    p["status"] = "Archived"
                    add_audit_log("Project Archived", st.session_state.current_user.get("name"), f"Project: {p['name']}")
                    st.success(f"Project '{p['name']}' archived.")
                    st.rerun()

def page_execute_analysis():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Execute Runtime Analysis</div>", unsafe_allow_html=True)

    projects = st.session_state.projects
    if not projects:
        st.warning("No projects available. Create a project first.")
        return

    proj_names = [p["name"] for p in projects]
    default_idx = 0
    if st.session_state.selected_project:
        try:
            default_idx = proj_names.index(st.session_state.selected_project["name"])
        except ValueError:
            default_idx = 0

    tab1, tab2, tab3, tab4 = st.tabs(["Code Input", "Input Scenarios", "Execution Monitor", "Results & Traces"])

    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            selected_proj_name = st.selectbox("Select Project", proj_names, index=default_idx, key="exec_proj_select")
            selected_proj = next((p for p in projects if p["name"] == selected_proj_name), projects[0])

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='card'>
                <div style='font-size:12px;font-weight:700;color:#8E8E8E;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;'>Project Config</div>
                <div style='font-size:13px;color:#262626;margin-bottom:6px;'><strong>Java:</strong> {selected_proj.get('java_version','')}</div>
                <div style='font-size:13px;color:#262626;margin-bottom:6px;'><strong>Timeout:</strong> {selected_proj.get('exec_timeout',30)}s</div>
                <div style='font-size:13px;color:#262626;margin-bottom:6px;'><strong>Memory:</strong> {selected_proj.get('memory_limit',512)} MB</div>
                <div style='font-size:13px;color:#262626;margin-bottom:8px;'><strong>Categories:</strong></div>
                <div class='tag-row'>
                    {''.join([f"<span class='tag'>{cat}</span>" for cat in selected_proj.get('defect_categories',[])])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            java_class = st.text_input("Target Class Name", value="MainController", key="target_class")
            java_method = st.text_input("Target Method", value="processRequest", key="target_method")
            iter_count = st.slider("Iterations", 1, 100, 25, key="iter_count")

        with c2:
            default_code = '''public class MainController {
    
    private AccountService accountService;
    private Logger logger;
    
    public MainController(AccountService service) {
        this.accountService = service;
        this.logger = Logger.getLogger(MainController.class);
    }
    
    public double calculateInterest(String accountId, double rate) {
        Account account = accountService.findById(accountId);
        // Potential NullPointerException if account is null
        double balance = account.getBalance();
        
        if (rate <= 0) {
            throw new IllegalArgumentException("Rate must be positive");
        }
        
        return balance * rate;
    }
    
    public int divideBalance(int total, int count) {
        // Potential ArithmeticException: division by zero
        return total / count;
    }
    
    public void processOrder(String orderId) {
        Order order = findOrder(orderId);
        // Missing null check before processing
        order.validate();
        order.process();
        logger.info("Order processed: " + orderId);
    }
    
    private Order findOrder(String id) {
        // Returns null if not found
        return null;
    }
}'''
            java_code = st.text_area("Java Source Code", value=default_code, height=500, key="java_source_code")

        col_compile, col_execute = st.columns(2)
        with col_compile:
            if st.button("Compile Code", use_container_width=True, key="compile_btn", type="secondary"):
                config = RuntimeConfiguration(
                    selected_proj.get("defect_categories", []),
                    iter_count,
                    selected_proj.get("memory_limit", 512),
                    selected_proj.get("exec_timeout", 30)
                )
                if config.validateConfiguration():
                    compiled = exec_manager.compileCode(java_code)
                    if compiled:
                        st.success("Compilation successful. Ready for execution.")
                        st.session_state.compiled_code = java_code
                        add_audit_log("Code Compiled", st.session_state.current_user.get("name"), f"Project: {selected_proj_name}")
                    else:
                        st.error("Compilation failed. Check Java source code syntax.")
                else:
                    st.error("Invalid configuration. Check project settings.")

        with col_execute:
            if st.button("Run Full Analysis", use_container_width=True, key="run_analysis_btn", type="primary"):
                with st.spinner("Executing runtime analysis..."):
                    time.sleep(1.5)
                    code_to_run = st.session_state.get("compiled_code", java_code)
                    result = exec_manager.executeCode(code_to_run)
                    st.session_state.last_execution_result = result

                    new_exec = {
                        "id": f"E{str(uuid.uuid4())[:4].upper()}",
                        "project": selected_proj_name,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "status": "Completed" if result["status"] == "success" else "Failed",
                        "inputs_generated": iter_count,
                        "defects_found": len(result.get("errors", [])),
                        "exceptions": len(result.get("errors", [])),
                        "duration_ms": result.get("execution_time_ms", 0),
                        "memory_mb": result.get("memory_used_mb", 0),
                        "traces": len(result.get("traces", []))
                    }
                    st.session_state.execution_results.append(new_exec)

                    for p in st.session_state.projects:
                        if p["name"] == selected_proj_name:
                            p["executions"] = p.get("executions", 0) + 1
                            p["defects_found"] = p.get("defects_found", 0) + len(result.get("errors", []))
                            p["last_run"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

                    for err in result.get("errors", []):
                        new_defect = {
                            "id": f"D{str(uuid.uuid4())[:4].upper()}",
                            "project_id": selected_proj.get("id", ""),
                            "project": selected_proj_name,
                            "type": err.get("type", "Unknown"),
                            "severity": err.get("severity", "Medium"),
                            "status": "Open",
                            "method": f"{java_class}.{java_method}()",
                            "line": err.get("line", 0),
                            "description": err.get("message", ""),
                            "detected_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "notes": "",
                            "patch_id": ""
                        }
                        st.session_state.defects.append(new_defect)

                    add_audit_log("Analysis Executed", st.session_state.current_user.get("name"), f"Project: {selected_proj_name} | Result: {result['status']}")

                    if result["status"] == "success":
                        st.success(f"Analysis completed. {len(result.get('errors', []))} defects detected.")
                    else:
                        st.error(f"Analysis completed with errors. {len(result.get('errors', []))} defects detected.")

    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Input Scenario Generator</div>", unsafe_allow_html=True)

        gen_col1, gen_col2 = st.columns(2)
        with gen_col1:
            input_type = st.radio("Generation Mode", ["Random Input", "Boundary Value", "Both"], horizontal=True, key="input_gen_type")
            count = st.slider("Random Input Count", 5, 50, 10, key="rand_input_count")

            if st.button("Generate Inputs", use_container_width=True, type="primary", key="gen_inputs_btn"):
                if input_type == "Random Input":
                    generated = input_gen.generateRandomInput(count)
                elif input_type == "Boundary Value":
                    generated = input_gen.generateBoundaryInput()
                else:
                    generated = input_gen.generateRandomInput(count) + input_gen.generateBoundaryInput()

                st.session_state.generated_inputs = generated
                add_audit_log("Inputs Generated", st.session_state.current_user.get("name"), f"Mode: {input_type}, Count: {len(generated)}")

        with gen_col2:
            if st.session_state.get("generated_inputs"):
                inputs = st.session_state.generated_inputs
                st.markdown(f"<div style='font-size:13px;font-weight:600;color:#262626;margin-bottom:8px;'>{len(inputs)} scenarios generated</div>", unsafe_allow_html=True)

                types_count = {}
                for inp in inputs:
                    t = str(inp.get("type", "unknown"))
                    types_count[t] = types_count.get(t, 0) + 1

                fig_inp = go.Figure(data=[go.Bar(
                    x=list(types_count.keys()),
                    y=list(types_count.values()),
                    marker_color=['#0095F6', '#00B06B', '#FD8D14', '#ED4956', '#AB47BC'][:len(types_count)]
                )])
                fig_inp.update_layout(
                    height=160,
                    margin=dict(l=0, r=0, t=10, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig_inp, use_container_width=True, config={"displayModeBar": False})

        if st.session_state.get("generated_inputs"):
            df_inputs = pd.DataFrame(st.session_state.generated_inputs[:20])
            st.dataframe(df_inputs, use_container_width=True, hide_index=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("""
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:16px;'>
            <div class='pulse-dot'></div>
            <div style='font-size:15px;font-weight:700;color:#262626;'>Runtime Execution Monitor</div>
        </div>
        """, unsafe_allow_html=True)

        executions = st.session_state.execution_results
        if executions:
            latest = executions[-1]
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Duration", f"{latest.get('duration_ms', 0)}ms")
            with m2:
                st.metric("Memory Used", f"{latest.get('memory_mb', 0)} MB")
            with m3:
                st.metric("Traces Captured", str(latest.get("traces", 0)))
            with m4:
                status = latest.get("status", "")
                st.metric("Status", status)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px;font-weight:700;color:#262626;margin-bottom:8px;'>Execution Logs</div>", unsafe_allow_html=True)

            log_entries = [
                ("INFO", f"[{latest.get('timestamp','')}] Analysis session initiated for project: {latest.get('project','')}"),
                ("INFO", f"Compiling Java source code using {st.session_state.system_config.get('java_version','OpenJDK 17')}..."),
                ("SUCCESS", f"Compilation completed successfully"),
                ("INFO", f"Generating {latest.get('inputs_generated', 0)} input scenarios..."),
                ("INFO", f"Starting controlled execution with {latest.get('inputs_generated', 0)} scenarios"),
                ("WARN", f"Execution timeout threshold set at {st.session_state.system_config.get('exec_timeout',30)}s"),
                ("INFO", f"Runtime monitoring active - capturing traces and exceptions"),
                ("INFO", f"Detected {latest.get('defects_found', 0)} potential defects"),
                ("INFO", f"Memory peak: {latest.get('memory_mb', 0)} MB"),
                ("SUCCESS", f"Analysis completed in {latest.get('duration_ms', 0)}ms"),
            ]

            for log_type, msg in log_entries:
                css_class = {"INFO": "log-info", "WARN": "log-warn", "ERROR": "log-error", "SUCCESS": "log-success"}.get(log_type, "log-info")
                st.markdown(f"<div class='log-entry {css_class}'>{msg}</div>", unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'></div>
                <div class='empty-state-title'>No executions yet</div>
                <div class='empty-state-text'>Run an analysis from the Code Input tab to see execution logs here</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        if st.session_state.get("last_execution_result"):
            result = st.session_state.last_execution_result
            trace_data = monitor.captureTrace(result)
            exceptions = monitor.recordException(result)

            r1, r2 = st.columns(2)
            with r1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>Execution Traces</div>", unsafe_allow_html=True)
                for i, trace in enumerate(trace_data.get("traces", [])):
                    st.markdown(f"""
                    <div class='timeline-item'>
                        <div class='timeline-dot' style='background:#E8F4FD;'>
                            <span style='font-size:14px;color:#0095F6;'>{i+1}</span>
                        </div>
                        <div class='timeline-content'>
                            <div class='timeline-title'>{trace}</div>
                            <div class='timeline-sub'>{random.choice(['Method call', 'Branch evaluation', 'Object access', 'Loop iteration'])}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with r2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>Detected Exceptions</div>", unsafe_allow_html=True)
                if exceptions:
                    for exc in exceptions:
                        sev = exc.get("severity", "Medium")
                        sev_color = {"Critical": "#ED4956", "High": "#FD8D14", "Medium": "#0095F6", "Low": "#00B06B"}.get(sev, "#8E8E8E")
                        st.markdown(f"""
                        <div class='defect-card {"medium" if sev=="Medium" else ("low" if sev=="Low" else "")}'>
                            <div class='defect-title'>{exc.get('type','Unknown')}</div>
                            <div class='defect-meta'>
                                <span class='badge badge-red'>{sev}</span>
                                <span class='badge badge-gray'>Line {exc.get('line',0)}</span>
                            </div>
                            <div class='defect-desc'>{exc.get('message','No description')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("No exceptions detected in this execution run.")

                inference = infer_engine.inferBehavior(result)
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:8px;'>Behavior Inference</div>", unsafe_allow_html=True)
                inf_color = "#00B06B" if inference["inference"] == "Expected Behavior" else "#ED4956"
                st.markdown(f"""
                <div style='background:#F5F5F5;border-radius:10px;padding:14px;'>
                    <div style='font-size:14px;font-weight:700;color:{inf_color};margin-bottom:6px;'>{inference['inference']}</div>
                    <div style='font-size:12px;color:#262626;margin-bottom:6px;'>Confidence: <strong>{round(inference['confidence'],1)}%</strong></div>
                    {'<div style="font-size:12px;color:#ED4956;">Anomalies: ' + ', '.join(inference.get('anomalies',[])) + '</div>' if inference.get('anomalies') else ''}
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'></div>
                <div class='empty-state-title'>No results yet</div>
                <div class='empty-state-text'>Execute an analysis to view traces and results here</div>
            </div>
            """, unsafe_allow_html=True)

def page_defect_analysis():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Defect Analysis Center</div>", unsafe_allow_html=True)

    defects = st.session_state.defects

    severity_counts = {}
    type_counts = {}
    status_counts = {}
    for d in defects:
        sev = d.get("severity", "Unknown")
        dtype = d.get("type", "Unknown")
        status = d.get("status", "Unknown")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        type_counts[dtype] = type_counts.get(dtype, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(defects)}</div><div class='stat-label'>Total Defects</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#ED4956;'>{severity_counts.get('Critical',0)}</div><div class='stat-label'>Critical</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#FD8D14;'>{severity_counts.get('High',0)}</div><div class='stat-label'>High</div></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#0095F6;'>{severity_counts.get('Medium',0)}</div><div class='stat-label'>Medium</div></div>", unsafe_allow_html=True)
    with m5:
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#00B06B;'>{status_counts.get('Resolved',0)}</div><div class='stat-label'>Resolved</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    chart_col1, chart_col2, chart_col3 = st.columns(3)

    with chart_col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:700;color:#262626;margin-bottom:8px;'>Severity Distribution</div>", unsafe_allow_html=True)
        if severity_counts:
            fig = go.Figure(go.Bar(
                x=list(severity_counts.keys()),
                y=list(severity_counts.values()),
                marker_color=["#ED4956", "#FD8D14", "#0095F6", "#00B06B"][:len(severity_counts)],
                text=list(severity_counts.values()),
                textposition='auto'
            ))
            fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:700;color:#262626;margin-bottom:8px;'>Status Breakdown</div>", unsafe_allow_html=True)
        if status_counts:
            fig2 = go.Figure(data=[go.Pie(
                labels=list(status_counts.keys()),
                values=list(status_counts.values()),
                hole=0.55,
                marker_colors=["#ED4956", "#00B06B"],
                textinfo='percent+label'
            )])
            fig2.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:700;color:#262626;margin-bottom:8px;'>Defects by Project</div>", unsafe_allow_html=True)
        proj_counts = {}
        for d in defects:
            pr = d.get("project", "Unknown")
            proj_counts[pr] = proj_counts.get(pr, 0) + 1
        if proj_counts:
            fig3 = go.Figure(go.Bar(
                x=list(proj_counts.values()),
                y=list(proj_counts.keys()),
                orientation='h',
                marker_color='#0095F6'
            ))
            fig3.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    filter_c1, filter_c2, filter_c3, filter_c4 = st.columns(4)
    with filter_c1:
        sev_filter = st.selectbox("Severity", ["All", "Critical", "High", "Medium", "Low"], key="def_sev_filter")
    with filter_c2:
        status_filter = st.selectbox("Status", ["All", "Open", "Resolved"], key="def_status_filter")
    with filter_c3:
        proj_filter = st.selectbox("Project", ["All"] + list(set(d.get("project","") for d in defects)), key="def_proj_filter")
    with filter_c4:
        type_filter = st.selectbox("Type", ["All"] + list(set(d.get("type","") for d in defects)), key="def_type_filter")

    filtered = defects
    if sev_filter != "All":
        filtered = [d for d in filtered if d.get("severity") == sev_filter]
    if status_filter != "All":
        filtered = [d for d in filtered if d.get("status") == status_filter]
    if proj_filter != "All":
        filtered = [d for d in filtered if d.get("project") == proj_filter]
    if type_filter != "All":
        filtered = [d for d in filtered if d.get("type") == type_filter]

    st.markdown(f"<div style='font-size:13px;color:#8E8E8E;margin-bottom:12px;'>Showing {len(filtered)} of {len(defects)} defects</div>", unsafe_allow_html=True)

    for i, d in enumerate(filtered):
        sev = d.get("severity", "Medium")
        status = d.get("status", "Open")
        sev_class = {"Critical": "", "High": "medium", "Medium": "medium", "Low": "low"}.get(sev, "")
        if status == "Resolved":
            sev_class = "resolved"

        sev_badge_class = {"Critical": "badge-red", "High": "badge-orange", "Medium": "badge-blue", "Low": "badge-green"}.get(sev, "badge-gray")
        status_badge_class = "badge-green" if status == "Resolved" else "badge-red"

        with st.container():
            st.markdown(f"""
            <div class='defect-card {sev_class}'>
                <div class='defect-title'>[{d.get('id','')}] {d.get('type','')}</div>
                <div class='defect-meta'>
                    <span class='badge {sev_badge_class}'>{sev}</span>
                    <span class='badge {status_badge_class}'>{status}</span>
                    <span class='badge badge-gray'>{d.get('project','')}</span>
                </div>
                <div class='defect-desc'>{d.get('description','')}</div>
                <div style='font-size:11px;color:#8E8E8E;margin-top:8px;'>
                    Method: <strong>{d.get('method','')}</strong> &bull; Line: {d.get('line',0)} &bull; Detected: {d.get('detected_at','')}
                </div>
                {f'<div style="font-size:12px;color:#8E8E8E;margin-top:4px;font-style:italic;">Note: {d.get("notes","")}</div>' if d.get("notes") else ''}
            </div>
            """, unsafe_allow_html=True)

            action_cols = st.columns(4)
            with action_cols[0]:
                new_sev = st.selectbox("Severity", ["Critical", "High", "Medium", "Low"], index=["Critical", "High", "Medium", "Low"].index(sev), key=f"sev_{d['id']}_{i}", label_visibility="collapsed")
                if new_sev != sev:
                    d["severity"] = new_sev
                    add_audit_log("Defect Classified", st.session_state.current_user.get("name"), f"Defect: {d['id']} -> {new_sev}")
            with action_cols[1]:
                if status == "Open":
                    if st.button("Mark Resolved", key=f"resolve_{d['id']}_{i}", use_container_width=True):
                        d["status"] = "Resolved"
                        add_audit_log("Defect Resolved", st.session_state.current_user.get("name"), f"Defect: {d['id']}")
                        st.rerun()
                else:
                    if st.button("Reopen", key=f"reopen_{d['id']}_{i}", use_container_width=True):
                        d["status"] = "Open"
                        st.rerun()
            with action_cols[2]:
                note_key = f"note_{d['id']}_{i}"
                if st.button("Add Note", key=f"add_note_btn_{d['id']}_{i}", use_container_width=True):
                    st.session_state[f"show_note_{d['id']}"] = True
            with action_cols[3]:
                if st.button("Gen Patch", key=f"gen_patch_{d['id']}_{i}", use_container_width=True, type="primary"):
                    patch = patch_rec.generatePatch(d.get("type", ""))
                    new_patch = {
                        "id": f"P{str(uuid.uuid4())[:4].upper()}",
                        "defect_id": d["id"],
                        "type": patch.get("type", ""),
                        "description": patch.get("explanation", ""),
                        "code": patch.get("code", ""),
                        "status": "Pending",
                        "confidence": patch.get("confidence", 80)
                    }
                    st.session_state.patches.append(new_patch)
                    d["patch_id"] = new_patch["id"]
                    add_audit_log("Patch Generated", st.session_state.current_user.get("name"), f"Defect: {d['id']} -> Patch: {new_patch['id']}")
                    st.success(f"Patch {new_patch['id']} generated with {patch.get('confidence',80)}% confidence!")

            if st.session_state.get(f"show_note_{d['id']}"):
                note_text = st.text_input("Developer Note", key=f"note_input_{d['id']}_{i}", placeholder="Add your note...")
                if st.button("Save Note", key=f"save_note_{d['id']}_{i}"):
                    if note_text:
                        d["notes"] = note_text
                        st.session_state[f"show_note_{d['id']}"] = False
                        st.rerun()

def page_behavior_inference():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Behavior Inference Engine</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
        <div class='card-header'>
            <div class='card-avatar card-avatar-purple'>B</div>
            <div>
                <div class='card-title'>Runtime Behavior Analysis</div>
                <div class='card-subtitle'>Infer expected versus observed behavior from execution data</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Inference Results", "3D Analysis View", "Behavior Heatmap"])

    with tab1:
        executions = st.session_state.execution_results
        defects = st.session_state.defects

        if not executions:
            st.info("No execution data available. Run an analysis first.")
        else:
            for exec_rec in executions[-4:]:
                dummy_result = {
                    "status": "success" if exec_rec.get("defects_found", 0) == 0 else "fail",
                    "errors": [{"type": "RuntimeException"}] * exec_rec.get("defects_found", 0)
                }
                inference = infer_engine.inferBehavior(dummy_result)
                inf_color = "#00B06B" if inference["inference"] == "Expected Behavior" else "#ED4956"
                conf = round(inference["confidence"], 1)

                st.markdown(f"""
                <div class='card'>
                    <div style='display:flex;align-items:center;gap:12px;'>
                        <div style='flex:1;'>
                            <div style='font-size:14px;font-weight:700;color:#262626;'>{exec_rec.get('id','')} &mdash; {exec_rec.get('project','')}</div>
                            <div style='font-size:12px;color:#8E8E8E;margin-top:2px;'>{exec_rec.get('timestamp','')}</div>
                        </div>
                        <span class='badge {"badge-green" if inference["inference"]=="Expected Behavior" else "badge-red"}'>{inference['inference']}</span>
                    </div>
                    <div style='margin-top:14px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;'>
                        <div style='text-align:center;background:#FAFAFA;border-radius:8px;padding:10px;'>
                            <div style='font-size:20px;font-weight:800;color:{inf_color};'>{conf}%</div>
                            <div style='font-size:11px;color:#8E8E8E;'>Confidence</div>
                        </div>
                        <div style='text-align:center;background:#FAFAFA;border-radius:8px;padding:10px;'>
                            <div style='font-size:20px;font-weight:800;color:#262626;'>{exec_rec.get('defects_found',0)}</div>
                            <div style='font-size:11px;color:#8E8E8E;'>Anomalies</div>
                        </div>
                        <div style='text-align:center;background:#FAFAFA;border-radius:8px;padding:10px;'>
                            <div style='font-size:20px;font-weight:800;color:#0095F6;'>{exec_rec.get('traces',0)}</div>
                            <div style='font-size:11px;color:#8E8E8E;'>Trace Points</div>
                        </div>
                    </div>
                    <div style='margin-top:12px;'>
                        <div style='font-size:12px;color:#8E8E8E;margin-bottom:3px;'>Inference Confidence</div>
                        <div class='progress-bar-wrapper'>
                            <div class='progress-bar-fill' style='width:{conf}%;background:{inf_color};'></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:12px;'>3D Defect Space Visualization</div>", unsafe_allow_html=True)

        defects = st.session_state.defects
        if defects:
            severity_num = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
            x = [severity_num.get(d.get("severity","Low"), 1) for d in defects]
            y = [d.get("line", random.randint(1,300)) for d in defects]
            z = [i+1 for i in range(len(defects))]
            colors_list = [{"Open": "#ED4956", "Resolved": "#00B06B"}.get(d.get("status","Open"), "#8E8E8E") for d in defects]
            hover_text = [f"{d.get('id','')} - {d.get('type','')}<br>{d.get('project','')}" for d in defects]

            fig_3d = go.Figure(data=[go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers+text',
                marker=dict(
                    size=12,
                    color=colors_list,
                    opacity=0.85,
                    line=dict(color='white', width=1)
                ),
                text=[d.get("id","") for d in defects],
                textposition='top center',
                hovertext=hover_text,
                hoverinfo='text'
            )])

            fig_3d.update_layout(
                height=420,
                scene=dict(
                    xaxis_title='Severity Level',
                    yaxis_title='Code Line',
                    zaxis_title='Detection Order',
                    bgcolor='rgba(250,250,250,0)',
                    xaxis=dict(gridcolor='#EFEFEF', backgroundcolor='rgba(0,0,0,0)'),
                    yaxis=dict(gridcolor='#EFEFEF', backgroundcolor='rgba(0,0,0,0)'),
                    zaxis=dict(gridcolor='#EFEFEF', backgroundcolor='rgba(0,0,0,0)')
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0,r=0,t=20,b=0)
            )
            st.plotly_chart(fig_3d, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No defect data for 3D visualization.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:12px;'>Defect Frequency Heatmap</div>", unsafe_allow_html=True)

        defect_types = ["NullPointerException", "ArithmeticException", "InvalidInputException", "OverflowException", "ExecutionOrderFault", "ParseException"]
        projects_names = list(set(d.get("project","") for d in st.session_state.defects)) or ["FinanceCore", "HealthAPI", "EcomOrder"]

        z_data = []
        for dtype in defect_types:
            row = []
            for proj in projects_names:
                count = sum(1 for d in st.session_state.defects if d.get("type")==dtype and d.get("project")==proj)
                row.append(count)
            z_data.append(row)

        fig_heat = go.Figure(data=go.Heatmap(
            z=z_data,
            x=projects_names,
            y=defect_types,
            colorscale=[[0, '#E8F4FD'], [0.5, '#0095F6'], [1, '#1a1a2e']],
            text=z_data,
            texttemplate='%{text}',
            showscale=True
        ))
        fig_heat.update_layout(
            height=320,
            margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

def page_patch_generator():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Patch Recommendation Engine</div>", unsafe_allow_html=True)

    patches = st.session_state.patches
    defects = st.session_state.defects

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(patches)}</div><div class='stat-label'>Total Patches</div></div>", unsafe_allow_html=True)
    with p2:
        pending = len([p for p in patches if p.get("status") == "Pending"])
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#FD8D14;'>{pending}</div><div class='stat-label'>Pending</div></div>", unsafe_allow_html=True)
    with p3:
        applied = len([p for p in patches if p.get("status") == "Applied"])
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#00B06B;'>{applied}</div><div class='stat-label'>Applied</div></div>", unsafe_allow_html=True)
    with p4:
        avg_conf = round(sum(p.get("confidence",0) for p in patches) / max(len(patches),1), 1)
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#0095F6;'>{avg_conf}%</div><div class='stat-label'>Avg Confidence</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    tab_patches, tab_manual = st.tabs(["Generated Patches", "Manual Generation"])

    with tab_patches:
        if not patches:
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'></div>
                <div class='empty-state-title'>No patches yet</div>
                <div class='empty-state-text'>Go to Defect Analysis and click Generate Patch on any defect</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for i, patch in enumerate(patches):
                defect = next((d for d in defects if d.get("id") == patch.get("defect_id")), None)
                status_color = "#00B06B" if patch.get("status") == "Applied" else "#FD8D14"
                conf = patch.get("confidence", 80)
                conf_color = "#00B06B" if conf >= 90 else ("#FD8D14" if conf >= 75 else "#ED4956")

                with st.container():
                    st.markdown(f"""
                    <div class='card'>
                        <div style='display:flex;align-items:flex-start;gap:12px;margin-bottom:12px;'>
                            <div class='card-avatar card-avatar-green'>{i+1}</div>
                            <div style='flex:1;'>
                                <div class='card-title'>Patch [{patch.get('id','')}] - {patch.get('type','')}</div>
                                <div class='card-subtitle'>{patch.get('description','')}</div>
                            </div>
                            <div>
                                <span class='badge {"badge-green" if patch.get("status")=="Applied" else "badge-orange"}'>{patch.get('status','')}</span>
                            </div>
                        </div>
                        <div style='display:flex;gap:12px;margin-bottom:12px;align-items:center;'>
                            <div style='flex:1;'>
                                <div style='font-size:11px;color:#8E8E8E;margin-bottom:3px;'>Confidence Score</div>
                                <div style='display:flex;align-items:center;gap:8px;'>
                                    <div class='progress-bar-wrapper' style='flex:1;'>
                                        <div class='progress-bar-fill' style='width:{conf}%;background:{conf_color};'></div>
                                    </div>
                                    <span style='font-size:13px;font-weight:700;color:{conf_color};'>{conf}%</span>
                                </div>
                            </div>
                            {f'<div><span class="badge badge-gray">Defect: {patch.get("defect_id","")}</span></div>' if patch.get('defect_id') else ''}
                        </div>
                        <div class='code-block'><pre style='margin:0;font-family:Courier New;font-size:12px;color:#E8E8E8;white-space:pre-wrap;'>{patch.get('code','')}</pre></div>
                    </div>
                    """, unsafe_allow_html=True)

                    action_c1, action_c2, action_c3 = st.columns(3)
                    with action_c1:
                        if patch.get("status") == "Pending":
                            if st.button("Apply Patch", key=f"apply_patch_{patch['id']}_{i}", use_container_width=True, type="primary"):
                                patch["status"] = "Applied"
                                if defect:
                                    defect["status"] = "Resolved"
                                    defect["notes"] = f"Patch {patch['id']} applied"
                                    for p in st.session_state.projects:
                                        if p.get("name") == defect.get("project"):
                                            p["patches_applied"] = p.get("patches_applied", 0) + 1
                                add_audit_log("Patch Applied", st.session_state.current_user.get("name"), f"Patch: {patch['id']}")
                                st.success(f"Patch {patch['id']} applied successfully!")
                                st.rerun()
                    with action_c2:
                        if st.button("View Defect", key=f"view_def_patch_{patch['id']}_{i}", use_container_width=True):
                            if defect:
                                st.info(f"Defect: {defect.get('type','')} in {defect.get('method','')} - {defect.get('description','')}")
                    with action_c3:
                        if st.button("Reject", key=f"reject_patch_{patch['id']}_{i}", use_container_width=True):
                            patch["status"] = "Rejected"
                            add_audit_log("Patch Rejected", st.session_state.current_user.get("name"), f"Patch: {patch['id']}")
                            st.rerun()

    with tab_manual:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:16px;'>Generate Patch Manually</div>", unsafe_allow_html=True)

        mc1, mc2 = st.columns(2)
        with mc1:
            manual_defect_type = st.selectbox("Defect Type", ["NullPointerException", "ArithmeticException", "OverflowException", "ParseException", "InvalidInputException", "ExecutionOrderFault"], key="manual_defect_type")
            manual_context = st.text_area("Code Context (optional)", placeholder="Paste relevant Java code snippet...", height=100, key="manual_context")
        with mc2:
            if st.button("Generate Patch", use_container_width=True, type="primary", key="manual_gen_patch"):
                patch_data = patch_rec.generatePatch(manual_defect_type, manual_context)
                st.session_state.manual_generated_patch = patch_data
                add_audit_log("Manual Patch Generated", st.session_state.current_user.get("name"), f"Type: {manual_defect_type}")

            if st.session_state.get("manual_generated_patch"):
                mp = st.session_state.manual_generated_patch
                conf = mp.get("confidence", 80)
                conf_color = "#00B06B" if conf >= 90 else ("#FD8D14" if conf >= 75 else "#ED4956")
                st.markdown(f"""
                <div style='margin-top:12px;background:#F5F5F5;border-radius:10px;padding:14px;'>
                    <div style='font-size:13px;font-weight:700;color:#262626;margin-bottom:4px;'>{mp.get('type','')}</div>
                    <div style='font-size:12px;color:#8E8E8E;margin-bottom:8px;'>{mp.get('explanation','')}</div>
                    <div style='display:flex;align-items:center;gap:8px;margin-bottom:10px;'>
                        <div class='progress-bar-wrapper' style='flex:1;'>
                            <div class='progress-bar-fill' style='width:{conf}%;background:{conf_color};'></div>
                        </div>
                        <span style='font-size:12px;font-weight:700;color:{conf_color};'>{conf}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.code(mp.get("code", ""), language="java")

                if st.button("Save as Patch", use_container_width=True, key="save_manual_patch"):
                    new_patch = {
                        "id": f"P{str(uuid.uuid4())[:4].upper()}",
                        "defect_id": "",
                        "type": mp.get("type",""),
                        "description": mp.get("explanation",""),
                        "code": mp.get("code",""),
                        "status": "Pending",
                        "confidence": mp.get("confidence", 80)
                    }
                    st.session_state.patches.append(new_patch)
                    st.success(f"Patch saved as {new_patch['id']}")
                    st.session_state.manual_generated_patch = None
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

def page_reports_export():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Reports & Export Center</div>", unsafe_allow_html=True)

    tab_report, tab_logs, tab_compare, tab_charts = st.tabs(["Analysis Report", "Execution Logs", "Compare Results", "Analytics Dashboard"])

    with tab_report:
        r_c1, r_c2 = st.columns([1, 2])
        with r_c1:
            projects = st.session_state.projects
            proj_names = [p["name"] for p in projects]
            selected_proj_report = st.selectbox("Select Project for Report", proj_names if proj_names else ["No projects"], key="report_proj_select")
            report_format = st.selectbox("Export Format", ["Plain Text (.txt)", "JSON (.json)", "Markdown (.md)"], key="report_format")

            include_defects = st.checkbox("Include Defects", value=True, key="rpt_include_defects")
            include_patches = st.checkbox("Include Patches", value=True, key="rpt_include_patches")
            include_executions = st.checkbox("Include Execution History", value=True, key="rpt_include_exec")

            if st.button("Generate Report", use_container_width=True, type="primary", key="gen_report_btn"):
                proj_defects = [d for d in st.session_state.defects if d.get("project") == selected_proj_report]
                proj_executions = [e for e in st.session_state.execution_results if e.get("project") == selected_proj_report]
                report_text = exporter.exportReport(selected_proj_report, proj_defects if include_defects else [], proj_executions if include_executions else [])
                st.session_state.generated_report = report_text
                st.session_state.report_project = selected_proj_report
                add_audit_log("Report Generated", st.session_state.current_user.get("name"), f"Project: {selected_proj_report}")
                st.success("Report generated!")

        with r_c2:
            if st.session_state.get("generated_report"):
                st.markdown(f"""
                <div style='background:#1a1a2e;border-radius:12px;padding:20px;margin-bottom:12px;'>
                    <div style='font-size:12px;color:#8E8E8E;margin-bottom:8px;'>REPORT PREVIEW</div>
                </div>
                """, unsafe_allow_html=True)
                st.text_area("Report Content", value=st.session_state.generated_report, height=400, key="report_preview", label_visibility="collapsed")
                st.download_button(
                    "Download Report",
                    data=st.session_state.generated_report,
                    file_name=f"javalens_report_{st.session_state.report_project.replace(' ','_')}_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.markdown("""
                <div class='empty-state'>
                    <div class='empty-state-icon'></div>
                    <div class='empty-state-title'>No report generated</div>
                    <div class='empty-state-text'>Select a project and click Generate Report</div>
                </div>
                """, unsafe_allow_html=True)

    with tab_logs:
        logs = st.session_state.audit_logs

        l_c1, l_c2, l_c3 = st.columns(3)
        with l_c1:
            st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(logs)}</div><div class='stat-label'>Total Log Entries</div></div>", unsafe_allow_html=True)
        with l_c2:
            users_in_logs = len(set(l.get("user","") for l in logs))
            st.markdown(f"<div class='stat-card'><div class='stat-number'>{users_in_logs}</div><div class='stat-label'>Unique Users</div></div>", unsafe_allow_html=True)
        with l_c3:
            today_logs = len([l for l in logs if l.get("timestamp","").startswith(datetime.datetime.now().strftime("%Y-%m-%d"))])
            st.markdown(f"<div class='stat-card'><div class='stat-number'>{today_logs}</div><div class='stat-label'>Today's Events</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if logs:
            for log in reversed(logs[-20:]):
                st.markdown(f"""
                <div class='log-entry log-info'>
                    [{log.get('timestamp','')}] [{log.get('level','INFO')}] <strong>{log.get('user','System')}</strong> | {log.get('action','')} | {log.get('details','')}
                </div>
                """, unsafe_allow_html=True)

            log_text = exporter.exportLogs(logs)
            st.download_button(
                "Export Audit Logs",
                data=log_text,
                file_name=f"javalens_audit_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_logs"
            )

    with tab_compare:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:16px;'>Execution Result Comparison</div>", unsafe_allow_html=True)

        executions = st.session_state.execution_results
        if len(executions) < 2:
            st.info("Need at least 2 execution results to compare. Run more analyses.")
        else:
            exec_ids = [e.get("id","") + " - " + e.get("project","") + " (" + e.get("timestamp","") + ")" for e in executions]

            comp_c1, comp_c2 = st.columns(2)
            with comp_c1:
                old_sel = st.selectbox("Baseline Execution", exec_ids, key="comp_old")
            with comp_c2:
                new_sel = st.selectbox("Comparison Execution", exec_ids, index=min(1, len(exec_ids)-1), key="comp_new")

            old_idx = exec_ids.index(old_sel)
            new_idx = exec_ids.index(new_sel)
            old_exec = executions[old_idx]
            new_exec = executions[new_idx]

            old_result = {"errors": [{}] * old_exec.get("defects_found", 0)}
            new_result = {"errors": [{}] * new_exec.get("defects_found", 0)}
            comparison = comparator.compareResults(old_result, new_result)

            st.markdown(f"""
            <div class='compare-grid'>
                <div class='compare-panel'>
                    <div class='compare-panel-header'>Baseline: {old_exec.get('id','')}</div>
                    <div style='font-size:13px;color:#262626;margin-bottom:4px;'>Defects: <strong style='color:#ED4956;'>{old_exec.get('defects_found',0)}</strong></div>
                    <div style='font-size:13px;color:#262626;margin-bottom:4px;'>Exceptions: <strong>{old_exec.get('exceptions',0)}</strong></div>
                    <div style='font-size:13px;color:#262626;margin-bottom:4px;'>Duration: <strong>{old_exec.get('duration_ms',0)}ms</strong></div>
                    <div style='font-size:13px;color:#262626;'>Memory: <strong>{old_exec.get('memory_mb',0)} MB</strong></div>
                </div>
                <div class='compare-panel'>
                    <div class='compare-panel-header'>Comparison: {new_exec.get('id','')}</div>
                    <div style='font-size:13px;color:#262626;margin-bottom:4px;'>Defects: <strong style='color:{"#00B06B" if new_exec.get("defects_found",0) <= old_exec.get("defects_found",0) else "#ED4956"};'>{new_exec.get('defects_found',0)}</strong></div>
                    <div style='font-size:13px;color:#262626;margin-bottom:4px;'>Exceptions: <strong>{new_exec.get('exceptions',0)}</strong></div>
                    <div style='font-size:13px;color:#262626;margin-bottom:4px;'>Duration: <strong>{new_exec.get('duration_ms',0)}ms</strong></div>
                    <div style='font-size:13px;color:#262626;'>Memory: <strong>{new_exec.get('memory_mb',0)} MB</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            impr = comparison.get("improvement", 0)
            impr_color = "#00B06B" if impr >= 0 else "#ED4956"
            impr_label = "Improved" if impr > 0 else ("No Change" if impr == 0 else "Regressed")

            st.markdown(f"""
            <div style='background:#F5F5F5;border-radius:12px;padding:16px;margin-top:12px;text-align:center;'>
                <div style='font-size:28px;font-weight:800;color:{impr_color};'>{impr:+d} Defects</div>
                <div style='font-size:14px;font-weight:600;color:#262626;margin-top:4px;'>{impr_label} &mdash; {comparison.get('improvement_pct',0)}% change</div>
            </div>
            """, unsafe_allow_html=True)

            metrics_df = pd.DataFrame({
                "Metric": ["Defects Found", "Exceptions", "Duration (ms)", "Memory (MB)", "Traces Captured"],
                "Baseline": [old_exec.get("defects_found",0), old_exec.get("exceptions",0), old_exec.get("duration_ms",0), old_exec.get("memory_mb",0), old_exec.get("traces",0)],
                "Comparison": [new_exec.get("defects_found",0), new_exec.get("exceptions",0), new_exec.get("duration_ms",0), new_exec.get("memory_mb",0), new_exec.get("traces",0)]
            })
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(name='Baseline', x=metrics_df["Metric"], y=metrics_df["Baseline"], marker_color='#0095F6'))
            fig_comp.add_trace(go.Bar(name='Comparison', x=metrics_df["Metric"], y=metrics_df["Comparison"], marker_color='#00B06B'))
            fig_comp.update_layout(
                barmode='group',
                height=280,
                margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', y=1.1),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#F5F5F5')
            )
            st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_charts:
        st.markdown("<div class='section-title'>Analytics Dashboard</div>", unsafe_allow_html=True)

        executions = st.session_state.execution_results
        defects = st.session_state.defects

        ac1, ac2 = st.columns(2)
        with ac1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:8px;'>Defect Detection Trend</div>", unsafe_allow_html=True)
            if executions:
                dates = [e.get("timestamp","")[:10] for e in executions]
                defects_per_exec = [e.get("defects_found",0) for e in executions]
                fig_trend = px.area(x=dates, y=defects_per_exec, labels={"x": "Date", "y": "Defects"})
                fig_trend.update_traces(line_color='#0095F6', fillcolor='rgba(0,149,246,0.1)')
                fig_trend.update_layout(height=220, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        with ac2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:8px;'>Patch Confidence Distribution</div>", unsafe_allow_html=True)
            if st.session_state.patches:
                conf_values = [p.get("confidence",80) for p in st.session_state.patches]
                fig_hist = px.histogram(x=conf_values, nbins=10, labels={"x": "Confidence %"})
                fig_hist.update_traces(marker_color='#00B06B')
                fig_hist.update_layout(height=220, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        ac3, ac4 = st.columns(2)
        with ac3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:8px;'>Memory Usage Over Executions</div>", unsafe_allow_html=True)
            if executions:
                mem_data = [e.get("memory_mb",0) for e in executions]
                fig_mem = go.Figure(go.Scatter(y=mem_data, fill='tozeroy', line_color='#FD8D14', fillcolor='rgba(253,141,20,0.1)', mode='lines+markers'))
                fig_mem.update_layout(height=200, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_mem, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        with ac4:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:8px;'>Radar - Project Metrics</div>", unsafe_allow_html=True)
            if st.session_state.projects:
                proj = st.session_state.projects[0]
                categories = ["Executions", "Defects", "Patches", "Resolution", "Coverage"]
                values = [
                    min(proj.get("executions",0) * 5, 100),
                    min(proj.get("defects_found",0) * 8, 100),
                    min(proj.get("patches_applied",0) * 10, 100),
                    int((proj.get("patches_applied",0) / max(proj.get("defects_found",1),1)) * 100),
                    random.randint(60, 95)
                ]
                fig_radar = go.Figure(data=go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill='toself',
                    line_color='#0095F6',
                    fillcolor='rgba(0,149,246,0.15)'
                ))
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0,100])),
                    height=200,
                    margin=dict(l=0,r=0,t=20,b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

def page_submit_code():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Submit Java Code for Analysis</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:14px;'>Upload or Paste Java Source Code</div>", unsafe_allow_html=True)

        projects = st.session_state.projects
        proj_names = [p["name"] for p in projects]
        if proj_names:
            submit_proj = st.selectbox("Target Project", proj_names, key="submit_code_proj")
        else:
            st.warning("No projects available. Ask your analyst to create a project first.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        java_class_name = st.text_input("Class Name", placeholder="e.g., OrderProcessor", key="submit_class_name")
        java_method_names = st.text_input("Methods to Analyze (comma-separated)", placeholder="e.g., processOrder, validatePayment", key="submit_methods")

        java_code_submit = st.text_area("Java Source Code", height=350, placeholder="Paste your Java class source code here...", key="submit_java_code")

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("Validate & Submit", use_container_width=True, type="primary", key="validate_submit_btn"):
                if java_code_submit and java_class_name:
                    compiled = exec_manager.compileCode(java_code_submit)
                    if compiled:
                        st.session_state.submitted_code = {
                            "class": java_class_name,
                            "methods": [m.strip() for m in java_method_names.split(",") if m.strip()],
                            "code": java_code_submit,
                            "project": submit_proj,
                            "submitted_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        add_audit_log("Code Submitted", st.session_state.current_user.get("name"), f"Class: {java_class_name} -> {submit_proj}")
                        st.success(f"Code validated successfully! Submitted to project '{submit_proj}'.")
                    else:
                        st.error("Code validation failed. Please check your Java syntax.")
                else:
                    st.warning("Please provide class name and source code.")
        with col_s2:
            if st.button("Clear", use_container_width=True, key="clear_submit_btn"):
                st.session_state.submitted_code = None
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if st.session_state.get("submitted_code"):
            sc = st.session_state.submitted_code
            st.markdown(f"""
            <div class='card'>
                <div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:12px;'>Submission Summary</div>
                <div class='timeline-item'>
                    <div class='timeline-dot' style='background:#E6F9F1;'><span style='color:#00B06B;font-size:14px;'></span></div>
                    <div class='timeline-content'>
                        <div class='timeline-title'>Code Submitted</div>
                        <div class='timeline-sub'>{sc.get('submitted_at','')}</div>
                    </div>
                </div>
                <div style='font-size:13px;color:#262626;margin:10px 0 6px;'><strong>Class:</strong> {sc.get('class','')}</div>
                <div style='font-size:13px;color:#262626;margin-bottom:6px;'><strong>Project:</strong> {sc.get('project','')}</div>
                <div style='font-size:13px;color:#262626;margin-bottom:8px;'><strong>Methods:</strong></div>
                <div class='tag-row'>
                    {''.join([f"<span class='tag'>{m}</span>" for m in sc.get('methods',[])])}
                </div>
                <div style='margin-top:12px;'>
                    <div style='font-size:11px;color:#8E8E8E;margin-bottom:3px;'>Code Size</div>
                    <div style='font-size:16px;font-weight:700;color:#262626;'>{len(sc.get('code',''))} chars</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='card'>
                <div class='empty-state'>
                    <div class='empty-state-icon'></div>
                    <div class='empty-state-title'>No submission yet</div>
                    <div class='empty-state-text'>Paste your Java code and click Validate & Submit</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def page_review_defects():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Review Defects & Recommendations</div>", unsafe_allow_html=True)

    defects = st.session_state.defects
    patches = st.session_state.patches
    user = st.session_state.current_user

    col_main, col_side = st.columns([2, 1])

    with col_main:
        for i, d in enumerate(defects):
            related_patch = next((p for p in patches if p.get("defect_id") == d.get("id")), None)
            sev = d.get("severity", "Medium")
            sev_color = {"Critical": "#ED4956", "High": "#FD8D14", "Medium": "#0095F6", "Low": "#00B06B"}.get(sev, "#8E8E8E")

            st.markdown(f"""
            <div class='card' style='border-left:4px solid {sev_color};'>
                <div style='display:flex;align-items:flex-start;gap:12px;margin-bottom:12px;'>
                    <div>
                        <div class='defect-title'>{d.get('type','')} &mdash; {d.get('id','')}</div>
                        <div style='font-size:12px;color:#8E8E8E;margin-top:3px;'>{d.get('project','')} &bull; {d.get('method','')} &bull; Line {d.get('line',0)}</div>
                    </div>
                    <div style='margin-left:auto;display:flex;gap:6px;'>
                        <span class='badge {"badge-red" if sev=="Critical" else "badge-orange" if sev=="High" else "badge-blue" if sev=="Medium" else "badge-green"}'>{sev}</span>
                        <span class='badge {"badge-green" if d.get("status")=="Resolved" else "badge-red"}'>{d.get('status','')}</span>
                    </div>
                </div>
                <div style='font-size:13px;color:#262626;line-height:1.6;margin-bottom:10px;'>{d.get('description','')}</div>
                {f'<div style="font-size:12px;color:#8E8E8E;font-style:italic;margin-bottom:10px;">Note: {d.get("notes","")}</div>' if d.get("notes") else ''}
            </div>
            """, unsafe_allow_html=True)

            if related_patch:
                st.markdown(f"""
                <div class='card' style='margin-left:20px;margin-top:-8px;background:#F5FFF9;border-color:#B3EFD4;'>
                    <div style='font-size:12px;font-weight:700;color:#00B06B;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;'>Recommended Patch: {related_patch.get('type','')}</div>
                    <div style='font-size:12px;color:#262626;margin-bottom:8px;'>{related_patch.get('description','')}</div>
                    <div class='code-block' style='font-size:11px;'><pre style='margin:0;color:#E8E8E8;white-space:pre-wrap;'>{related_patch.get('code','')}</pre></div>
                    <div style='display:flex;align-items:center;gap:8px;margin-top:10px;'>
                        <div class='progress-bar-wrapper' style='flex:1;'>
                            <div class='progress-bar-fill' style='width:{related_patch.get("confidence",80)}%;background:#00B06B;'></div>
                        </div>
                        <span style='font-size:12px;font-weight:700;color:#00B06B;'>{related_patch.get("confidence",80)}% confidence</span>
                        <span class='badge {"badge-green" if related_patch.get("status")=="Applied" else "badge-orange"}'>{related_patch.get('status','')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            note_c1, note_c2 = st.columns(2)
            with note_c1:
                note_text = st.text_input(f"Add note for {d.get('id','')}", key=f"dev_note_{d.get('id','')}_{i}", placeholder="Developer note...", label_visibility="collapsed")
                if note_text:
                    if st.button("Save Note", key=f"save_dev_note_{d.get('id','')}_{i}"):
                        d["notes"] = note_text
                        add_audit_log("Note Added", user.get("name"), f"Defect: {d.get('id','')}")
                        st.rerun()
            with note_c2:
                if d.get("status") == "Open" and related_patch:
                    if st.button("Mark Resolved", key=f"dev_resolve_{d.get('id','')}_{i}", use_container_width=True, type="primary"):
                        d["status"] = "Resolved"
                        related_patch["status"] = "Applied"
                        for p in st.session_state.projects:
                            if p.get("name") == d.get("project"):
                                p["patches_applied"] = p.get("patches_applied",0) + 1
                        add_audit_log("Defect Marked Resolved", user.get("name"), f"Defect: {d.get('id','')}")
                        st.rerun()

    with col_side:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;color:#262626;margin-bottom:12px;'>My Summary</div>", unsafe_allow_html=True)
        my_resolved = len([d for d in defects if d.get("status") == "Resolved"])
        my_open = len([d for d in defects if d.get("status") == "Open"])
        st.markdown(f"""
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>
            <div style='text-align:center;background:#FEE8E8;border-radius:8px;padding:12px;'>
                <div style='font-size:22px;font-weight:800;color:#ED4956;'>{my_open}</div>
                <div style='font-size:11px;color:#8E8E8E;'>Open</div>
            </div>
            <div style='text-align:center;background:#E6F9F1;border-radius:8px;padding:12px;'>
                <div style='font-size:22px;font-weight:800;color:#00B06B;'>{my_resolved}</div>
                <div style='font-size:11px;color:#8E8E8E;'>Resolved</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def page_compare_results():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Compare Runtime Results</div>", unsafe_allow_html=True)

    executions = st.session_state.execution_results

    if len(executions) < 2:
        st.info("Need at least 2 execution results. Run more analyses from the Execute Analysis section.")
        return

    c1, c2 = st.columns(2)
    with c1:
        exec1_options = [f"{e.get('id','')} - {e.get('project','')} - {e.get('timestamp','')}" for e in executions]
        sel1 = st.selectbox("Before (Baseline)", exec1_options, key="cmp_exec1")
    with c2:
        sel2 = st.selectbox("After (Comparison)", exec1_options, index=min(1, len(exec1_options)-1), key="cmp_exec2")

    idx1 = exec1_options.index(sel1)
    idx2 = exec1_options.index(sel2)
    e1 = executions[idx1]
    e2 = executions[idx2]

    m1, m2, m3, m4 = st.columns(4)
    improvements = {
        "Defects": e1.get("defects_found",0) - e2.get("defects_found",0),
        "Exceptions": e1.get("exceptions",0) - e2.get("exceptions",0),
        "Duration": e1.get("duration_ms",0) - e2.get("duration_ms",0),
        "Memory": e1.get("memory_mb",0) - e2.get("memory_mb",0)
    }

    for col, (metric, diff) in zip([m1, m2, m3, m4], improvements.items()):
        diff_color = "#00B06B" if diff > 0 else ("#ED4956" if diff < 0 else "#8E8E8E")
        arrow = "+" if diff > 0 else ""
        unit = "ms" if metric == "Duration" else ("MB" if metric == "Memory" else "")
        col.markdown(f"""
        <div class='stat-card'>
            <div style='font-size:20px;font-weight:800;color:{diff_color};'>{arrow}{diff}{unit}</div>
            <div class='stat-label'>{metric} Change</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    categories = ["Defects Found", "Exceptions", "Traces", "Memory (MB)", "Duration (ms)"]
    val1 = [e1.get("defects_found",0), e1.get("exceptions",0), e1.get("traces",0), e1.get("memory_mb",0), e1.get("duration_ms",0)]
    val2 = [e2.get("defects_found",0), e2.get("exceptions",0), e2.get("traces",0), e2.get("memory_mb",0), e2.get("duration_ms",0)]

    fig_compare = go.Figure()
    fig_compare.add_trace(go.Scatterpolar(r=val1, theta=categories, fill='toself', name='Baseline', line_color='#ED4956', fillcolor='rgba(237,73,86,0.1)'))
    fig_compare.add_trace(go.Scatterpolar(r=val2, theta=categories, fill='toself', name='Comparison', line_color='#0095F6', fillcolor='rgba(0,149,246,0.1)'))
    fig_compare.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        height=350,
        showlegend=True,
        legend=dict(orientation='h', y=-0.1),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10,r=10,t=20,b=30)
    )
    st.plotly_chart(fig_compare, use_container_width=True, config={"displayModeBar": False})

def page_export_code():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Export Corrected Java Code</div>", unsafe_allow_html=True)

    defects = st.session_state.defects
    patches = st.session_state.patches

    applied_patches = [p for p in patches if p.get("status") == "Applied"]

    st.markdown(f"""
    <div class='card'>
        <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:16px;'>
            <div style='text-align:center;'>
                <div style='font-size:26px;font-weight:800;color:#0095F6;'>{len(patches)}</div>
                <div style='font-size:12px;color:#8E8E8E;'>Total Patches</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:26px;font-weight:800;color:#00B06B;'>{len(applied_patches)}</div>
                <div style='font-size:12px;color:#8E8E8E;'>Applied</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:26px;font-weight:800;color:#FD8D14;'>{len(patches)-len(applied_patches)}</div>
                <div style='font-size:12px;color:#8E8E8E;'>Pending</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if not applied_patches:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'></div>
            <div class='empty-state-title'>No patches applied yet</div>
            <div class='empty-state-text'>Apply patches from the Review Defects section to export corrected code</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for patch in applied_patches:
            defect = next((d for d in defects if d.get("id") == patch.get("defect_id")), None)
            st.markdown(f"""
            <div class='card'>
                <div style='display:flex;align-items:center;gap:10px;margin-bottom:12px;'>
                    <span class='badge badge-green'>Applied</span>
                    <div style='font-size:14px;font-weight:700;color:#262626;'>{patch.get('type','')} &mdash; {patch.get('id','')}</div>
                </div>
                <div style='font-size:13px;color:#8E8E8E;margin-bottom:10px;'>{patch.get('description','')}</div>
                <div class='code-block'><pre style='margin:0;color:#E8E8E8;white-space:pre-wrap;font-size:12px;'>{patch.get('code','')}</pre></div>
                {f'<div style="font-size:11px;color:#8E8E8E;margin-top:8px;">Applied to defect: {defect.get("id","")} in {defect.get("project","")}</div>' if defect else ''}
            </div>
            """, unsafe_allow_html=True)

        export_content = "\n\n".join([
            f"// Patch: {p.get('id','')} - {p.get('type','')}\n// Applied to: Defect {p.get('defect_id','')}\n{p.get('code','')}"
            for p in applied_patches
        ])
        st.download_button(
            "Export All Applied Patches",
            data=export_content,
            file_name=f"javalens_patches_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.java",
            mime="text/plain",
            use_container_width=True
        )

def page_system_config():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>System Configuration</div>", unsafe_allow_html=True)

    config = st.session_state.system_config

    tab_runtime, tab_categories, tab_perf = st.tabs(["Runtime Settings", "Defect Categories", "Performance"])

    with tab_runtime:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:14px;font-weight:700;margin-bottom:14px;'>Java Runtime Configuration</div>", unsafe_allow_html=True)
            new_java_ver = st.selectbox("Java Version", ["OpenJDK 8", "OpenJDK 11", "OpenJDK 17", "OpenJDK 21"], index=["OpenJDK 8","OpenJDK 11","OpenJDK 17","OpenJDK 21"].index(config.get("java_version","OpenJDK 17")), key="cfg_java_ver")
            new_timeout = st.slider("Execution Timeout (seconds)", 5, 300, config.get("exec_timeout",30), key="cfg_timeout")
            new_mem = st.slider("Memory Limit (MB)", 64, 4096, config.get("memory_limit",512), key="cfg_memory")
            new_log = st.selectbox("Log Level", ["DEBUG", "INFO", "WARN", "ERROR"], index=["DEBUG","INFO","WARN","ERROR"].index(config.get("log_level","INFO")), key="cfg_log")
            new_iters = st.slider("Max Iterations", 10, 1000, config.get("max_iterations",100), key="cfg_iters")
            if st.button("Save Runtime Config", use_container_width=True, type="primary", key="save_runtime_cfg"):
                config["java_version"] = new_java_ver
                config["exec_timeout"] = new_timeout
                config["memory_limit"] = new_mem
                config["log_level"] = new_log
                config["max_iterations"] = new_iters
                add_audit_log("System Config Updated", st.session_state.current_user.get("name"), f"Java: {new_java_ver}, Timeout: {new_timeout}s, Memory: {new_mem}MB")
                st.success("Configuration saved successfully.")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:14px;font-weight:700;margin-bottom:14px;'>Current Configuration</div>", unsafe_allow_html=True)
            cfg_display = [
                ("Java Version", config.get("java_version","")),
                ("Timeout", f"{config.get('exec_timeout',30)}s"),
                ("Memory Limit", f"{config.get('memory_limit',512)} MB"),
                ("Log Level", config.get("log_level","INFO")),
                ("Max Iterations", str(config.get("max_iterations",100)))
            ]
            for label, val in cfg_display:
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #F5F5F5;'>
                    <span style='font-size:13px;color:#8E8E8E;'>{label}</span>
                    <span style='font-size:13px;font-weight:700;color:#262626;'>{val}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_categories:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;margin-bottom:14px;'>Defect Detection Categories</div>", unsafe_allow_html=True)

        all_categories = config.get("defect_categories", [])
        active_categories = config.get("active_categories", [])

        for cat in all_categories:
            is_active = cat in active_categories
            col_cat1, col_cat2 = st.columns([3, 1])
            with col_cat1:
                st.markdown(f"""
                <div style='display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid #F5F5F5;'>
                    <div class='status-indicator {"status-green" if is_active else "status-gray"}'></div>
                    <span style='font-size:13px;font-weight:600;color:#262626;'>{cat}</span>
                    <span class='badge {"badge-green" if is_active else "badge-gray"}'>{"Active" if is_active else "Disabled"}</span>
                </div>
                """, unsafe_allow_html=True)
            with col_cat2:
                toggle_label = "Disable" if is_active else "Enable"
                if st.button(toggle_label, key=f"toggle_cat_{cat}", use_container_width=True):
                    if is_active:
                        config["active_categories"] = [c for c in active_categories if c != cat]
                    else:
                        config["active_categories"] = active_categories + [cat]
                    add_audit_log(f"Category {toggle_label}d", st.session_state.current_user.get("name"), f"Category: {cat}")
                    st.rerun()

        new_cat = st.text_input("Add New Category", placeholder="e.g., Thread Safety Issues", key="new_category_input")
        if st.button("Add Category", key="add_cat_btn"):
            if new_cat and new_cat not in all_categories:
                config["defect_categories"].append(new_cat)
                config["active_categories"].append(new_cat)
                add_audit_log("Category Added", st.session_state.current_user.get("name"), f"Category: {new_cat}")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_perf:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px;font-weight:700;margin-bottom:14px;'>Performance Metrics</div>", unsafe_allow_html=True)

        perf_data = {
            "Metric": ["CPU Usage", "Memory Usage", "Analysis Queue", "Active Analyses", "Patch Success Rate", "Avg Execution Time"],
            "Value": [f"{random.randint(20,45)}%", f"{random.randint(40,65)}%", f"{random.randint(0,5)} pending", f"{random.randint(0,3)} running", f"{random.randint(80,98)}%", f"{random.randint(800,2500)}ms"]
        }
        df_perf = pd.DataFrame(perf_data)
        st.dataframe(df_perf, use_container_width=True, hide_index=True)

        time_data = list(range(20))
        cpu_data = [random.randint(15, 55) for _ in time_data]
        mem_data = [random.randint(40, 70) for _ in time_data]

        fig_perf = go.Figure()
        fig_perf.add_trace(go.Scatter(x=time_data, y=cpu_data, name='CPU %', line=dict(color='#0095F6', width=2)))
        fig_perf.add_trace(go.Scatter(x=time_data, y=mem_data, name='Memory %', line=dict(color='#FD8D14', width=2)))
        fig_perf.update_layout(
            height=200,
            margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', y=1.1),
            xaxis=dict(showgrid=False, title="Time"),
            yaxis=dict(showgrid=True, gridcolor='#F5F5F5', title="%")
        )
        st.plotly_chart(fig_perf, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

def page_user_management():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>User Management</div>", unsafe_allow_html=True)

    users = st.session_state.users_db

    st.markdown(f"""
    <div class='card'>
        <div style='font-size:13px;font-weight:700;color:#8E8E8E;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;'>Registered Users ({len(users)})</div>
    </div>
    """, unsafe_allow_html=True)

    for email, user_data in users.items():
        role_color = {"Software Analyst": "#0095F6", "Java Developer": "#00B06B", "System Administrator": "#FD8D14"}.get(user_data.get("role",""), "#8E8E8E")
        initials = "".join([n[0] for n in user_data.get("name","U").split()[:2]]).upper()
        st.markdown(f"""
        <div class='card'>
            <div style='display:flex;align-items:center;gap:14px;'>
                <div class='avatar-circle' style='width:48px;height:48px;font-size:16px;background:linear-gradient(135deg,#667eea,#764ba2);border:none;'>{initials}</div>
                <div style='flex:1;'>
                    <div style='font-size:15px;font-weight:700;color:#262626;'>{user_data.get('name','')}</div>
                    <div style='font-size:12px;color:#8E8E8E;'>{email}</div>
                    <div style='margin-top:4px;'>
                        <span class='badge' style='background:{role_color}22;color:{role_color};'>{user_data.get('role','')}</span>
                    </div>
                </div>
                <div style='text-align:right;'>
                    <div style='font-size:12px;color:#8E8E8E;'>Joined: {user_data.get('joined','')}</div>
                    <div style='font-size:12px;color:#8E8E8E;margin-top:2px;'>{user_data.get('projects',0)} projects &bull; {user_data.get('analyses',0)} analyses</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:14px;font-weight:700;margin-bottom:14px;'>Add New User</div>", unsafe_allow_html=True)

    nu_c1, nu_c2 = st.columns(2)
    with nu_c1:
        nu_name = st.text_input("Full Name", key="nu_name")
        nu_email = st.text_input("Email", key="nu_email")
        nu_role = st.selectbox("Role", ["Software Analyst", "Java Developer", "System Administrator"], key="nu_role")
    with nu_c2:
        nu_username = st.text_input("Username", key="nu_username")
        nu_password = st.text_input("Temporary Password", type="password", key="nu_password")

        if st.button("Create User", use_container_width=True, type="primary", key="create_user_btn"):
            if nu_name and nu_email and nu_password:
                if nu_email not in st.session_state.users_db:
                    st.session_state.users_db[nu_email] = {
                        "password": hash_password(nu_password),
                        "name": nu_name,
                        "role": nu_role,
                        "username": nu_username or nu_name.lower().replace(" ","_"),
                        "bio": f"{nu_role} | JavaLens",
                        "joined": datetime.datetime.now().strftime("%Y-%m-%d"),
                        "projects": 0,
                        "analyses": 0,
                        "defects": 0
                    }
                    add_audit_log("User Created", st.session_state.current_user.get("name"), f"New user: {nu_name} ({nu_role})")
                    st.success(f"User '{nu_name}' created successfully.")
                    st.rerun()
                else:
                    st.error("A user with this email already exists.")
            else:
                st.warning("Please fill name, email, and password.")

    st.markdown("</div>", unsafe_allow_html=True)

def page_audit_logs():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Audit Log Viewer</div>", unsafe_allow_html=True)

    logs = st.session_state.audit_logs

    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(logs)}</div><div class='stat-label'>Total Events</div></div>", unsafe_allow_html=True)
    with a2:
        unique_users = len(set(l.get("user","") for l in logs))
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{unique_users}</div><div class='stat-label'>Unique Users</div></div>", unsafe_allow_html=True)
    with a3:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_count = len([l for l in logs if l.get("timestamp","").startswith(today)])
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{today_count}</div><div class='stat-label'>Today</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    filter_log_col1, filter_log_col2 = st.columns(2)
    with filter_log_col1:
        log_user_filter = st.selectbox("Filter by User", ["All"] + list(set(l.get("user","") for l in logs)), key="log_user_filter")
    with filter_log_col2:
        log_search = st.text_input("Search Logs", placeholder="Search actions or details...", key="log_search")

    filtered_logs = logs
    if log_user_filter != "All":
        filtered_logs = [l for l in filtered_logs if l.get("user") == log_user_filter]
    if log_search:
        filtered_logs = [l for l in filtered_logs if log_search.lower() in l.get("action","").lower() or log_search.lower() in l.get("details","").lower()]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for log in reversed(filtered_logs[-50:]):
        st.markdown(f"""
        <div class='log-entry log-info' style='margin-bottom:4px;'>
            <span style='color:#8E8E8E;'>[{log.get('timestamp','')}]</span>
            <strong style='color:#0095F6;'> {log.get('user','System')} </strong>
            &rarr; {log.get('action','')}
            {f'<span style="color:#8E8E8E;"> | {log.get("details","")}</span>' if log.get('details') else ''}
        </div>
        """, unsafe_allow_html=True)

    if not filtered_logs:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'></div>
            <div class='empty-state-title'>No log entries found</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if logs:
        log_export = exporter.exportLogs(filtered_logs)
        st.download_button("Export Filtered Logs", data=log_export, file_name=f"audit_logs_{datetime.datetime.now().strftime('%Y%m%d')}.txt", mime="text/plain", use_container_width=True)

def page_resource_monitor():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Resource Monitor</div>", unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)
    cpu = random.randint(20, 55)
    mem = random.randint(40, 70)
    disk = random.randint(30, 60)
    queue = random.randint(0, 8)

    with r1:
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#0095F6;'>{cpu}%</div><div class='stat-label'>CPU Usage</div></div>", unsafe_allow_html=True)
    with r2:
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#FD8D14;'>{mem}%</div><div class='stat-label'>Memory</div></div>", unsafe_allow_html=True)
    with r3:
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#00B06B;'>{disk}%</div><div class='stat-label'>Disk Usage</div></div>", unsafe_allow_html=True)
    with r4:
        st.markdown(f"<div class='stat-card'><div class='stat-number' style='color:#AB47BC;'>{queue}</div><div class='stat-label'>Queue Size</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    chart_r1, chart_r2 = st.columns(2)

    with chart_r1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:8px;'>CPU & Memory Over Time</div>", unsafe_allow_html=True)
        t = list(range(30))
        cpu_series = [random.randint(10, 70) for _ in t]
        mem_series = [random.randint(35, 75) for _ in t]
        fig_res = go.Figure()
        fig_res.add_trace(go.Scatter(x=t, y=cpu_series, name='CPU %', line=dict(color='#0095F6')))
        fig_res.add_trace(go.Scatter(x=t, y=mem_series, name='Memory %', line=dict(color='#FD8D14')))
        fig_res.update_layout(height=240, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation='h', y=1.1), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#F5F5F5'))
        st.plotly_chart(fig_res, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_r2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:8px;'>Analysis Execution Distribution</div>", unsafe_allow_html=True)
        executions = st.session_state.execution_results
        proj_exec_count = {}
        for e in executions:
            pr = e.get("project","Unknown")
            proj_exec_count[pr] = proj_exec_count.get(pr, 0) + 1

        if proj_exec_count:
            fig_dist = go.Figure(data=[go.Pie(
                labels=list(proj_exec_count.keys()),
                values=list(proj_exec_count.values()),
                hole=0.4,
                marker_colors=['#0095F6','#00B06B','#FD8D14','#ED4956']
            )])
            fig_dist.update_layout(height=240, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', showlegend=True, legend=dict(orientation='h', y=-0.1))
            st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:12px;'>Active Analysis Sessions</div>", unsafe_allow_html=True)
    running = [e for e in st.session_state.execution_results if e.get("status") == "Running"]
    if running:
        for e in running:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #F5F5F5;'>
                <div class='pulse-dot'></div>
                <div style='flex:1;'>
                    <div style='font-size:13px;font-weight:700;color:#262626;'>{e.get('id','')} &mdash; {e.get('project','')}</div>
                    <div style='font-size:11px;color:#8E8E8E;'>{e.get('timestamp','')}</div>
                </div>
                <span class='badge badge-blue'>Running</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:13px;color:#8E8E8E;'>No active sessions currently running.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def page_system_reports():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>System Usage Reports</div>", unsafe_allow_html=True)

    users = st.session_state.users_db
    projects = st.session_state.projects
    defects = st.session_state.defects
    patches = st.session_state.patches
    executions = st.session_state.execution_results

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(users)}</div><div class='stat-label'>Total Users</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(projects)}</div><div class='stat-label'>Projects</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(defects)}</div><div class='stat-label'>Defects</div></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(executions)}</div><div class='stat-label'>Executions</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:8px;'>Users by Role</div>", unsafe_allow_html=True)
        role_counts = {}
        for u in users.values():
            r = u.get("role","Unknown")
            role_counts[r] = role_counts.get(r, 0) + 1
        fig_roles = go.Figure(data=[go.Pie(labels=list(role_counts.keys()), values=list(role_counts.values()), hole=0.4, marker_colors=['#0095F6','#00B06B','#FD8D14'])])
        fig_roles.update_layout(height=220, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', showlegend=True)
        st.plotly_chart(fig_roles, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with ch2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:8px;'>Project Status Distribution</div>", unsafe_allow_html=True)
        status_counts = {}
        for p in projects:
            s = p.get("status","Unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        fig_status = go.Figure(data=[go.Bar(x=list(status_counts.keys()), y=list(status_counts.values()), marker_color=['#0095F6','#00B06B','#FD8D14','#8E8E8E'])])
        fig_status.update_layout(height=220, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig_status, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    report_summary = f"""JAVALENS SYSTEM USAGE REPORT
{'='*60}
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated By: {st.session_state.current_user.get('name','')}

PLATFORM SUMMARY
{'-'*40}
Total Users: {len(users)}
Total Projects: {len(projects)}
Total Defects: {len(defects)}
Total Patches: {len(patches)}
Total Executions: {len(executions)}

USER BREAKDOWN
{'-'*40}
{chr(10).join([f"{u.get('name','')} ({u.get('role','')}) - Joined: {u.get('joined','')}" for u in users.values()])}

PROJECT SUMMARY
{'-'*40}
{chr(10).join([f"{p.get('name','')} | Status: {p.get('status','')} | Defects: {p.get('defects_found',0)} | Patches: {p.get('patches_applied',0)}" for p in projects])}
"""

    st.download_button("Export System Report", data=report_summary, file_name=f"system_report_{datetime.datetime.now().strftime('%Y%m%d')}.txt", mime="text/plain", use_container_width=True)

def main():
    if not st.session_state.logged_in:
        show_auth_page()
        return

    user = st.session_state.current_user
    role = user.get("role", "")
    page = st.session_state.current_page

    st.markdown("<div style='padding:0 0 0 0;'>", unsafe_allow_html=True)
    render_navbar()
    st.markdown("<div style='padding:0 24px;max-width:1400px;margin:0 auto;'>", unsafe_allow_html=True)

    if role == "Software Analyst":
        page_map = {
            "Dashboard": page_dashboard,
            "Projects": page_projects,
            "Execute Analysis": page_execute_analysis,
            "Defect Analysis": page_defect_analysis,
            "Behavior Inference": page_behavior_inference,
            "Patch Generator": page_patch_generator,
            "Reports & Export": page_reports_export,
        }
    elif role == "Java Developer":
        page_map = {
            "Dashboard": page_dashboard,
            "Submit Code": page_submit_code,
            "Review Defects": page_review_defects,
            "Apply Patches": page_patch_generator,
            "Compare Results": page_compare_results,
            "Export Code": page_export_code,
        }
    else:
        page_map = {
            "Dashboard": page_dashboard,
            "System Config": page_system_config,
            "User Management": page_user_management,
            "Audit Logs": page_audit_logs,
            "Resource Monitor": page_resource_monitor,
            "System Reports": page_system_reports,
        }

    current_func = page_map.get(page, page_dashboard)
    current_func()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

main()