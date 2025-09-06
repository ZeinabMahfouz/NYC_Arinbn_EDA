🏠 NYC Airbnb Analytics Dashboard
A comprehensive data analysis and interactive dashboard for NYC Airbnb listings (2019), providing insights for hosts, guests, investors, and policymakers through advanced exploratory data analysis and distance-based analytics.
Show Image
Show Image
Show Image
📋 Table of Contents

Project Overview
Features
Technology Stack
Installation
Usage
Data Analysis
Dashboard Components
Key Insights
Stakeholder Benefits
Project Structure
Contributing
License

🎯 Project Overview
This project provides a comprehensive analysis of NYC Airbnb data with a focus on:

Geographic Analysis: Location impact on pricing and demand
Distance Analytics: Properties' proximity to city center (Times Square)
Market Segmentation: Room types, boroughs, and host categories
Pricing Intelligence: Dynamic pricing patterns and optimization
Interactive Dashboard: Stakeholder-specific insights and visualizations

✨ Features
🔍 Advanced Analytics

Distance Calculation: Using geopy library to calculate distances from Times Square
Host Type Analysis: Single listing to commercial host categorization
Activity Status: Property activity levels based on review patterns
Seasonal Analysis: Review and booking patterns by season
Market Saturation: Neighborhood-level supply and demand analysis

📊 Interactive Dashboard

Multi-Stakeholder Views: Customized insights for hosts, guests, investors, and policymakers
Dynamic Filtering: Real-time data filtering by location, price, reviews
Interactive Maps: Geographic distribution with price density heatmaps
Comprehensive EDA: Multiple visualization tabs for different analysis aspects

🎨 Rich Visualizations

Price vs Distance scatter plots with interactive bubbles
Geographic heatmaps with Folium/Plotly integration
Statistical distributions and correlation analysis
Time-series analysis of review patterns
Host performance metrics and comparisons

🛠 Technology Stack
python# Core Libraries
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.11.0

# Interactive Visualizations
plotly>=5.0.0
streamlit>=1.15.0
streamlit-folium>=0.6.0

# Geospatial Analysis
folium>=0.12.0
geopy>=2.2.0

# Statistical Analysis
scipy>=1.7.0
scikit-learn>=1.0.0
⚙️ Installation
1. Clone the Repository
bashgit clone https://github.com/yourusername/nyc-airbnb-analytics.git
cd nyc-airbnb-analytics
2. Create Virtual Environment
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bashpip install -r requirements.txt
4. Download Dataset
Place the AB_NYC_2019.csv file in the project root directory.

Dataset source: NYC Airbnb Open Data

🚀 Usage
Running the Dashboard
bashstreamlit run Airnbn_dashboard.py
Running EDA Analysis
python# Execute the comprehensive EDA script
python nyc_airbnb_eda.py

# For distance-specific analysis
python distance_analysis.py
Key Functions
python# Calculate distance from city center
def calculate_distance_from_center(lat, lon):
    """Calculate distance in km from NYC city center"""
    # Implementation using geopy

# Host type categorization
def categorize_host_type(count):
    """Categorize hosts based on listing count"""
    # Returns: Single, Small Scale, Medium Scale, Large Scale, Commercial

# Activity status based on reviews
def categorize_activity_status(days_since):
    """Determine property activity level"""
    # Returns: Very Active, Active, Moderately Active, Less Active, Inactive
📈 Data Analysis
1. Data Cleaning & Preprocessing

Handled missing values in reviews and host information
Removed extreme price outliers (>99th percentile)
Geocoded properties and validated coordinates
Created distance feature using geopy library

2. Feature Engineering
python# Distance from city center
data['distance'] = calculate_distance_from_center(lat, lon)

# Host type classification
data['host_type'] = categorize_host_type(calculated_host_listings_count)

# Activity status based on last review
data['activity_status'] = categorize_activity_status(days_since_last_review)

# Seasonal analysis
data['last_review_season'] = get_season(last_review_month)
3. Key Analysis Areas

Geographic Distribution: Borough and neighborhood analysis
Pricing Analysis: Price vs location, room type, and amenities
Host Performance: Multi-property vs single-property hosts
Market Activity: Review patterns and availability trends
Distance Impact: Proximity effects on pricing and demand

🖥 Dashboard Components
Main Features

🎯 Key Metrics Overview: Total listings, average price, reviews, availability
📍 Featured Analysis: Price vs Distance interactive scatter plot
📊 EDA Tabs: Distributions, Geographic, Price, Review patterns
👥 Stakeholder Views: Customized insights per user type

Interactive Elements

Filters: Neighborhood, room type, price range, minimum reviews
Maps: Density heatmaps with price overlays
Charts: Plotly interactive visualizations
Metrics: Real-time calculated KPIs

🔍 Key Insights
💰 Pricing Patterns

Manhattan Premium: 40-60% higher prices than outer boroughs
Distance Effect: 15-20% price decrease per 10km from Times Square
Room Type Impact: Entire homes command 2-3x price of shared rooms

🏠 Host Analysis

Single Listing Hosts: 70%+ of total hosts
Commercial Operations: <5% but significant market share
Performance Variation: Large-scale hosts show higher availability but variable pricing

📍 Geographic Distribution

Manhattan Concentration: 40%+ of listings in 23% of land area
Brooklyn Growth: Fastest growing segment with balanced price/value
Outer Borough Opportunity: Underserved markets with growth potential

🎯 Market Dynamics

Review Correlation: Higher reviews = higher prices (up to inflection point)
Seasonal Patterns: Summer peak, winter low demand
Activity Levels: 60% properties "Very Active" or "Active"

👥 Stakeholder Benefits
🏠 For Hosts

Pricing Optimization: Market-rate comparisons and recommendations
Performance Benchmarking: Reviews, availability, and revenue metrics
Market Positioning: Competitive analysis and differentiation strategies

✈️ For Guests

Value Discovery: Best price-to-location ratios
Booking Intelligence: Optimal timing and area selection
Quality Indicators: Review patterns and host reliability metrics

💼 For Investors

ROI Analysis: Revenue potential by neighborhood and property type
Market Opportunity: Underserved areas and growth potential
Risk Assessment: Market saturation and competition levels

🏛️ For Policymakers

Market Impact: Housing availability and tourism distribution
Regulatory Insights: Commercial vs personal rental identification
Economic Analysis: Tourism revenue and local economic impact

📁 Project Structure
nyc-airbnb-analytics/
│
├── data/
│   └── AB_NYC_2019.csv              # Main dataset
│
├── notebooks/
│   ├── data_cleaning.ipynb          # Data preprocessing
│   ├── eda_analysis.ipynb           # Exploratory data analysis
│   └── distance_analysis.ipynb     # Distance feature analysis
│
├── src/
│   ├── Airnbn_dashboard.py          # Main Streamlit dashboard
│   ├── data_processing.py           # Data cleaning functions
│   ├── visualization.py             # Plotting functions
│   └── distance_calc.py             # Distance calculation utilities
│
├── assets/
│   ├── screenshots/                 # Dashboard screenshots
│   └── plots/                       # Generated visualizations
│
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
└── .gitignore                      # Git ignore rules
📊 Sample Visualizations
Distance Analysis

Price vs Distance: Scatter plot with room type colors and review size
Borough Distribution: Box plots showing distance variations
Heatmaps: Price patterns across distance/borough combinations

Market Analysis

Host Performance: Multi-metric dashboard comparing host types
Geographic Distribution: Interactive maps with price density
Temporal Patterns: Review activity and seasonal trends

Statistical Analysis

Correlation Matrix: Relationship between numerical variables
Distribution Analysis: Price, reviews, and availability patterns
Market Segmentation: Room type and location cross-analysis

🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the repository
Create feature branch: git checkout -b feature/amazing-feature
Commit changes: git commit -m 'Add amazing feature'
Push to branch: git push origin feature/amazing-feature
Open Pull Request

Development Guidelines

Follow PEP 8 style guidelines
Add docstrings to all functions
Include unit tests for new features
Update README for significant changes

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Dataset: NYC Open Data & Inside Airbnb
Libraries: Streamlit, Plotly, Pandas, GeoPy communities
Inspiration: NYC tourism and housing policy research

📞 Contact
Project Maintainer: [Your Name]

GitHub: @yourusername
LinkedIn: Your LinkedIn
Email: your.email@example.com


🚀 Quick Start
bash# Clone and setup
git clone https://github.com/ZeinabMahfouz/.git
cd nyc-airbnb-analytics
pip install -r requirements.txt

# Run dashboard
streamlit run Airnbn_dashboard.py

# Access at: http://localhost:8501
⭐ Star this repository if it helped you!

Made with ❤️ for data-driven decision making in the sharing economy
