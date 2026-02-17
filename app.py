import streamlit as st
import google.generativeai as genai

# 1. BRAIN SETUP: Securely fetch the API key from your Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key not found. Please add GEMINI_API_KEY to your Streamlit Secrets.")

# 2. UI DESIGN
st.set_page_config(page_title="FlexFuel AI", page_icon="💪", layout="wide")
st.title("💪 FlexFuel AI: Your Personalized Coach")

# 3. SIDEBAR: User Profile
with st.sidebar:
    st.header("⚙️ Profile Settings")
    goal = st.radio("Current Goal:", ["Bulk", "Cut"])
    diet = st.selectbox("Diet Type:", ["Non-Vegetarian", "Vegetarian", "Vegan"])
    budget = st.slider("Daily Budget (₹)", 100, 2000, 300)
    weight = st.number_input("Your Weight (kg):", min_value=30, max_value=200, value=70)

# 4. DASHBOARD: Calculations
calories = weight * 32 if goal == "Bulk" else weight * 24

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Target Calories", f"{int(calories)} kcal")
with col2:
    st.metric("Daily Budget", f"₹{budget}")
with col3:
    st.metric("Diet Mode", diet)

# 5. AI CHAT: The Coach
st.divider()
st.subheader("💬 Chat with FlexAI")
user_input = st.text_input("Example: 'Give me a high protein lunch for ₹150'", key="user_chat")

if user_input:
    full_prompt = f"Coach, I am {weight}kg, my goal is {goal}, my diet is {diet}, and my budget is ₹{budget}. Question: {user_input}"
    
    try:
        with st.spinner('FlexAI is thinking...'):
            response = model.generate_content(full_prompt)
            if response.text:
                st.markdown("### 🥗 Coach's Recommendation")
                st.write(response.text)
    except Exception as e:
        st.error(f"FlexAI is having trouble. Please check if your API Key is valid in Secrets.")

# 6. SUPPLEMENT TIPS
st.divider()
st.subheader("💊 Quick Supplement Guide")
st.info("Don't forget to stay hydrated and prioritize 7-8 hours of sleep for muscle recovery!")
