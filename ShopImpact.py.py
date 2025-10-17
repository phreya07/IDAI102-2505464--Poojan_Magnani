import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(
    page_title="ShopImpact - Your Eco Companion",
    page_icon="🌍",
    layout="wide"
)

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'purchases' not in st.session_state:
    st.session_state.purchases = []
if 'badges' not in st.session_state:
    st.session_state.badges = set()
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

CO2_IMPACT = {
    'Electronics': 0.8,
    'Clothing': 0.6,
    'Food': 0.3,
    'Home & Garden': 0.4,
    'Beauty & Personal Care': 0.5,
    'Toys & Games': 0.7,
    'Books & Media': 0.2,
    'Transportation': 1.2,
    'Furniture': 0.9
}

ECO_BRANDS = {
    'Electronics': ['Apple (Refurbished)', 'Fairphone', 'Framework', 'Patagonia Electronics'],
    'Clothing': ['Patagonia', 'Everlane', 'Reformation', 'Allbirds', 'Tentree'],
    'Food': ['Local Farms', 'Organic Valley', 'Whole Foods 365', 'Thrive Market'],
    'Home & Garden': ['IKEA Sustainable', 'Seventh Generation', 'Method', 'Grove Collaborative'],
    'Beauty & Personal Care': ['The Body Shop', 'Lush', 'Ethique', 'Native', 'Thinx'],
    'Toys & Games': ['Green Toys', 'PlanToys', 'Hape', 'Melissa & Doug Wood'],
    'Books & Media': ['Better World Books', 'ThriftBooks', 'Local Library', 'Project Gutenberg'],
    'Transportation': ['Tesla', 'Rivian', 'Public Transit Pass', 'Bike Share'],
    'Furniture': ['IKEA Circular', 'West Elm Sustainable', 'Thrift Stores', 'Habitat ReStore']
}

ECO_ALTERNATIVES = {
    'Electronics': ['Buy refurbished devices', 'Choose energy-efficient models', 'Repair instead of replace', 'Donate old electronics'],
    'Clothing': ['Choose organic cotton', 'Buy from sustainable brands', 'Shop second-hand', 'Rent for special occasions'],
    'Food': ['Buy local and seasonal', 'Choose plant-based options', 'Reduce food waste', 'Grow your own herbs'],
    'Home & Garden': ['Use LED bulbs', 'Choose sustainable materials', 'Install solar panels', 'Compost organic waste'],
    'Beauty & Personal Care': ['Choose cruelty-free products', 'Use refillable containers', 'Buy organic', 'Make DIY products'],
    'Toys & Games': ['Choose wooden toys', 'Buy second-hand', 'Select educational games', 'Swap with friends'],
    'Books & Media': ['Use e-books', 'Borrow from library', 'Buy used books', 'Share subscriptions'],
    'Transportation': ['Use public transport', 'Carpool', 'Consider electric vehicles', 'Bike or walk when possible'],
    'Furniture': ['Buy second-hand', 'Choose sustainable wood', 'Upcycle old furniture', 'Rent furniture']
}

ECO_TIPS = [
    "💡 Did you know? Bamboo grows 35 inches per day and has a lower carbon footprint!",
    "🌍 Fun fact: Buying local can reduce transport emissions by up to 90%!",
    "♻️ Remember: Recycling one aluminum can saves enough energy to run a TV for 3 hours!",
    "🌱 Tip: Cotton bags become eco-friendly after 131 uses compared to plastic bags!",
    "🌿 Know: LED bulbs use 75% less energy than traditional incandescent bulbs!",
    "💚 Believe: Your eco-friendly choices inspire others to do the same!",
    "🐢 Nature fact: Sea turtles can live over 100 years when oceans are clean!",
    "🌳 Amazing: One tree can absorb 48 pounds of CO₂ per year!",
    "🍃 Tip: Organic food uses 45% less energy than conventional farming!",
    "💧 Did you know? A reusable water bottle saves 167 plastic bottles per year!"
]

QUOTES = [
    '"The Earth is what we all have in common." - Wendell Berry',
    '"Be the change you wish to see in the world." - Mahatma Gandhi',
    '"The greatest threat to our planet is the belief that someone else will save it." - Robert Swan',
    '"We don\'t need a handful of people doing zero waste perfectly. We need millions doing it imperfectly." - Anne Marie Bonneau',
    '"The environment is where we all meet; where we all have a mutual interest." - Lady Bird Johnson',
    '"Small acts, when multiplied by millions, can transform the world." - Howard Zinn',
    '"Nature is not a place to visit. It is home." - Gary Snyder'
]

def calculate_co2(category, price):
    return round(CO2_IMPACT.get(category, 0.5) * price, 2)

def check_badges(purchases):
    badges = set()
    total_purchases = len(purchases)
    
    if total_purchases >= 1:
        badges.add('🌱 Eco Newbie')
    if total_purchases >= 5:
        badges.add('🌿 Green Shopper')
    if total_purchases >= 10:
        badges.add('🌳 Eco Warrior')
    if total_purchases >= 20:
        badges.add('♻️ Sustainable Star')
    if total_purchases >= 30:
        badges.add('🏆 Eco Champion')
    
    df = pd.DataFrame(purchases)
    if not df.empty:
        total_co2 = df['co2'].sum()
        co2_saved = total_co2 * 0.2
        
        if co2_saved >= 5:
            badges.add('💚 Planet Protector')
        if co2_saved >= 10:
            badges.add('🌍 Low Impact Shopper')
        if co2_saved >= 25:
            badges.add('🌎 Eco Saver')
        if co2_saved >= 50:
            badges.add('⭐ Earth Champion')
    
    return badges

def draw_turtle_footprint():
    return """
    🐢 Eco-Friendly Choice!
    
        🦶 👣
       /     \\
      🌿     🌿
     /         \\
    🍃         🍃
    
    You left a GREEN footprint! 
    """

def draw_leaf_badge():
    return """
    🍃 Amazing Choice! 🍃
    
         🌿
        /|\\
       / | \\
      🌱 | 🌱
         |
        🌍
    
    You earned a leaf badge!
    """

def draw_eco_badge():
    return """
    ⭐ EXCELLENT! ⭐
    
       ___🌟___
      /         \\
     |  ECO WIN  |
     |    💚     |
      \\_________/
         |   |
        🌍 🌱
    
    Fantastic sustainable choice!
    """

def apply_theme():
    if st.session_state.dark_mode:
        st.markdown("""
            <style>
            .main {
                background-color: #1e3a1e;
                color: #e8f5e9;
            }
            .stButton>button {
                background-color: #2e7d32;
                color: white;
                border-radius: 15px;
                padding: 12px 28px;
                font-weight: bold;
                font-size: 18px;
                border: 2px solid #4caf50;
            }
            .stButton>button:hover {
                background-color: #388e3c;
                border-color: #66bb6a;
            }
            h1, h2, h3 {
                color: #a5d6a7 !important;
                font-size: 2.5em !important;
            }
            .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
                background-color: #2d4a2d;
                color: #e8f5e9;
                font-size: 18px;
                border: 2px solid #4caf50;
            }
            </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .main {
                background-color: #f1f8e9;
                color: #1b5e20;
            }
            .stButton>button {
                background-color: #52b788;
                color: white;
                border-radius: 15px;
                padding: 12px 28px;
                font-weight: bold;
                font-size: 18px;
                border: 2px solid #2d6a4f;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #40916c;
                transform: scale(1.05);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            h1 {
                color: #1b4332 !important;
                font-size: 3em !important;
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            h2 {
                color: #2d6a4f !important;
                font-size: 2em !important;
            }
            h3 {
                color: #40916c !important;
                font-size: 1.5em !important;
            }
            .stMetric {
                background-color: #d8f3dc;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .stMetric label {
                font-size: 20px !important;
                font-weight: bold;
            }
            .stMetric [data-testid="stMetricValue"] {
                font-size: 32px !important;
            }
            .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
                font-size: 18px;
                border: 2px solid #52b788;
                border-radius: 10px;
            }
            .stDataFrame {
                font-size: 16px;
            }
            </style>
            """, unsafe_allow_html=True)

apply_theme()

if st.session_state.user_profile is None:
    st.title("🌍 Welcome to ShopImpact!")
    st.markdown("### Your Friendly Eco Shopping Companion")
    st.markdown("---")
    
    st.markdown("## 👋 Let's Get to Know You!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("What's your name?", placeholder="Enter your name", key="name_input")
        age = st.number_input("How old are you?", min_value=13, max_value=120, value=25, step=1)
    
    with col2:
        gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Non-binary", "Other"])
        monthly_income = st.number_input("Monthly Income ($)", min_value=0, value=3000, step=100)
    
    st.markdown("---")
    
    if st.button("🚀 Start Your Eco Journey!", key="start_journey"):
        if name.strip():
            st.session_state.user_profile = {
                'name': name,
                'gender': gender,
                'age': age,
                'monthly_income': monthly_income
            }
            st.balloons()
            st.success(f"Welcome aboard, {name}! Let's make a difference together! 🌱")
            st.rerun()
        else:
            st.warning("Please enter your name to continue!")
    
    st.markdown("---")
    st.info("💚 ShopImpact helps you track and reduce your environmental footprint while shopping!")

else:
    user = st.session_state.user_profile
    
    st.title(f"🌍 Hello, {user['name']}! Welcome Back!")
    st.markdown("### *Your Friendly Eco Shopping Companion*")
    
    with st.sidebar:
        st.header("⚙️ Your Profile")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Age:** {user['age']}")
        st.write(f"**Gender:** {user['gender']}")
        st.write(f"**Monthly Income:** ${user['monthly_income']:,.2f}")
        
        st.markdown("---")
        
        if st.button("🌙 Toggle Dark Mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        st.markdown("---")
        
        st.info(random.choice(ECO_TIPS))
        
        st.success(random.choice(QUOTES))
        
        st.markdown("---")
        
        st.subheader("🏆 Your Badges")
        current_badges = check_badges(st.session_state.purchases)
        if current_badges:
            for badge in current_badges:
                st.markdown(f"### {badge}")
        else:
            st.write("🌱 Start shopping to earn badges!")
        
        if st.session_state.purchases:
            st.markdown("---")
            st.subheader("📊 Quick Stats")
            df = pd.DataFrame(st.session_state.purchases)
            st.metric("Total Purchases", len(st.session_state.purchases))
            st.metric("Categories Tracked", df['category'].nunique())
            st.metric("Eco Score", f"{min(100, len(st.session_state.purchases) * 5)}%")
        
        st.markdown("---")
        if st.button("🔄 Reset Profile"):
            st.session_state.user_profile = None
            st.session_state.purchases = []
            st.session_state.badges = set()
            st.rerun()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🛍️ Add New Purchase")
        
        with st.form("purchase_form"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                category = st.selectbox("Product Category", list(CO2_IMPACT.keys()))
                
                eco_brand_suggestions = ECO_BRANDS.get(category, [])
                brand_options = [""] + eco_brand_suggestions + ["Other"]
                selected_brand = st.selectbox("Brand (Eco-friendly suggestions)", brand_options)
                
                if selected_brand == "Other" or selected_brand == "":
                    brand = st.text_input("Enter brand name", value="" if selected_brand == "" else "")
                else:
                    brand = selected_brand
            
            with col_b:
                price = st.number_input("Price ($)", min_value=0.0, step=0.01)
                date = st.date_input("Purchase Date", datetime.now())
            
            submitted = st.form_submit_button("🌱 Add Purchase & See Impact!")
            
            if submitted and price > 0:
                co2 = calculate_co2(category, price)
                purchase = {
                    'date': date,
                    'category': category,
                    'brand': brand if brand else "Unknown",
                    'price': price,
                    'co2': co2
                }
                st.session_state.purchases.append(purchase)
                
                st.success(f"✅ Purchase added! CO₂ Impact: **{co2} kg**")
                
                st.balloons()
                
                if co2 < 3:
                    st.code(draw_eco_badge())
                elif co2 < 5:
                    st.code(draw_leaf_badge())
                else:
                    st.code(draw_turtle_footprint())
                
                st.info(random.choice(ECO_TIPS))
                
                new_badges = check_badges(st.session_state.purchases) - st.session_state.badges
                if new_badges:
                    for badge in new_badges:
                        st.success(f"🎉 NEW BADGE UNLOCKED: {badge}")
                    st.session_state.badges = check_badges(st.session_state.purchases)
                
                st.rerun()
    
    with col2:
        st.header("💡 Eco Tips")
        if 'category' in locals():
            st.markdown("### 🌿 Greener Alternatives:")
            alternatives = ECO_ALTERNATIVES.get(category, [])
            for alt in alternatives:
                st.markdown(f"✓ {alt}")
            
            st.markdown("---")
            st.markdown("### 🏪 Eco-Friendly Brands:")
            eco_brands = ECO_BRANDS.get(category, [])
            for brand_name in eco_brands[:3]:
                st.markdown(f"🌱 {brand_name}")
    
    if st.session_state.purchases:
        st.markdown("---")
        st.header("📈 Your Impact Dashboard")
        
        df = pd.DataFrame(st.session_state.purchases)
        df['date'] = pd.to_datetime(df['date'])
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_data = df[(df['date'].dt.month == current_month) & (df['date'].dt.year == current_year)]
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            monthly_spend = monthly_data['price'].sum()
            st.metric("💰 Monthly Spend", f"${monthly_spend:.2f}")
        
        with metric_col2:
            monthly_co2 = monthly_data['co2'].sum()
            st.metric("🌍 Monthly CO₂", f"{monthly_co2:.2f} kg")
        
        with metric_col3:
            st.metric("🛒 Total Purchases", len(st.session_state.purchases))
        
        with metric_col4:
            potential_saved = df['co2'].sum() * 0.2
            st.metric("💚 CO₂ You're Saving", f"{potential_saved:.2f} kg")
        
        st.markdown("---")
        
        budget_col1, budget_col2 = st.columns(2)
        
        with budget_col1:
            budget_percentage = (monthly_spend / user['monthly_income'] * 100) if user['monthly_income'] > 0 else 0
            st.metric("📊 Budget Used", f"{budget_percentage:.1f}%")
            if budget_percentage > 80:
                st.warning("⚠️ You've used over 80% of your monthly income!")
            elif budget_percentage > 50:
                st.info("💡 You've used over half your monthly budget.")
        
        with budget_col2:
            avg_co2_per_purchase = df['co2'].mean()
            st.metric("🌿 Avg CO₂/Purchase", f"{avg_co2_per_purchase:.2f} kg")
            if avg_co2_per_purchase < 3:
                st.success("🌟 Excellent! You're making low-impact choices!")
            elif avg_co2_per_purchase < 5:
                st.info("👍 Good job! Keep choosing eco-friendly options!")
        
        st.markdown("---")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("🌍 CO₂ Impact by Category")
            category_co2 = df.groupby('category')['co2'].sum().sort_values(ascending=False)
            st.bar_chart(category_co2)
        
        with chart_col2:
            st.subheader("💵 Spending by Category")
            category_spend = df.groupby('category')['price'].sum().sort_values(ascending=False)
            st.bar_chart(category_spend)
        
        st.markdown("---")
        st.subheader("📋 Recent Purchases")
        display_df = df.sort_values('date', ascending=False).head(10)
        display_df = display_df[['date', 'category', 'brand', 'price', 'co2']]
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(display_df, use_container_width=True)
        
        if st.button("🗑️ Clear All Purchase Data"):
            st.session_state.purchases = []
            st.session_state.badges = set()
            st.rerun()
    
    else:
        st.info(f"👋 Hi {user['name']}! Start by adding your first purchase above to see your environmental impact in real-time!")
        st.markdown("## 🌱 Why Track Your Eco Impact?")
        st.markdown("""
        - 🌍 **Understand** your carbon footprint
        - 💚 **Make** better shopping choices
        - 🏆 **Earn** fun badges and achievements
        - 🌿 **Discover** eco-friendly alternatives
        - 📊 **Track** your progress over time
        """)
    
    st.markdown("---")
    st.markdown(f"*ShopImpact - Your friendly companion for sustainable shopping* 🌱 | Made with 💚 for {user['name']}")