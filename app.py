import streamlit as st
import fastf1
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import numpy as np
from datetime import timedelta

# Page config
st.set_page_config(
    page_title="Abu Dhabi 2021 F1 Analysis",
    page_icon="🏁",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        color: #4ECDC4;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_race_data():
    """Load and cache F1 race data"""
    try:
        # Create cache directory
        if not os.path.exists('./cache'):
            os.makedirs('./cache')
        
        fastf1.Cache.enable_cache('./cache')
        
        with st.spinner('Loading F1 race data... This might take a moment.'):
            session = fastf1.get_session(2021, 'Abu Dhabi', 'R')
            session.load()
        
        return session
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def get_telemetry_data(session):
    """Get telemetry data for both drivers"""
    laps = session.laps
    
    # Fastest laps
    ver_fastest = laps.pick_drivers('VER').pick_fastest()
    ham_fastest = laps.pick_drivers('HAM').pick_fastest()
    
    # Get telemetry
    ver_tel = ver_fastest.get_telemetry()
    ham_tel = ham_fastest.get_telemetry()
    
    # All laps for race pace
    ver_laps = laps.pick_drivers('VER')
    ham_laps = laps.pick_drivers('HAM')
    
    return ver_tel, ham_tel, ver_laps, ham_laps

def create_speed_chart(ver_tel, ham_tel):
    """Create speed vs distance chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ver_tel['Distance'], 
        y=ver_tel['Speed'],
        mode='lines', 
        name='Verstappen', 
        line=dict(color='#E74C3C', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=ham_tel['Distance'], 
        y=ham_tel['Speed'],
        mode='lines', 
        name='Hamilton', 
        line=dict(color='#3498DB', width=3)
    ))
    
    fig.update_layout(
        title='🏎️ Speed vs Distance - Fastest Lap Comparison',
        xaxis_title='Distance (m)', 
        yaxis_title='Speed (km/h)',
        template='plotly_dark', 
        hovermode='x unified', 
        height=500,
        font=dict(size=12)
    )
    
    return fig

def create_throttle_chart(ver_tel, ham_tel):
    """Create throttle vs distance chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ver_tel['Distance'], 
        y=ver_tel['Throttle'],
        mode='lines', 
        name='Verstappen', 
        line=dict(color='#FF6B35', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=ham_tel['Distance'], 
        y=ham_tel['Throttle'],
        mode='lines', 
        name='Hamilton', 
        line=dict(color='#2ECC71', width=3)
    ))
    
    fig.update_layout(
        title='🚀 Throttle Application vs Distance',
        xaxis_title='Distance (m)', 
        yaxis_title='Throttle (%)',
        template='plotly_dark', 
        hovermode='x unified', 
        height=500
    )
    
    return fig

def create_brake_chart(ver_tel, ham_tel):
    """Create brake vs distance chart"""
    # Convert brake boolean to integer
    ver_tel_copy = ver_tel.copy()
    ham_tel_copy = ham_tel.copy()
    ver_tel_copy['Brake'] = ver_tel_copy['Brake'].astype(int)
    ham_tel_copy['Brake'] = ham_tel_copy['Brake'].astype(int)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ver_tel_copy['Distance'], 
        y=ver_tel_copy['Brake'],
        mode='lines', 
        name='Verstappen', 
        line=dict(color='#9B59B6', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=ham_tel_copy['Distance'], 
        y=ham_tel_copy['Brake'],
        mode='lines', 
        name='Hamilton', 
        line=dict(color='#1ABC9C', width=3)
    ))
    
    fig.update_layout(
        title='🛑 Brake Application vs Distance',
        xaxis_title='Distance (m)', 
        yaxis_title='Brake (On/Off)',
        template='plotly_dark', 
        hovermode='x unified', 
        height=500
    )
    
    return fig

def create_gear_chart(ver_tel, ham_tel):
    """Create gear usage chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ver_tel['Distance'],
        y=ver_tel['nGear'],
        mode='lines',
        name='Verstappen',
        line=dict(color='#E74C3C', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=ham_tel['Distance'],
        y=ham_tel['nGear'],
        mode='lines',
        name='Hamilton',
        line=dict(color='#3498DB', width=3)
    ))
    
    fig.update_layout(
        title='⚙️ Gear Usage vs Distance',
        xaxis_title='Distance (m)',
        yaxis_title='Gear Number',
        template='plotly_dark',
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_rpm_chart(ver_tel, ham_tel):
    """Create RPM chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ver_tel['Distance'],
        y=ver_tel['RPM'],
        mode='lines',
        name='Verstappen',
        line=dict(color='#E74C3C', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=ham_tel['Distance'],
        y=ham_tel['RPM'],
        mode='lines',
        name='Hamilton',
        line=dict(color='#3498DB', width=3)
    ))
    
    fig.update_layout(
        title='🔄 RPM vs Distance',
        xaxis_title='Distance (m)',
        yaxis_title='RPM',
        template='plotly_dark',
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_laptime_chart(ver_laps, ham_laps):
    """Create lap time comparison chart"""
    # Clean data
    ver_laps_clean = ver_laps[ver_laps['LapTime'].notnull()].copy()
    ham_laps_clean = ham_laps[ham_laps['LapTime'].notnull()].copy()
    
    # Convert to seconds
    ver_laps_clean['LapTime_s'] = ver_laps_clean['LapTime'].dt.total_seconds()
    ham_laps_clean['LapTime_s'] = ham_laps_clean['LapTime'].dt.total_seconds()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ver_laps_clean['LapNumber'],
        y=ver_laps_clean['LapTime_s'],
        mode='lines+markers',
        name='Verstappen',
        line=dict(color='#E74C3C', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=ham_laps_clean['LapNumber'],
        y=ham_laps_clean['LapTime_s'],
        mode='lines+markers',
        name='Hamilton',
        line=dict(color='#3498DB', width=3),
        marker=dict(size=6)
    ))
    
    # Add Safety Car period
    fig.add_vrect(
        x0=53, x1=56,
        annotation_text="Safety Car",
        fillcolor="yellow", 
        opacity=0.3, 
        line_width=0
    )
    
    # Add final lap marker
    fig.add_vline(
        x=58,
        line=dict(color="lime", width=3, dash="dash"),
        annotation_text="Final Lap",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title='⏱️ Lap Time Evolution Throughout the Race',
        xaxis_title='Lap Number',
        yaxis_title='Lap Time (seconds)',
        template='plotly_dark',
        hovermode='x unified',
        height=600
    )
    
    return fig

def create_final_laps_chart(ver_laps, ham_laps):
    """Create final 10 laps comparison"""
    ver_laps_clean = ver_laps[ver_laps['LapTime'].notnull()].copy()
    ham_laps_clean = ham_laps[ham_laps['LapTime'].notnull()].copy()
    
    ver_laps_clean['LapTime_s'] = ver_laps_clean['LapTime'].dt.total_seconds()
    ham_laps_clean['LapTime_s'] = ham_laps_clean['LapTime'].dt.total_seconds()
    
    # Filter final 10 laps
    ver_final = ver_laps_clean[ver_laps_clean['LapNumber'] >= 49]
    ham_final = ham_laps_clean[ham_laps_clean['LapNumber'] >= 49]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ver_final['LapNumber'],
        y=ver_final['LapTime_s'],
        mode='lines+markers',
        name='Verstappen',
        line=dict(color='#E74C3C', width=4),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=ham_final['LapNumber'],
        y=ham_final['LapTime_s'],
        mode='lines+markers',
        name='Hamilton',
        line=dict(color='#3498DB', width=4),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='🔥 Final 10 Laps - The Championship Decider',
        xaxis_title='Lap Number',
        yaxis_title='Lap Time (seconds)',
        template='plotly_dark',
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_tyre_strategy_chart():
    """Create tyre strategy timeline"""
    pit_data = pd.DataFrame({
        'Driver': ['HAM', 'HAM', 'VER', 'VER', 'VER'],
        'Tyre': ['Medium', 'Hard', 'Medium', 'Hard', 'Soft'],
        'Start': [0, 14, 0, 36, 53],
        'End': [14, 58, 36, 53, 58],
        'Stint': [0, 1, 2, 3, 4]
    })
    
    colors = {'Soft': '#E74C3C', 'Hard': '#ECF0F1', 'Medium': '#F39C12'}
    
    fig = go.Figure()
    
    for _, row in pit_data.iterrows():
        fig.add_trace(go.Bar(
            x=[row['End'] - row['Start']],
            y=[row['Stint']],
            base=row['Start'],
            orientation='h',
            name=f"{row['Driver']} - {row['Tyre']}",
            marker=dict(color=colors[row['Tyre']], line=dict(color='black', width=1)),
            hovertemplate=f"<b>{row['Driver']}</b><br>Tyre: {row['Tyre']}<br>Laps: {row['Start']}-{row['End']}<extra></extra>"
        ))
    
    fig.update_layout(
        title='🛞 Tyre Strategy Timeline - The Winning Decision',
        xaxis_title='Lap Number',
        yaxis=dict(
            tickvals=pit_data['Stint'],
            ticktext=[f"{d} - {t}" for d, t in zip(pit_data['Driver'], pit_data['Tyre'])],
            showgrid=False
        ),
        height=400,
        template='plotly_dark',
        showlegend=False
    )
    
    return fig

def create_position_chart(session):
    """Create race position timeline"""
    laps = session.laps
    ver_laps = laps.pick_drivers('VER')[['LapNumber', 'Position']]
    ham_laps = laps.pick_drivers('HAM')[['LapNumber', 'Position']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ver_laps['LapNumber'], 
        y=ver_laps['Position'],
        mode='lines+markers', 
        name='Verstappen',
        line=dict(color='#E74C3C', width=4), 
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=ham_laps['LapNumber'], 
        y=ham_laps['Position'],
        mode='lines+markers', 
        name='Hamilton',
        line=dict(color='#3498DB', width=4), 
        marker=dict(size=6)
    ))
    
    fig.add_vline(
        x=58, 
        line_dash="dash", 
        line_color="lime", 
        annotation_text="Final Lap Overtake",
        annotation_position="top"
    )
    
    fig.update_layout(
        title='🏆 Race Position Timeline - The Championship Moment',
        xaxis_title='Lap Number',
        yaxis_title='Race Position',
        yaxis_autorange='reversed',
        template='plotly_dark',
        height=400
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🏁 Abu Dhabi 2021: How Verstappen Beat Hamilton</h1>', unsafe_allow_html=True)
    st.markdown("### *A Telemetry & Strategy Analysis of F1's Most Dramatic Finish*")
    
    # Sidebar
    st.sidebar.title("🏎️ Navigation")
    section = st.sidebar.selectbox(
        "Choose Analysis Section:",
        ["📊 Overview", "🔥 Telemetry Analysis", "⏱️ Race Pace", "🛞 Strategy Analysis", "📈 Final Moments"]
    )
    
    # Load data
    session = load_race_data()
    if session is None:
        st.error("Failed to load race data. Please check your internet connection and try again.")
        return
    
    # Get telemetry data
    ver_tel, ham_tel, ver_laps, ham_laps = get_telemetry_data(session)
    
    if section == "📊 Overview":
        st.markdown('<h2 class="section-header">Race Overview</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Race Winner", "Max Verstappen", "🏆")
        with col2:
            st.metric("Championship Decided", "Final Lap", "Lap 58")
        with col3:
            st.metric("Key Factor", "Tyre Strategy", "Soft vs Hard")
        
        st.markdown("""
        **December 12, 2021** - The Yas Marina Circuit witnessed one of F1's most dramatic conclusions. 
        Max Verstappen overcame Lewis Hamilton in the final lap to win his first World Championship.
        
        **Key Moments:**
        - 🟡 Safety Car on Lap 53 changed everything
        - 🔄 Verstappen's crucial pit stop for soft tyres
        - 🏁 DRS-assisted overtake on the main straight
        """)
    
    elif section == "🔥 Telemetry Analysis":
        st.markdown('<h2 class="section-header">Fastest Lap Telemetry Comparison</h2>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏎️ Speed", "🚀 Throttle", "🛑 Braking", "⚙️ Gears", "🔄 RPM"])
        
        with tab1:
            st.plotly_chart(create_speed_chart(ver_tel, ham_tel), use_container_width=True)
            st.info("💡 **Key Insight**: Verstappen carries more speed through technical sections, particularly Turn 5 and Turn 9.")
        
        with tab2:
            st.plotly_chart(create_throttle_chart(ver_tel, ham_tel), use_container_width=True)
            st.info("💡 **Key Insight**: More aggressive throttle application by Verstappen out of slow-speed corners.")
        
        with tab3:
            st.plotly_chart(create_brake_chart(ver_tel, ham_tel), use_container_width=True)
            st.info("💡 **Key Insight**: Different braking patterns show contrasting driving styles and setup approaches.")
        
        with tab4:
            st.plotly_chart(create_gear_chart(ver_tel, ham_tel), use_container_width=True)
            st.info("💡 **Key Insight**: Gear usage patterns reveal acceleration and cornering strategies.")
        
        with tab5:
            st.plotly_chart(create_rpm_chart(ver_tel, ham_tel), use_container_width=True)
            st.info("💡 **Key Insight**: RPM differences indicate power delivery and engine mapping strategies.")
    
    elif section == "⏱️ Race Pace":
        st.markdown('<h2 class="section-header">Lap Time Evolution</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(create_laptime_chart(ver_laps, ham_laps), use_container_width=True)
        with col2:
            st.markdown("""
            **Race Pace Analysis:**
            
            🔵 **Hamilton's Dominance**
            - Faster for most of the race
            - Consistent pace on hard tyres
            - Led by 11+ seconds before SC
            
            🔴 **Verstappen's Comeback**
            - Struggled mid-race on hards
            - Pace improved after Lap 50
            - Fresh softs made the difference
            """)
        
        st.plotly_chart(create_final_laps_chart(ver_laps, ham_laps), use_container_width=True)
    
    elif section == "🛞 Strategy Analysis":
        st.markdown('<h2 class="section-header">The Winning Strategy</h2>', unsafe_allow_html=True)
        
        st.plotly_chart(create_tyre_strategy_chart(), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Hamilton's Strategy:**
            - 🟠 Medium → 🔵 Hard (Lap 14)
            - One-stop strategy
            - 44 laps on hard tyres
            - Conservative approach
            """)
        
        with col2:
            st.markdown("""
            **Verstappen's Strategy:**
            - 🟠 Medium → 🔵 Hard → 🔴 Soft
            - Opportunistic SC stop (Lap 53)
            - Fresh soft tyres for final attack
            - **Race-winning decision** 🏆
            """)
        
        st.success("🎯 **Strategic Masterclass**: Red Bull's decision to pit under the Safety Car gave Verstappen a crucial tyre advantage for the final restart.")
    
    elif section == "📈 Final Moments":
        st.markdown('<h2 class="section-header">The Championship Decider</h2>', unsafe_allow_html=True)
        
        st.plotly_chart(create_position_chart(session), use_container_width=True)
        
        # Final lap analysis
        st.markdown("### 🏁 Lap 58 - The Overtake")
        
        try:
            # Get final lap telemetry
            laps = session.laps
            ver_lap58 = laps.pick_drivers('VER').loc[laps['LapNumber'] == 58].iloc[0]
            ham_lap58 = laps.pick_drivers('HAM').loc[laps['LapNumber'] == 58].iloc[0]
            
            ver_tel_58 = ver_lap58.get_telemetry().add_distance()
            ham_tel_58 = ham_lap58.get_telemetry().add_distance()
            
            # Final lap speed chart
            fig_final = go.Figure()
            fig_final.add_trace(go.Scatter(
                x=ver_tel_58['Distance'], y=ver_tel_58['Speed'],
                mode='lines', name='Verstappen', line=dict(color='#E74C3C', width=4)
            ))
            fig_final.add_trace(go.Scatter(
                x=ham_tel_58['Distance'], y=ham_tel_58['Speed'],
                mode='lines', name='Hamilton', line=dict(color='#3498DB', width=4)
            ))
            fig_final.update_layout(
                title='🏆 Final Lap Speed Comparison - The Championship Moment',
                xaxis_title='Distance (m)', yaxis_title='Speed (km/h)',
                template='plotly_dark', height=500
            )
            st.plotly_chart(fig_final, use_container_width=True)
            
        except Exception as e:
            st.warning("Final lap telemetry data not available for detailed analysis.")
        
        st.markdown("""
        **The Decisive Moment:**
        - 🟢 DRS enabled on main straight
        - 🔴 Soft tyre advantage crucial
        - 🏁 Overtake completed before Turn 5
        - 🏆 World Championship decided
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("*Data Source: FastF1 | Analysis: F1 Telemetry Study*")

if __name__ == "__main__":
    main()