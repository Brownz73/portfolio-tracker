# ============================================================================
# 💎 ULTIMATE PORTFOLIO TRACKER PRO - BULLETPROOF EDITION 💎
# ============================================================================
# The most comprehensive portfolio management system with:
#
# 📊 CORE FEATURES:
# - Real-time price tracking with smart caching
# - Multi-portfolio support (Retirement, Trading, Long-term, etc.)
# - Full transaction history with tax lot tracking
# - Cloud backup/restore via JSON export
#
# 🚨 INTELLIGENT ALERTS:
# - Smart buy/sell signals with scoring
# - Custom price alerts (above/below/% change)
# - Push notifications via Email & Telegram
# - Volume spike detection
# - Earnings date warnings
#
# 📈 TECHNICAL ANALYSIS:
# - 15+ technical indicators
# - Pattern recognition
# - Support/Resistance levels
# - Technical score (-100 to +100)
# - Interactive charts with indicators
#
# 💰 PORTFOLIO ANALYTICS:
# - Performance vs S&P 500 benchmark
# - Sector allocation
# - Risk metrics (Beta, Sharpe, VaR)
# - Dividend income tracking
# - Tax-loss harvesting suggestions
# - Concentration risk warnings
#
# 🪙 MULTI-ASSET SUPPORT:
# - Stocks & ETFs
# - Cryptocurrencies (BTC, ETH, etc.)
# - Options tracking (covered calls/puts)
#
# 📱 MOBILE OPTIMIZED:
# - Touch-friendly interface
# - PWA-ready design
# - Works perfectly on iPhone
#
# ============================================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import time
import json
import hashlib
import requests
from typing import Dict, List, Optional, Tuple, Any
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Portfolio Pro Ultimate",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# COMPREHENSIVE CSS STYLING
# ============================================================================

st.markdown("""
<style>
    /* ===== ROOT VARIABLES ===== */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        --danger-gradient: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        --warning-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --info-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --gold-gradient: linear-gradient(135deg, #f5af19 0%, #f12711 100%);
        --crypto-gradient: linear-gradient(135deg, #f7931a 0%, #ffcc00 100%);
    }
    
    /* ===== MAIN HEADER ===== */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 15px 0;
        margin-bottom: 10px;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    
    /* ===== PORTFOLIO SELECTOR ===== */
    .portfolio-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .portfolio-badge-active {
        background: var(--primary-gradient);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .portfolio-badge-inactive {
        background: #f0f0f0;
        color: #666;
    }
    
    /* ===== ALERT CARDS ===== */
    .alert-critical {
        background: var(--danger-gradient);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .alert-opportunity {
        background: var(--success-gradient);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.3);
    }
    
    .alert-warning {
        background: var(--warning-gradient);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    .alert-info {
        background: var(--info-gradient);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    .alert-earnings {
        background: var(--gold-gradient);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    .alert-crypto {
        background: var(--crypto-gradient);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    /* ===== STAT CARDS ===== */
    .stat-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 5px 0;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stat-change {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 5px;
    }
    
    /* ===== POSITION CARDS ===== */
    .position-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .position-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .position-card-profit {
        border-left-color: #38ef7d;
    }
    
    .position-card-loss {
        border-left-color: #ff416c;
    }
    
    .position-card-crypto {
        border-left-color: #f7931a;
    }
    
    .position-card-option {
        border-left-color: #9c27b0;
    }
    
    /* ===== TICKER BADGE ===== */
    .ticker-badge {
        display: inline-block;
        background: var(--primary-gradient);
        color: white;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .ticker-badge-crypto {
        background: var(--crypto-gradient);
    }
    
    .ticker-badge-option {
        background: linear-gradient(135deg, #9c27b0 0%, #e040fb 100%);
    }
    
    /* ===== SIGNAL BADGES ===== */
    .signal-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 3px;
        text-transform: uppercase;
    }
    
    .signal-strong-buy { background: #00c853; color: white; }
    .signal-buy { background: #69f0ae; color: #1b5e20; }
    .signal-hold { background: #fff176; color: #f57f17; }
    .signal-sell { background: #ff8a80; color: #b71c1c; }
    .signal-strong-sell { background: #ff1744; color: white; }
    
    /* ===== TECHNICAL INDICATORS ===== */
    .indicator-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.7rem;
        font-weight: 500;
        margin: 2px;
    }
    
    .bullish { background: #c8e6c9; color: #2e7d32; }
    .bearish { background: #ffcdd2; color: #c62828; }
    .neutral { background: #e0e0e0; color: #424242; }
    
    /* ===== RISK METER ===== */
    .risk-meter-container {
        background: #f0f0f0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .risk-meter-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .risk-low { background: var(--success-gradient); }
    .risk-medium { background: linear-gradient(90deg, #ffd54f 0%, #ff9800 100%); }
    .risk-high { background: var(--danger-gradient); }
    
    /* ===== NEWS CARDS ===== */
    .news-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .news-card-bullish { border-left-color: #38ef7d; }
    .news-card-bearish { border-left-color: #ff416c; }
    
    /* ===== OPTIONS TABLE ===== */
    .option-call { color: #2e7d32; font-weight: 600; }
    .option-put { color: #c62828; font-weight: 600; }
    
    /* ===== TAX LOT TABLE ===== */
    .tax-lot-wash { background: #fff3e0; }
    .tax-lot-ltcg { background: #e8f5e9; }
    .tax-lot-stcg { background: #fce4ec; }
    
    /* ===== DIVIDEND CALENDAR ===== */
    .dividend-upcoming {
        background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    /* ===== BENCHMARK COMPARISON ===== */
    .benchmark-card {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        color: white;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* ===== MOBILE RESPONSIVE ===== */
    @media (max-width: 768px) {
        .main-header { font-size: 1.6rem; }
        .stat-value { font-size: 1.4rem; }
        .position-card { padding: 15px; }
        .stat-card { padding: 15px; }
    }
    
    /* ===== SCROLLBAR STYLING ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    /* ===== LOADING ANIMATION ===== */
    .loading-pulse {
        animation: loadingPulse 1.5s ease-in-out infinite;
    }
    
    @keyframes loadingPulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }
    
    /* ===== NOTIFICATION BADGE ===== */
    .notification-badge {
        display: inline-block;
        background: #ff1744;
        color: white;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 10px;
        margin-left: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables with comprehensive defaults"""
    
    defaults = {
        # Multi-portfolio support
        'portfolios': {
            'Main Portfolio': {},
            'Retirement (401k/IRA)': {},
            'Trading Account': {},
            'Long-term Holdings': {},
            'Crypto Portfolio': {},
        },
        'active_portfolio': 'Main Portfolio',
        
        # Watchlist
        'watchlist': [],
        
        # Options tracking
        'options_positions': [],
        
        # Alerts
        'price_alerts': {},
        'triggered_alerts': [],
        
        # Notifications
        'notification_settings': {
            'email_enabled': False,
            'email_address': '',
            'email_smtp_server': 'smtp.gmail.com',
            'email_smtp_port': 587,
            'email_password': '',
            'telegram_enabled': False,
            'telegram_bot_token': '',
            'telegram_chat_id': '',
            'notify_on_profit_target': True,
            'notify_on_stop_loss': True,
            'notify_on_earnings': True,
            'notify_on_dividend': True,
            'notify_on_price_alert': True,
        },
        
        # Transaction history (for tax lots)
        'transaction_history': [],
        
        # Tax lots
        'tax_lots': {},
        
        # Dividends received
        'dividends_received': [],
        
        # App settings
        'settings': {
            'take_profit_threshold': 50,
            'stop_loss_threshold': -20,
            'volume_spike_multiplier': 3.0,
            'show_technicals': True,
            'show_news': True,
            'show_fundamentals': True,
            'show_options_greeks': True,
            'benchmark_symbol': 'SPY',
            'tax_rate_stcg': 0.35,  # Short-term capital gains
            'tax_rate_ltcg': 0.15,  # Long-term capital gains
            'enable_tax_loss_harvesting': True,
            'wash_sale_window': 30,
            'default_chart_period': '6mo',
            'currency': 'USD',
        },
        
        # Caching
        'cached_data': {},
        'cache_timestamp': {},
        'benchmark_data': None,
        'benchmark_timestamp': None,
        
        # UI state
        'last_refresh': None,
        'auto_refresh': False,
        'refresh_interval': 30,
        'dark_mode': False,
        
        # Pending notifications
        'pending_notifications': [],
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Ensure all portfolios exist
    if 'portfolios' in st.session_state:
        for portfolio_name in defaults['portfolios'].keys():
            if portfolio_name not in st.session_state.portfolios:
                st.session_state.portfolios[portfolio_name] = {}

init_session_state()

# ============================================================================
# NOTIFICATION SYSTEM
# ============================================================================

class NotificationManager:
    """Handle email and Telegram notifications"""
    
    @staticmethod
    def send_email(subject: str, body: str) -> bool:
        """Send email notification"""
        settings = st.session_state.notification_settings
        
        if not settings['email_enabled'] or not settings['email_address']:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = settings['email_address']
            msg['To'] = settings['email_address']
            msg['Subject'] = f"📊 Portfolio Pro: {subject}"
            
            # HTML email body
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #667eea;">💎 Portfolio Pro Alert</h2>
                <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
                    {body}
                </div>
                <p style="color: #888; font-size: 12px; margin-top: 20px;">
                    Sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            server = smtplib.SMTP(settings['email_smtp_server'], settings['email_smtp_port'])
            server.starttls()
            server.login(settings['email_address'], settings['email_password'])
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            st.session_state.pending_notifications.append({
                'type': 'email_error',
                'message': f"Failed to send email: {str(e)}",
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    @staticmethod
    def send_telegram(message: str) -> bool:
        """Send Telegram notification"""
        settings = st.session_state.notification_settings
        
        if not settings['telegram_enabled'] or not settings['telegram_bot_token']:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{settings['telegram_bot_token']}/sendMessage"
            payload = {
                'chat_id': settings['telegram_chat_id'],
                'text': f"💎 Portfolio Pro\n\n{message}",
                'parse_mode': 'HTML'
            }
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            return False
    
    @staticmethod
    def notify(title: str, message: str, notification_type: str = 'info'):
        """Send notification via all enabled channels"""
        settings = st.session_state.notification_settings
        
        # Check if this type of notification is enabled
        type_mapping = {
            'profit_target': 'notify_on_profit_target',
            'stop_loss': 'notify_on_stop_loss',
            'earnings': 'notify_on_earnings',
            'dividend': 'notify_on_dividend',
            'price_alert': 'notify_on_price_alert',
        }
        
        if notification_type in type_mapping:
            if not settings.get(type_mapping[notification_type], True):
                return
        
        full_message = f"<b>{title}</b>\n{message}"
        
        if settings['email_enabled']:
            NotificationManager.send_email(title, message)
        
        if settings['telegram_enabled']:
            NotificationManager.send_telegram(full_message)
        
        # Store for in-app display
        st.session_state.pending_notifications.append({
            'title': title,
            'message': message,
            'type': notification_type,
            'timestamp': datetime.now().isoformat(),
            'read': False
        })

# ============================================================================
# DATA FETCHING & CACHING
# ============================================================================

class DataFetcher:
    """Unified data fetcher for stocks, crypto, and options"""
    
    CACHE_DURATION = 60  # seconds
    
    # Crypto mapping for yfinance
    CRYPTO_MAP = {
        'BTC': 'BTC-USD',
        'ETH': 'ETH-USD',
        'SOL': 'SOL-USD',
        'ADA': 'ADA-USD',
        'DOT': 'DOT-USD',
        'DOGE': 'DOGE-USD',
        'XRP': 'XRP-USD',
        'AVAX': 'AVAX-USD',
        'MATIC': 'MATIC-USD',
        'LINK': 'LINK-USD',
        'UNI': 'UNI-USD',
        'ATOM': 'ATOM-USD',
        'LTC': 'LTC-USD',
        'BCH': 'BCH-USD',
        'SHIB': 'SHIB-USD',
    }
    
    @staticmethod
    def is_crypto(ticker: str) -> bool:
        """Check if ticker is a cryptocurrency"""
        return ticker.upper() in DataFetcher.CRYPTO_MAP or ticker.upper().endswith('-USD')
    
    @staticmethod
    def normalize_ticker(ticker: str) -> str:
        """Normalize ticker for yfinance"""
        ticker = ticker.upper().strip()
        if ticker in DataFetcher.CRYPTO_MAP:
            return DataFetcher.CRYPTO_MAP[ticker]
        return ticker
    
    @staticmethod
    def get_data(ticker: str, force_refresh: bool = False) -> Optional[Dict]:
        """Fetch comprehensive data for any asset type"""
        
        original_ticker = ticker.upper().strip()
        normalized_ticker = DataFetcher.normalize_ticker(ticker)
        is_crypto = DataFetcher.is_crypto(original_ticker)
        
        cache_key = f"data_{normalized_ticker}"
        current_time = datetime.now()
        
        # Check cache
        if not force_refresh and cache_key in st.session_state.cached_data:
            cache_time = st.session_state.cache_timestamp.get(cache_key)
            if cache_time and (current_time - cache_time).seconds < DataFetcher.CACHE_DURATION:
                return st.session_state.cached_data[cache_key]
        
        try:
            stock = yf.Ticker(normalized_ticker)
            info = stock.info
            
            # Get current price
            current_price = (
                info.get('currentPrice') or 
                info.get('regularMarketPrice') or
                info.get('previousClose') or
                info.get('regularMarketPreviousClose')
            )
            
            if not current_price:
                # Try to get from history
                hist = stock.history(period="5d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                else:
                    return None
            
            # Get historical data
            hist = stock.history(period="1y")
            
            # Calculate technical indicators
            technicals = DataFetcher._calculate_technicals(hist, current_price) if not hist.empty else {}
            
            # Base data structure
            data = {
                # Identity
                'ticker': original_ticker,
                'normalized_ticker': normalized_ticker,
                'is_crypto': is_crypto,
                'asset_type': 'crypto' if is_crypto else 'stock',
                
                # Price data
                'price': current_price,
                'previous_close': info.get('previousClose') or info.get('regularMarketPreviousClose', current_price),
                'open': info.get('open') or info.get('regularMarketOpen', current_price),
                'day_high': info.get('dayHigh') or info.get('regularMarketDayHigh', current_price),
                'day_low': info.get('dayLow') or info.get('regularMarketDayLow', current_price),
                'change': info.get('regularMarketChange', 0),
                'change_pct': info.get('regularMarketChangePercent', 0),
                
                # Company/Asset info
                'name': info.get('shortName') or info.get('name', original_ticker),
                'sector': info.get('sector', 'Crypto' if is_crypto else 'Unknown'),
                'industry': info.get('industry', 'Cryptocurrency' if is_crypto else 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'description': info.get('longBusinessSummary', ''),
                'website': info.get('website', ''),
                'country': info.get('country', ''),
                'employees': info.get('fullTimeEmployees', 0),
                
                # 52-week data
                'week_52_high': info.get('fiftyTwoWeekHigh', current_price),
                'week_52_low': info.get('fiftyTwoWeekLow', current_price),
                'week_52_change': info.get('52WeekChange', 0),
                
                # Volume
                'volume': info.get('volume') or info.get('regularMarketVolume', 0),
                'avg_volume': info.get('averageVolume', 0),
                'avg_volume_10d': info.get('averageDailyVolume10Day', 0),
                
                # Valuation (stocks only)
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'peg_ratio': info.get('pegRatio'),
                'price_to_book': info.get('priceToBook'),
                'price_to_sales': info.get('priceToSalesTrailing12Months'),
                'enterprise_value': info.get('enterpriseValue'),
                'ev_to_revenue': info.get('enterpriseToRevenue'),
                'ev_to_ebitda': info.get('enterpriseToEbitda'),
                
                # Dividends
                'dividend_yield': (info.get('dividendYield') or 0) * 100,
                'dividend_rate': info.get('dividendRate', 0),
                'ex_dividend_date': info.get('exDividendDate'),
                'payout_ratio': info.get('payoutRatio'),
                'five_year_avg_dividend_yield': info.get('fiveYearAvgDividendYield'),
                
                # Analyst data
                'target_low': info.get('targetLowPrice'),
                'target_mean': info.get('targetMeanPrice'),
                'target_median': info.get('targetMedianPrice'),
                'target_high': info.get('targetHighPrice'),
                'recommendation': info.get('recommendationKey', 'none'),
                'recommendation_mean': info.get('recommendationMean'),
                'num_analysts': info.get('numberOfAnalystOpinions', 0),
                
                # Risk metrics
                'beta': info.get('beta', 1.0 if not is_crypto else 2.0),
                'short_ratio': info.get('shortRatio'),
                'short_percent': info.get('shortPercentOfFloat'),
                'held_percent_insiders': info.get('heldPercentInsiders'),
                'held_percent_institutions': info.get('heldPercentInstitutions'),
                
                # Financials
                'revenue': info.get('totalRevenue', 0),
                'revenue_per_share': info.get('revenuePerShare'),
                'profit_margin': info.get('profitMargins'),
                'operating_margin': info.get('operatingMargins'),
                'gross_margin': info.get('grossMargins'),
                'ebitda_margin': info.get('ebitdaMargins'),
                'roe': info.get('returnOnEquity'),
                'roa': info.get('returnOnAssets'),
                'debt_to_equity': info.get('debtToEquity'),
                'current_ratio': info.get('currentRatio'),
                'quick_ratio': info.get('quickRatio'),
                'free_cash_flow': info.get('freeCashflow'),
                'operating_cash_flow': info.get('operatingCashflow'),
                'total_cash': info.get('totalCash'),
                'total_debt': info.get('totalDebt'),
                'book_value': info.get('bookValue'),
                'eps_trailing': info.get('trailingEps'),
                'eps_forward': info.get('forwardEps'),
                
                # Earnings
                'earnings_date': info.get('earningsTimestamp'),
                'earnings_quarterly_growth': info.get('earningsQuarterlyGrowth'),
                'revenue_growth': info.get('revenueGrowth'),
                
                # Technical indicators
                'technicals': technicals,
                
                # Historical data for charts
                'history': hist,
                
                # Crypto specific
                'circulating_supply': info.get('circulatingSupply'),
                'max_supply': info.get('maxSupply'),
                
                # Timestamp
                'fetched_at': current_time.isoformat()
            }
            
            # Cache the data
            st.session_state.cached_data[cache_key] = data
            st.session_state.cache_timestamp[cache_key] = current_time
            
            return data
            
        except Exception as e:
            return None
    
    @staticmethod
    def _calculate_technicals(hist: pd.DataFrame, current_price: float) -> Dict:
        """Calculate comprehensive technical indicators"""
        
        if hist.empty or len(hist) < 20:
            return {'signals': [], 'score': 0}
        
        close = hist['Close']
        high = hist['High']
        low = hist['Low']
        volume = hist['Volume']
        
        technicals = {}
        signals = []
        
        # ===== MOVING AVERAGES =====
        technicals['sma_5'] = close.rolling(window=5).mean().iloc[-1] if len(close) >= 5 else None
        technicals['sma_10'] = close.rolling(window=10).mean().iloc[-1] if len(close) >= 10 else None
        technicals['sma_20'] = close.rolling(window=20).mean().iloc[-1] if len(close) >= 20 else None
        technicals['sma_50'] = close.rolling(window=50).mean().iloc[-1] if len(close) >= 50 else None
        technicals['sma_100'] = close.rolling(window=100).mean().iloc[-1] if len(close) >= 100 else None
        technicals['sma_200'] = close.rolling(window=200).mean().iloc[-1] if len(close) >= 200 else None
        
        technicals['ema_9'] = close.ewm(span=9, adjust=False).mean().iloc[-1]
        technicals['ema_12'] = close.ewm(span=12, adjust=False).mean().iloc[-1]
        technicals['ema_21'] = close.ewm(span=21, adjust=False).mean().iloc[-1]
        technicals['ema_26'] = close.ewm(span=26, adjust=False).mean().iloc[-1]
        technicals['ema_50'] = close.ewm(span=50, adjust=False).mean().iloc[-1] if len(close) >= 50 else None
        
        # MA Signals
        if technicals['sma_20']:
            if current_price > technicals['sma_20']:
                signals.append(('Above SMA20', 'bullish'))
            else:
                signals.append(('Below SMA20', 'bearish'))
        
        if technicals['sma_50']:
            if current_price > technicals['sma_50']:
                signals.append(('Above SMA50', 'bullish'))
            else:
                signals.append(('Below SMA50', 'bearish'))
        
        if technicals['sma_200']:
            if current_price > technicals['sma_200']:
                signals.append(('Above SMA200', 'bullish'))
            else:
                signals.append(('Below SMA200', 'bearish'))
        
        # Golden/Death Cross
        if technicals['sma_50'] and technicals['sma_200']:
            if technicals['sma_50'] > technicals['sma_200']:
                signals.append(('Golden Cross', 'bullish'))
            else:
                signals.append(('Death Cross', 'bearish'))
        
        # ===== MACD =====
        macd_line = technicals['ema_12'] - technicals['ema_26']
        signal_line = close.ewm(span=9, adjust=False).mean().iloc[-1]
        macd_histogram = macd_line - signal_line
        
        technicals['macd_line'] = macd_line
        technicals['macd_signal'] = signal_line
        technicals['macd_histogram'] = macd_histogram
        
        if macd_histogram > 0:
            signals.append(('MACD Bullish', 'bullish'))
        else:
            signals.append(('MACD Bearish', 'bearish'))
        
        # MACD Zero Line Cross
        if macd_line > 0:
            signals.append(('MACD Above Zero', 'bullish'))
        else:
            signals.append(('MACD Below Zero', 'bearish'))
        
        # ===== RSI =====
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        technicals['rsi'] = rsi.iloc[-1]
        technicals['rsi_prev'] = rsi.iloc[-2] if len(rsi) > 1 else rsi.iloc[-1]
        
        if technicals['rsi'] > 80:
            signals.append(('RSI Extremely Overbought', 'bearish'))
        elif technicals['rsi'] > 70:
            signals.append(('RSI Overbought', 'bearish'))
        elif technicals['rsi'] < 20:
            signals.append(('RSI Extremely Oversold', 'bullish'))
        elif technicals['rsi'] < 30:
            signals.append(('RSI Oversold', 'bullish'))
        else:
            signals.append(('RSI Neutral', 'neutral'))
        
        # RSI Divergence (simple check)
        if len(close) >= 14:
            price_higher = close.iloc[-1] > close.iloc[-14]
            rsi_higher = technicals['rsi'] > rsi.iloc[-14]
            
            if price_higher and not rsi_higher:
                signals.append(('Bearish RSI Divergence', 'bearish'))
            elif not price_higher and rsi_higher:
                signals.append(('Bullish RSI Divergence', 'bullish'))
        
        # ===== STOCHASTIC =====
        lowest_low = low.rolling(window=14).min()
        highest_high = high.rolling(window=14).max()
        stoch_k = ((close - lowest_low) / (highest_high - lowest_low) * 100)
        stoch_d = stoch_k.rolling(window=3).mean()
        
        technicals['stoch_k'] = stoch_k.iloc[-1]
        technicals['stoch_d'] = stoch_d.iloc[-1]
        
        if technicals['stoch_k'] > 80 and technicals['stoch_d'] > 80:
            signals.append(('Stochastic Overbought', 'bearish'))
        elif technicals['stoch_k'] < 20 and technicals['stoch_d'] < 20:
            signals.append(('Stochastic Oversold', 'bullish'))
        
        # Stochastic crossover
        if technicals['stoch_k'] > technicals['stoch_d']:
            signals.append(('Stoch K > D', 'bullish'))
        else:
            signals.append(('Stoch K < D', 'bearish'))
        
        # ===== BOLLINGER BANDS =====
        bb_period = 20
        bb_std = close.rolling(window=bb_period).std()
        technicals['bb_middle'] = technicals['sma_20']
        technicals['bb_upper'] = technicals['bb_middle'] + (bb_std.iloc[-1] * 2)
        technicals['bb_lower'] = technicals['bb_middle'] - (bb_std.iloc[-1] * 2)
        technicals['bb_width'] = (technicals['bb_upper'] - technicals['bb_lower']) / technicals['bb_middle'] * 100
        
        # Bollinger Band position
        if current_price > technicals['bb_upper']:
            signals.append(('Above Upper BB', 'bearish'))
        elif current_price < technicals['bb_lower']:
            signals.append(('Below Lower BB', 'bullish'))
        else:
            bb_position = (current_price - technicals['bb_lower']) / (technicals['bb_upper'] - technicals['bb_lower'])
            if bb_position > 0.8:
                signals.append(('Near Upper BB', 'bearish'))
            elif bb_position < 0.2:
                signals.append(('Near Lower BB', 'bullish'))
        
        # BB Squeeze
        if technicals['bb_width'] < 5:  # Tight bands
            signals.append(('BB Squeeze', 'neutral'))
        
        # ===== ATR (AVERAGE TRUE RANGE) =====
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        technicals['atr'] = tr.rolling(window=14).mean().iloc[-1]
        technicals['atr_percent'] = (technicals['atr'] / current_price) * 100
        
        # ===== ADX (TREND STRENGTH) =====
        try:
            plus_dm = high.diff()
            minus_dm = -low.diff()
            plus_dm[plus_dm < 0] = 0
            minus_dm[minus_dm < 0] = 0
            
            tr_smooth = tr.rolling(window=14).sum()
            plus_di = 100 * (plus_dm.rolling(window=14).sum() / tr_smooth)
            minus_di = 100 * (minus_dm.rolling(window=14).sum() / tr_smooth)
            
            dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
            adx = dx.rolling(window=14).mean()
            
            technicals['adx'] = adx.iloc[-1] if not np.isnan(adx.iloc[-1]) else 25
            technicals['plus_di'] = plus_di.iloc[-1]
            technicals['minus_di'] = minus_di.iloc[-1]
            
            if technicals['adx'] > 40:
                signals.append(('Strong Trend', 'neutral'))
            elif technicals['adx'] < 20:
                signals.append(('Weak Trend', 'neutral'))
        except:
            technicals['adx'] = 25
        
        # ===== VOLUME ANALYSIS =====
        avg_volume_20 = volume.rolling(window=20).mean().iloc[-1]
        technicals['volume_ratio'] = volume.iloc[-1] / avg_volume_20 if avg_volume_20 > 0 else 1
        
        if technicals['volume_ratio'] > 3:
            signals.append(('Extreme Volume', 'neutral'))
        elif technicals['volume_ratio'] > 2:
            signals.append(('High Volume', 'neutral'))
        elif technicals['volume_ratio'] < 0.5:
            signals.append(('Low Volume', 'neutral'))
        
        # On-Balance Volume trend
        obv = (np.sign(close.diff()) * volume).cumsum()
        obv_sma = obv.rolling(window=20).mean()
        if obv.iloc[-1] > obv_sma.iloc[-1]:
            signals.append(('OBV Bullish', 'bullish'))
        else:
            signals.append(('OBV Bearish', 'bearish'))
        
        # ===== SUPPORT & RESISTANCE =====
        technicals['resistance_1'] = high.tail(20).max()
        technicals['support_1'] = low.tail(20).min()
        technicals['resistance_2'] = high.tail(50).max() if len(high) >= 50 else technicals['resistance_1']
        technicals['support_2'] = low.tail(50).min() if len(low) >= 50 else technicals['support_1']
        
        # Pivot Points
        pivot = (high.iloc[-1] + low.iloc[-1] + close.iloc[-1]) / 3
        technicals['pivot'] = pivot
        technicals['r1'] = 2 * pivot - low.iloc[-1]
        technicals['s1'] = 2 * pivot - high.iloc[-1]
        technicals['r2'] = pivot + (high.iloc[-1] - low.iloc[-1])
        technicals['s2'] = pivot - (high.iloc[-1] - low.iloc[-1])
        
        # ===== MOMENTUM =====
        technicals['momentum_10'] = ((current_price / close.iloc[-10]) - 1) * 100 if len(close) >= 10 else 0
        technicals['momentum_20'] = ((current_price / close.iloc[-20]) - 1) * 100 if len(close) >= 20 else 0
        
        # ===== WILLIAMS %R =====
        williams_r = -100 * (highest_high - close) / (highest_high - lowest_low)
        technicals['williams_r'] = williams_r.iloc[-1]
        
        if technicals['williams_r'] > -20:
            signals.append(('Williams %R Overbought', 'bearish'))
        elif technicals['williams_r'] < -80:
            signals.append(('Williams %R Oversold', 'bullish'))
        
        # ===== CCI (COMMODITY CHANNEL INDEX) =====
        typical_price = (high + low + close) / 3
        cci = (typical_price - typical_price.rolling(window=20).mean()) / (0.015 * typical_price.rolling(window=20).std())
        technicals['cci'] = cci.iloc[-1]
        
        if technicals['cci'] > 100:
            signals.append(('CCI Overbought', 'bearish'))
        elif technicals['cci'] < -100:
            signals.append(('CCI Oversold', 'bullish'))
        
        # ===== CALCULATE OVERALL SCORE =====
        bullish_count = sum(1 for s in signals if s[1] == 'bullish')
        bearish_count = sum(1 for s in signals if s[1] == 'bearish')
        total_signals = bullish_count + bearish_count
        
        if total_signals > 0:
            technicals['score'] = ((bullish_count - bearish_count) / total_signals) * 100
        else:
            technicals['score'] = 0
        
        technicals['signals'] = signals
        technicals['bullish_count'] = bullish_count
        technicals['bearish_count'] = bearish_count
        
        return technicals
    
    @staticmethod
    def get_benchmark_data(symbol: str = 'SPY') -> Optional[pd.DataFrame]:
        """Fetch benchmark data for comparison"""
        
        current_time = datetime.now()
        
        # Check cache
        if st.session_state.benchmark_data is not None:
            if st.session_state.benchmark_timestamp:
                age = (current_time - st.session_state.benchmark_timestamp).seconds
                if age < 300:  # 5 minute cache
                    return st.session_state.benchmark_data
        
        try:
            benchmark = yf.Ticker(symbol)
            hist = benchmark.history(period="1y")
            
            if not hist.empty:
                st.session_state.benchmark_data = hist
                st.session_state.benchmark_timestamp = current_time
                return hist
        except:
            pass
        
        return None
    
    @staticmethod
    def get_options_chain(ticker: str) -> Optional[Dict]:
        """Fetch options chain data"""
        try:
            stock = yf.Ticker(ticker)
            
            # Get available expiration dates
            expirations = stock.options
            
            if not expirations:
                return None
            
            options_data = {
                'expirations': list(expirations),
                'chains': {}
            }
            
            # Get chain for nearest expiration
            for exp in expirations[:3]:  # First 3 expirations
                try:
                    chain = stock.option_chain(exp)
                    options_data['chains'][exp] = {
                        'calls': chain.calls.to_dict('records'),
                        'puts': chain.puts.to_dict('records')
                    }
                except:
                    continue
            
            return options_data
        except:
            return None
    
    @staticmethod
    def get_news(ticker: str, limit: int = 10) -> List[Dict]:
        """Fetch news for a ticker"""
        try:
            stock = yf.Ticker(DataFetcher.normalize_ticker(ticker))
            news = stock.news[:limit] if stock.news else []
            
            return [{
                'title': item.get('title', ''),
                'publisher': item.get('publisher', ''),
                'link': item.get('link', ''),
                'published': datetime.fromtimestamp(item.get('providerPublishTime', 0)),
                'type': item.get('type', ''),
                'thumbnail': item.get('thumbnail', {}).get('resolutions', [{}])[0].get('url', '') if item.get('thumbnail') else '',
            } for item in news]
        except:
            return []

# ============================================================================
# POSITION & PORTFOLIO ANALYZERS
# ============================================================================

class PositionAnalyzer:
    """Comprehensive position analysis"""
    
    @staticmethod
    def analyze(ticker: str, position: Dict, data: Dict, settings: Dict) -> Dict:
        """Full position analysis with signals"""
        
        shares = position['shares']
        avg_cost = position['avg_cost']
        current_price = data['price']
        
        # ===== BASIC CALCULATIONS =====
        gain_loss_pct = ((current_price - avg_cost) / avg_cost) * 100
        gain_loss_dollars = (current_price - avg_cost) * shares
        total_value = current_price * shares
        cost_basis = avg_cost * shares
        
        # ===== 52-WEEK ANALYSIS =====
        week_52_range = data['week_52_high'] - data['week_52_low']
        pct_in_range = ((current_price - data['week_52_low']) / week_52_range * 100) if week_52_range > 0 else 50
        pct_from_high = ((data['week_52_high'] - current_price) / data['week_52_high'] * 100)
        pct_from_low = ((current_price - data['week_52_low']) / data['week_52_low'] * 100)
        
        # ===== GENERATE SIGNALS =====
        signals = []
        sell_score = 0
        buy_score = 0
        
        # ----- PROFIT TAKING -----
        if gain_loss_pct >= 100:
            signals.append({
                'type': 'STRONG_SELL',
                'title': '🎉 DOUBLED YOUR MONEY!',
                'message': f'Position up {gain_loss_pct:.1f}% - consider taking profits',
                'priority': 1,
                'category': 'profit_target'
            })
            sell_score += 45
        elif gain_loss_pct >= 75:
            signals.append({
                'type': 'SELL',
                'title': '📈 Exceptional Gains',
                'message': f'Up {gain_loss_pct:.1f}% - consider scaling out',
                'priority': 2,
                'category': 'profit_target'
            })
            sell_score += 35
        elif gain_loss_pct >= settings['take_profit_threshold']:
            signals.append({
                'type': 'SELL',
                'title': f"📈 Profit Target Hit",
                'message': f"Up {gain_loss_pct:.1f}% (target: {settings['take_profit_threshold']}%)",
                'priority': 2,
                'category': 'profit_target'
            })
            sell_score += 30
        elif gain_loss_pct >= 30:
            signals.append({
                'type': 'INFO',
                'title': '📈 Solid Gains',
                'message': 'Consider setting a trailing stop',
                'priority': 4,
                'category': 'info'
            })
            sell_score += 15
        
        # ----- STOP LOSS -----
        if gain_loss_pct <= -50:
            signals.append({
                'type': 'STRONG_SELL',
                'title': '🚨 CRITICAL LOSS',
                'message': 'Down 50%+ - evaluate if thesis still valid',
                'priority': 1,
                'category': 'stop_loss'
            })
            sell_score += 50
        elif gain_loss_pct <= -30:
            signals.append({
                'type': 'SELL',
                'title': '⚠️ Major Loss',
                'message': 'Consider cutting losses or averaging down',
                'priority': 2,
                'category': 'stop_loss'
            })
            sell_score += 30
        elif gain_loss_pct <= settings['stop_loss_threshold']:
            signals.append({
                'type': 'WARNING',
                'title': '💰 Stop Loss Level',
                'message': f"Down {abs(gain_loss_pct):.1f}% - at your stop loss threshold",
                'priority': 2,
                'category': 'stop_loss'
            })
            sell_score += 20
        
        # ----- 52-WEEK POSITION -----
        if pct_from_high <= 2:
            signals.append({
                'type': 'SELL',
                'title': '🔝 At 52-Week HIGH',
                'message': 'Stock at peak - high resistance',
                'priority': 2,
                'category': 'technical'
            })
            sell_score += 25
        elif pct_from_high <= 5:
            signals.append({
                'type': 'INFO',
                'title': '📊 Near 52-Week High',
                'message': f'Only {pct_from_high:.1f}% from peak',
                'priority': 4,
                'category': 'technical'
            })
            sell_score += 10
        
        if pct_from_low <= 5:
            signals.append({
                'type': 'BUY',
                'title': '📉 Near 52-Week LOW',
                'message': 'Potential value opportunity',
                'priority': 2,
                'category': 'technical'
            })
            buy_score += 25
        elif pct_from_low <= 15:
            signals.append({
                'type': 'INFO',
                'title': '📊 Near 52-Week Low',
                'message': f'{pct_from_low:.1f}% from bottom',
                'priority': 4,
                'category': 'technical'
            })
            buy_score += 10
        
        # ----- ANALYST TARGETS -----
        if data.get('target_mean') and data['target_mean'] > 0:
            upside = ((data['target_mean'] - current_price) / current_price * 100)
            
            if current_price >= data['target_mean']:
                signals.append({
                    'type': 'SELL',
                    'title': '🎯 Above Analyst Target',
                    'message': f"Trading above ${data['target_mean']:.2f} consensus",
                    'priority': 2,
                    'category': 'analyst'
                })
                sell_score += 20
            elif upside >= 50:
                signals.append({
                    'type': 'STRONG_BUY',
                    'title': f"🎯 {upside:.0f}% Upside Potential",
                    'message': f"Target ${data['target_mean']:.2f}",
                    'priority': 2,
                    'category': 'analyst'
                })
                buy_score += 35
            elif upside >= 25:
                signals.append({
                    'type': 'BUY',
                    'title': f"🎯 {upside:.0f}% Upside",
                    'message': f"Target ${data['target_mean']:.2f}",
                    'priority': 3,
                    'category': 'analyst'
                })
                buy_score += 20
        
        # ----- ANALYST RATING -----
        rec = data.get('recommendation', 'none')
        if rec in ['strong_buy', 'strongBuy']:
            signals.append({
                'type': 'STRONG_BUY',
                'title': '👍 Analyst: STRONG BUY',
                'message': f"{data.get('num_analysts', 0)} analysts recommend",
                'priority': 2,
                'category': 'analyst'
            })
            buy_score += 25
        elif rec == 'buy':
            signals.append({
                'type': 'BUY',
                'title': '👍 Analyst: BUY',
                'message': 'Wall Street recommends buying',
                'priority': 3,
                'category': 'analyst'
            })
            buy_score += 15
        elif rec == 'sell':
            signals.append({
                'type': 'SELL',
                'title': '👎 Analyst: SELL',
                'message': 'Wall Street recommends selling',
                'priority': 2,
                'category': 'analyst'
            })
            sell_score += 20
        elif rec in ['strong_sell', 'strongSell']:
            signals.append({
                'type': 'STRONG_SELL',
                'title': '👎 Analyst: STRONG SELL',
                'message': 'Strong sell recommendation',
                'priority': 1,
                'category': 'analyst'
            })
            sell_score += 30
        
        # ----- VOLUME ANALYSIS -----
        volume_ratio = data['volume'] / data['avg_volume'] if data['avg_volume'] > 0 else 1
        
        if volume_ratio >= settings['volume_spike_multiplier']:
            signals.append({
                'type': 'WARNING',
                'title': '🔥 VOLUME SPIKE',
                'message': f'{volume_ratio:.1f}x average - check for news!',
                'priority': 1,
                'category': 'volume'
            })
        elif volume_ratio >= 2:
            signals.append({
                'type': 'INFO',
                'title': '📊 High Volume',
                'message': f'{volume_ratio:.1f}x average volume',
                'priority': 4,
                'category': 'volume'
            })
        
        # ----- TECHNICAL SIGNALS -----
        technicals = data.get('technicals', {})
        
        if technicals:
            tech_score = technicals.get('score', 0)
            
            if tech_score >= 60:
                signals.append({
                    'type': 'STRONG_BUY',
                    'title': '📊 Strong Bullish Technicals',
                    'message': f'Technical score: {tech_score:.0f}/100',
                    'priority': 2,
                    'category': 'technical'
                })
                buy_score += 30
            elif tech_score >= 30:
                signals.append({
                    'type': 'BUY',
                    'title': '📊 Bullish Technicals',
                    'message': f'Technical score: {tech_score:.0f}/100',
                    'priority': 3,
                    'category': 'technical'
                })
                buy_score += 15
            elif tech_score <= -60:
                signals.append({
                    'type': 'STRONG_SELL',
                    'title': '📊 Strong Bearish Technicals',
                    'message': f'Technical score: {tech_score:.0f}/100',
                    'priority': 2,
                    'category': 'technical'
                })
                sell_score += 30
            elif tech_score <= -30:
                signals.append({
                    'type': 'SELL',
                    'title': '📊 Bearish Technicals',
                    'message': f'Technical score: {tech_score:.0f}/100',
                    'priority': 3,
                    'category': 'technical'
                })
                sell_score += 15
            
            # RSI extremes
            rsi = technicals.get('rsi', 50)
            if rsi >= 80:
                signals.append({
                    'type': 'SELL',
                    'title': '📉 RSI Extremely Overbought',
                    'message': f'RSI at {rsi:.0f} - extended',
                    'priority': 2,
                    'category': 'technical'
                })
                sell_score += 20
            elif rsi >= 70:
                signals.append({
                    'type': 'INFO',
                    'title': '📉 RSI Overbought',
                    'message': f'RSI at {rsi:.0f}',
                    'priority': 4,
                    'category': 'technical'
                })
                sell_score += 10
            elif rsi <= 20:
                signals.append({
                    'type': 'BUY',
                    'title': '📈 RSI Extremely Oversold',
                    'message': f'RSI at {rsi:.0f} - potential bounce',
                    'priority': 2,
                    'category': 'technical'
                })
                buy_score += 20
            elif rsi <= 30:
                signals.append({
                    'type': 'INFO',
                    'title': '📈 RSI Oversold',
                    'message': f'RSI at {rsi:.0f}',
                    'priority': 4,
                    'category': 'technical'
                })
                buy_score += 10
        
        # ----- EARNINGS WARNING -----
        if data.get('earnings_date'):
            try:
                earnings_ts = data['earnings_date']
                if isinstance(earnings_ts, (int, float)):
                    earnings_date = datetime.fromtimestamp(earnings_ts)
                    days_to_earnings = (earnings_date - datetime.now()).days
                    
                    if 0 <= days_to_earnings <= 7:
                        signals.append({
                            'type': 'WARNING',
                            'title': '📅 Earnings Coming',
                            'message': f'Earnings in {days_to_earnings} days - expect volatility',
                            'priority': 1,
                            'category': 'earnings'
                        })
                    elif -1 <= days_to_earnings < 0:
                        signals.append({
                            'type': 'WARNING',
                            'title': '📅 Earnings Today/Yesterday',
                            'message': 'Check earnings results',
                            'priority': 1,
                            'category': 'earnings'
                        })
            except:
                pass
        
        # ----- DIVIDEND INFO -----
        if data.get('dividend_yield', 0) >= 5:
            signals.append({
                'type': 'BUY',
                'title': '💵 High Dividend Yield',
                'message': f"{data['dividend_yield']:.2f}% yield",
                'priority': 3,
                'category': 'dividend'
            })
            buy_score += 10
        elif data.get('dividend_yield', 0) >= 3:
            signals.append({
                'type': 'INFO',
                'title': '💵 Good Dividend',
                'message': f"{data['dividend_yield']:.2f}% yield",
                'priority': 5,
                'category': 'dividend'
            })
        
        if data.get('ex_dividend_date'):
            try:
                ex_div_date = datetime.fromtimestamp(data['ex_dividend_date'])
                days_to_ex_div = (ex_div_date - datetime.now()).days
                
                if 0 <= days_to_ex_div <= 7:
                    signals.append({
                        'type': 'INFO',
                        'title': '📅 Ex-Dividend Coming',
                        'message': f'Ex-div in {days_to_ex_div} days',
                        'priority': 3,
                        'category': 'dividend'
                    })
            except:
                pass
        
        # ----- VALUE METRICS -----
        pe = data.get('pe_ratio')
        if pe:
            if pe < 10:
                signals.append({
                    'type': 'BUY',
                    'title': '💎 Very Low P/E',
                    'message': f'P/E of {pe:.1f} - potentially undervalued',
                    'priority': 3,
                    'category': 'valuation'
                })
                buy_score += 15
            elif pe < 15:
                signals.append({
                    'type': 'INFO',
                    'title': '💎 Low P/E',
                    'message': f'P/E of {pe:.1f}',
                    'priority': 5,
                    'category': 'valuation'
                })
                buy_score += 5
            elif pe > 50:
                signals.append({
                    'type': 'WARNING',
                    'title': '⚠️ Very High P/E',
                    'message': f'P/E of {pe:.1f} - expensive valuation',
                    'priority': 3,
                    'category': 'valuation'
                })
                sell_score += 10
        
        # ----- SHORT INTEREST -----
        if data.get('short_percent') and data['short_percent'] > 0.2:
            signals.append({
                'type': 'WARNING',
                'title': '⚠️ High Short Interest',
                'message': f"{data['short_percent']*100:.1f}% of float shorted",
                'priority': 2,
                'category': 'risk'
            })
        
        # ----- INSIDER/INSTITUTIONAL HOLDINGS -----
        if data.get('held_percent_insiders') and data['held_percent_insiders'] > 0.3:
            signals.append({
                'type': 'INFO',
                'title': '👔 High Insider Ownership',
                'message': f"{data['held_percent_insiders']*100:.1f}% insider owned",
                'priority': 5,
                'category': 'ownership'
            })
        
        # ===== SORT SIGNALS =====
        signals.sort(key=lambda x: x['priority'])
        
        # ===== DETERMINE OVERALL ACTION =====
        net_score = buy_score - sell_score
        
        if sell_score >= 60 and sell_score > buy_score * 1.5:
            action = "STRONG SELL"
            action_color = "#ff1744"
        elif sell_score >= 40 and sell_score > buy_score:
            action = "CONSIDER SELLING"
            action_color = "#ff5722"
        elif buy_score >= 60 and buy_score > sell_score * 1.5:
            action = "STRONG BUY"
            action_color = "#00c853"
        elif buy_score >= 40 and buy_score > sell_score:
            action = "CONSIDER BUYING"
            action_color = "#69f0ae"
        else:
            action = "HOLD"
            action_color = "#ffd54f"
        
        # ===== RISK SCORE =====
        risk_score = 0
        
        # Beta risk
        beta = data.get('beta', 1) or 1
        risk_score += min(abs(beta - 1) * 15, 25)
        
        # Position loss risk
        if gain_loss_pct < -20:
            risk_score += 15
        if gain_loss_pct < -40:
            risk_score += 15
        
        # Volume spike risk
        if volume_ratio > 3:
            risk_score += 10
        
        # Short interest risk
        if data.get('short_percent', 0) > 0.15:
            risk_score += 10
        
        # Earnings risk
        if data.get('earnings_date'):
            try:
                earnings_ts = data['earnings_date']
                if isinstance(earnings_ts, (int, float)):
                    days_to_earnings = (datetime.fromtimestamp(earnings_ts) - datetime.now()).days
                    if 0 <= days_to_earnings <= 7:
                        risk_score += 15
            except:
                pass
        
        # Crypto risk
        if data.get('is_crypto'):
            risk_score += 20
        
        risk_score = min(risk_score, 100)
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'shares': shares,
            'avg_cost': avg_cost,
            'gain_loss_pct': gain_loss_pct,
            'gain_loss_dollars': gain_loss_dollars,
            'total_value': total_value,
            'cost_basis': cost_basis,
            'pct_in_range': pct_in_range,
            'pct_from_high': pct_from_high,
            'pct_from_low': pct_from_low,
            'signals': signals,
            'action': action,
            'action_color': action_color,
            'sell_score': sell_score,
            'buy_score': buy_score,
            'risk_score': risk_score,
            'data': data,
            'is_crypto': data.get('is_crypto', False),
        }


class PortfolioAnalyzer:
    """Portfolio-level analysis"""
    
    @staticmethod
    def calculate_metrics(portfolio: Dict, analyses: Dict) -> Dict:
        """Calculate comprehensive portfolio metrics"""
        
        if not portfolio or not analyses:
            return {}
        
        total_value = 0
        total_cost = 0
        total_gain = 0
        total_dividends_annual = 0
        
        sector_values = {}
        position_weights = {}
        asset_types = {'stock': 0, 'crypto': 0}
        
        weighted_beta = 0
        
        for ticker, analysis in analyses.items():
            if not analysis:
                continue
            
            total_value += analysis['total_value']
            total_cost += analysis['cost_basis']
            total_gain += analysis['gain_loss_dollars']
            
            # Sector allocation
            sector = analysis['data'].get('sector', 'Unknown')
            sector_values[sector] = sector_values.get(sector, 0) + analysis['total_value']
            
            # Asset type
            asset_type = 'crypto' if analysis.get('is_crypto') else 'stock'
            asset_types[asset_type] = asset_types.get(asset_type, 0) + analysis['total_value']
            
            # Dividends
            div_yield = analysis['data'].get('dividend_yield', 0)
            total_dividends_annual += analysis['total_value'] * (div_yield / 100)
        
        # Calculate weights and weighted metrics
        for ticker, analysis in analyses.items():
            if analysis and total_value > 0:
                weight = analysis['total_value'] / total_value
                position_weights[ticker] = weight * 100
                
                beta = analysis['data'].get('beta', 1) or 1
                weighted_beta += weight * beta
        
        # Convert sector to percentages
        sector_allocation = {}
        for sector, value in sector_values.items():
            if total_value > 0:
                sector_allocation[sector] = (value / total_value) * 100
        
        # Asset type percentages
        asset_allocation = {}
        for asset_type, value in asset_types.items():
            if total_value > 0:
                asset_allocation[asset_type] = (value / total_value) * 100
        
        # Return metrics
        total_return_pct = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
        
        # Concentration risk
        max_weight = max(position_weights.values()) if position_weights else 0
        
        # Diversification score (0-100, higher is better)
        num_positions = len(analyses)
        num_sectors = len(sector_allocation)
        
        if num_positions >= 15 and num_sectors >= 8:
            diversification = 90
        elif num_positions >= 10 and num_sectors >= 5:
            diversification = 70
        elif num_positions >= 5 and num_sectors >= 3:
            diversification = 50
        else:
            diversification = 30
        
        if max_weight > 40:
            diversification -= 30
        elif max_weight > 25:
            diversification -= 15
        
        diversification = max(0, min(100, diversification))
        
        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'total_gain': total_gain,
            'total_return_pct': total_return_pct,
            'total_dividends_annual': total_dividends_annual,
            'dividend_yield': (total_dividends_annual / total_value * 100) if total_value > 0 else 0,
            'sector_allocation': sector_allocation,
            'asset_allocation': asset_allocation,
            'position_weights': position_weights,
            'portfolio_beta': weighted_beta,
            'num_positions': num_positions,
            'num_sectors': num_sectors,
            'concentration_risk': max_weight,
            'diversification_score': diversification,
        }
    
    @staticmethod
    def calculate_benchmark_comparison(portfolio: Dict, analyses: Dict, 
                                       benchmark_data: pd.DataFrame) -> Dict:
        """Compare portfolio performance to benchmark"""
        
        if benchmark_data is None or benchmark_data.empty:
            return {}
        
        # Calculate benchmark returns for different periods
        try:
            current_bench = benchmark_data['Close'].iloc[-1]
            
            periods = {
                '1D': 1,
                '1W': 5,
                '1M': 21,
                '3M': 63,
                '6M': 126,
                'YTD': None,  # Special handling
                '1Y': 252,
            }
            
            benchmark_returns = {}
            
            for period, days in periods.items():
                if period == 'YTD':
                    # Find first trading day of year
                    year_start = datetime(datetime.now().year, 1, 1)
                    ytd_data = benchmark_data[benchmark_data.index >= year_start]
                    if not ytd_data.empty:
                        start_price = ytd_data['Close'].iloc[0]
                        benchmark_returns['YTD'] = ((current_bench - start_price) / start_price) * 100
                elif days and len(benchmark_data) > days:
                    start_price = benchmark_data['Close'].iloc[-days]
                    benchmark_returns[period] = ((current_bench - start_price) / start_price) * 100
            
            return benchmark_returns
        except:
            return {}


class TaxLotTracker:
    """Track tax lots for tax-loss harvesting"""
    
    @staticmethod
    def add_lot(ticker: str, shares: float, cost: float, date: datetime):
        """Add a new tax lot"""
        if ticker not in st.session_state.tax_lots:
            st.session_state.tax_lots[ticker] = []
        
        st.session_state.tax_lots[ticker].append({
            'shares': shares,
            'cost_per_share': cost,
            'purchase_date': date.isoformat(),
            'id': hashlib.md5(f"{ticker}{shares}{cost}{date.isoformat()}".encode()).hexdigest()[:8]
        })
    
    @staticmethod
    def get_lots(ticker: str) -> List[Dict]:
        """Get all tax lots for a ticker"""
        return st.session_state.tax_lots.get(ticker, [])
    
    @staticmethod
    def analyze_lots(ticker: str, current_price: float) -> Dict:
        """Analyze tax lots for a position"""
        lots = TaxLotTracker.get_lots(ticker)
        
        if not lots:
            return {}
        
        today = datetime.now()
        ltcg_threshold = today - timedelta(days=365)
        wash_sale_window = st.session_state.settings.get('wash_sale_window', 30)
        wash_sale_start = today - timedelta(days=wash_sale_window)
        
        long_term_gains = 0
        short_term_gains = 0
        long_term_losses = 0
        short_term_losses = 0
        
        harvestable_losses = []
        
        for lot in lots:
            purchase_date = datetime.fromisoformat(lot['purchase_date'])
            gain_per_share = current_price - lot['cost_per_share']
            total_gain = gain_per_share * lot['shares']
            
            is_long_term = purchase_date < ltcg_threshold
            
            if total_gain >= 0:
                if is_long_term:
                    long_term_gains += total_gain
                else:
                    short_term_gains += total_gain
            else:
                if is_long_term:
                    long_term_losses += abs(total_gain)
                else:
                    short_term_losses += abs(total_gain)
                
                # Tax-loss harvesting candidate
                harvestable_losses.append({
                    'lot_id': lot['id'],
                    'shares': lot['shares'],
                    'loss': abs(total_gain),
                    'is_long_term': is_long_term,
                    'purchase_date': purchase_date,
                    'days_held': (today - purchase_date).days
                })
        
        # Calculate tax impact
        tax_rate_stcg = st.session_state.settings.get('tax_rate_stcg', 0.35)
        tax_rate_ltcg = st.session_state.settings.get('tax_rate_ltcg', 0.15)
        
        tax_liability = (short_term_gains * tax_rate_stcg) + (long_term_gains * tax_rate_ltcg)
        potential_tax_savings = (short_term_losses * tax_rate_stcg) + (long_term_losses * tax_rate_ltcg)
        
        return {
            'long_term_gains': long_term_gains,
            'short_term_gains': short_term_gains,
            'long_term_losses': long_term_losses,
            'short_term_losses': short_term_losses,
            'tax_liability': tax_liability,
            'potential_tax_savings': potential_tax_savings,
            'harvestable_losses': sorted(harvestable_losses, key=lambda x: x['loss'], reverse=True),
            'total_lots': len(lots)
        }

# ============================================================================
# CHART BUILDERS
# ============================================================================

class ChartBuilder:
    """Build interactive Plotly charts"""
    
    @staticmethod
    def price_chart(ticker: str, history: pd.DataFrame, 
                   avg_cost: Optional[float] = None,
                   technicals: Optional[Dict] = None,
                   show_indicators: bool = True) -> go.Figure:
        """Build comprehensive price chart"""
        
        if history.empty:
            return None
        
        # Determine number of rows
        num_rows = 3 if show_indicators else 1
        row_heights = [0.6, 0.2, 0.2] if show_indicators else [1.0]
        
        subplot_titles = (f'{ticker} Price', 'Volume', 'RSI') if show_indicators else (f'{ticker} Price',)
        
        fig = make_subplots(
            rows=num_rows, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=row_heights,
            subplot_titles=subplot_titles
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=history.index,
                open=history['Open'],
                high=history['High'],
                low=history['Low'],
                close=history['Close'],
                name='Price',
                increasing_line_color='#26a69a',
                decreasing_line_color='#ef5350'
            ),
            row=1, col=1
        )
        
        # Moving averages
        if len(history) >= 20:
            sma20 = history['Close'].rolling(window=20).mean()
            fig.add_trace(
                go.Scatter(x=history.index, y=sma20, name='SMA 20',
                          line=dict(color='#ff9800', width=1)),
                row=1, col=1
            )
        
        if len(history) >= 50:
            sma50 = history['Close'].rolling(window=50).mean()
            fig.add_trace(
                go.Scatter(x=history.index, y=sma50, name='SMA 50',
                          line=dict(color='#2196f3', width=1)),
                row=1, col=1
            )
        
        if len(history) >= 200:
            sma200 = history['Close'].rolling(window=200).mean()
            fig.add_trace(
                go.Scatter(x=history.index, y=sma200, name='SMA 200',
                          line=dict(color='#9c27b0', width=1)),
                row=1, col=1
            )
        
        # Bollinger Bands
        if len(history) >= 20:
            bb_middle = history['Close'].rolling(window=20).mean()
            bb_std = history['Close'].rolling(window=20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            fig.add_trace(
                go.Scatter(x=history.index, y=bb_upper, name='BB Upper',
                          line=dict(color='rgba(128, 128, 128, 0.5)', width=1, dash='dot'),
                          showlegend=False),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=history.index, y=bb_lower, name='BB Lower',
                          line=dict(color='rgba(128, 128, 128, 0.5)', width=1, dash='dot'),
                          fill='tonexty', fillcolor='rgba(128, 128, 128, 0.1)',
                          showlegend=False),
                row=1, col=1
            )
        
        # Cost basis line
        if avg_cost:
            fig.add_hline(
                y=avg_cost, 
                line_dash="dash", 
                line_color="#ff1744",
                annotation_text=f"Your Cost: ${avg_cost:.2f}",
                annotation_position="right",
                row=1, col=1
            )
        
        # Support/Resistance
        if technicals:
            if technicals.get('support_1'):
                fig.add_hline(y=technicals['support_1'], line_dash="dot", 
                             line_color="#4caf50", annotation_text="Support",
                             row=1, col=1)
            if technicals.get('resistance_1'):
                fig.add_hline(y=technicals['resistance_1'], line_dash="dot",
                             line_color="#f44336", annotation_text="Resistance",
                             row=1, col=1)
        
        if show_indicators:
            # Volume
            colors = ['#26a69a' if c >= o else '#ef5350' 
                     for c, o in zip(history['Close'], history['Open'])]
            fig.add_trace(
                go.Bar(x=history.index, y=history['Volume'], name='Volume',
                      marker_color=colors, showlegend=False),
                row=2, col=1
            )
            
            # RSI
            delta = history['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            fig.add_trace(
                go.Scatter(x=history.index, y=rsi, name='RSI',
                          line=dict(color='#7c4dff', width=1.5)),
                row=3, col=1
            )
            
            fig.add_hline(y=70, line_dash="dot", line_color="#ef5350", row=3, col=1)
            fig.add_hline(y=30, line_dash="dot", line_color="#26a69a", row=3, col=1)
            fig.add_hrect(y0=70, y1=100, fillcolor="rgba(239, 83, 80, 0.1)", 
                         line_width=0, row=3, col=1)
            fig.add_hrect(y0=0, y1=30, fillcolor="rgba(38, 166, 154, 0.1)",
                         line_width=0, row=3, col=1)
        
        fig.update_layout(
            height=700 if show_indicators else 400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_rangeslider_visible=False,
            template='plotly_white',
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.1)')
        
        return fig
    
    @staticmethod
    def portfolio_allocation_pie(weights: Dict[str, float], title: str = "Portfolio Allocation") -> go.Figure:
        """Build portfolio allocation pie chart"""
        
        # Sort by weight
        sorted_weights = dict(sorted(weights.items(), key=lambda x: x[1], reverse=True))
        
        fig = go.Figure(data=[go.Pie(
            labels=list(sorted_weights.keys()),
            values=list(sorted_weights.values()),
            hole=0.4,
            textinfo='label+percent',
            textposition='outside',
            marker=dict(colors=px.colors.qualitative.Set3),
            pull=[0.05 if i == 0 else 0 for i in range(len(sorted_weights))]
        )])
        
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16)),
            height=400,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
            margin=dict(l=20, r=120, t=50, b=20)
        )
        
        return fig
    
    @staticmethod
    def sector_bar_chart(sectors: Dict[str, float]) -> go.Figure:
        """Build sector allocation horizontal bar chart"""
        
        sorted_sectors = dict(sorted(sectors.items(), key=lambda x: x[1], reverse=True))
        
        colors = px.colors.qualitative.Pastel[:len(sorted_sectors)]
        
        fig = go.Figure(data=[go.Bar(
            x=list(sorted_sectors.values()),
            y=list(sorted_sectors.keys()),
            orientation='h',
            marker=dict(color=colors),
            text=[f'{v:.1f}%' for v in sorted_sectors.values()],
            textposition='outside'
        )])
        
        fig.update_layout(
            title=dict(text="Sector Allocation", x=0.5),
            xaxis_title="Percentage",
            height=max(250, len(sorted_sectors) * 35),
            template='plotly_white',
            margin=dict(l=150, r=50, t=50, b=50)
        )
        
        return fig
    
    @staticmethod
    def performance_comparison(analyses: Dict) -> go.Figure:
        """Build performance comparison bar chart"""
        
        if not analyses:
            return None
        
        data = []
        for ticker, analysis in analyses.items():
            if analysis:
                data.append({
                    'ticker': ticker,
                    'gain_pct': analysis['gain_loss_pct'],
                    'color': '#26a69a' if analysis['gain_loss_pct'] >= 0 else '#ef5350'
                })
        
        # Sort by gain
        data.sort(key=lambda x: x['gain_pct'], reverse=True)
        
        fig = go.Figure(data=[go.Bar(
            x=[d['ticker'] for d in data],
            y=[d['gain_pct'] for d in data],
            marker_color=[d['color'] for d in data],
            text=[f"{d['gain_pct']:+.1f}%" for d in data],
            textposition='outside'
        )])
        
        fig.add_hline(y=0, line_dash="solid", line_color="black", line_width=1)
        
        fig.update_layout(
            title=dict(text="Position Performance", x=0.5),
            yaxis_title="Gain/Loss %",
            height=400,
            template='plotly_white',
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
    
    @staticmethod
    def benchmark_comparison(portfolio_return: float, benchmark_returns: Dict) -> go.Figure:
        """Build benchmark comparison chart"""
        
        if not benchmark_returns:
            return None
        
        periods = list(benchmark_returns.keys())
        benchmark_values = list(benchmark_returns.values())
        
        # For simplicity, show portfolio YTD vs benchmark periods
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='S&P 500',
            x=periods,
            y=benchmark_values,
            marker_color='#1a237e'
        ))
        
        fig.add_hline(y=portfolio_return, line_dash="dash", line_color="#ff9800",
                     annotation_text=f"Your Portfolio: {portfolio_return:+.1f}%")
        
        fig.update_layout(
            title=dict(text="S&P 500 Performance by Period", x=0.5),
            yaxis_title="Return %",
            height=350,
            template='plotly_white',
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def risk_gauge(risk_score: float) -> go.Figure:
        """Build risk gauge chart"""
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 30], 'color': '#c8e6c9'},
                    {'range': [30, 60], 'color': '#fff9c4'},
                    {'range': [60, 100], 'color': '#ffcdd2'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': risk_score
                }
            },
            title={'text': "Risk Score"}
        ))
        
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        
        return fig

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_header():
    """Render app header with portfolio selector"""
    
    st.markdown('<h1 class="main-header">💎 Portfolio Pro Ultimate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time • Multi-Portfolio • Smart Signals • Tax Optimization</p>', 
                unsafe_allow_html=True)
    
    # Portfolio selector and controls
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        active = st.selectbox(
            "📁 Active Portfolio",
            options=list(st.session_state.portfolios.keys()),
            index=list(st.session_state.portfolios.keys()).index(st.session_state.active_portfolio),
            label_visibility="collapsed"
        )
        st.session_state.active_portfolio = active
    
    with col2:
        if st.button("🔄 Refresh", type="primary", use_container_width=True):
            st.session_state.cached_data = {}
            st.session_state.cache_timestamp = {}
            st.session_state.last_refresh = datetime.now()
            st.rerun()
    
    with col3:
        auto = st.toggle("Auto", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto
    
    with col4:
        if st.session_state.last_refresh:
            st.caption(f"📡 {st.session_state.last_refresh.strftime('%H:%M:%S')}")
        
        # Notification badge
        unread = len([n for n in st.session_state.pending_notifications if not n.get('read')])
        if unread > 0:
            st.markdown(f'<span class="notification-badge">{unread}</span>', unsafe_allow_html=True)


def render_alert(signal: Dict, ticker: str = ""):
    """Render styled alert"""
    
    signal_type = signal['type']
    
    if signal_type in ['STRONG_SELL']:
        css_class = 'alert-critical'
    elif signal_type in ['SELL']:
        css_class = 'alert-warning'
    elif signal_type in ['STRONG_BUY']:
        css_class = 'alert-opportunity'
    elif signal_type in ['BUY']:
        css_class = 'alert-info'
    elif signal.get('category') == 'earnings':
        css_class = 'alert-earnings'
    else:
        css_class = 'alert-info'
    
    prefix = f"<strong>{ticker}</strong>: " if ticker else ""
    
    st.markdown(f"""
    <div class="{css_class}">
        {prefix}<strong>{signal['title']}</strong><br>
        <small>{signal['message']}</small>
    </div>
    """, unsafe_allow_html=True)


def render_position_card(ticker: str, position: Dict, analysis: Dict):
    """Render comprehensive position card"""
    
    data = analysis['data']
    is_crypto = analysis.get('is_crypto', False)
    
    # Determine card styling
    if is_crypto:
        card_icon = "🪙"
        badge_class = "ticker-badge-crypto"
    else:
        card_icon = "📈" if analysis['gain_loss_pct'] >= 0 else "📉"
        badge_class = "ticker-badge"
    
    # Build expander title
    gain_str = f"{analysis['gain_loss_pct']:+.1f}%"
    gain_color = "🟢" if analysis['gain_loss_pct'] >= 0 else "🔴"
    
    urgent_count = len([s for s in analysis['signals'] if s['priority'] <= 2])
    
    title = f"{card_icon} **{ticker}** | ${analysis['current_price']:.2f} | {gain_color} {gain_str}"
    if urgent_count > 0:
        title += f" | 🚨 {urgent_count}"
    
    with st.expander(title, expanded=urgent_count > 0):
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Shares", f"{position['shares']:,.4f}" if is_crypto else f"{position['shares']:,.2f}")
        col2.metric("Avg Cost", f"${position['avg_cost']:.2f}")
        col3.metric("Value", f"${analysis['total_value']:,.2f}")
        col4.metric("P/L", f"${analysis['gain_loss_dollars']:+,.2f}", f"{analysis['gain_loss_pct']:+.1f}%")
        
        # Action recommendation
        st.markdown("---")
        
        action = analysis['action']
        if 'SELL' in action:
            st.error(f"**🔴 {action}** (Sell Score: {analysis['sell_score']})")
        elif 'BUY' in action:
            st.success(f"**🟢 {action}** (Buy Score: {analysis['buy_score']})")
        else:
            st.warning(f"**🟡 {action}**")
        
        # Signals
        if analysis['signals']:
            st.markdown("**Active Signals:**")
            for signal in analysis['signals'][:6]:
                render_alert(signal)
        
        # 52-week range
        st.markdown("---")
        st.markdown("**52-Week Position:**")
        st.progress(min(max(analysis['pct_in_range'] / 100, 0), 1))
        
        col1, col2, col3 = st.columns(3)
        col1.caption(f"Low: ${data['week_52_low']:.2f}")
        col2.caption(f"Current: ${analysis['current_price']:.2f}")
        col3.caption(f"High: ${data['week_52_high']:.2f}")
        
        # Technical Indicators
        if st.session_state.settings['show_technicals'] and data.get('technicals'):
            st.markdown("---")
            st.markdown("**Technical Analysis:**")
            
            tech = data['technicals']
            score = tech.get('score', 0)
            
            # Score bar
            score_color = "🟢" if score > 20 else "🔴" if score < -20 else "🟡"
            st.write(f"Technical Score: {score_color} **{score:+.0f}** / 100")
            
            # Indicator badges
            signals_html = ""
            for sig, sentiment in tech.get('signals', [])[:12]:
                badge_class = 'bullish' if sentiment == 'bullish' else 'bearish' if sentiment == 'bearish' else 'neutral'
                signals_html += f'<span class="indicator-pill {badge_class}">{sig}</span> '
            st.markdown(signals_html, unsafe_allow_html=True)
            
            # Key levels
            col1, col2, col3, col4 = st.columns(4)
            if tech.get('rsi'):
                col1.metric("RSI", f"{tech['rsi']:.1f}")
            if tech.get('macd_histogram'):
                col2.metric("MACD", f"{tech['macd_histogram']:.2f}")
            if tech.get('support_1'):
                col3.metric("Support", f"${tech['support_1']:.2f}")
            if tech.get('resistance_1'):
                col4.metric("Resistance", f"${tech['resistance_1']:.2f}")
        
        # Fundamentals
        if st.session_state.settings['show_fundamentals'] and not is_crypto:
            st.markdown("---")
            st.markdown("**Fundamentals:**")
            
            col1, col2, col3, col4 = st.columns(4)
            
            if data.get('pe_ratio'):
                col1.metric("P/E", f"{data['pe_ratio']:.1f}")
            if data.get('dividend_yield'):
                col2.metric("Div Yield", f"{data['dividend_yield']:.2f}%")
            if data.get('market_cap'):
                cap = data['market_cap']
                if cap >= 1e12:
                    cap_str = f"${cap/1e12:.1f}T"
                elif cap >= 1e9:
                    cap_str = f"${cap/1e9:.1f}B"
                else:
                    cap_str = f"${cap/1e6:.1f}M"
                col3.metric("Mkt Cap", cap_str)
            if data.get('beta'):
                col4.metric("Beta", f"{data['beta']:.2f}")
            
            # Analyst targets
            if data.get('target_mean'):
                upside = ((data['target_mean'] - analysis['current_price']) / analysis['current_price'] * 100)
                st.write(f"**Analyst Target:** ${data['target_mean']:.2f} ({upside:+.1f}% upside)")
                if data.get('target_low') and data.get('target_high'):
                    st.caption(f"Range: ${data['target_low']:.2f} - ${data['target_high']:.2f}")
        
        # Chart
        st.markdown("---")
        if st.button(f"📈 Show Chart", key=f"chart_{ticker}"):
            history = data.get('history')
            if history is not None and not history.empty:
                chart = ChartBuilder.price_chart(
                    ticker, history, position['avg_cost'], 
                    data.get('technicals'), 
                    st.session_state.settings['show_technicals']
                )
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
        
        # News
        if st.session_state.settings['show_news']:
            if st.button(f"📰 Load News", key=f"news_{ticker}"):
                news = DataFetcher.get_news(ticker, 5)
                if news:
                    for item in news:
                        st.markdown(f"""
                        <div class="news-card">
                            <strong>{item['title']}</strong><br>
                            <small>{item['publisher']} • {item['published'].strftime('%b %d, %Y')}</small><br>
                            <a href="{item['link']}" target="_blank">Read more →</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("No recent news")
        
        # Tax lot analysis
        if st.session_state.settings.get('enable_tax_loss_harvesting', True):
            lots = TaxLotTracker.get_lots(ticker)
            if lots:
                st.markdown("---")
                tax_analysis = TaxLotTracker.analyze_lots(ticker, analysis['current_price'])
                
                if tax_analysis:
                    st.markdown("**Tax Lot Analysis:**")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Lots", tax_analysis['total_lots'])
                    col2.metric("LT Gains", f"${tax_analysis['long_term_gains']:,.2f}")
                    col3.metric("ST Gains", f"${tax_analysis['short_term_gains']:,.2f}")
                    
                    if tax_analysis['harvestable_losses']:
                        st.warning(f"💡 Potential tax-loss harvesting: ${sum(l['loss'] for l in tax_analysis['harvestable_losses']):,.2f}")
        
        # Quick actions
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✏️ Edit", key=f"edit_{ticker}", use_container_width=True):
                st.session_state[f'editing_{ticker}'] = True
        
        with col2:
            if st.button("➕ Add", key=f"add_{ticker}", use_container_width=True):
                st.session_state[f'adding_{ticker}'] = True
        
        with col3:
            if st.button("🔔 Alert", key=f"alert_{ticker}", use_container_width=True):
                st.session_state[f'alert_{ticker}'] = True
        
        with col4:
            if st.button("🗑️", key=f"remove_{ticker}", use_container_width=True):
                portfolio = st.session_state.portfolios[st.session_state.active_portfolio]
                del portfolio[ticker]
                st.rerun()
        
        # Edit modal
        if st.session_state.get(f'editing_{ticker}'):
            with st.form(key=f"edit_form_{ticker}"):
                st.write("**Edit Position**")
                new_shares = st.number_input("Shares", value=float(position['shares']), min_value=0.0)
                new_cost = st.number_input("Avg Cost", value=float(position['avg_cost']), min_value=0.0)
                
                if st.form_submit_button("💾 Save"):
                    portfolio = st.session_state.portfolios[st.session_state.active_portfolio]
                    portfolio[ticker] = {'shares': new_shares, 'avg_cost': new_cost}
                    st.session_state[f'editing_{ticker}'] = False
                    st.rerun()
        
        # Add shares modal
        if st.session_state.get(f'adding_{ticker}'):
            with st.form(key=f"add_form_{ticker}"):
                st.write("**Add Shares**")
                add_shares = st.number_input("Shares to Add", min_value=0.001)
                add_price = st.number_input("Purchase Price", value=analysis['current_price'])
                
                if st.form_submit_button("➕ Add"):
                    portfolio = st.session_state.portfolios[st.session_state.active_portfolio]
                    old = portfolio[ticker]
                    old_total = old['shares'] * old['avg_cost']
                    new_total = add_shares * add_price
                    combined = old['shares'] + add_shares
                    new_avg = (old_total + new_total) / combined
                    
                    portfolio[ticker] = {'shares': combined, 'avg_cost': new_avg}
                    
                    # Add tax lot
                    TaxLotTracker.add_lot(ticker, add_shares, add_price, datetime.now())
                    
                    # Log transaction
                    st.session_state.transaction_history.append({
                        'date': datetime.now().isoformat(),
                        'portfolio': st.session_state.active_portfolio,
                        'ticker': ticker,
                        'action': 'BUY',
                        'shares': add_shares,
                        'price': add_price
                    })
                    
                    st.session_state[f'adding_{ticker}'] = False
                    st.success(f"Added {add_shares} shares at ${add_price:.2f}")
                    st.rerun()
        
        # Price alert modal
        if st.session_state.get(f'alert_{ticker}'):
            with st.form(key=f"alert_form_{ticker}"):
                st.write("**Set Price Alert**")
                alert_type = st.selectbox("Type", ["Price Above", "Price Below", "% Change Up", "% Change Down"])
                alert_value = st.number_input("Value", value=analysis['current_price'] if 'Price' in alert_type else 5.0)
                
                if st.form_submit_button("🔔 Set Alert"):
                    if ticker not in st.session_state.price_alerts:
                        st.session_state.price_alerts[ticker] = []
                    
                    st.session_state.price_alerts[ticker].append({
                        'type': alert_type,
                        'value': alert_value,
                        'base_price': analysis['current_price'],
                        'created': datetime.now().isoformat(),
                        'triggered': False
                    })
                    
                    st.session_state[f'alert_{ticker}'] = False
                    st.success(f"Alert set: {alert_type} {alert_value}")
                    st.rerun()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    render_header()
    
    # Main tabs
    tabs = st.tabs([
        "📊 Portfolio",
        "➕ Add Position",
        "🪙 Crypto",
        "📋 Options",
        "👁️ Watchlist",
        "📈 Analytics",
        "💰 Dividends",
        "📊 Tax Center",
        "🔔 Notifications",
        "⚙️ Settings"
    ])
    
    # Get active portfolio
    active_portfolio = st.session_state.portfolios[st.session_state.active_portfolio]
    
    # =========================================================================
    # TAB 1: PORTFOLIO
    # =========================================================================
    with tabs[0]:
        if not active_portfolio:
            st.info("👆 Add positions to get started!")
            
            st.markdown("""
            ### Welcome to Portfolio Pro Ultimate! 💎
            
            **What makes this special:**
            
            🚀 **Multi-Portfolio Support** - Track Retirement, Trading, Long-term separately
            
            🚨 **Smart Signals** - 15+ technical indicators, analyst ratings, volume analysis
            
            🪙 **Crypto Support** - Track BTC, ETH, SOL and 15+ cryptocurrencies
            
            📋 **Options Tracking** - Monitor covered calls, puts, and strategies
            
            💰 **Dividend Tracking** - Annual income projections and ex-div alerts
            
            📊 **Tax Optimization** - Tax lot tracking and loss harvesting suggestions
            
            📱 **Push Notifications** - Email and Telegram alerts
            
            📈 **Benchmark Comparison** - Compare your returns to S&P 500
            """)
        
        else:
            # Fetch and analyze all positions
            analyses = {}
            urgent_alerts = []
            
            with st.spinner("Loading portfolio..."):
                for ticker, position in active_portfolio.items():
                    data = DataFetcher.get_data(ticker)
                    if data:
                        analysis = PositionAnalyzer.analyze(
                            ticker, position, data, st.session_state.settings
                        )
                        analyses[ticker] = analysis
                        
                        for signal in analysis['signals']:
                            if signal['priority'] <= 2:
                                urgent_alerts.append((ticker, signal, analysis))
            
            # Portfolio metrics
            metrics = PortfolioAnalyzer.calculate_metrics(active_portfolio, analyses)
            
            # ===== SUMMARY ROW =====
            st.subheader("💰 Portfolio Summary")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            col1.metric(
                "Total Value",
                f"${metrics.get('total_value', 0):,.2f}"
            )
            
            col2.metric(
                "Total Cost",
                f"${metrics.get('total_cost', 0):,.2f}"
            )
            
            col3.metric(
                "Total P/L",
                f"${metrics.get('total_gain', 0):+,.2f}",
                f"{metrics.get('total_return_pct', 0):+.2f}%"
            )
            
            col4.metric(
                "Positions",
                metrics.get('num_positions', 0)
            )
            
            col5.metric(
                "Annual Dividends",
                f"${metrics.get('total_dividends_annual', 0):,.2f}",
                f"{metrics.get('dividend_yield', 0):.2f}% yield"
            )
            
            # Additional metrics
            col1, col2, col3, col4 = st.columns(4)
            
            col1.metric("Portfolio Beta", f"{metrics.get('portfolio_beta', 1):.2f}")
            col2.metric("Sectors", metrics.get('num_sectors', 0))
            col3.metric("Concentration", f"{metrics.get('concentration_risk', 0):.1f}%")
            col4.metric("Diversification", f"{metrics.get('diversification_score', 50)}/100")
            
            # Benchmark comparison
            benchmark_data = DataFetcher.get_benchmark_data(st.session_state.settings['benchmark_symbol'])
            if benchmark_data is not None:
                benchmark_returns = PortfolioAnalyzer.calculate_benchmark_comparison(
                    active_portfolio, analyses, benchmark_data
                )
                if benchmark_returns and 'YTD' in benchmark_returns:
                    portfolio_return = metrics.get('total_return_pct', 0)
                    spy_ytd = benchmark_returns.get('YTD', 0)
                    
                    outperformance = portfolio_return - spy_ytd
                    
                    if outperformance >= 0:
                        st.success(f"📈 **Outperforming S&P 500 by {outperformance:+.1f}%** (You: {portfolio_return:+.1f}% vs SPY: {spy_ytd:+.1f}%)")
                    else:
                        st.warning(f"📉 **Underperforming S&P 500 by {abs(outperformance):.1f}%** (You: {portfolio_return:+.1f}% vs SPY: {spy_ytd:+.1f}%)")
            
            st.divider()
            
            # ===== URGENT ALERTS =====
            if urgent_alerts:
                st.subheader("🚨 Action Required")
                
                urgent_alerts.sort(key=lambda x: x[1]['priority'])
                
                for ticker, signal, analysis in urgent_alerts[:8]:
                    render_alert(signal, ticker)
                    
                    # Send notification
                    if st.session_state.notification_settings.get('notify_on_' + signal.get('category', 'info'), False):
                        NotificationManager.notify(
                            f"{ticker}: {signal['title']}",
                            signal['message'],
                            signal.get('category', 'info')
                        )
                
                st.divider()
            
            # ===== CHECK PRICE ALERTS =====
            triggered = []
            for ticker, alerts in st.session_state.price_alerts.items():
                if ticker in analyses:
                    current = analyses[ticker]['current_price']
                    for alert in alerts:
                        if not alert.get('triggered'):
                            trigger = False
                            
                            if alert['type'] == 'Price Above' and current >= alert['value']:
                                trigger = True
                            elif alert['type'] == 'Price Below' and current <= alert['value']:
                                trigger = True
                            elif alert['type'] == '% Change Up':
                                change = ((current - alert['base_price']) / alert['base_price']) * 100
                                if change >= alert['value']:
                                    trigger = True
                            elif alert['type'] == '% Change Down':
                                change = ((current - alert['base_price']) / alert['base_price']) * 100
                                if change <= -alert['value']:
                                    trigger = True
                            
                            if trigger:
                                alert['triggered'] = True
                                triggered.append((ticker, alert))
                                NotificationManager.notify(
                                    f"Price Alert: {ticker}",
                                    f"{alert['type']}: {alert['value']}",
                                    'price_alert'
                                )
            
            if triggered:
                st.subheader("🔔 Price Alerts Triggered!")
                for ticker, alert in triggered:
                    st.warning(f"**{ticker}**: {alert['type']} {alert['value']}")
                st.divider()
            
            # ===== POSITIONS =====
            st.subheader("📈 Your Positions")
            
            # Sort options
            sort_by = st.selectbox(
                "Sort by",
                ["Gain/Loss %", "Total Value", "Urgency", "Alphabetical"],
                key="sort_portfolio"
            )
            
            if sort_by == "Gain/Loss %":
                sorted_tickers = sorted(analyses.keys(), 
                    key=lambda t: analyses[t]['gain_loss_pct'] if analyses[t] else 0, reverse=True)
            elif sort_by == "Total Value":
                sorted_tickers = sorted(analyses.keys(),
                    key=lambda t: analyses[t]['total_value'] if analyses[t] else 0, reverse=True)
            elif sort_by == "Urgency":
                sorted_tickers = sorted(analyses.keys(),
                    key=lambda t: len([s for s in analyses[t]['signals'] if s['priority'] <= 2]) if analyses[t] else 0, reverse=True)
            else:
                sorted_tickers = sorted(analyses.keys())
            
            for ticker in sorted_tickers:
                if analyses.get(ticker):
                    render_position_card(ticker, active_portfolio[ticker], analyses[ticker])
            
            st.session_state.last_refresh = datetime.now()
        
        # Auto-refresh
        if st.session_state.auto_refresh and active_portfolio:
            time.sleep(st.session_state.refresh_interval)
            st.session_state.cached_data = {}
            st.rerun()
    
    # =========================================================================
    # TAB 2: ADD POSITION
    # =========================================================================
    with tabs[1]:
        st.subheader("➕ Add New Position")
        
        with st.form("add_position_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                ticker = st.text_input("Ticker Symbol", placeholder="AAPL").upper().strip()
                shares = st.number_input("Number of Shares", min_value=0.0, step=0.01)
            
            with col2:
                target_portfolio = st.selectbox(
                    "Add to Portfolio",
                    options=list(st.session_state.portfolios.keys()),
                    index=list(st.session_state.portfolios.keys()).index(st.session_state.active_portfolio)
                )
                avg_cost = st.number_input("Average Cost ($)", min_value=0.0, step=0.01)
            
            purchase_date = st.date_input("Purchase Date", value=date.today())
            
            submitted = st.form_submit_button("➕ Add Position", type="primary", use_container_width=True)
            
            if submitted and ticker and shares > 0 and avg_cost > 0:
                with st.spinner(f"Verifying {ticker}..."):
                    data = DataFetcher.get_data(ticker, force_refresh=True)
                
                if data:
                    portfolio = st.session_state.portfolios[target_portfolio]
                    
                    if ticker in portfolio:
                        old = portfolio[ticker]
                        old_total = old['shares'] * old['avg_cost']
                        new_total = shares * avg_cost
                        combined = old['shares'] + shares
                        new_avg = (old_total + new_total) / combined
                        portfolio[ticker] = {'shares': combined, 'avg_cost': new_avg}
                        st.success(f"Updated {ticker}: {combined:.2f} shares @ ${new_avg:.2f}")
                    else:
                        portfolio[ticker] = {'shares': shares, 'avg_cost': avg_cost}
                        st.success(f"Added {data['name']} ({ticker})")
                    
                    # Add tax lot
                    TaxLotTracker.add_lot(ticker, shares, avg_cost, datetime.combine(purchase_date, datetime.min.time()))
                    
                    # Log transaction
                    st.session_state.transaction_history.append({
                        'date': datetime.combine(purchase_date, datetime.min.time()).isoformat(),
                        'portfolio': target_portfolio,
                        'ticker': ticker,
                        'action': 'BUY',
                        'shares': shares,
                        'price': avg_cost
                    })
                    
                    st.rerun()
                else:
                    st.error(f"Could not find {ticker}")
        
        # Quick add buttons
        st.markdown("---")
        st.write("**🔥 Popular Stocks:**")
        
        popular = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD', 'NFLX', 'DIS']
        cols = st.columns(5)
        for i, sym in enumerate(popular):
            with cols[i % 5]:
                if st.button(sym, key=f"pop_{sym}", use_container_width=True):
                    st.session_state.quick_ticker = sym
        
        st.write("**📊 Popular ETFs:**")
        etfs = ['SPY', 'QQQ', 'VOO', 'VTI', 'IWM', 'DIA', 'ARKK', 'XLF', 'XLE', 'XLK']
        cols = st.columns(5)
        for i, sym in enumerate(etfs):
            with cols[i % 5]:
                if st.button(sym, key=f"etf_{sym}", use_container_width=True):
                    st.session_state.quick_ticker = sym
    
    # =========================================================================
    # TAB 3: CRYPTO
    # =========================================================================
    with tabs[2]:
        st.subheader("🪙 Cryptocurrency Portfolio")
        
        crypto_portfolio = st.session_state.portfolios.get('Crypto Portfolio', {})
        
        # Add crypto
        st.write("**Add Cryptocurrency:**")
        
        with st.form("add_crypto"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                crypto_select = st.selectbox(
                    "Cryptocurrency",
                    options=list(DataFetcher.CRYPTO_MAP.keys()) + ['Other']
                )
                
                if crypto_select == 'Other':
                    crypto_ticker = st.text_input("Enter symbol (e.g., SOL)")
                else:
                    crypto_ticker = crypto_select
            
            with col2:
                crypto_amount = st.number_input("Amount", min_value=0.0, step=0.0001)
            
            with col3:
                crypto_cost = st.number_input("Avg Cost ($)", min_value=0.0, step=0.01)
            
            if st.form_submit_button("🪙 Add Crypto", use_container_width=True):
                if crypto_ticker and crypto_amount > 0 and crypto_cost > 0:
                    data = DataFetcher.get_data(crypto_ticker)
                    if data:
                        crypto_portfolio[crypto_ticker.upper()] = {
                            'shares': crypto_amount,
                            'avg_cost': crypto_cost
                        }
                        st.session_state.portfolios['Crypto Portfolio'] = crypto_portfolio
                        st.success(f"Added {crypto_amount} {crypto_ticker.upper()}")
                        st.rerun()
                    else:
                        st.error("Could not find cryptocurrency")
        
        st.markdown("---")
        
        # Show crypto positions
        if crypto_portfolio:
            analyses = {}
            for ticker, pos in crypto_portfolio.items():
                data = DataFetcher.get_data(ticker)
                if data:
                    analysis = PositionAnalyzer.analyze(ticker, pos, data, st.session_state.settings)
                    analyses[ticker] = analysis
            
            # Summary
            total_value = sum(a['total_value'] for a in analyses.values() if a)
            total_cost = sum(a['cost_basis'] for a in analyses.values() if a)
            total_gain = total_value - total_cost
            return_pct = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Crypto Value", f"${total_value:,.2f}")
            col2.metric("Total P/L", f"${total_gain:+,.2f}")
            col3.metric("Return", f"{return_pct:+.2f}%")
            
            st.markdown("---")
            
            for ticker, analysis in analyses.items():
                if analysis:
                    render_position_card(ticker, crypto_portfolio[ticker], analysis)
        else:
            st.info("No crypto positions yet. Add some above!")
    
    # =========================================================================
    # TAB 4: OPTIONS
    # =========================================================================
    with tabs[3]:
        st.subheader("📋 Options Tracker")
        
        # Add option position
        with st.expander("➕ Add Option Position"):
            with st.form("add_option"):
                col1, col2 = st.columns(2)
                
                with col1:
                    opt_ticker = st.text_input("Underlying Ticker").upper()
                    opt_type = st.selectbox("Type", ["CALL", "PUT"])
                    opt_strike = st.number_input("Strike Price", min_value=0.0, step=0.5)
                    opt_expiry = st.date_input("Expiration Date")
                
                with col2:
                    opt_contracts = st.number_input("Contracts", min_value=1, step=1)
                    opt_premium = st.number_input("Premium Paid/Received", step=0.01)
                    opt_action = st.selectbox("Action", ["BUY", "SELL (Covered)"])
                
                if st.form_submit_button("Add Option"):
                    st.session_state.options_positions.append({
                        'ticker': opt_ticker,
                        'type': opt_type,
                        'strike': opt_strike,
                        'expiry': opt_expiry.isoformat(),
                        'contracts': opt_contracts,
                        'premium': opt_premium,
                        'action': opt_action,
                        'added': datetime.now().isoformat()
                    })
                    st.success("Option position added!")
                    st.rerun()
        
        st.markdown("---")
        
        # Display options
        if st.session_state.options_positions:
            for i, opt in enumerate(st.session_state.options_positions):
                expiry = datetime.fromisoformat(opt['expiry'])
                days_to_expiry = (expiry - datetime.now()).days
                
                # Get current underlying price
                data = DataFetcher.get_data(opt['ticker'])
                underlying_price = data['price'] if data else 0
                
                # Calculate basic option status
                if opt['type'] == 'CALL':
                    itm = underlying_price > opt['strike']
                    intrinsic = max(0, underlying_price - opt['strike'])
                else:
                    itm = underlying_price < opt['strike']
                    intrinsic = max(0, opt['strike'] - underlying_price)
                
                status_color = "🟢" if itm else "🔴"
                status_text = "ITM" if itm else "OTM"
                
                with st.expander(f"{opt['action']} {opt['contracts']}x {opt['ticker']} ${opt['strike']} {opt['type']} - {expiry.strftime('%m/%d/%Y')}"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    col1.metric("Status", f"{status_color} {status_text}")
                    col2.metric("Days to Expiry", days_to_expiry)
                    col3.metric("Underlying", f"${underlying_price:.2f}" if underlying_price else "N/A")
                    col4.metric("Intrinsic Value", f"${intrinsic:.2f}")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Premium", f"${opt['premium']:.2f}")
                    col2.metric("Total Premium", f"${opt['premium'] * opt['contracts'] * 100:.2f}")
                    col3.metric("Break-even", f"${opt['strike'] + opt['premium'] if opt['type'] == 'CALL' else opt['strike'] - opt['premium']:.2f}")
                    
                    if days_to_expiry <= 7:
                        st.warning("⚠️ Expiring soon!")
                    
                    if st.button("🗑️ Remove", key=f"remove_opt_{i}"):
                        st.session_state.options_positions.pop(i)
                        st.rerun()
        else:
            st.info("No options positions. Add covered calls, protective puts, or other strategies above!")
    
    # =========================================================================
    # TAB 5: WATCHLIST
    # =========================================================================
    with tabs[4]:
        st.subheader("👁️ Watchlist")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            watch_input = st.text_input("Add to watchlist", placeholder="AAPL", label_visibility="collapsed")
        with col2:
            if st.button("➕ Add", use_container_width=True):
                if watch_input:
                    ticker = watch_input.upper().strip()
                    if ticker not in st.session_state.watchlist:
                        data = DataFetcher.get_data(ticker)
                        if data:
                            st.session_state.watchlist.append(ticker)
                            st.rerun()
                        else:
                            st.error("Ticker not found")
        
        st.markdown("---")
        
        if st.session_state.watchlist:
            for ticker in st.session_state.watchlist:
                data = DataFetcher.get_data(ticker)
                if data:
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                    
                    col1.write(f"**{ticker}**")
                    col2.write(f"${data['price']:.2f}")
                    
                    change_icon = "🟢" if data['change_pct'] >= 0 else "🔴"
                    col3.write(f"{change_icon} {data['change_pct']:+.2f}%")
                    
                    # 52-week position
                    range_52 = data['week_52_high'] - data['week_52_low']
                    pos = ((data['price'] - data['week_52_low']) / range_52 * 100) if range_52 > 0 else 50
                    col4.write(f"{'📈' if pos > 70 else '📉' if pos < 30 else '➡️'} {pos:.0f}%")
                    
                    with col5:
                        if st.button("❌", key=f"rm_watch_{ticker}"):
                            st.session_state.watchlist.remove(ticker)
                            st.rerun()
        else:
            st.info("Your watchlist is empty")
    
    # =========================================================================
    # TAB 6: ANALYTICS
    # =========================================================================
    with tabs[5]:
        st.subheader("📈 Portfolio Analytics")
        
        if not active_portfolio:
            st.info("Add positions to see analytics")
        else:
            # Re-analyze
            analyses = {}
            for ticker, pos in active_portfolio.items():
                data = DataFetcher.get_data(ticker)
                if data:
                    analysis = PositionAnalyzer.analyze(ticker, pos, data, st.session_state.settings)
                    analyses[ticker] = analysis
            
            metrics = PortfolioAnalyzer.calculate_metrics(active_portfolio, analyses)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                if metrics.get('position_weights'):
                    pie = ChartBuilder.portfolio_allocation_pie(metrics['position_weights'])
                    st.plotly_chart(pie, use_container_width=True)
            
            with col2:
                if metrics.get('sector_allocation'):
                    sector = ChartBuilder.sector_bar_chart(metrics['sector_allocation'])
                    st.plotly_chart(sector, use_container_width=True)
            
            # Performance chart
            perf = ChartBuilder.performance_comparison(analyses)
            if perf:
                st.plotly_chart(perf, use_container_width=True)
            
            # Benchmark comparison
            st.markdown("---")
            st.subheader("📊 Benchmark Comparison")
            
            benchmark_data = DataFetcher.get_benchmark_data()
            if benchmark_data is not None:
                bench_returns = PortfolioAnalyzer.calculate_benchmark_comparison(
                    active_portfolio, analyses, benchmark_data
                )
                
                if bench_returns:
                    bench_chart = ChartBuilder.benchmark_comparison(
                        metrics.get('total_return_pct', 0), bench_returns
                    )
                    if bench_chart:
                        st.plotly_chart(bench_chart, use_container_width=True)
            
            # Risk analysis
            st.markdown("---")
            st.subheader("⚠️ Risk Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_risk = np.mean([a['risk_score'] for a in analyses.values() if a])
                risk_gauge = ChartBuilder.risk_gauge(avg_risk)
                st.plotly_chart(risk_gauge, use_container_width=True)
            
            with col2:
                st.metric("Portfolio Beta", f"{metrics.get('portfolio_beta', 1):.2f}")
                st.metric("Concentration Risk", f"{metrics.get('concentration_risk', 0):.1f}%")
                st.metric("Diversification Score", f"{metrics.get('diversification_score', 50)}/100")
            
            with col3:
                # Top risks
                st.write("**Highest Risk Positions:**")
                risk_sorted = sorted(analyses.items(), key=lambda x: x[1]['risk_score'] if x[1] else 0, reverse=True)
                for ticker, analysis in risk_sorted[:5]:
                    if analysis:
                        st.write(f"🔴 {ticker}: {analysis['risk_score']:.0f}/100")
    
    # =========================================================================
    # TAB 7: DIVIDENDS
    # =========================================================================
    with tabs[6]:
        st.subheader("💰 Dividend Center")
        
        if not active_portfolio:
            st.info("Add positions to see dividend analysis")
        else:
            # Calculate dividend income
            annual_income = 0
            dividend_positions = []
            
            for ticker, pos in active_portfolio.items():
                data = DataFetcher.get_data(ticker)
                if data and data.get('dividend_yield', 0) > 0:
                    annual_div = pos['shares'] * data['price'] * (data['dividend_yield'] / 100)
                    dividend_positions.append({
                        'ticker': ticker,
                        'shares': pos['shares'],
                        'yield': data['dividend_yield'],
                        'annual': annual_div,
                        'ex_date': data.get('ex_dividend_date')
                    })
                    annual_income += annual_div
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Annual Dividend Income", f"${annual_income:,.2f}")
            col2.metric("Monthly Average", f"${annual_income/12:,.2f}")
            col3.metric("Paying Positions", len(dividend_positions))
            
            st.markdown("---")
            
            if dividend_positions:
                st.write("**Dividend Positions:**")
                
                # Sort by yield
                dividend_positions.sort(key=lambda x: x['yield'], reverse=True)
                
                for pos in dividend_positions:
                    col1, col2, col3, col4 = st.columns(4)
                    col1.write(f"**{pos['ticker']}**")
                    col2.write(f"{pos['yield']:.2f}% yield")
                    col3.write(f"${pos['annual']:,.2f}/year")
                    
                    if pos['ex_date']:
                        try:
                            ex_date = datetime.fromtimestamp(pos['ex_date'])
                            days = (ex_date - datetime.now()).days
                            if 0 <= days <= 30:
                                col4.write(f"📅 Ex-div in {days} days")
                        except:
                            pass
            else:
                st.info("No dividend-paying positions in your portfolio")
    
    # =========================================================================
    # TAB 8: TAX CENTER
    # =========================================================================
    with tabs[7]:
        st.subheader("📊 Tax Center")
        
        # Tax lot summary
        st.write("**Tax Lot Summary:**")
        
        total_stcg = 0
        total_ltcg = 0
        total_st_loss = 0
        total_lt_loss = 0
        harvestable = []
        
        for ticker, lots in st.session_state.tax_lots.items():
            data = DataFetcher.get_data(ticker)
            if data:
                analysis = TaxLotTracker.analyze_lots(ticker, data['price'])
                if analysis:
                    total_stcg += analysis['short_term_gains']
                    total_ltcg += analysis['long_term_gains']
                    total_st_loss += analysis['short_term_losses']
                    total_lt_loss += analysis['long_term_losses']
                    
                    for loss in analysis['harvestable_losses']:
                        harvestable.append({'ticker': ticker, **loss})
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("ST Gains", f"${total_stcg:,.2f}", help="Short-term capital gains (<1 year)")
        col2.metric("LT Gains", f"${total_ltcg:,.2f}", help="Long-term capital gains (>1 year)")
        col3.metric("ST Losses", f"${total_st_loss:,.2f}")
        col4.metric("LT Losses", f"${total_lt_loss:,.2f}")
        
        # Tax estimate
        st.markdown("---")
        st.write("**Estimated Tax Impact:**")
        
        tax_rate_st = st.session_state.settings['tax_rate_stcg']
        tax_rate_lt = st.session_state.settings['tax_rate_ltcg']
        
        net_st = total_stcg - total_st_loss
        net_lt = total_ltcg - total_lt_loss
        
        tax_st = max(0, net_st) * tax_rate_st
        tax_lt = max(0, net_lt) * tax_rate_lt
        total_tax = tax_st + tax_lt
        
        col1, col2, col3 = st.columns(3)
        col1.metric("ST Tax", f"${tax_st:,.2f}", f"@ {tax_rate_st*100:.0f}%")
        col2.metric("LT Tax", f"${tax_lt:,.2f}", f"@ {tax_rate_lt*100:.0f}%")
        col3.metric("Total Estimated Tax", f"${total_tax:,.2f}")
        
        # Tax-loss harvesting opportunities
        if harvestable:
            st.markdown("---")
            st.subheader("💡 Tax-Loss Harvesting Opportunities")
            
            harvestable.sort(key=lambda x: x['loss'], reverse=True)
            
            total_harvestable = sum(h['loss'] for h in harvestable)
            potential_savings = total_harvestable * max(tax_rate_st, tax_rate_lt)
            
            st.success(f"**Potential Tax Savings: ${potential_savings:,.2f}**")
            
            for h in harvestable[:10]:
                term = "LT" if h['is_long_term'] else "ST"
                st.write(f"🔴 **{h['ticker']}**: Harvest ${h['loss']:.2f} loss ({term}, held {h['days_held']} days)")
    
    # =========================================================================
    # TAB 9: NOTIFICATIONS
    # =========================================================================
    with tabs[8]:
        st.subheader("🔔 Notification Settings")
        
        settings = st.session_state.notification_settings
        
        # Email settings
        st.write("**📧 Email Notifications:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            email_enabled = st.checkbox("Enable Email", value=settings['email_enabled'])
            settings['email_enabled'] = email_enabled
            
            if email_enabled:
                settings['email_address'] = st.text_input("Email Address", value=settings['email_address'])
                settings['email_password'] = st.text_input("App Password", value=settings['email_password'], type="password",
                    help="Use Gmail App Password, not your regular password")
        
        st.markdown("---")
        
        # Telegram settings
        st.write("**📱 Telegram Notifications:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            telegram_enabled = st.checkbox("Enable Telegram", value=settings['telegram_enabled'])
            settings['telegram_enabled'] = telegram_enabled
            
            if telegram_enabled:
                settings['telegram_bot_token'] = st.text_input("Bot Token", value=settings['telegram_bot_token'], type="password")
                settings['telegram_chat_id'] = st.text_input("Chat ID", value=settings['telegram_chat_id'])
        
        st.markdown("---")
        
        # Notification preferences
        st.write("**🔔 Notification Preferences:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings['notify_on_profit_target'] = st.checkbox("Profit Target Alerts", value=settings['notify_on_profit_target'])
            settings['notify_on_stop_loss'] = st.checkbox("Stop Loss Alerts", value=settings['notify_on_stop_loss'])
            settings['notify_on_earnings'] = st.checkbox("Earnings Alerts", value=settings['notify_on_earnings'])
        
        with col2:
            settings['notify_on_dividend'] = st.checkbox("Dividend Alerts", value=settings['notify_on_dividend'])
            settings['notify_on_price_alert'] = st.checkbox("Price Alert Triggers", value=settings['notify_on_price_alert'])
        
        if st.button("💾 Save Notification Settings"):
            st.session_state.notification_settings = settings
            st.success("Settings saved!")
        
        st.markdown("---")
        
        # Test notifications
        st.write("**🧪 Test Notifications:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📧 Test Email"):
                if NotificationManager.send_email("Test Alert", "This is a test from Portfolio Pro!"):
                    st.success("Email sent!")
                else:
                    st.error("Failed to send email")
        
        with col2:
            if st.button("📱 Test Telegram"):
                if NotificationManager.send_telegram("🧪 Test notification from Portfolio Pro!"):
                    st.success("Telegram sent!")
                else:
                    st.error("Failed to send Telegram")
        
        st.markdown("---")
        
        # Recent notifications
        st.write("**📜 Recent Notifications:**")
        
        if st.session_state.pending_notifications:
            for notif in reversed(st.session_state.pending_notifications[-20:]):
                time_str = datetime.fromisoformat(notif['timestamp']).strftime('%b %d, %H:%M')
                st.write(f"• {time_str}: **{notif['title']}** - {notif['message']}")
        else:
            st.caption("No recent notifications")
    
    # =========================================================================
    # TAB 10: SETTINGS
    # =========================================================================
    with tabs[9]:
        st.subheader("⚙️ Settings")
        
        settings = st.session_state.settings
        
        # Alert thresholds
        st.write("**🎯 Alert Thresholds:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings['take_profit_threshold'] = st.slider(
                "Take Profit Alert (%)",
                10, 200, settings['take_profit_threshold'], 5
            )
        
        with col2:
            settings['stop_loss_threshold'] = st.slider(
                "Stop Loss Alert (%)",
                -50, -5, settings['stop_loss_threshold'], 5
            )
        
        settings['volume_spike_multiplier'] = st.slider(
            "Volume Spike Multiplier",
            1.5, 10.0, float(settings['volume_spike_multiplier']), 0.5
        )
        
        st.markdown("---")
        
        # Display options
        st.write("**📊 Display Options:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings['show_technicals'] = st.checkbox("Show Technical Indicators", value=settings['show_technicals'])
            settings['show_news'] = st.checkbox("Show News", value=settings['show_news'])
            settings['show_fundamentals'] = st.checkbox("Show Fundamentals", value=settings['show_fundamentals'])
        
        with col2:
            settings['benchmark_symbol'] = st.text_input("Benchmark Symbol", value=settings['benchmark_symbol'])
            settings['default_chart_period'] = st.selectbox(
                "Default Chart Period",
                ['1mo', '3mo', '6mo', '1y', '2y'],
                index=['1mo', '3mo', '6mo', '1y', '2y'].index(settings['default_chart_period'])
            )
        
        st.markdown("---")
        
        # Tax settings
        st.write("**💰 Tax Settings:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings['tax_rate_stcg'] = st.slider(
                "Short-term Capital Gains Rate",
                0.0, 0.5, settings['tax_rate_stcg'], 0.01,
                format="%.0f%%"
            )
        
        with col2:
            settings['tax_rate_ltcg'] = st.slider(
                "Long-term Capital Gains Rate",
                0.0, 0.3, settings['tax_rate_ltcg'], 0.01,
                format="%.0f%%"
            )
        
        settings['enable_tax_loss_harvesting'] = st.checkbox(
            "Enable Tax-Loss Harvesting Suggestions",
            value=settings['enable_tax_loss_harvesting']
        )
        
        st.markdown("---")
        
        # Auto-refresh
        st.write("**🔄 Auto-Refresh:**")
        
        st.session_state.refresh_interval = st.selectbox(
            "Refresh Interval",
            [15, 30, 60, 120, 300],
            index=[15, 30, 60, 120, 300].index(st.session_state.refresh_interval),
            format_func=lambda x: f"{x}s" if x < 60 else f"{x//60}m"
        )
        
        st.markdown("---")
        
        # Portfolio management
        st.write("**📁 Portfolio Management:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_portfolio_name = st.text_input("New Portfolio Name")
            if st.button("➕ Create Portfolio"):
                if new_portfolio_name and new_portfolio_name not in st.session_state.portfolios:
                    st.session_state.portfolios[new_portfolio_name] = {}
                    st.success(f"Created '{new_portfolio_name}'")
                    st.rerun()
        
        with col2:
            delete_portfolio = st.selectbox(
                "Delete Portfolio",
                options=[p for p in st.session_state.portfolios.keys() if p != st.session_state.active_portfolio]
            )
            if st.button("🗑️ Delete Portfolio"):
                if delete_portfolio:
                    del st.session_state.portfolios[delete_portfolio]
                    st.success(f"Deleted '{delete_portfolio}'")
                    st.rerun()
        
        st.markdown("---")
        
        # Data management
        st.write("**💾 Data Management:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_data = json.dumps({
                'portfolios': st.session_state.portfolios,
                'watchlist': st.session_state.watchlist,
                'options_positions': st.session_state.options_positions,
                'price_alerts': st.session_state.price_alerts,
                'tax_lots': st.session_state.tax_lots,
                'transaction_history': st.session_state.transaction_history,
                'settings': st.session_state.settings,
                'exported_at': datetime.now().isoformat()
            }, indent=2, default=str)
            
            st.download_button(
                "📥 Export All Data (JSON)",
                export_data,
                "portfolio_pro_backup.json",
                "application/json",
                use_container_width=True
            )
        
        with col2:
            uploaded = st.file_uploader("📤 Import Data", type=['json'])
            if uploaded:
                try:
                    data = json.loads(uploaded.read().decode('utf-8'))
                    
                    if st.button("Import This File"):
                        if 'portfolios' in data:
                            st.session_state.portfolios = data['portfolios']
                        if 'watchlist' in data:
                            st.session_state.watchlist = data['watchlist']
                        if 'options_positions' in data:
                            st.session_state.options_positions = data['options_positions']
                        if 'price_alerts' in data:
                            st.session_state.price_alerts = data['price_alerts']
                        if 'tax_lots' in data:
                            st.session_state.tax_lots = data['tax_lots']
                        if 'transaction_history' in data:
                            st.session_state.transaction_history = data['transaction_history']
                        if 'settings' in data:
                            st.session_state.settings = data['settings']
                        
                        st.success("Data imported!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Import failed: {e}")
        
        st.markdown("---")
        
        # Danger zone
        st.write("**⚠️ Danger Zone:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear All Data", type="secondary"):
                for key in ['portfolios', 'watchlist', 'options_positions', 'price_alerts', 
                           'tax_lots', 'transaction_history', 'cached_data', 'cache_timestamp']:
                    if key == 'portfolios':
                        st.session_state[key] = {'Main Portfolio': {}}
                    elif key in ['watchlist', 'options_positions', 'transaction_history']:
                        st.session_state[key] = []
                    else:
                        st.session_state[key] = {}
                st.success("All data cleared")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset Settings"):
                st.session_state.settings = {
                    'take_profit_threshold': 50,
                    'stop_loss_threshold': -20,
                    'volume_spike_multiplier': 3.0,
                    'show_technicals': True,
                    'show_news': True,
                    'show_fundamentals': True,
                    'benchmark_symbol': 'SPY',
                    'tax_rate_stcg': 0.35,
                    'tax_rate_ltcg': 0.15,
                    'enable_tax_loss_harvesting': True,
                    'default_chart_period': '6mo',
                }
                st.success("Settings reset")
                st.rerun()
        
        st.markdown("---")
        
        st.caption("""
        **Portfolio Pro Ultimate** v2.0
        
        Built with ❤️ using Streamlit • Market data from Yahoo Finance
        
        ⚠️ This tool is for informational purposes only and is not financial advice.
        Always do your own research before making investment decisions.
        """)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
