import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration with custom styling
st.set_page_config(
    page_title='🏃‍♂️ Fitness Tracker Analytics Hub',
    layout='wide',
    initial_sidebar_state='expanded',
    page_icon='🏃‍♂️'
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric > div {
        color: white !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        color: white;
        margin: 10px 0;
    }
    .insight-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv('Fitness_trackers_updated.csv')
    # Clean numeric columns
    df['Selling Price'] = pd.to_numeric(
        df['Selling Price'].replace({',': ''}, regex=True), errors='coerce')
    df['Original Price'] = pd.to_numeric(
        df['Original Price'].replace({',': ''}, regex=True), errors='coerce')
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0)  # Fill NaNs with 0

    
    # Create additional calculated fields
    df['Discount (%)'] = 100 * (df['Original Price'] - df['Selling Price']) / df['Original Price']
    df['Value Score'] = (df['Rating (Out of 5)'] * df['Reviews']) / df['Selling Price']
    df['Price Category'] = pd.cut(df['Selling Price'], 
                                 bins=[0, 2000, 5000, 10000, float('inf')], 
                                 labels=['Budget', 'Mid-Range', 'Premium', 'Luxury'])
    return df

df = load_data()

# Enhanced Sidebar with beautiful styling
st.sidebar.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;'>
    <h2 style='color: white; margin: 0;'>🏃‍♂️ Fitness Analytics</h2>
    <p style='color: #e0e0e0; margin: 5px 0 0 0;'>Comprehensive Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Navigation
page = st.sidebar.selectbox(
    '📍 Navigate to',
    ['🏠 Executive Summary', 
     '📊 Feature Analysis', '🏆 Product Rankings', '🔍 Deep Dive Analytics']
)

# Advanced Filters
st.sidebar.markdown("### 🎛️ Smart Filters")
brand_filter = st.sidebar.multiselect('🏷️ Brands', options=sorted(df['Brand Name'].unique()))
device_filter = st.sidebar.multiselect('📱 Device Types', options=sorted(df['Device Type'].unique()))
color_filter = st.sidebar.multiselect('🎨 Colors', options=sorted(df['Color'].unique()))

# Price range filter
price_range = st.sidebar.slider(
    '💵 Price Range (₹)',
    min_value=int(df['Selling Price'].min()),
    max_value=int(df['Selling Price'].max()),
    value=(int(df['Selling Price'].min()), int(df['Selling Price'].max()))
)

# Rating filter
rating_filter = st.sidebar.slider('⭐ Minimum Rating', 1.0, 5.0, 1.0, 0.1)

# Apply filters
filtered_df = df.copy()
if brand_filter:
    filtered_df = filtered_df[filtered_df['Brand Name'].isin(brand_filter)]
if device_filter:
    filtered_df = filtered_df[filtered_df['Device Type'].isin(device_filter)]
if color_filter:
    filtered_df = filtered_df[filtered_df['Color'].isin(color_filter)]

filtered_df = filtered_df[
    (filtered_df['Selling Price'] >= price_range[0]) & 
    (filtered_df['Selling Price'] <= price_range[1]) &
    (filtered_df['Rating (Out of 5)'] >= rating_filter)
]

# Color palette for consistent styling
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']

# ========== Executive Summary Page ==========
if page == '🏠 Executive Summary':
    st.title('🏃‍♂️ Fitness Tracker Market Overview')
    st.markdown("### 📈 Executive Dashboard - Real-time Market Insights")
    
    # Key Performance Indicators
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📱 Total Products</h3>
            <h2>{len(filtered_df):,}</h2>
            <p>Available Models</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_rating = filtered_df['Rating (Out of 5)'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>⭐ Avg Rating</h3>
            <h2>{avg_rating:.2f}/5</h2>
            <p>Customer Satisfaction</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_price = filtered_df['Selling Price'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Avg Price</h3>
            <h2>₹{avg_price:,.0f}</h2>
            <p>Market Average</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_battery = filtered_df['Average Battery Life (in days)'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔋 Avg Battery</h3>
            <h2>{avg_battery:.1f} days</h2>
            <p>Power Performance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        avg_discount = filtered_df['Discount (%)'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏷️ Avg Discount</h3>
            <h2>{avg_discount:.1f}%</h2>
            <p>Savings Available</p>
        </div>
        """, unsafe_allow_html=True)
    
       
    # Key Insights
    st.markdown("### 🧠 AI-Powered Insights")
    
    # Calculate insights
    best_value = filtered_df.loc[filtered_df['Value Score'].idxmax()]
    most_reviewed = filtered_df.loc[filtered_df['Reviews'].idxmax()]
    highest_rated = filtered_df.loc[filtered_df['Rating (Out of 5)'].idxmax()]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
            🏆 Best Value Pick<br>
            <strong>{best_value['Model Name']}</strong><br>
            ₹{best_value['Selling Price']:,.0f} | {best_value['Rating (Out of 5)']:.1f}⭐
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box">
            📈 Most Popular<br>
            <strong>{most_reviewed['Model Name']}</strong><br>
            {most_reviewed['Reviews']:,.0f} reviews | {most_reviewed['Rating (Out of 5)']:.1f}⭐
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="insight-box">
            👑 Top Rated<br>
            <strong>{highest_rated['Model Name']}</strong><br>
            {highest_rated['Rating (Out of 5)']:.1f}⭐ | ₹{highest_rated['Selling Price']:,.0f}
        </div>
        """, unsafe_allow_html=True)


# ========== Feature Analysis Page ==========
elif page == '📊 Feature Analysis':
    st.title('📊 Comprehensive Feature Analysis')
    
    # Device features overview
    st.markdown("### 🔍 Feature Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Display type analysis
        display_counts = filtered_df['Display'].value_counts()
        fig_display = px.pie(
            values=display_counts.values,
            names=display_counts.index,
            title='Display Type Distribution',
            color_discrete_sequence=colors,
            hole=0.3
        )
        st.plotly_chart(fig_display, use_container_width=True)
    
    with col2:
        # Strap material analysis
        strap_counts = filtered_df['Strap Material'].value_counts()
        fig_strap = px.pie(
            values=strap_counts.values,
            names=strap_counts.index,
            title='Strap Material Distribution',
            color_discrete_sequence=colors,
            hole=0.3
        )
        st.plotly_chart(fig_strap, use_container_width=True)
    
    # Battery life analysis
    st.markdown("### 🔋 Battery Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Battery life distribution
        fig_battery = px.histogram(
            filtered_df,
            x='Average Battery Life (in days)',
            nbins=20,
            title='Battery Life Distribution',
            color_discrete_sequence=['#4ECDC4']
        )
        fig_battery.update_layout(height=400)
        st.plotly_chart(fig_battery, use_container_width=True)
    
    with col2:
        # Battery life by brand
        battery_by_brand = filtered_df.groupby('Brand Name')['Average Battery Life (in days)'].mean().sort_values(ascending=False)
        fig_battery_brand = px.bar(
            x=battery_by_brand.index,
            y=battery_by_brand.values,
            title='Average Battery Life by Brand',
            color=battery_by_brand.values,
            color_continuous_scale='Greens'
        )
        fig_battery_brand.update_xaxes(tickangle=45)
        fig_battery_brand.update_layout(height=400)
        st.plotly_chart(fig_battery_brand, use_container_width=True)
    
    # Color preference analysis
    st.markdown("### 🎨 Color Preference Insights")
    color_preference = filtered_df['Color'].value_counts().head(10)
    fig_color = px.bar(
        x=color_preference.values,
        y=color_preference.index,
        orientation='h',
        title='Top 10 Popular Colors',
        color=color_preference.values,
        color_continuous_scale='Rainbow'
    )
    fig_color.update_layout(height=500)
    st.plotly_chart(fig_color, use_container_width=True)
    
       

# ========== Product Rankings Page ==========
elif page == '🏆 Product Rankings':
    st.title('🏆 Comprehensive Product Rankings')
    
    # Top performers dashboard
    st.markdown("### 🎯 Performance Leaders")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏅 Overall Best", "💰 Best Value", "⭐ Top Rated", "📈 Most Popular"])
    
    with tab1:
        # Overall best products (weighted score)
        filtered_df['Overall Score'] = (
            filtered_df['Rating (Out of 5)'] * 0.4 +
            (filtered_df['Reviews'] / filtered_df['Reviews'].max() * 5) * 0.3 +
            (filtered_df['Discount (%)'] / 100 * 5) * 0.2 +
            (filtered_df['Average Battery Life (in days)'] / filtered_df['Average Battery Life (in days)'].max() * 5) * 0.1
        )
        
        top_overall = filtered_df.nlargest(10, 'Overall Score')
        
        fig_overall = px.bar(
            top_overall,
            x='Overall Score',
            y='Model Name',
            orientation='h',
            color='Brand Name',
            title='Top 10 Overall Best Products',
            color_discrete_sequence=colors
        )
        fig_overall.update_layout(height=600)
        st.plotly_chart(fig_overall, use_container_width=True)
        
        st.dataframe(
            top_overall[['Brand Name', 'Model Name', 'Selling Price', 'Rating (Out of 5)', 
                        'Reviews', 'Overall Score']].round(2),
            use_container_width=True
        )
    
    with tab2:
        # Best value products
        top_value = filtered_df.nlargest(10, 'Value Score')
        
        fig_value = px.scatter(
            top_value,
            x='Selling Price',
            y='Rating (Out of 5)',
            size='Reviews',
            color='Brand Name',
            hover_data=['Model Name', 'Value Score'],
            title='Best Value Products (Bubble size = Reviews)',
            color_discrete_sequence=colors
        )
        fig_value.update_layout(height=500)
        st.plotly_chart(fig_value, use_container_width=True)
        
        st.dataframe(
            top_value[['Brand Name', 'Model Name', 'Selling Price', 'Rating (Out of 5)', 
                      'Reviews', 'Value Score']].round(3),
            use_container_width=True
        )
    
    with tab3:
        # Top rated products
        top_rated = filtered_df.nlargest(10, 'Rating (Out of 5)')
        
        fig_rated = px.bar(
            top_rated,
            x='Rating (Out of 5)',
            y='Model Name',
            orientation='h',
            color='Selling Price',
            title='Top 10 Highest Rated Products',
            color_continuous_scale='Viridis'
        )
        fig_rated.update_layout(height=600)
        st.plotly_chart(fig_rated, use_container_width=True)
        
        st.dataframe(
            top_rated[['Brand Name', 'Model Name', 'Selling Price', 'Rating (Out of 5)', 'Reviews']],
            use_container_width=True
        )
    
    with tab4:
        # Most popular products
        top_popular = filtered_df.nlargest(10, 'Reviews')
        
        fig_popular = px.bar(
            top_popular,
            x='Reviews',
            y='Model Name',
            orientation='h',
            color='Rating (Out of 5)',
            title='Top 10 Most Popular Products',
            color_continuous_scale='RdYlGn'
        )
        fig_popular.update_layout(height=600)
        st.plotly_chart(fig_popular, use_container_width=True)
        
        st.dataframe(
            top_popular[['Brand Name', 'Model Name', 'Selling Price', 'Rating (Out of 5)', 'Reviews']],
            use_container_width=True
        )

# ========== Deep Dive Analytics Page ==========
elif page == '🔍 Deep Dive Analytics':
    st.title('🔍 Advanced Analytics & Insights')
    
    # Advanced analytics dashboard
   
    
      
    # Advanced insights
    st.markdown("### 🎯 Strategic Insights")
    
    col1, col2, col3 = st.columns(3)
    
    # Market concentration
    with col1:
        market_concentration = filtered_df['Brand Name'].value_counts().head(3).sum() / len(filtered_df) * 100
        st.markdown(f"""
        <div class="insight-box">
            📊 Market Concentration<br>
            <strong>Top 3 Brands Control</strong><br>
            {market_concentration:.1f}% of Market
        </div>
        """, unsafe_allow_html=True)
    
    # Price elasticity insight
    with col2:
        price_rating_corr = filtered_df['Selling Price'].corr(filtered_df['Rating (Out of 5)'])
        elasticity_msg = "Strong" if abs(price_rating_corr) > 0.5 else "Moderate" if abs(price_rating_corr) > 0.3 else "Weak"
        st.markdown(f"""
        <div class="insight-box">
            💰 Price-Quality Correlation<br>
            <strong>{elasticity_msg}</strong><br>
            Correlation: {price_rating_corr:.3f}
        </div>
        """, unsafe_allow_html=True)
    
    # Feature opportunity
    with col3:
        battery_price_corr = filtered_df['Average Battery Life (in days)'].corr(filtered_df['Selling Price'])
        battery_msg = "Premium Feature" if battery_price_corr > 0.3 else "Standard Feature"
        st.markdown(f"""
        <div class="insight-box">
            🔋 Battery Life Impact<br>
            <strong>{battery_msg}</strong><br>
            Price Correlation: {battery_price_corr:.3f}
        </div>
        """, unsafe_allow_html=True)
    
    # Competitive landscape matrix
    st.markdown("### 🏁 Competitive Landscape Matrix")
    
    # Create competitive matrix
    comp_matrix = filtered_df.groupby('Brand Name').agg({
        'Selling Price': ['mean', 'min', 'max'],
        'Rating (Out of 5)': 'mean',
        'Reviews': 'sum',
        'Model Name': 'count',
        'Discount (%)': 'mean'
    }).round(2)
    
    comp_matrix.columns = ['Avg_Price', 'Min_Price', 'Max_Price', 'Avg_Rating', 'Total_Reviews', 'Product_Count', 'Avg_Discount']
    comp_matrix = comp_matrix.reset_index()
    
    # Display competitive matrix
    st.write(
        comp_matrix.style.background_gradient(subset=['Avg_Rating', 'Total_Reviews'], cmap='Greens')
                          .background_gradient(subset=['Avg_Price'], cmap='Reds_r')
                          .background_gradient(subset=['Avg_Discount'], cmap='Blues'),
        use_container_width=True
    )
    
    # Recommendation engine
    st.markdown("### 🤖 AI Recommendation Engine")
    
    # User preference inputs
    st.markdown("#### Find Your Perfect Fitness Tracker")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        budget = st.selectbox("💰 Budget Range", ["Budget (₹0-2K)", "Mid-Range (₹2K-5K)", "Premium (₹5K-10K)", "Luxury (₹10K+)"])
        priority = st.selectbox("🎯 Priority", ["Best Value", "Highest Quality", "Most Popular", "Longest Battery"])
    
    with col2:
        preferred_brand = st.selectbox("🏷️ Brand Preference", ["No Preference"] + list(filtered_df['Brand Name'].unique()))
        device_type = st.selectbox("📱 Device Type", ["No Preference"] + list(filtered_df['Device Type'].unique()))
    
    with col3:
        min_rating = st.slider("⭐ Minimum Rating", 1.0, 5.0, 4.0, 0.1)
        min_battery = st.slider("🔋 Minimum Battery (days)", 1, 30, 5)
    
    # Generate recommendations
    if st.button("🔍 Get Recommendations", type="primary"):
        rec_df = filtered_df.copy()
        
        # Apply budget filter
        if budget == "Budget (₹0-2K)":
            rec_df = rec_df[rec_df['Selling Price'] <= 2000]
        elif budget == "Mid-Range (₹2K-5K)":
            rec_df = rec_df[(rec_df['Selling Price'] > 2000) & (rec_df['Selling Price'] <= 5000)]
        elif budget == "Premium (₹5K-10K)":
            rec_df = rec_df[(rec_df['Selling Price'] > 5000) & (rec_df['Selling Price'] <= 10000)]
        else:
            rec_df = rec_df[rec_df['Selling Price'] > 10000]
        
        # Apply other filters
        if preferred_brand != "No Preference":
            rec_df = rec_df[rec_df['Brand Name'] == preferred_brand]
        if device_type != "No Preference":
            rec_df = rec_df[rec_df['Device Type'] == device_type]
        
        rec_df = rec_df[
            (rec_df['Rating (Out of 5)'] >= min_rating) &
            (rec_df['Average Battery Life (in days)'] >= min_battery)
        ]
        
        if len(rec_df) > 0:
            # Sort by priority
            if priority == "Best Value":
                recommendations = rec_df.nlargest(5, 'Value Score')
            elif priority == "Highest Quality":
                recommendations = rec_df.nlargest(5, 'Rating (Out of 5)')
            elif priority == "Most Popular":
                recommendations = rec_df.nlargest(5, 'Reviews')
            else:  # Longest Battery
                recommendations = rec_df.nlargest(5, 'Average Battery Life (in days)')
            
            st.markdown("#### 🎯 Your Personalized Recommendations")
            
            for idx, (_, product) in enumerate(recommendations.iterrows(), 1):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin: 5px;'>
                        <h3>#{idx}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    **{product['Brand Name']} {product['Model Name']}**
                    - 💰 Price: ₹{product['Selling Price']:,.0f} (Original: ₹{product['Original Price']:,.0f})
                    - ⭐ Rating: {product['Rating (Out of 5)']:.1f}/5 ({product['Reviews']:,.0f} reviews)
                    - 🔋 Battery: {product['Average Battery Life (in days)']:.0f} days
                    - 🏷️ Discount: {product['Discount (%)']:.1f}%
                    """)
                
                st.markdown("---")
        else:
            st.warning("No products match your criteria. Please adjust your filters.")
    
    # Market opportunity analysis
    st.markdown("### 💡 Market Opportunity Analysis")
    
    # Gap analysis
    gap_analysis = pd.DataFrame({
        'Segment': ['Budget High-Quality', 'Premium Long-Battery', 'Mid-Range Popular'],
        'Opportunity_Score': [
            len(filtered_df[(filtered_df['Selling Price'] < 3000) & (filtered_df['Rating (Out of 5)'] > 4.5)]),
            len(filtered_df[(filtered_df['Selling Price'] > 8000) & (filtered_df['Average Battery Life (in days)'] > 20)]),
            len(filtered_df[(filtered_df['Selling Price'].between(3000, 8000)) & (filtered_df['Reviews'] > 1000)])
        ],
        'Market_Size': [
            len(filtered_df[filtered_df['Selling Price'] < 3000]),
            len(filtered_df[filtered_df['Selling Price'] > 8000]),
            len(filtered_df[filtered_df['Selling Price'].between(3000, 8000)])
        ]
    })
    
    gap_analysis['Gap_Ratio'] = gap_analysis['Opportunity_Score'] / gap_analysis['Market_Size']
    
    fig_gap = px.bar(
        gap_analysis,
        x='Segment',
        y='Gap_Ratio',
        title='Market Gap Analysis (Lower = More Opportunity)',
        color='Gap_Ratio',
        color_continuous_scale='RdYlGn_r'
    )
    fig_gap.update_layout(height=400)
    st.plotly_chart(fig_gap, use_container_width=True)

# Footer with additional info
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-top: 30px;'>
    <h3>🏃‍♂️ Fitness Tracker Analytics Hub</h3>
    <p>Comprehensive market intelligence powered by advanced data analytics</p>
    <p><small>Data insights updated in real-time | Advanced filtering and AI recommendations</small></p>
</div>
""", unsafe_allow_html=True)
