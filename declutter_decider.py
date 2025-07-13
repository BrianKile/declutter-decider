import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize the item log if not already present
if 'declutter_log' not in st.session_state:
    st.session_state['declutter_log'] = []

# App title
st.title("🧹 Declutter Decider")

# Item input
st.header("Step 1: Enter an Item")
item_name = st.text_input("What's the item?", "")
category = st.selectbox("Category", ["Functional", "Personal", "Decor/Storage", "Aspirational"])

# Step 2: 5-point test
st.header("Step 2: 5-Point Decision Test")
q1 = st.checkbox("Have you used it in the last 6 months?")
q2 = st.checkbox("Would you buy it again today for full price?")
q3 = st.checkbox("Does it serve a current purpose or fit a real plan?")
q4 = st.checkbox("Would you miss it if it disappeared?")
q5 = st.checkbox("Does it improve your space, time, or peace of mind?")

# Calculate score
score = sum([q1, q2, q3, q4, q5])

# Step 3: Recommendation
st.header("Step 3: Recommendation")
if score >= 4:
    recommendation = "✅ Keep"
elif 2 <= score <= 3:
    recommendation = "🤔 Re-evaluate (Sell or Donate)"
else:
    recommendation = "🚮 Toss or Give Away"

if item_name:
    st.subheader(f"Recommendation for **{item_name}**: {recommendation}")

    if st.button("Log This Decision"):
        # Add item to log
        st.session_state['declutter_log'].append({
            "Item": item_name,
            "Category": category,
            "Score": score,
            "Decision": recommendation,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        st.success("Item logged!")
        st.experimental_rerun()

# Step 4: View Decision Log
st.header("📋 Decision Log")
if st.session_state['declutter_log']:
    df = pd.DataFrame(st.session_state['declutter_log'])
    st.dataframe(df)
else:
    st.write("No items logged yet.")

# Export to CSV
if st.session_state['declutter_log']:
    df = pd.DataFrame(st.session_state['declutter_log'])
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Log as CSV",
        data=csv,
        file_name='declutter_log.csv',
        mime='text/csv'
    )
