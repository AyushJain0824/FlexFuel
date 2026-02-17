import streamlit as st
import google.generativeai as genai

# 1. BRAIN SETUP: Fetch the secret key from the Streamlit vault
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key not found. Please add GEMINI_API_KEY to your Streamlit Secrets.")

# 2. UI DESIGN: High-End Fitness Aesthetic
st.set_page_config(page_title="FlexFuel AI", page_icon="💪", layout="wide")

# Custom CSS for a darker, professional look
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 15px; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("💪 FlexFuel AI: Your Personalized Coach")
st.markdown("---")

# 3. SIDEBAR: User Profile & Goals
with st.sidebar:
    st.header("⚙️ Profile Settings")
    goal = st.radio("Current Goal:", ["Bulk", "Cut"])
    diet = st.selectbox("Diet Type:", ["Non-Vegetarian", "Vegetarian", "Vegan"])
    budget = st.slider("Daily Budget (₹)", 100, 2000, 300)
    weight = st.number_input("Your Weight (kg):", min_value=30, max_value=200, value=70)
    
    st.divider()
    st.info("Tip: Bulking requires more carbs, while Cutting requires higher protein density.")

# 4. DASHBOARD: Automated Calculations
# Simple calculation logic: Bulk (32 cal/kg) vs Cut (24 cal/kg)
calories = weight * 32 if goal == "Bulk" else weight * 24

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Target Calories", f"{int(calories)} kcal")
with col2:
    st.metric("Daily Budget", f"₹{budget}")
with col3:
    st.metric("Diet Mode", diet)

# 5. AI CHAT: The FlexAI Coach
st.divider()
st.subheader("💬 Chat with FlexAI")
st.write(f"Ask me anything about your {goal} plan or {diet} recipes!")

user_input = st.text_input("Example: 'Give me a high protein lunch for ₹150'", key="user_chat")

# Only trigger the AI if the user types something and presses Enter
if user_input:
    # Context ensures the AI knows the user's specifics immediately
    full_prompt = f"""
    You are an expert fitness coach and nutritionist. 
    Context: User weighs {weight}kg, Goal is to {goal}, Diet is {diet}, Budget is ₹{budget} per day.
    Question: {user_input}
    Provide a concise, helpful answer with specific food names and portion sizes.
    """
    
    try:
        with st.spinner('FlexAI is analyzing your request...'):
            response = model.generate_content(full_prompt)
            if response.text:
                st.markdown("### 🥗 Coach's Recommendation")
                st.write(response.text)
            else:
                st.warning("I couldn't generate a plan. Please try rephrasing your question.")
    except Exception as e:
        st.error(f"FlexAI encountered an error: {e}")

# 6. SUPPLEMENTS SECTION (Static advice based on Profile)
st.divider()
st.subheader("💊 Recommended Supplement Stack")
supp_col1, supp_col2 = st.columns(2)

with supp_col1:
    if diet == "Vegan" or diet == "Vegetarian":
        st.write("- **Vitamin B12:** Essential for plant-based athletes.")
        st.write("- **Creatine:** 5g daily to improve strength.")
    else:
        st.write("- **Whey Protein:** Convenient for hitting protein goals.")
        st.write("- **Creatine:** 5g daily for muscle volume.")

with supp_col2:
    if goal == "Cut":
        st.write("- **Caffeine/Pre-workout:** Helps maintain energy during low calories.")
        st.write("- **Multivitamins:** Ensures micronutrient coverage.")
    else:
        st.write("- **Mass Gainer (Optional):** If you struggle to eat enough.")
        st.write("- **Omega-3 Fish Oil:** For joint health during heavy lifting.")
