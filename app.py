import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- LANGUAGE CODE MAPPING ---
LANGUAGE_NAMES = {
    'en': 'English',
    'en-US': 'English (US)',
    'en-GB': 'English (UK)',
    'en-IN': 'English (India)',
    'es': 'Spanish',
    'es-ES': 'Spanish (Spain)',
    'es-MX': 'Spanish (Mexico)',
    'pt': 'Portuguese',
    'pt-BR': 'Portuguese (Brazil)',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'id': 'Indonesian',
    'ms': 'Malay',
    'tl': 'Filipino',
    'tr': 'Turkish',
    'pl': 'Polish',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'da': 'Danish',
    'no': 'Norwegian',
    'fi': 'Finnish',
    'el': 'Greek',
    'he': 'Hebrew',
    'uk': 'Ukrainian',
    'cs': 'Czech',
    'ro': 'Romanian',
    'hu': 'Hungarian',
    'bg': 'Bulgarian',
    'hr': 'Croatian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'sr': 'Serbian',
    'bn': 'Bengali',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'pa': 'Punjabi',
    'ne': 'Nepali',
    'si': 'Sinhala',
    'km': 'Khmer',
    'lo': 'Lao',
    'my': 'Burmese',
    'zxx': 'No Speech',
    'und': 'Unknown',
    'Unknown': 'Unknown'
}

# --- COUNTRY CODE MAPPING ---
COUNTRY_NAMES = {
    'US': 'United States', 'GB': 'United Kingdom', 'IN': 'India', 'CA': 'Canada',
    'AU': 'Australia', 'DE': 'Germany', 'FR': 'France', 'BR': 'Brazil',
    'MX': 'Mexico', 'ES': 'Spain', 'IT': 'Italy', 'JP': 'Japan',
    'KR': 'South Korea', 'RU': 'Russia', 'ID': 'Indonesia', 'TH': 'Thailand',
    'VN': 'Vietnam', 'PH': 'Philippines', 'MY': 'Malaysia', 'SG': 'Singapore',
    'TW': 'Taiwan', 'HK': 'Hong Kong', 'NL': 'Netherlands', 'BE': 'Belgium',
    'SE': 'Sweden', 'NO': 'Norway', 'DK': 'Denmark', 'FI': 'Finland',
    'PL': 'Poland', 'TR': 'Turkey', 'SA': 'Saudi Arabia', 'AE': 'UAE',
    'EG': 'Egypt', 'ZA': 'South Africa', 'NG': 'Nigeria', 'KE': 'Kenya',
    'AR': 'Argentina', 'CL': 'Chile', 'CO': 'Colombia', 'PE': 'Peru',
    'PT': 'Portugal', 'AT': 'Austria', 'CH': 'Switzerland', 'IE': 'Ireland',
    'NZ': 'New Zealand', 'IL': 'Israel', 'GR': 'Greece', 'CZ': 'Czech Republic',
    'RO': 'Romania', 'HU': 'Hungary', 'UA': 'Ukraine', 'PK': 'Pakistan',
    'BD': 'Bangladesh', 'LK': 'Sri Lanka', 'NP': 'Nepal', 'MM': 'Myanmar',
    'KH': 'Cambodia', 'LA': 'Laos', 'SV': 'El Salvador', 'GT': 'Guatemala',
    'HN': 'Honduras', 'NI': 'Nicaragua', 'CR': 'Costa Rica', 'PA': 'Panama',
    'DO': 'Dominican Rep.', 'PR': 'Puerto Rico', 'JM': 'Jamaica', 'CU': 'Cuba',
    'VE': 'Venezuela', 'EC': 'Ecuador', 'BO': 'Bolivia', 'PY': 'Paraguay',
    'UY': 'Uruguay', 'HR': 'Croatia', 'RS': 'Serbia', 'BG': 'Bulgaria',
    'SK': 'Slovakia', 'SI': 'Slovenia', 'LT': 'Lithuania', 'LV': 'Latvia',
    'EE': 'Estonia', 'BY': 'Belarus', 'MD': 'Moldova', 'GE': 'Georgia',
    'AM': 'Armenia', 'AZ': 'Azerbaijan', 'KZ': 'Kazakhstan', 'UZ': 'Uzbekistan',
    'CY': 'Cyprus', 'MT': 'Malta', 'LU': 'Luxembourg', 'IS': 'Iceland',
    'MA': 'Morocco', 'TN': 'Tunisia', 'DZ': 'Algeria', 'JO': 'Jordan',
    'LB': 'Lebanon', 'IQ': 'Iraq', 'KW': 'Kuwait', 'QA': 'Qatar',
    'BH': 'Bahrain', 'OM': 'Oman', 'YE': 'Yemen', 'UG': 'Uganda'
}

def get_language_name(code):
    """Convert language code to readable name"""
    if pd.isna(code):
        return 'Unknown'
    return LANGUAGE_NAMES.get(str(code), str(code))

def get_country_name(code):
    """Convert country code to readable name"""
    if pd.isna(code):
        return 'Unknown'
    return COUNTRY_NAMES.get(str(code), str(code))

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YouTube Trends Analytics | BDA Project",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PROFESSIONAL DARK THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main Background */
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #111118 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d12 0%, #0a0a0f 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span {
        color: #a0a0a0 !important;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Metrics Cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 16px 20px;
    }
    div[data-testid="metric-container"] > label {
        color: #666 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #666;
        font-size: 1rem;
        font-weight: 400;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 1rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(255,255,255,0.02);
        border-radius: 8px;
        padding: 4px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: #666;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 0.9rem;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #fff;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
    }
    
    /* Dividers */
    hr {
        border-color: rgba(255,255,255,0.06) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Tech Badge */
    .tech-badge {
        display: inline-block;
        background: rgba(255, 107, 0, 0.15);
        color: #ff6b00;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    
    /* Info Box */
    .info-box {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
    }
    
</style>
""", unsafe_allow_html=True)

# --- OPTIMIZED DATA LOADER ---
@st.cache_data(ttl=3600, show_spinner="Loading dataset...")
def load_data():
    """Load pre-sampled data for Streamlit Cloud deployment"""
    try:
        cols = ['title', 'channel_name', 'view_count', 'like_count', 'comment_count', 
                'country', 'publish_date', 'langauge', 'daily_rank']
        
        # Load the pre-sampled file (for deployment)
        # For local dev with full file, uncomment the chunked reading below
        df = pd.read_csv('yt_trending_sample.csv', usecols=cols)
        
        # Cap at 15k rows for performance
        if len(df) > 15000:
            df = df.sample(n=15000, random_state=42)
        
        # Optimize dtypes
        df['country'] = df['country'].fillna('Unknown').astype('category')
        df['langauge'] = df['langauge'].fillna('Unknown').astype('category')
        df['channel_name'] = df['channel_name'].astype('category')
        
        # Parse dates
        df['publish_date'] = pd.to_datetime(df['publish_date'], utc=True, errors='coerce')
        
        # Engagement rate
        df['engagement_rate'] = np.where(
            df['view_count'] > 0,
            ((df['like_count'] + df['comment_count']) / df['view_count'] * 100).clip(0, 100),
            0
        )
        
        # Filter noise
        df = df[df['view_count'] > 5000]
        
        return df
    except Exception as e:
        st.error(f"Data loading error: {e}")
        return pd.DataFrame()

# --- SIDEBAR: PROJECT INFO + FILTER ---
with st.sidebar:
    st.markdown("## 📊 About This Project")
    st.markdown("---")
    
    st.markdown("""
    **YouTube Global Trends Analytics** is a Big Data project analyzing 
    trending video patterns across **113 countries**.
    """)
    
    st.markdown("### 🛠️ Technology Stack")
    st.markdown("""
    <span class="tech-badge">Apache Spark</span>
    <span class="tech-badge">PySpark</span>
    <span class="tech-badge">Python</span>
    <span class="tech-badge">Streamlit</span>
    <span class="tech-badge">Plotly</span>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>Why Spark?</strong><br>
    The dataset contains <strong>5.5GB+</strong> of video metadata. 
    Apache Spark enables distributed processing for efficient 
    analysis at this scale.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📁 Dataset Info")
    st.markdown("""
    **Source:** YouTube Trending Videos  
    **Size:** 5.5 GB (113 countries)  
    **Records:** ~10M+ videos
    """)
    
    st.markdown("""
    <div class="info-box" style="border-color: rgba(255,200,0,0.3);">
    <strong>⚠️ Data Note</strong><br>
    This dashboard uses a <strong>stratified sample</strong> of ~12,000 videos 
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 👤 Contact")
    st.markdown("""
    **Hemanth Raj**  
    [GitHub](https://github.com/Hemanthraj09) • [LinkedIn](https://www.linkedin.com/in/hemanthrajmv)
    """)

# Load data
df = load_data()
if df.empty:
    st.error("Failed to load data. Please check CSV path.")
    st.stop()

# Get unique values for filter options
country_codes = df['country'].dropna().unique().tolist()
country_names_list = sorted([get_country_name(c) for c in country_codes])[:30]
lang_codes = df['langauge'].dropna().unique().tolist()
lang_names_list = sorted([get_language_name(l) for l in lang_codes])[:15]

# --- PRE-AGGREGATE DATA ---
@st.cache_data
def get_aggregates(_df):
    # Country stats
    country_stats = _df.groupby('country', observed=True).agg({
        'view_count': ['sum', 'mean', 'count'],
        'engagement_rate': 'mean'
    }).reset_index()
    country_stats.columns = ['country', 'total_views', 'avg_views', 'video_count', 'avg_engagement']
    country_stats['country'] = country_stats['country'].apply(get_country_name)
    country_stats = country_stats.sort_values('total_views', ascending=False)
    
    # Language stats
    lang_stats = _df.groupby('langauge', observed=True).agg({
        'view_count': 'sum',
        'title': 'count',
        'engagement_rate': 'mean'
    }).reset_index()
    lang_stats.columns = ['language', 'total_views', 'video_count', 'avg_engagement']
    lang_stats['language'] = lang_stats['language'].apply(get_language_name)
    lang_stats = lang_stats.sort_values('total_views', ascending=False).head(12)
    
    # Channel stats
    channel_stats = _df.groupby('channel_name', observed=True).agg({
        'view_count': 'sum',
        'title': 'count',
        'engagement_rate': 'mean'
    }).reset_index()
    channel_stats.columns = ['channel', 'total_views', 'video_count', 'avg_engagement']
    channel_stats = channel_stats.sort_values('total_views', ascending=False).head(15)
    
    # Time series
    df_time = _df.dropna(subset=['publish_date']).copy()
    df_time['month'] = df_time['publish_date'].dt.to_period('M').astype(str)
    time_stats = df_time.groupby('month').agg({
        'view_count': 'sum',
        'title': 'count'
    }).reset_index()
    time_stats.columns = ['month', 'total_views', 'video_count']
    
    return country_stats, lang_stats, channel_stats, time_stats

country_stats, lang_stats, channel_stats, time_stats = get_aggregates(df)

# --- HEADER ---
st.markdown('<h1 class="main-header">YouTube Global Trends Analytics</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analyzing trending video patterns across 113 countries using Apache Spark</p>', unsafe_allow_html=True)

st.markdown("---")

# --- METRICS ROW ---
m1, m2, m3, m4, m5 = st.columns(5)

total_views = df['view_count'].sum()
avg_views = df['view_count'].mean()
avg_eng = df['engagement_rate'].median()

with m1:
    st.metric("Total Views", f"{total_views/1e9:.2f}B")
with m2:
    st.metric("Avg Views", f"{avg_views/1e6:.2f}M")
with m3:
    st.metric("Countries", f"{df['country'].nunique()}")
with m4:
    st.metric("Channels", f"{df['channel_name'].nunique():,}")
with m5:
    st.metric("Median Engagement", f"{avg_eng:.2f}%")

st.markdown("")

# --- KEY INSIGHTS SECTION ---
st.markdown("### 💡 Key Insights")

# Auto-generate insights from data
top_country = country_stats.iloc[0]['country']
top_country_views = country_stats.iloc[0]['total_views']
top_language = lang_stats.iloc[0]['language']
top_channel = channel_stats.iloc[0]['channel']
highest_eng_lang = lang_stats.loc[lang_stats['avg_engagement'].idxmax(), 'language']
highest_eng_val = lang_stats['avg_engagement'].max()

i1, i2, i3 = st.columns(3)

with i1:
    st.markdown(f"""
    <div class="info-box">
    <strong>🌍 Top Region</strong><br>
    <span style="color: #ff6b6b; font-size: 1.2rem;">{top_country}</span><br>
    leads with <strong>{top_country_views/1e9:.1f}B</strong> total views
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown(f"""
    <div class="info-box">
    <strong>🗣️ Dominant Language</strong><br>
    <span style="color: #ff6b6b; font-size: 1.2rem;">{top_language}</span><br>
    content dominates the trending charts
    </div>
    """, unsafe_allow_html=True)

with i3:
    st.markdown(f"""
    <div class="info-box">
    <strong>📈 Highest Engagement</strong><br>
    <span style="color: #ff6b6b; font-size: 1.2rem;">{highest_eng_lang}</span><br>
    videos average <strong>{highest_eng_val:.2f}%</strong> engagement
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# --- INTERACTIVE FILTER ---
st.markdown("### 🎛️ Filter Data")
filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 1])

with filter_col1:
    selected_country = st.selectbox(
        "🌍 Region",
        ['All Countries'] + country_names_list,
        key="country_filter"
    )

with filter_col2:
    selected_lang = st.selectbox(
        "🗣️ Language",
        ['All Languages'] + lang_names_list,
        key="lang_filter"
    )

with filter_col3:
    st.markdown("")  # Spacing

# --- APPLY FILTERS TO DATA ---
filtered_df = df.copy()

# Create reverse mappings for filtering
reverse_country_map = {v: k for k, v in COUNTRY_NAMES.items()}
reverse_lang_map = {v: k for k, v in LANGUAGE_NAMES.items()}

if selected_country != 'All Countries':
    # Get the original country code
    country_code = reverse_country_map.get(selected_country, selected_country)
    filtered_df = filtered_df[filtered_df['country'] == country_code]

if selected_lang != 'All Languages':
    # Get the original language code
    lang_code = reverse_lang_map.get(selected_lang, selected_lang)
    filtered_df = filtered_df[filtered_df['langauge'] == lang_code]

# Show filter status
if selected_country != 'All Countries' or selected_lang != 'All Languages':
    filters_applied = []
    if selected_country != 'All Countries':
        filters_applied.append(f"**{selected_country}**")
    if selected_lang != 'All Languages':
        filters_applied.append(f"**{selected_lang}**")
    filtered_note = f"📌 Showing data for: {' • '.join(filters_applied)} ({len(filtered_df):,} videos)"
    st.markdown(f"<p style='color: #ff6b6b; font-size: 0.9rem;'>{filtered_note}</p>", unsafe_allow_html=True)

# Re-aggregate filtered data for charts (NO CACHING - must recalculate on filter change)
MIN_VIDEOS_THRESHOLD = 3  # Minimum videos to show in charts (reduces noise)

if len(filtered_df) > 0:
    # Country stats (filtered)
    filtered_country_stats = filtered_df.groupby('country', observed=True).agg({
        'view_count': ['sum', 'mean', 'count'],
        'engagement_rate': 'mean'
    }).reset_index()
    filtered_country_stats.columns = ['country', 'total_views', 'avg_views', 'video_count', 'avg_engagement']
    filtered_country_stats['country'] = filtered_country_stats['country'].apply(get_country_name)
    # Filter out countries with very few videos (noise reduction)
    filtered_country_stats = filtered_country_stats[filtered_country_stats['video_count'] >= MIN_VIDEOS_THRESHOLD]
    filtered_country_stats = filtered_country_stats.sort_values('total_views', ascending=False)
    
    # Language stats (filtered)
    filtered_lang_stats = filtered_df.groupby('langauge', observed=True).agg({
        'view_count': 'sum',
        'title': 'count',
        'engagement_rate': 'mean'
    }).reset_index()
    filtered_lang_stats.columns = ['language', 'total_views', 'video_count', 'avg_engagement']
    filtered_lang_stats['language'] = filtered_lang_stats['language'].apply(get_language_name)
    # Filter out languages with very few videos (noise reduction)
    filtered_lang_stats = filtered_lang_stats[filtered_lang_stats['video_count'] >= MIN_VIDEOS_THRESHOLD]
    filtered_lang_stats = filtered_lang_stats.sort_values('total_views', ascending=False).head(12)
    
    # Channel stats (filtered)
    filtered_channel_stats = filtered_df.groupby('channel_name', observed=True).agg({
        'view_count': 'sum',
        'title': 'count',
        'engagement_rate': 'mean'
    }).reset_index()
    filtered_channel_stats.columns = ['channel', 'total_views', 'video_count', 'avg_engagement']
    # Filter out channels with very few videos (noise reduction)
    filtered_channel_stats = filtered_channel_stats[filtered_channel_stats['video_count'] >= MIN_VIDEOS_THRESHOLD]
    filtered_channel_stats = filtered_channel_stats.sort_values('total_views', ascending=False).head(15)
    
    # Time series (filtered)
    df_time = filtered_df.dropna(subset=['publish_date']).copy()
    if len(df_time) > 0:
        df_time['month'] = df_time['publish_date'].dt.to_period('M').astype(str)
        filtered_time_stats = df_time.groupby('month').agg({
            'view_count': 'sum',
            'title': 'count'
        }).reset_index()
        filtered_time_stats.columns = ['month', 'total_views', 'video_count']
    else:
        filtered_time_stats = pd.DataFrame(columns=['month', 'total_views', 'video_count'])
else:
    st.warning("No data matches the selected filters.")
    filtered_country_stats = country_stats
    filtered_lang_stats = lang_stats
    filtered_channel_stats = channel_stats
    filtered_time_stats = time_stats

st.markdown("")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🌍 Geographic Insights", "📊 Content Analysis", "🏆 Top Performers"])

with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<p class="section-title">Views by Country (Top 15)</p>', unsafe_allow_html=True)
        
        top_countries = filtered_country_stats.head(15)
        fig = px.bar(
            top_countries,
            x='total_views',
            y='country',
            orientation='h',
            color='total_views',
            color_continuous_scale=[[0, '#1a1a2e'], [0.5, '#4a1942'], [1, '#ff6b6b']]
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=420,
            showlegend=False,
            coloraxis_showscale=False,
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Total Views",
            yaxis_title="",
            margin=dict(l=0, r=20, t=10, b=40),
            font=dict(size=11)
        )
        fig.update_traces(hovertemplate='<b>%{y}</b><br>Views: %{x:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<p class="section-title">Views by Language</p>', unsafe_allow_html=True)
        
        fig = px.pie(
            filtered_lang_stats.head(8),
            values='total_views',
            names='language',
            color_discrete_sequence=px.colors.sequential.Plasma_r,
            hole=0.45
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            height=420,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=10, color='#888')
            ),
            margin=dict(l=10, r=10, t=10, b=50)
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent',
            textfont=dict(size=11, color='white'),
            hovertemplate='<b>%{label}</b><br>Views: %{value:,.0f}<extra></extra>'
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-title">Language Distribution by Views</p>', unsafe_allow_html=True)
        
        fig = px.bar(
            filtered_lang_stats,
            x='language',
            y='total_views',
            color='avg_engagement',
            color_continuous_scale='RdYlGn',
            labels={'avg_engagement': 'Engagement %'}
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=380,
            xaxis_tickangle=-45,
            xaxis_title="",
            yaxis_title="Total Views",
            margin=dict(l=0, r=0, t=10, b=80),
            font=dict(size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<p class="section-title">Engagement vs Popularity</p>', unsafe_allow_html=True)
        
        # Use language stats for scatter (clean, aggregated data)
        fig = px.scatter(
            filtered_lang_stats,
            x='total_views',
            y='avg_engagement',
            size='video_count',
            color='language',
            size_max=45,
            labels={
                'total_views': 'Total Views',
                'avg_engagement': 'Avg Engagement %',
                'video_count': 'Videos'
            }
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=380,
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=40),
            font=dict(size=11)
        )
        fig.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>Views: %{x:,.0f}<br>Engagement: %{y:.2f}%<extra></extra>',
            customdata=filtered_lang_stats[['language']].values
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown('<p class="section-title">Top 15 Channels by Total Views</p>', unsafe_allow_html=True)
    
    fig = px.bar(
        filtered_channel_stats,
        x='total_views',
        y='channel',
        orientation='h',
        color='avg_engagement',
        color_continuous_scale=[[0, '#1a1a2e'], [0.5, '#2d4a3e'], [1, '#4ade80']],
        labels={'avg_engagement': 'Engagement %'}
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=450,
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title="Total Views",
        yaxis_title="",
        margin=dict(l=0, r=20, t=10, b=40),
        font=dict(size=11)
    )
    fig.update_traces(hovertemplate='<b>%{y}</b><br>Views: %{x:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True)
    
    # Time series
    if not filtered_time_stats.empty and len(filtered_time_stats) > 1:
        st.markdown('<p class="section-title">Trending Activity Over Time</p>', unsafe_allow_html=True)
        
        fig = px.area(
            filtered_time_stats,
            x='month',
            y='total_views',
            labels={'month': 'Month', 'total_views': 'Total Views'}
        )
        fig.update_traces(
            line_color='#ff6b6b',
            fillcolor='rgba(255, 107, 107, 0.15)'
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=280,
            margin=dict(l=0, r=0, t=10, b=40),
            xaxis_title="",
            yaxis_title="Views",
            font=dict(size=11)
        )
        st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])

with footer_col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <p style="color: #666; font-size: 0.9rem; margin-bottom: 8px;">
            <strong>Big Data Analytics Project</strong> • Built with Apache Spark & Streamlit
        </p>
        <p style="color: #888; font-size: 0.8rem;">
            Developed by <strong style="color: #ff6b6b;">Hemanth Raj</strong> | 
            <a href="https://github.com/Hemanthraj09" target="_blank" style="color: #888;">GitHub</a> • 
            <a href="https://www.linkedin.com/in/hemanthrajmv" target="_blank" style="color: #888;">LinkedIn</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
