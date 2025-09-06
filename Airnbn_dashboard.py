import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="NYC Airbnb Analytics Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF5A5F;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #484848;
        margin: 1.5rem 0 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF5A5F;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess Airbnb data"""
    try:
        data = pd.read_csv("AB_NYC_2019.csv")  
        
        # Convert date column
        data['last_review'] = pd.to_datetime(data['last_review'], errors='coerce',dayfirst=True)
        
        # Clean location data
        data = data.dropna(subset=['latitude', 'longitude'])
        data = data[(data['latitude'] != 0) & (data['longitude'] != 0)]
        
        # Remove extreme outliers in price
        data = data[data['price'] <= data['price'].quantile(0.99)]
        data = data[data['price'] > 0]
        
        return data
    except FileNotFoundError:
        st.error("❌ Data file 'AB_NYC_2019.csv' not found. Please ensure the file is in the same directory.")
        return pd.DataFrame()

def haversine_array(lat1, lon1, lat2, lon2):
    """Calculate distance between points using Haversine formula"""
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def create_price_distance_plot(filtered_data):
    """Create enhanced price vs distance scatter plot using Plotly"""
    if len(filtered_data) == 0:
        return None
    
    # Sample data if too large for better performance
    sample_size = min(2000, len(filtered_data))
    plot_data = filtered_data.sample(sample_size) if len(filtered_data) > sample_size else filtered_data
    
    fig = px.scatter(
        plot_data,
        x='distance_km',
        y='price',
        color='room_type',
        size='number_of_reviews',
        hover_data={
            'neighbourhood_group': True,
            'neighbourhood': True,
            'availability_365': True,
            'distance_km': ':.1f',
            'price': '$:.0f'
        },
        title="💰 Price vs Distance from Times Square",
        labels={
            'distance_km': 'Distance from Times Square (km)',
            'price': 'Price per Night ($)',
            'room_type': 'Room Type'
        },
        color_discrete_sequence=['#FF5A5F', '#00A699', '#FC642D']
    )
    
    fig.update_layout(
        height=500,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=16,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
    )
    
    return fig

def display_eda_section(data, filtered_data):
    """Display comprehensive EDA section"""
    st.markdown('<div class="sub-header">📊 Exploratory Data Analysis</div>', unsafe_allow_html=True)
    
    # Create tabs for different EDA sections
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Distributions", "🗺️ Geographic Analysis", "💰 Price Analysis", "📝 Review Patterns"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Room Type Distribution")
            room_dist = filtered_data['room_type'].value_counts()
            fig = px.pie(
                values=room_dist.values, 
                names=room_dist.index,
                title="Distribution of Room Types",
                color_discrete_sequence=['#FF5A5F', '#00A699', '#FC642D']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Neighbourhood Group Distribution")
            neigh_dist = filtered_data['neighbourhood_group'].value_counts()
            fig = px.bar(
                x=neigh_dist.index,
                y=neigh_dist.values,
                title="Listings by Neighbourhood Group",
                color=neigh_dist.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Geographic Distribution of Listings")
        if len(filtered_data) > 0:
            # Create density heatmap
            fig = px.density_mapbox(
                filtered_data,
                lat='latitude',
                lon='longitude',
                z='price',
                radius=10,
                mapbox_style="open-street-map",
                title="Price Density Heatmap",
                height=500
            )
            fig.update_layout(mapbox_center_lat=40.7580, mapbox_center_lon=-73.9855, mapbox_zoom=10)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Price Distribution by Room Type")
            fig = px.box(
                filtered_data,
                x='room_type',
                y='price',
                title="Price Range by Room Type",
                color='room_type',
                color_discrete_sequence=['#FF5A5F', '#00A699', '#FC642D']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Average Price by Neighbourhood Group")
            avg_prices = filtered_data.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False)
            fig = px.bar(
                x=avg_prices.values,
                y=avg_prices.index,
                orientation='h',
                title="Average Price by Area",
                color=avg_prices.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Reviews vs Availability")
            fig = px.scatter(
                filtered_data,
                x='availability_365',
                y='number_of_reviews',
                color='room_type',
                title="Reviews vs Availability Pattern",
                color_discrete_sequence=['#FF5A5F', '#00A699', '#FC642D']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Review Activity Timeline")
            reviews_data = filtered_data[filtered_data['last_review'].notna()]
            if len(reviews_data) > 0:
                monthly_reviews = reviews_data.groupby(reviews_data['last_review'].dt.to_period("M")).size()
                monthly_reviews.index = monthly_reviews.index.to_timestamp()
                
                fig = px.line(
                    x=monthly_reviews.index,
                    y=monthly_reviews.values,
                    title="Review Activity Over Time"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

# Main Dashboard
def main():
    # Load data
    data = load_data()
    
    if data.empty:
        st.stop()
    
    # Header
    st.markdown('<div class="main-header">🏠 NYC Airbnb Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown("### Comprehensive insights for Hosts, Guests, Investors, and Policymakers")
    
    # Sidebar filters
    with st.sidebar:
        st.title("🎛️ Dashboard Controls")
        
        stakeholder = st.selectbox("👤 Select Stakeholder", 
                                   ["Hosts", "Guests", "Investors", "Policymakers"])
        
        st.markdown("---")
        st.subheader("🔍 Data Filters")
        
        neigh_group = st.multiselect("📍 Neighbourhood Group", 
                                     options=sorted(data['neighbourhood_group'].unique()),
                                     default=sorted(data['neighbourhood_group'].unique()))
        
        room_type = st.multiselect("🏠 Room Type",
                                   options=sorted(data['room_type'].unique()),
                                   default=sorted(data['room_type'].unique()))
        
        price_range = st.slider("💰 Price Range ($)", 
                                int(data['price'].min()), 
                                int(min(data['price'].max(), 1000)), 
                                (0, 500))
        
        min_reviews = st.slider("⭐ Minimum Reviews", 0, 100, 0)
        
        st.markdown("---")
        
        # Filter data
        filtered = data[
            (data['neighbourhood_group'].isin(neigh_group)) &
            (data['room_type'].isin(room_type)) &
            (data['price'].between(price_range[0], price_range[1])) &
            (data['number_of_reviews'] >= min_reviews)
        ]
        
        st.markdown(f"### 📊 {len(filtered):,} listings selected")
        st.markdown(f"*Out of {len(data):,} total listings*")
    
    if len(filtered) == 0:
        st.warning("⚠️ No data matches your current filters. Please adjust your selection.")
        st.stop()
    
    # Calculate distance from Times Square
    center_lat, center_lon = 40.7580, -73.9855
    filtered = filtered.copy()
    
    try:
        filtered['distance_km'] = haversine_array(
            filtered['latitude'], filtered['longitude'],
            center_lat, center_lon
        )
        filtered = filtered[filtered['distance_km'].notna() & (filtered['distance_km'] >= 0)]
    except Exception as e:
        st.error(f"❌ Error calculating distances: {e}")
        filtered['distance_km'] = np.nan
    
    # Main content area
    # Key Metrics Overview
    st.markdown('<div class="sub-header">🎯 Key Metrics Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🏠 Total Listings", f"{len(filtered):,}")
    
    with col2:
        avg_price = filtered['price'].mean()
        st.metric("💰 Avg Price", f"${avg_price:.0f}")
    
    with col3:
        avg_reviews = filtered['number_of_reviews'].mean()
        st.metric("⭐ Avg Reviews", f"{avg_reviews:.1f}")
    
    with col4:
        avg_availability = filtered['availability_365'].mean()
        st.metric("📅 Avg Availability", f"{avg_availability:.0f} days")
    
    with col5:
        if 'distance_km' in filtered.columns and filtered['distance_km'].notna().any():
            avg_distance = filtered['distance_km'].mean()
            st.metric("📍 Avg Distance", f"{avg_distance:.1f} km")
        else:
            st.metric("📍 Distance", "N/A")
    
    st.markdown("---")
    
    # Enhanced Price vs Distance Plot - Featured prominently
    st.markdown('<div class="sub-header">🎯 Featured Analysis: Location Impact on Pricing</div>', unsafe_allow_html=True)
    
    if 'distance_km' in filtered.columns:
        price_distance_fig = create_price_distance_plot(filtered)
        if price_distance_fig:
            st.plotly_chart(price_distance_fig, use_container_width=True)
            
            # Add insights box
            st.markdown("""
            <div class="insight-box">
            <strong>💡 Key Insights:</strong><br>
            • Listings closer to Times Square (0-5 km) command premium prices<br>
            • Outer boroughs offer better value for money<br>
            • Room type significantly impacts pricing regardless of location<br>
            • Size of bubbles indicates review popularity
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # EDA Section
    display_eda_section(data, filtered)
    
    st.markdown("---")
    
    # Stakeholder-specific insights
    st.markdown(f'<div class="sub-header">🎯 Insights for {stakeholder}</div>', unsafe_allow_html=True)
    
    if stakeholder == "Hosts":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🚀 Optimization Strategies:**
            - Compare your pricing with neighborhood averages
            - Encourage guest reviews to improve visibility
            - Balance availability for optimal income
            - Consider seasonal pricing adjustments
            """)
        
        with col2:
            # Host-specific metrics
            st.subheader("📊 Host Performance Indicators")
            avg_price = filtered['price'].mean()
            avg_reviews = filtered['number_of_reviews'].mean()
            avg_avail = filtered['availability_365'].mean()
            
            st.metric("💰 Market Price", f"${avg_price:.0f}")
            st.metric("⭐ Expected Reviews", f"{avg_reviews:.1f}")
            st.metric("📅 Typical Availability", f"{avg_avail:.0f} days")
    
    elif stakeholder == "Guests":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🎯 Smart Booking Tips:**
            - Compare prices across different neighborhoods
            - Look for hosts with consistent positive reviews
            - Book early during peak seasons
            - Consider outer boroughs for better value
            """)
        
        with col2:
            # Guest-specific recommendations
            st.subheader("💰 Best Value Recommendations")
            cheapest_neigh = filtered.groupby("neighbourhood_group")['price'].mean().sort_values().head(1)
            st.metric("Most Affordable Area", f"{cheapest_neigh.index[0]}")
            st.metric("Average Price", f"${cheapest_neigh.values[0]:.0f}")
    
    elif stakeholder == "Investors":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **💼 Investment Insights:**
            - Focus on high-demand, high-price areas
            - Consider entire home properties for better ROI
            - Diversify across multiple neighborhoods
            - Monitor occupancy rates and seasonal trends
            """)
        
        with col2:
            # Investment analysis
            st.subheader("📈 Investment Potential")
            roi_data = filtered.groupby("neighbourhood_group").agg({
                'price': 'mean',
                'availability_365': 'mean'
            })
            roi_data['ROI_Score'] = roi_data['price'] * (roi_data['availability_365'] / 365)
            top_roi = roi_data['ROI_Score'].idxmax()
            
            st.metric("Best ROI Area", f"{top_roi}")
            st.metric("ROI Score", f"{roi_data.loc[top_roi, 'ROI_Score']:.0f}")
    
    elif stakeholder == "Policymakers":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🏛️ Policy Considerations:**
            - Monitor housing market impact
            - Track tourism distribution patterns
            - Identify commercial vs. personal rentals
            - Ensure compliance with local regulations
            """)
        
        with col2:
            # Policy metrics
            st.subheader("🏛️ Regulatory Insights")
            entire_homes_pct = (filtered['room_type'] == "Entire home/apt").mean() * 100
            high_avail_pct = (filtered['availability_365'] > 300).mean() * 100
            
            st.metric("% Entire Homes", f"{entire_homes_pct:.1f}%")
            st.metric("% High Availability", f"{high_avail_pct:.1f}%")
    
    # Footer
    st.markdown("---")
    st.markdown("*Dashboard created with Streamlit • Data: NYC Airbnb 2019*")

if __name__ == "__main__":
    main()