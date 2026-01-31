"""
SIMPLE ONE-FILE VERSION
India Derivatives Sales Dashboard - Complete in one file for easy Replit setup

SETUP INSTRUCTIONS:
1. Create new Python Repl on replit.com
2. Delete the default main.py file
3. Create a file called: app_simple.py
4. Copy-paste this ENTIRE file into it
5. In Shell, run: pip install streamlit pandas
6. In .replit file, change run command to: streamlit run app_simple.py --server.port 5000 --server.address 0.0.0.0
7. Click Run!
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO

# ==================== SAMPLE DATA ====================
# This is embedded so you don't need a separate CSV file

SAMPLE_DATA = """trade_id,trade_date,client_name,country,product,volume_usd,fees_usd,margin_utilization
T001,2026-01-31,Reliance Capital,India,Perpetual,2500000,2500,0.45
T002,2026-01-31,Tata Securities,India,Futures,1800000,1800,0.52
T003,2026-01-31,HDFC Trading,India,Options,950000,1425,0.38
T004,2026-01-30,Reliance Capital,India,Perpetual,2200000,2200,0.48
T005,2026-01-30,Bajaj Finance,India,Futures,1500000,1500,0.65
T006,2026-01-30,Kotak Institutional,India,Perpetual,3200000,3200,0.55
T007,2026-01-29,Tata Securities,India,Options,1100000,1650,0.51
T008,2026-01-29,Reliance Capital,India,Futures,1900000,1900,0.46
T009,2026-01-29,Aditya Birla Group,India,Perpetual,850000,850,0.72
T010,2026-01-28,HDFC Trading,India,Perpetual,1200000,1200,0.41
T011,2026-01-28,Kotak Institutional,India,Futures,2800000,2800,0.58
T012,2026-01-28,Reliance Capital,India,Options,750000,1125,0.44
T013,2026-01-27,Tata Securities,India,Perpetual,1600000,1600,0.49
T014,2026-01-27,Bajaj Finance,India,Options,680000,1020,0.68
T015,2026-01-27,Mahindra Trading,India,Futures,920000,920,0.33
T016,2026-01-26,Reliance Capital,India,Perpetual,2400000,2400,0.47
T017,2026-01-26,Kotak Institutional,India,Perpetual,3100000,3100,0.56
T018,2026-01-25,HDFC Trading,India,Futures,1100000,1100,0.39
T019,2026-01-25,Aditya Birla Group,India,Perpetual,780000,780,0.75
T020,2026-01-24,Tata Securities,India,Perpetual,1700000,1700,0.50
T021,2026-01-24,Reliance Capital,India,Futures,2100000,2100,0.45
T022,2026-01-24,Bajaj Finance,India,Perpetual,1400000,1400,0.66
T023,2026-01-23,Kotak Institutional,India,Options,1250000,1875,0.57
T024,2026-01-23,Mahindra Trading,India,Perpetual,880000,880,0.35
T025,2026-01-23,HDFC Trading,India,Perpetual,1050000,1050,0.40
T026,2026-01-22,Reliance Capital,India,Perpetual,2300000,2300,0.46
T027,2026-01-22,Tata Securities,India,Futures,1650000,1650,0.48
T028,2026-01-21,Aditya Birla Group,India,Perpetual,820000,820,0.73
T029,2026-01-21,Kotak Institutional,India,Perpetual,3000000,3000,0.54
T030,2026-01-20,Bajaj Finance,India,Options,720000,1080,0.67
T031,2026-01-20,HDFC Trading,India,Futures,1150000,1150,0.38
T032,2026-01-19,Reliance Capital,India,Perpetual,2250000,2250,0.44
T033,2026-01-19,Tata Securities,India,Perpetual,1750000,1750,0.51
T034,2026-01-18,Kotak Institutional,India,Futures,2900000,2900,0.55
T035,2026-01-18,Mahindra Trading,India,Perpetual,910000,910,0.34
T036,2026-01-17,Reliance Capital,India,Options,680000,1020,0.43
T037,2026-01-17,Aditya Birla Group,India,Perpetual,800000,800,0.74
T038,2026-01-16,HDFC Trading,India,Perpetual,1080000,1080,0.37
T039,2026-01-16,Tata Securities,India,Futures,1680000,1680,0.49
T040,2026-01-15,Bajaj Finance,India,Perpetual,1350000,1350,0.64
T041,2026-01-15,Kotak Institutional,India,Perpetual,3150000,3150,0.53
T042,2026-01-14,Reliance Capital,India,Futures,2050000,2050,0.45
T043,2026-01-14,Mahindra Trading,India,Options,560000,840,0.36
T044,2026-01-13,Tata Securities,India,Perpetual,1720000,1720,0.50
T045,2026-01-13,HDFC Trading,India,Futures,1120000,1120,0.39
T046,2026-01-12,Reliance Capital,India,Perpetual,2350000,2350,0.46
T047,2026-01-12,Kotak Institutional,India,Options,1180000,1770,0.56
T048,2026-01-11,Aditya Birla Group,India,Perpetual,790000,790,0.71
T049,2026-01-11,Bajaj Finance,India,Futures,1420000,1420,0.65
T050,2026-01-10,Tata Securities,India,Perpetual,1680000,1680,0.52
T051,2026-01-10,HDFC Trading,India,Perpetual,1090000,1090,0.40
T052,2026-01-09,Reliance Capital,India,Futures,2180000,2180,0.47
T053,2026-01-09,Kotak Institutional,India,Perpetual,3050000,3050,0.54
T054,2026-01-08,Mahindra Trading,India,Perpetual,895000,895,0.35
T055,2026-01-08,Aditya Birla Group,India,Options,520000,780,0.76
T056,2026-01-07,Reliance Capital,India,Perpetual,2280000,2280,0.44
T057,2026-01-07,Tata Securities,India,Futures,1710000,1710,0.53
T058,2026-01-06,Bajaj Finance,India,Perpetual,1380000,1380,0.63
T059,2026-01-06,HDFC Trading,India,Options,780000,1170,0.41
T060,2026-01-05,Kotak Institutional,India,Futures,2950000,2950,0.57
T061,2026-01-05,Reliance Capital,India,Perpetual,2320000,2320,0.48
T062,2026-01-04,Tata Securities,India,Perpetual,1690000,1690,0.50
T063,2026-01-04,Mahindra Trading,India,Futures,870000,870,0.32
T064,2026-01-03,Aditya Birla Group,India,Perpetual,810000,810,0.70
T065,2026-01-03,HDFC Trading,India,Perpetual,1060000,1060,0.38
T066,2026-01-02,Reliance Capital,India,Options,710000,1065,0.45
T067,2026-01-02,Kotak Institutional,India,Perpetual,3180000,3180,0.55
T068,2026-01-01,Bajaj Finance,India,Futures,1410000,1410,0.66
T069,2026-01-01,Tata Securities,India,Perpetual,1730000,1730,0.51
T070,2025-12-31,Reliance Capital,India,Perpetual,2100000,2100,0.42
T071,2025-12-30,HDFC Trading,India,Futures,980000,980,0.36
T072,2025-12-29,Kotak Institutional,India,Perpetual,2850000,2850,0.52"""

# ==================== HELPER FUNCTIONS ====================

@st.cache_data
def load_data():
    """Load sample data from embedded CSV string."""
    df = pd.read_csv(StringIO(SAMPLE_DATA))
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    return df

def format_currency(value):
    """Format large currency values with M/B suffixes."""
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.1f}K"
    else:
        return f"${value:,.0f}"

def get_client_performance_table(df):
    """Generate client performance metrics."""
    if len(df) == 0:
        return pd.DataFrame()
    
    max_date = df['trade_date'].max()
    cutoff_7d = max_date - timedelta(days=7)
    cutoff_prev_7d = cutoff_7d - timedelta(days=7)
    
    # 7D volume
    df_7d = df[df['trade_date'] > cutoff_7d].groupby('client_name').agg({'volume_usd': 'sum'}).reset_index()
    df_7d.columns = ['client_name', '7D Volume']
    
    # Previous 7D volume
    df_prev_7d = df[(df['trade_date'] > cutoff_prev_7d) & (df['trade_date'] <= cutoff_7d)].groupby('client_name').agg({'volume_usd': 'sum'}).reset_index()
    df_prev_7d.columns = ['client_name', 'Prev 7D Volume']
    
    # MTD volume
    df_mtd = df.groupby('client_name').agg({'volume_usd': 'sum'}).reset_index()
    df_mtd.columns = ['client_name', 'MTD Volume']
    
    # Merge
    result = df_mtd.merge(df_7d, on='client_name', how='left')
    result = result.merge(df_prev_7d, on='client_name', how='left')
    result = result.fillna(0)
    
    # WoW change
    result['WoW % Change'] = result.apply(
        lambda x: ((x['7D Volume'] - x['Prev 7D Volume']) / x['Prev 7D Volume'] * 100) if x['Prev 7D Volume'] > 0 else 0,
        axis=1
    )
    
    # Status
    def get_status(row):
        if row['7D Volume'] == 0:
            return "Inactive"
        elif row['WoW % Change'] > 20:
            return "Growing"
        elif row['WoW % Change'] < -20:
            return "Declining"
        else:
            return "Stable"
    
    result['Status'] = result.apply(get_status, axis=1)
    
    # Last trade date
    last_trades = df.groupby('client_name')['trade_date'].max().reset_index()
    last_trades.columns = ['client_name', 'Last Trade']
    result = result.merge(last_trades, on='client_name', how='left')
    
    result = result.rename(columns={'client_name': 'Client'})
    result = result[['Client', '7D Volume', 'MTD Volume', 'Prev 7D Volume', 'WoW % Change', 'Status', 'Last Trade']]
    
    return result.sort_values('MTD Volume', ascending=False)

def get_risk_signals(df):
    """Identify clients with elevated risk."""
    if len(df) == 0:
        return pd.DataFrame()
    
    # Latest margin per client
    latest_margins = df.sort_values('trade_date').groupby('client_name').tail(1)[['client_name', 'margin_utilization']]
    
    # Performance metrics
    perf_df = get_client_performance_table(df)
    
    # Merge
    risk_df = latest_margins.merge(perf_df[['Client', 'WoW % Change']], left_on='client_name', right_on='Client', how='inner')
    
    # Risk level
    def get_risk_level(row):
        margin = row['margin_utilization']
        wow_change = row['WoW % Change']
        if margin > 0.7:
            return "High"
        elif margin > 0.6 and wow_change < -10:
            return "Medium"
        return None
    
    risk_df['Risk Level'] = risk_df.apply(get_risk_level, axis=1)
    risk_df = risk_df[risk_df['Risk Level'].notna()]
    
    if len(risk_df) == 0:
        return pd.DataFrame()
    
    # Reason
    def get_reason(row):
        margin = row['margin_utilization']
        wow_change = row['WoW % Change']
        if margin > 0.7 and wow_change < -10:
            return "High margin + declining volume"
        elif margin > 0.7:
            return "High margin utilization"
        return "Elevated margin + volume decline"
    
    risk_df['Reason'] = risk_df.apply(get_reason, axis=1)
    risk_df = risk_df.drop(columns=['client_name'])
    risk_df = risk_df.rename(columns={'margin_utilization': 'Margin Utilization', 'WoW % Change': 'WoW Volume Change'})
    risk_df = risk_df[['Client', 'Margin Utilization', 'WoW Volume Change', 'Risk Level', 'Reason']]
    
    return risk_df.sort_values('Margin Utilization', ascending=False)

def get_sales_action_list(df, n=10):
    """Generate prioritized outreach list."""
    if len(df) == 0:
        return pd.DataFrame()
    
    max_date = df['trade_date'].max()
    perf_df = get_client_performance_table(df)
    risk_df = get_risk_signals(df)
    risky_clients = set(risk_df['Client'].unique()) if len(risk_df) > 0 else set()
    
    perf_df['Days Since Last Trade'] = (max_date - perf_df['Last Trade']).dt.days
    
    def get_priority_and_reason(row):
        days_inactive = row['Days Since Last Trade']
        wow_change = row['WoW % Change']
        client = row['Client']
        
        if client in risky_clients:
            return ("High", "High risk - margin check needed")
        elif wow_change < -30:
            return ("High", f"Volume dropped {abs(wow_change):.0f}% - urgent call")
        elif days_inactive >= 5 and row['7D Volume'] == 0:
            return ("High", f"Inactive for {days_inactive} days")
        elif wow_change < -20:
            return ("Medium", f"Volume down {abs(wow_change):.0f}% WoW")
        elif days_inactive >= 3 and row['7D Volume'] == 0:
            return ("Medium", f"No trades for {days_inactive} days")
        return (None, None)
    
    perf_df[['Priority', 'Reason']] = perf_df.apply(lambda row: pd.Series(get_priority_and_reason(row)), axis=1)
    action_df = perf_df[perf_df['Priority'].notna()].copy()
    
    if len(action_df) == 0:
        return pd.DataFrame()
    
    priority_order = {'High': 0, 'Medium': 1}
    action_df['priority_rank'] = action_df['Priority'].map(priority_order)
    action_df = action_df.sort_values(['priority_rank', 'MTD Volume'], ascending=[True, False])
    action_df = action_df[['Client', 'Priority', 'Reason', '7D Volume', 'Prev 7D Volume', 'Days Since Last Trade']]
    
    return action_df.head(n)

# ==================== STREAMLIT APP ====================

st.set_page_config(page_title="India Derivatives Sales Dashboard", page_icon="🇮🇳", layout="wide")

st.title("🇮🇳 India Derivatives Sales Dashboard")

# Load data
india_trades = load_data()

# Morning Check
st.markdown("---")
st.subheader("☀️ Morning Check")
st.caption("Key metrics I track every morning to gauge performance and client health.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_volume = india_trades['volume_usd'].sum()
    st.metric(label="MTD Volume (USD)", value=format_currency(total_volume))

with col2:
    total_fees = india_trades['fees_usd'].sum()
    st.metric(label="MTD Fees (USD)", value=format_currency(total_fees))

with col3:
    cutoff = india_trades['trade_date'].max() - timedelta(days=7)
    active_7d = india_trades[india_trades['trade_date'] > cutoff]['client_name'].nunique()
    st.metric(label="Active Clients (7D)", value=f"{active_7d}")

with col4:
    first_trades = india_trades.groupby('client_name')['trade_date'].min().reset_index()
    cutoff_30d = india_trades['trade_date'].max() - timedelta(days=30)
    new_clients = len(first_trades[first_trades['trade_date'] > cutoff_30d])
    st.metric(label="New Clients (MTD)", value=f"{new_clients}")

st.info("💡 **Quick insight:** If volume is up but active clients are down, that's a concentration risk.")

# Market Insights
st.markdown("---")
st.subheader("📊 Market & Client Insights")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("**Top 5 Clients by MTD Volume**")
    top_clients = india_trades.groupby('client_name').agg({'volume_usd': 'sum'}).reset_index()
    top_clients = top_clients.sort_values('volume_usd', ascending=False).head(5)
    st.bar_chart(top_clients.set_index('client_name')['volume_usd'], color="#1f77b4")

with col_chart2:
    st.markdown("**Product Mix (MTD Volume)**")
    product_data = india_trades.groupby('product').agg({'volume_usd': 'sum'}).reset_index()
    total = product_data['volume_usd'].sum()
    for _, row in product_data.iterrows():
        pct = (row['volume_usd'] / total * 100)
        st.metric(label=row['product'], value=format_currency(row['volume_usd']), delta=f"{pct:.1f}% of total")

st.markdown("**Daily Volume Trend (Last 30 Days)**")
date_data = india_trades.groupby('trade_date').agg({'volume_usd': 'sum'}).reset_index()
st.line_chart(date_data.set_index('trade_date')['volume_usd'], color="#2ecc71")

# Client Performance
st.markdown("---")
st.subheader("📈 Client Performance")
performance_df = get_client_performance_table(india_trades)

if len(performance_df) > 0:
    display_perf = performance_df.copy()
    display_perf['7D Volume'] = display_perf['7D Volume'].apply(format_currency)
    display_perf['MTD Volume'] = display_perf['MTD Volume'].apply(format_currency)
    display_perf['WoW % Change'] = display_perf['WoW % Change'].apply(lambda x: f"{x:+.1f}%")
    st.dataframe(display_perf, use_container_width=True, hide_index=True)

# Risk Signals
st.markdown("---")
st.subheader("⚠️ Risk Signals")
risk_df = get_risk_signals(india_trades)

if len(risk_df) > 0:
    display_risk = risk_df.copy()
    display_risk['Margin Utilization'] = display_risk['Margin Utilization'].apply(lambda x: f"{x:.1%}")
    display_risk['WoW Volume Change'] = display_risk['WoW Volume Change'].apply(lambda x: f"{x:+.1f}%")
    display_risk['Risk Level'] = display_risk['Risk Level'].apply(lambda x: f"🔴 {x}" if x == "High" else f"🟡 {x}")
    st.dataframe(display_risk, use_container_width=True, hide_index=True)
else:
    st.success("✅ No clients currently flagged for risk.")

# Sales Action List
st.markdown("---")
st.subheader("📞 Who I Should Call Today")
sales_df = get_sales_action_list(india_trades, 10)

if len(sales_df) > 0:
    display_sales = sales_df.copy()
    display_sales['7D Volume'] = display_sales['7D Volume'].apply(format_currency)
    display_sales['Prev 7D Volume'] = display_sales['Prev 7D Volume'].apply(format_currency)
    st.dataframe(display_sales, use_container_width=True, hide_index=True)
else:
    st.success("✅ All clients are healthy - no urgent outreach needed.")

st.markdown("---")
st.caption("🇮🇳 India Derivatives Sales Dashboard | Built with Streamlit")
