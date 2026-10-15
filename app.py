import html

import streamlit as st
import pandas as pd
import numpy as np
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
    'aa': 'Afar', 'ab': 'Abkhazian', 'ase': 'American Sign Language', 'az': 'Azerbaijani',
    'bgc': 'Haryanvi', 'bh': 'Bihari', 'bm': 'Bambara', 'bn-IN': 'Bengali (India)', 'bs': 'Bosnian',
    'de-AT': 'German (Austria)', 'de-CH': 'German (Switzerland)', 'de-DE': 'German (Germany)',
    'en-AU': 'English (Australia)', 'en-CA': 'English (Canada)', 'es-419': 'Spanish (Latin America)',
    'es-US': 'Spanish (US)', 'et': 'Estonian', 'fa': 'Persian', 'ff': 'Fula', 'fil': 'Filipino',
    'fr-BE': 'French (Belgium)', 'fr-CA': 'French (Canada)', 'fr-FR': 'French (France)', 'ga': 'Irish',
    'hi-Latn': 'Hindi (Latin script)', 'ht': 'Haitian Creole', 'hy': 'Armenian', 'iw': 'Hebrew',
    'jv': 'Javanese', 'ka': 'Georgian', 'kk': 'Kazakh', 'ku': 'Kurdish', 'lg': 'Ganda',
    'lt': 'Lithuanian', 'lv': 'Latvian', 'mk': 'Macedonian', 'mn': 'Mongolian',
    'mn-Mong': 'Mongolian (Mongolian script)', 'mo': 'Moldovan', 'nl-NL': 'Dutch (Netherlands)',
    'or': 'Odia', 'pt-PT': 'Portuguese (Portugal)', 'sh': 'Serbo-Croatian', 'sn': 'Shona',
    'sq': 'Albanian', 'sr-Cyrl': 'Serbian (Cyrillic)', 'sr-Latn': 'Serbian (Latin)', 'sw': 'Swahili',
    'tg': 'Tajik', 'ur': 'Urdu', 'uz': 'Uzbek', 'vro': 'Võro', 'wo': 'Wolof', 'yo': 'Yoruba',
    'yue': 'Cantonese', 'yue-HK': 'Cantonese (Hong Kong)', 'zh-HK': 'Chinese (Hong Kong)',
    'zh-Hans': 'Chinese (Simplified)', 'zh-Hant': 'Chinese (Traditional)', 'zu': 'Zulu',
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
    'BH': 'Bahrain', 'OM': 'Oman', 'YE': 'Yemen', 'UG': 'Uganda',
    'AL': 'Albania', 'BA': 'Bosnia & Herzegovina', 'GH': 'Ghana', 'LI': 'Liechtenstein',
    'LY': 'Libya', 'ME': 'Montenegro', 'MK': 'North Macedonia', 'MN': 'Mongolia',
    'PG': 'Papua New Guinea', 'SN': 'Senegal', 'TZ': 'Tanzania', 'ZW': 'Zimbabwe'
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

# ISO-3166 alpha-3 codes, needed by the Plotly world map
COUNTRY_ISO3 = {
    'AE': 'ARE', 'AL': 'ALB', 'AM': 'ARM', 'AR': 'ARG', 'AT': 'AUT', 'AU': 'AUS', 'AZ': 'AZE',
    'BA': 'BIH', 'BD': 'BGD', 'BE': 'BEL', 'BG': 'BGR', 'BH': 'BHR', 'BO': 'BOL', 'BR': 'BRA',
    'BY': 'BLR', 'CA': 'CAN', 'CH': 'CHE', 'CL': 'CHL', 'CO': 'COL', 'CR': 'CRI', 'CY': 'CYP',
    'CZ': 'CZE', 'DE': 'DEU', 'DK': 'DNK', 'DO': 'DOM', 'DZ': 'DZA', 'EC': 'ECU', 'EE': 'EST',
    'EG': 'EGY', 'ES': 'ESP', 'FI': 'FIN', 'FR': 'FRA', 'GB': 'GBR', 'GE': 'GEO', 'GH': 'GHA',
    'GR': 'GRC', 'GT': 'GTM', 'HK': 'HKG', 'HN': 'HND', 'HR': 'HRV', 'HU': 'HUN', 'ID': 'IDN',
    'IE': 'IRL', 'IL': 'ISR', 'IN': 'IND', 'IQ': 'IRQ', 'IS': 'ISL', 'IT': 'ITA', 'JM': 'JAM',
    'JO': 'JOR', 'JP': 'JPN', 'KE': 'KEN', 'KH': 'KHM', 'KR': 'KOR', 'KW': 'KWT', 'KZ': 'KAZ',
    'LA': 'LAO', 'LB': 'LBN', 'LI': 'LIE', 'LK': 'LKA', 'LT': 'LTU', 'LU': 'LUX', 'LV': 'LVA',
    'LY': 'LBY', 'MA': 'MAR', 'MD': 'MDA', 'ME': 'MNE', 'MK': 'MKD', 'MN': 'MNG', 'MT': 'MLT',
    'MX': 'MEX', 'MY': 'MYS', 'NG': 'NGA', 'NI': 'NIC', 'NL': 'NLD', 'NO': 'NOR', 'NP': 'NPL',
    'NZ': 'NZL', 'OM': 'OMN', 'PA': 'PAN', 'PE': 'PER', 'PG': 'PNG', 'PH': 'PHL', 'PK': 'PAK',
    'PL': 'POL', 'PR': 'PRI', 'PT': 'PRT', 'PY': 'PRY', 'QA': 'QAT', 'RO': 'ROU', 'RS': 'SRB',
    'RU': 'RUS', 'SA': 'SAU', 'SE': 'SWE', 'SG': 'SGP', 'SI': 'SVN', 'SK': 'SVK', 'SN': 'SEN',
    'SV': 'SLV', 'TH': 'THA', 'TN': 'TUN', 'TR': 'TUR', 'TW': 'TWN', 'TZ': 'TZA', 'UA': 'UKR',
    'UG': 'UGA', 'US': 'USA', 'UY': 'URY', 'VE': 'VEN', 'VN': 'VNM', 'YE': 'YEM', 'ZA': 'ZAF',
    'ZW': 'ZWE',
}

# --- DESIGN TOKENS (dark theme; matches .streamlit/config.toml) ---
PAGE_BG = '#0d0d0d'
SURFACE = '#1a1a19'
INK = '#f0efec'          # primary text
INK_2 = '#c3c2b7'        # secondary text
MUTED = '#898781'        # axis labels, captions
GRID = '#2c2c2a'         # hairline gridlines
AXIS = '#383835'         # baselines
BORDER = 'rgba(255,255,255,0.10)'
ACCENT = '#3987e5'       # default single-series colour (categorical slot 1, dark step)
CORAL = '#e66767'        # app accent, selection highlight and geography (slot 8, dark step)
GOOD = '#0ca30c'         # status colour for an improvement; always paired with an icon and label
# Identity colours for the top three named languages: the most a scatter can carry while
# every pair stays distinguishable, including for colour-blind readers (validated)
LANG_COLORS = ['#3987e5', '#d95926', '#199e70']
UNKNOWN_GREY = '#8a8984'
OTHER_GREY = '#5f5e59'
DIMMED = '#4b4a46'       # de-emphasised marks when a selection is highlighted
NO_DATA = '#242423'      # map land without data
FONT = '"Source Sans Pro", "Source Sans 3", system-ui, -apple-system, "Segoe UI", sans-serif'
# Single-hue sequential ramp (coral) for the map; on a dark surface low values sit darkest.
# Its mid step is CORAL, the colour of the country bars, so map and ranking read as one.
SEQ_RAMP = ['#3b1614', '#5c201c', '#7f2b25', '#a3362f', '#c4453c', '#e66767',
            '#ee8a84', '#f5aca7', '#fbd0cc']

MIN_GROUP = 10           # minimum videos for a country/language to be ranked
MIN_CHANNEL_VIDEOS = 2   # minimum videos for a channel to be ranked
SCATTER_MIN = 30         # minimum videos for a language to appear in the scatter
ALL_COUNTRIES = 'All countries'
ALL_LANGUAGES = 'All languages'


def fmt_pct(p):
    """Percentage that never rounds a non-zero share down to 0."""
    return '<0.1%' if 0 < p < 0.1 else f'{p:.1f}%'


def plural(n, singular, plural_form):
    return f"{n:,} {singular if n == 1 else plural_form}"


def fmt_num(n):
    """Compact human-readable number: 1.2K, 3.4M, 5.6B."""
    if pd.isna(n):
        return '–'
    n = float(n)
    for div, suffix in ((1e9, 'B'), (1e6, 'M'), (1e3, 'K')):
        if abs(n) >= div:
            return f'{n / div:.1f}{suffix}'
    return f'{n:,.0f}'


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YouTube Trends Analytics | BDA Project",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLES (theme colours come from .streamlit/config.toml) ---
st.markdown(f"""
<style>
    .block-container {{ padding-top: 2.2rem; padding-bottom: 2rem; max-width: 1400px; }}

    /* Header */
    .hero-title {{ font-size: 2.1rem; font-weight: 700; color: {INK}; margin: 0; line-height: 1.2; }}
    .hero-sub {{ color: {INK_2}; font-size: 1rem; margin: 6px 0 14px 0; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 4px; }}
    .chip {{
        background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 999px;
        color: {INK_2}; font-size: 0.8rem; padding: 3px 12px;
    }}

    /* Section labels */
    .section-label {{
        color: {MUTED}; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em;
        text-transform: uppercase; margin: 18px 0 8px 0;
    }}
    .chart-title {{ color: {INK}; font-size: 1.02rem; font-weight: 600; margin: 4px 0 0 0; }}
    .chart-sub {{ color: {MUTED}; font-size: 0.85rem; margin: 2px 0 6px 0; }}
    .legend {{ display: flex; flex-wrap: wrap; gap: 6px 16px; color: {INK_2}; font-size: 0.85rem; margin: 2px 0 10px 0; }}
    .legend i {{ display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }}

    /* Stat tiles (st.metric with border=True) */
    [data-testid="stMetric"] {{
        background: {SURFACE}; border: 1px solid {BORDER} !important; border-radius: 12px;
        padding: 14px 18px;
    }}
    [data-testid="stMetricLabel"] p {{ color: {MUTED} !important; font-size: 0.82rem !important; }}
    [data-testid="stMetricValue"] {{ color: {INK} !important; font-size: 1.75rem !important; font-weight: 600; }}

    /* Insight cards */
    .insight {{
        background: {SURFACE}; border: 1px solid {BORDER}; border-left: 3px solid {CORAL};
        border-radius: 12px; padding: 14px 18px; min-height: 124px;
    }}
    .insight-label {{ color: {MUTED}; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }}
    .insight-value {{ color: {INK}; font-size: 1.25rem; font-weight: 600; margin: 4px 0 2px 0; }}
    .insight-note {{ color: {INK_2}; font-size: 0.9rem; }}
    .insight-note b {{ color: {INK}; }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BORDER}; }}
    .stTabs [data-baseweb="tab"] {{ padding: 8px 16px; color: {INK_2}; font-weight: 500; }}
    .stTabs [aria-selected="true"] {{ color: {INK} !important; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{ border-right: 1px solid {BORDER}; }}
    .side-title {{ color: {INK}; font-size: 1.05rem; font-weight: 700; margin-bottom: 4px; }}
    .side-text {{ color: {INK_2}; font-size: 0.88rem; line-height: 1.55; }}
    .side-label {{ color: {MUTED}; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin: 18px 0 6px 0; }}
    .tech-badge {{
        display: inline-block; background: rgba(230,103,103,0.14); color: #f5aca7;
        border-radius: 6px; font-size: 0.75rem; font-weight: 600;
        padding: 3px 9px; margin: 0 6px 6px 0;
    }}
    .side-card {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 10px; padding: 12px 14px; margin-top: 4px; }}
    .side-card .big {{ color: {INK}; font-size: 1.15rem; font-weight: 700; }}
    .side-card .small {{ color: {MUTED}; font-size: 0.8rem; }}
    .side-card .good {{ color: {GOOD}; font-size: 0.8rem; font-weight: 600; }}

    /* Footer */
    .footer {{ text-align: center; color: {MUTED}; font-size: 0.82rem; padding: 18px 0 6px 0; border-top: 1px solid {BORDER}; margin-top: 28px; }}
    .footer a {{ color: {INK_2}; }}
</style>
""", unsafe_allow_html=True)


# --- DATA LOADER ---
@st.cache_data(ttl=3600, show_spinner="Loading dataset...")
def load_data():
    """Load pre-sampled data for Streamlit Cloud deployment.

    Errors are raised rather than caught here, so a failed load is not cached.
    """
    cols = ['title', 'channel_name', 'view_count', 'like_count', 'comment_count',
            'country', 'publish_date', 'langauge', 'daily_rank']

    # Load the pre-sampled file (for deployment)
    df = pd.read_csv('yt_trending_sample.csv', usecols=cols)

    # Cap at 15k rows for performance
    if len(df) > 15000:
        df = df.sample(n=15000, random_state=42)

    # Optimize dtypes
    df['country'] = df['country'].fillna('Unknown').astype('category')
    df['langauge'] = df['langauge'].fillna('Unknown').astype('category')
    df['channel_name'] = df['channel_name'].astype('category')

    # Readable names, used for grouping and filtering. Codes that share a name
    # (e.g. missing language and 'und' are both "Unknown") collapse into one group.
    df['country_name'] = df['country'].map(get_country_name).astype('category')
    df['language_name'] = df['langauge'].map(get_language_name).astype('category')
    df['iso3'] = df['country'].map(lambda c: COUNTRY_ISO3.get(str(c)))

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


def group_stats(data, key, min_videos=1):
    """Per-group video count, total/median views and median engagement."""
    g = data.groupby(key, observed=True).agg(
        videos=('view_count', 'size'),
        total_views=('view_count', 'sum'),
        median_views=('view_count', 'median'),
        engagement=('engagement_rate', 'median'),
    ).reset_index()
    return g[g['videos'] >= min_videos]


# --- CHART HELPERS ---
def style_fig(fig, height):
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=4, r=12, t=8, b=4),
        font=dict(family=FONT, size=12, color=INK_2),
        hoverlabel=dict(bgcolor=SURFACE, bordercolor=AXIS, font=dict(family=FONT, size=13, color=INK)),
        showlegend=False,
        bargap=0.35,
        barcornerradius=4,
    )
    axis = dict(gridcolor=GRID, linecolor=AXIS, zeroline=False, tickfont=dict(color=MUTED),
                title_font=dict(color=MUTED, size=12), exponentformat='B')
    fig.update_xaxes(**axis)
    fig.update_yaxes(**axis)
    return fig


def show_chart(fig):
    st.plotly_chart(fig, width='stretch', theme=None, config={'displayModeBar': False})


def chart_heading(title, subtitle=None):
    st.markdown(f'<div class="chart-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="chart-sub">{html.escape(subtitle)}</div>', unsafe_allow_html=True)


def hbar(data, label_col, value_col, highlight=None, value_title='', hover_extra=None, height=420,
         color=ACCENT, color_map=None):
    """Horizontal bar chart, largest at the top.

    Bars use `color`, or per-label identity colours from `color_map` (others grey). With a
    `highlight`, that bar keeps its colour (coral if it had none) and the rest are dimmed.
    """
    data = data.sort_values(value_col)
    base = [color_map.get(lbl, OTHER_GREY) if color_map else color for lbl in data[label_col]]
    if highlight is None:
        colors = base
    else:
        colors = [(CORAL if b in (OTHER_GREY, UNKNOWN_GREY) else b) if lbl == highlight else DIMMED
                  for lbl, b in zip(data[label_col], base)]
    custom = np.stack([data[value_col].map(fmt_num)] + [data[c] for c, _ in (hover_extra or [])], axis=-1)
    extra = ''.join(f'<br>{name}: %{{customdata[{i + 1}]}}' for i, (_, name) in enumerate(hover_extra or []))
    fig = go.Figure(go.Bar(
        x=data[value_col], y=data[label_col].astype(str), orientation='h',
        marker=dict(color=colors, line=dict(width=0)), customdata=custom,
        hovertemplate=f'<b>%{{y}}</b><br>{value_title}: %{{customdata[0]}}{extra}<extra></extra>',
    ))
    style_fig(fig, height)
    fig.update_xaxes(title_text=value_title, showgrid=True)
    fig.update_yaxes(showgrid=False, ticksuffix='  ', tickfont=dict(color=INK_2))
    return fig


def language_colors(stats):
    """Identity colours for the top three named languages in this scope; the rest are grey."""
    named = stats[stats['language_name'] != 'Unknown'].nlargest(len(LANG_COLORS), 'total_views')
    cmap = dict(zip(named['language_name'], LANG_COLORS))
    cmap['Unknown'] = UNKNOWN_GREY
    return cmap


def legend(items):
    """Colour key shared by the charts below it; names stay in text colour."""
    st.markdown('<div class="legend">' + ''.join(
        f'<span><i style="background:{color}"></i>{html.escape(str(name))}</span>' for name, color in items
    ) + '</div>', unsafe_allow_html=True)


def table_view(data, columns):
    """Accessible table twin for a chart."""
    with st.expander('View as table'):
        st.dataframe(data, hide_index=True, width='stretch', column_config=columns)


def insight_card(label, value, note_html):
    st.markdown(f"""
    <div class="insight">
        <div class="insight-label">{label}</div>
        <div class="insight-value">{html.escape(str(value))}</div>
        <div class="insight-note">{note_html}</div>
    </div>""", unsafe_allow_html=True)


# --- SIDEBAR: PROJECT INFO ---
with st.sidebar:
    st.markdown('<div class="side-title">YouTube Global Trends Analytics</div>', unsafe_allow_html=True)
    st.markdown("""<div class="side-text">A Big Data project analysing what trends on YouTube
        across <b>113 countries</b>, from a 5.5 GB dataset of ~4.3M trending records.</div>""",
                unsafe_allow_html=True)

    st.markdown('<div class="side-label">Technology</div>', unsafe_allow_html=True)
    st.markdown("""
    <span class="tech-badge">Apache Spark</span><span class="tech-badge">PySpark</span>
    <span class="tech-badge">Spark MLlib</span><span class="tech-badge">Parquet</span>
    <span class="tech-badge">Streamlit</span><span class="tech-badge">Plotly</span>
    """, unsafe_allow_html=True)

    st.markdown('<div class="side-label">View-count forecast (Spark MLlib)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="side-card">
        <div class="big">1.6% median error</div>
        <div class="small">1 day ahead · baseline 9.6%</div>
        <div class="good">▼ 84% lower error than baseline</div>
        <div class="big" style="margin-top:8px;">3.7% median error</div>
        <div class="small">3 days ahead · baseline 20.4%</div>
        <div class="good">▼ 82% lower error than baseline</div>
        <div class="small" style="margin-top:8px;">Baseline = assume views don't change</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="side-label">About the data</div>', unsafe_allow_html=True)
    st.markdown("""<div class="side-text">
        Source: YouTube trending lists across 113 countries.<br>
        This dashboard uses a <b>random sample of ~15,000</b> trending entries.
        View counts are global per video.</div>""", unsafe_allow_html=True)

    st.markdown('<div class="side-label">Contact</div>', unsafe_allow_html=True)
    st.markdown("""<div class="side-text"><b>Hemanth Raj</b><br>
        <a href="https://github.com/Hemanthraj09">GitHub</a> ·
        <a href="https://www.linkedin.com/in/hemanthrajmv">LinkedIn</a></div>""", unsafe_allow_html=True)


# --- LOAD DATA ---
try:
    df = load_data()
except Exception as e:
    st.error(f"Data loading error: {e}")
    st.stop()
if df.empty:
    st.error("Failed to load data. Please check CSV path.")
    st.stop()

# --- HEADER ---
pub = df['publish_date'].dropna()
st.markdown('<div class="hero-title">YouTube Global Trends Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">What trends on YouTube across 113 countries, processed with Apache Spark</div>',
            unsafe_allow_html=True)
st.markdown(f"""
<div class="chips">
    <span class="chip">{len(df):,} sampled trending entries</span>
    <span class="chip">{df['country_name'].nunique()} countries</span>
    <span class="chip">{df['language_name'].nunique()} languages</span>
    <span class="chip">Published {pub.min():%b %Y} – {pub.max():%b %Y}</span>
</div>""", unsafe_allow_html=True)

# --- FILTERS (one row, scoping everything below) ---
def reset_filters():
    st.session_state['country_filter'] = ALL_COUNTRIES
    st.session_state['lang_filter'] = ALL_LANGUAGES

st.markdown('<div class="section-label">Filters</div>', unsafe_allow_html=True)
f1, f2, f3 = st.columns([3, 3, 1], vertical_alignment='bottom')
with f1:
    selected_country = st.selectbox(
        "Region", [ALL_COUNTRIES] + sorted(df['country_name'].unique().tolist()), key="country_filter")
with f2:
    selected_lang = st.selectbox(
        "Language", [ALL_LANGUAGES] + sorted(df['language_name'].unique().tolist()), key="lang_filter")
with f3:
    st.button("Reset", on_click=reset_filters, width='stretch',
              disabled=selected_country == ALL_COUNTRIES and selected_lang == ALL_LANGUAGES)

country_sel = None if selected_country == ALL_COUNTRIES else selected_country
lang_sel = None if selected_lang == ALL_LANGUAGES else selected_lang

# Each dimension's own chart shows its full distribution (filtered by the other
# dimension only) and highlights the selection; everything else uses both filters.
by_lang = df if lang_sel is None else df[df['language_name'] == lang_sel]
by_country = df if country_sel is None else df[df['country_name'] == country_sel]
fdf = by_lang if country_sel is None else by_lang[by_lang['country_name'] == country_sel]

if fdf.empty:
    st.warning("No videos match this combination of filters. Try another region or language, or reset.")
    st.stop()

scope = ' · '.join(s for s in (country_sel, lang_sel) if s) or 'All regions and languages'

# --- STAT TILES ---
st.markdown(f'<div class="section-label">Overview · {html.escape(scope)}</div>', unsafe_allow_html=True)
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Trending entries", f"{len(fdf):,}", border=True)
m2.metric("Total views", fmt_num(fdf['view_count'].sum()), border=True)
m3.metric("Median views", fmt_num(fdf['view_count'].median()), border=True,
          help="Typical views of a trending video (half have more, half fewer)")
m4.metric("Engagement", f"{fdf['engagement_rate'].median():.2f}%", border=True,
          help="Median of (likes + comments) ÷ views")
m5.metric("Channels", f"{fdf['channel_name'].nunique():,}", border=True)

# --- KEY INSIGHTS (respond to the filters) ---
st.markdown('<div class="section-label">Key insights</div>', unsafe_allow_html=True)
i1, i2, i3 = st.columns(3)

with i1:
    if country_sel is None:
        cs = group_stats(fdf, 'country_name', MIN_GROUP)
        if cs.empty:
            cs = group_stats(fdf, 'country_name')
        top = cs.loc[cs['median_views'].idxmax()]
        insight_card("Top region", top['country_name'],
                     f"Its trending videos have the highest median views: <b>{fmt_num(top['median_views'])}</b>")
    else:
        ch = group_stats(fdf, 'channel_name')
        top = ch.loc[ch['total_views'].idxmax()]
        insight_card("Top channel here", top['channel_name'],
                     f"<b>{fmt_num(top['total_views'])}</b> views across {plural(int(top['videos']), 'trending entry', 'trending entries')}")

with i2:
    if lang_sel is None:
        ls = group_stats(fdf, 'language_name')
        top = ls.loc[ls['total_views'].idxmax()]
        share = top['total_views'] / fdf['view_count'].sum() * 100
        insight_card("Dominant language", top['language_name'],
                     f"<b>{share:.0f}%</b> of all views in this selection")
    else:
        share = fdf['view_count'].sum() / by_country['view_count'].sum() * 100
        where = html.escape(country_sel) if country_sel else 'all regions'
        insight_card("Share of views", fmt_pct(share),
                     f"of views in {where} come from <b>{html.escape(lang_sel)}</b> videos")

with i3:
    if lang_sel is None:
        ls = group_stats(fdf, 'language_name', MIN_GROUP)
        if ls.empty:
            ls = group_stats(fdf, 'language_name')
        top = ls.loc[ls['engagement'].idxmax()]
        insight_card("Most engaging language", top['language_name'],
                     f"Median engagement <b>{top['engagement']:.2f}%</b> "
                     f"vs {fdf['engagement_rate'].median():.2f}% overall")
    else:
        ch = group_stats(fdf, 'channel_name', MIN_CHANNEL_VIDEOS)
        if ch.empty:
            ch = group_stats(fdf, 'channel_name')
        top = ch.loc[ch['engagement'].idxmax()]
        insight_card("Most engaging channel", top['channel_name'],
                     f"Median engagement <b>{top['engagement']:.2f}%</b> "
                     f"vs {fdf['engagement_rate'].median():.2f}% overall")

st.write("")

# --- TABS (the dashboard's three sections) ---
tab_geo, tab_content, tab_top = st.tabs(["🌍 Geographic Insights", "📊 Content Analysis", "🏆 Top Performers"])

COMMON_COLUMNS = {
    'videos': st.column_config.NumberColumn('Trending entries', format='%d'),
    'total_views': st.column_config.NumberColumn('Total views', format='compact'),
    'median_views': st.column_config.NumberColumn('Median views', format='compact'),
    'engagement': st.column_config.NumberColumn('Median engagement', format='%.2f%%'),
}

with tab_geo:
    geo = group_stats(by_lang, ['country_name', 'iso3'])
    ranked = geo[geo['videos'] >= MIN_GROUP] if (geo['videos'] >= MIN_GROUP).any() else geo
    note = f" · {lang_sel} videos" if lang_sel else ""

    chart_heading("Median views per trending video, by country",
                  f"Typical global views of the videos trending in each country{note}. "
                  "Dark grey: not in the dataset. Countries too small for the map appear in the ranking and table.")
    mapped = geo.dropna(subset=['iso3'])
    fig = go.Figure(go.Choropleth(
        locations=mapped['iso3'], z=np.log10(mapped['median_views']),
        colorscale=[[i / (len(SEQ_RAMP) - 1), c] for i, c in enumerate(SEQ_RAMP)],
        marker=dict(line=dict(color=PAGE_BG, width=0.5)),
        customdata=np.stack([mapped['country_name'].astype(str), mapped['median_views'].map(fmt_num),
                             mapped['videos'], mapped['total_views'].map(fmt_num)], axis=-1),
        hovertemplate='<b>%{customdata[0]}</b><br>Median views: %{customdata[1]}'
                      '<br>Trending entries: %{customdata[2]}<br>Total views: %{customdata[3]}<extra></extra>',
        colorbar=dict(
            title=dict(text='Median views', font=dict(color=MUTED, size=12)),
            tickvals=[4, 5, 6, 7, 8], ticktext=['10K', '100K', '1M', '10M', '100M'],
            tickfont=dict(color=MUTED), outlinewidth=0, thickness=10, len=0.7, x=1.0,
        ),
    ))
    if country_sel is not None and not mapped[mapped['country_name'] == country_sel].empty:
        sel_iso = mapped.loc[mapped['country_name'] == country_sel, 'iso3']
        fig.add_trace(go.Choropleth(
            locations=sel_iso, z=[0] * len(sel_iso), showscale=False, hoverinfo='skip',
            colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],
            marker=dict(line=dict(color=INK, width=2)),
        ))
    style_fig(fig, 460)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), geo=dict(
        bgcolor='rgba(0,0,0,0)', showframe=False, showcoastlines=False, showocean=False,
        showland=True, landcolor=NO_DATA, showcountries=True, countrycolor=PAGE_BG,
        projection_type='natural earth', lataxis_range=[-58, 85],
    ))
    show_chart(fig)

    top_c = ranked.nlargest(15, 'median_views')
    if country_sel is not None and country_sel not in top_c['country_name'].values:
        top_c = pd.concat([top_c, geo[geo['country_name'] == country_sel]])
    chart_heading("Top 15 countries by median views per trending video",
                  f"Countries with at least {MIN_GROUP} trending entries"
                  + (f"; {country_sel} highlighted" if country_sel else ""))
    show_chart(hbar(top_c, 'country_name', 'median_views', highlight=country_sel, color=CORAL,
                    value_title='Median views', hover_extra=[('videos', 'Trending entries')], height=440))
    table_view(geo.drop(columns='iso3').sort_values('median_views', ascending=False),
               {'country_name': st.column_config.TextColumn('Country'), **COMMON_COLUMNS})

with tab_content:
    langs = group_stats(by_country, 'language_name')
    lang_cmap = language_colors(langs)
    where = f" in {country_sel}" if country_sel else ""
    if lang_sel is None:
        legend([(name, color) for name, color in lang_cmap.items() if name in set(langs['language_name'])]
               + [('Other languages', OTHER_GREY)])
    else:
        legend([(lang_sel, lang_cmap.get(lang_sel, CORAL)), ('Other languages', DIMMED)])
    col1, col2 = st.columns(2, gap='large')

    with col1:
        top_l = langs.nlargest(12, 'total_views')
        if lang_sel is not None and lang_sel not in top_l['language_name'].values:
            top_l = pd.concat([top_l, langs[langs['language_name'] == lang_sel]])
        top_l = top_l.assign(share=lambda d: (d['total_views'] / langs['total_views'].sum() * 100).round(1).astype(str) + '%')
        chart_heading("Top languages by total views",
                      f"Share of all views{where}" + (f"; {lang_sel} highlighted" if lang_sel else ""))
        show_chart(hbar(top_l, 'language_name', 'total_views', highlight=lang_sel, color_map=lang_cmap,
                        value_title='Total views',
                        hover_extra=[('share', 'Share of views'), ('videos', 'Trending entries')], height=440))

    with col2:
        sc = langs[langs['videos'] >= SCATTER_MIN]
        chart_heading("Engagement vs typical views, by language",
                      f"Languages with at least {SCATTER_MIN} trending entries{where}; the largest are labelled")
        if sc.empty:
            st.info("Not enough videos per language for this selection.")
        else:
            labelled = set(sc.nlargest(5, 'videos')['language_name']) | (set(lang_cmap) & set(sc['language_name']))
            if lang_sel:
                labelled.add(lang_sel)
            # Place each label away from its nearest labelled neighbour (log-x distance),
            # and keep labels near the right edge inside the plot
            pts = (sc[sc['language_name'].isin(labelled)]
                   .assign(lx=lambda d: np.log10(d['median_views'])).sort_values('lx'))
            names, xs = list(pts['language_name']), list(pts['lx'])
            x_max = np.log10(sc['median_views']).max()
            positions = {}
            for i, name in enumerate(names):
                left_gap = xs[i] - xs[i - 1] if i > 0 else np.inf
                right_gap = xs[i + 1] - xs[i] if i < len(names) - 1 else np.inf
                if xs[i] >= x_max - 0.25:
                    positions[name] = 'top left'
                elif min(left_gap, right_gap) > 0.35:
                    positions[name] = 'top center'
                else:
                    positions[name] = 'top left' if right_gap < left_gap else 'top right'
            if lang_sel is None:
                colors = [lang_cmap.get(l, OTHER_GREY) for l in sc['language_name']]
            else:
                colors = [lang_cmap.get(l, CORAL) if l == lang_sel else DIMMED for l in sc['language_name']]
            sizes = [13 if (l in lang_cmap or l == lang_sel) else 9 for l in sc['language_name']]
            fig = go.Figure(go.Scatter(
                x=sc['median_views'], y=sc['engagement'], mode='markers+text',
                text=[l if l in labelled else '' for l in sc['language_name']],
                textposition=[positions.get(l, 'top center') for l in sc['language_name']],
                textfont=dict(color=INK_2, size=11),
                marker=dict(size=sizes, color=colors, line=dict(color=PAGE_BG, width=2)),
                customdata=np.stack([sc['language_name'].astype(str), sc['median_views'].map(fmt_num),
                                     sc['videos']], axis=-1),
                hovertemplate='<b>%{customdata[0]}</b><br>Median views: %{customdata[1]}'
                              '<br>Median engagement: %{y:.2f}%<br>Trending entries: %{customdata[2]}<extra></extra>',
            ))
            style_fig(fig, 440)
            fig.update_xaxes(type='log', title_text='Median views per video (log scale)',
                             tickvals=[1e4, 1e5, 1e6, 1e7, 1e8], ticktext=['10K', '100K', '1M', '10M', '100M'])
            fig.update_yaxes(title_text='Median engagement (%)', ticksuffix='%')
            show_chart(fig)

    table_view(langs.sort_values('total_views', ascending=False),
               {'language_name': st.column_config.TextColumn('Language'), **COMMON_COLUMNS})

with tab_top:
    col1, col2 = st.columns([4, 7], gap='large')
    with col1:
        ch = group_stats(fdf, 'channel_name', MIN_CHANNEL_VIDEOS).nlargest(15, 'total_views')
        chart_heading("Top 15 channels by total views",
                      f"Channels with at least {MIN_CHANNEL_VIDEOS} trending entries in this selection")
        if ch.empty:
            st.info("No channel has enough trending entries in this selection.")
        else:
            show_chart(hbar(ch, 'channel_name', 'total_views', value_title='Total views',
                            hover_extra=[('videos', 'Trending entries')], height=500))
    with col2:
        chart_heading("Most-viewed trending videos",
                      "Each video once, with the number of countries it trended in within this sample")
        vids = (fdf.groupby(['title', 'channel_name'], observed=True)
                .agg(views=('view_count', 'max'), engagement=('engagement_rate', 'median'),
                     countries=('country', 'nunique'))
                .reset_index().nlargest(25, 'views'))
        st.dataframe(
            vids, hide_index=True, width='stretch', height=500,
            column_config={
                'title': st.column_config.TextColumn('Video', width='medium'),
                'channel_name': st.column_config.TextColumn('Channel', width='small'),
                'views': st.column_config.NumberColumn('Views', format='compact'),
                'engagement': st.column_config.NumberColumn('Engagement', format='%.2f%%'),
                'countries': st.column_config.NumberColumn('Countries', format='%d'),
            })

    # Trending activity over time
    st.write("")
    t = fdf.dropna(subset=['publish_date']).copy()
    t['month'] = t['publish_date'].dt.tz_localize(None).dt.to_period('M').dt.to_timestamp()
    monthly = t.groupby('month').agg(videos=('view_count', 'size'),
                                     median_views=('view_count', 'median')).reset_index()
    # The first and last months are only partly covered by the data; drop them when thin
    if len(monthly) > 3:
        thin = monthly['videos'] < 0.75 * monthly['videos'].median()
        edge = monthly.index.isin([monthly.index[0], monthly.index[-1]])
        monthly = monthly[~(edge & thin)]
    if len(monthly) < 2:
        st.info("Not enough dated videos in this selection to show trending activity over time.")
    else:
        col1, col2 = st.columns(2, gap='large')
        # A count over time reads as an area; a median does not, so it stays a line
        for col, field, title, sub, fmt, fill in (
            (col1, 'videos', "Trending activity over time",
             "Trending entries by publish month (partial edge months omitted)", '%{y:,}', 'tozeroy'),
            (col2, 'median_views', "Median views by publish month",
             "Recent months are lower partly because those videos had less time to gather views",
             '%{customdata}', None),
        ):
            with col:
                chart_heading(title, sub)
                fig = go.Figure(go.Scatter(
                    x=monthly['month'], y=monthly[field], mode='lines',
                    line=dict(color=ACCENT, width=2), fill=fill, fillcolor='rgba(57,135,229,0.10)',
                    customdata=monthly[field].map(fmt_num),
                    hovertemplate=f'%{{x|%b %Y}}<br><b>{fmt}</b><extra></extra>',
                ))
                style_fig(fig, 320)
                fig.update_layout(hovermode='x')
                fig.update_xaxes(showgrid=False, showspikes=True, spikecolor=AXIS, spikethickness=1,
                                 spikedash='solid', spikemode='across')
                fig.update_yaxes(rangemode='tozero')
                show_chart(fig)
        table_view(monthly.assign(month=monthly['month'].dt.strftime('%Y-%m')),
                   {'month': st.column_config.TextColumn('Publish month'),
                    'videos': COMMON_COLUMNS['videos'], 'median_views': COMMON_COLUMNS['median_views']})

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <b>Big Data Analytics Project</b> · Apache Spark, Spark MLlib &amp; Streamlit ·
    Developed by <b>Hemanth Raj</b> ·
    <a href="https://github.com/Hemanthraj09" target="_blank">GitHub</a> ·
    <a href="https://www.linkedin.com/in/hemanthrajmv" target="_blank">LinkedIn</a>
</div>""", unsafe_allow_html=True)
