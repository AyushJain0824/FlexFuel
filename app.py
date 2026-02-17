import streamlit as st
import google.generativeai as genai

# 1. Fetch the secret key you saved in Streamlit
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Page UI Setup
st.set_page_config(page_title="FlexFuel AI", page_icon="💪", layout="wide")
st.title("💪 FlexFuel AI: Your Personalized Coach")

# 3. Sidebar for Settings
with st.sidebar:
    st.header("Settings")
    goal = st.radio("Current Goal:", ["Bulk", "Cut"])
    diet = st.selectbox("Diet Type:", ["Non-Vegetarian", "Vegetarian", "Vegan"])
    budget = st.slider("Daily Budget (₹)", 100, 1000, 300)
    weight = st.number_input("Your Weight (kg):", value=70)

# 4. Dashboard Calculation
calories = weight * 32 if goal == "Bulk" else weight * 24
col1, col2 = st.columns(2)
col1.metric("Target Calories", f"{int(calories)} kcal")
col2.metric("Daily Budget", f"₹{budget}")

# --- THE UPDATED AI SECTION ---
st.subheader("💬 Chat with FlexAI")
user_input = st.text_input("Example: 'Suggest a high protein dinner for ₹150'", key="user_chat")

# Only run the AI if the user has typed something
if user_input:
    # Giving the AI clear context
    full_prompt = f"Coach, I am {weight}kg, my goal is to {goal}, my diet is {diet}, and my budget is ₹{budget}. User Question: {user_input}"
    
    try:
        with st.spinner('FlexAI is thinking...'):
            response = model.generate_content(full_prompt)
            if response.text:
                st.markdown(response.text)
            else:
                st.error("AI couldn't generate a response. Try rephrasing.")
    except Exception as e:
        st.error(f"Error: {e}")
