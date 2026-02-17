import streamlit as st
import google.generativeai as genai

# Setup the AI (We will add the key later)
st.set_page_config(page_title="FlexFuel AI", page_icon="💪")

# --- UI Design ---
st.title("💪 FlexFuel AI")
st.markdown("### Personalized Bulking & Cutting Coach")

# --- User Inputs ---
with st.sidebar:
    st.header("Profile Settings")
    goal = st.radio("Current Goal:", ["Bulk", "Cut"])
    diet = st.selectbox("Diet Type:", ["Non-Vegetarian", "Vegetarian", "Vegan"])
    budget = st.slider("Daily Budget (₹)", 100, 1000, 300)
    weight = st.number_input("Your Weight (kg):", value=70)

# --- Logic ---
calories = weight * 30 if goal == "Bulk" else weight * 22

# --- Dashboard Display ---
col1, col2 = st.columns(2)
col1.metric("Target Calories", f"{int(calories)} kcal")
col2.metric("Budget Limit", f"₹{budget}")

# --- AI Section ---
st.subheader("💬 Chat with FlexAI")
user_input = st.text_input("Ask about your diet or workout:")
if user_input:
    st.info(f"AI: Since you are {diet} and want to {goal}, I suggest focusing on high protein sources like {'Eggs' if diet == 'Non-Vegetarian' else 'Soya chunks'}.")
