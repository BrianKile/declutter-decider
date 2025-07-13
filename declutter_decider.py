
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time

NOTION_TOKEN = "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"
NOTION_DATABASE_ID = "22fd31277a9b8096be0ff5197e6cac4d"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def add_to_notion(item, category, room, capsule, score, decision, memory, date_str):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": { "database_id": NOTION_DATABASE_ID },
        "properties": {
            "Item": { "title": [{ "text": { "content": item } }] },
            "Category": { "select": { "name": category } },
            "Room": { "select": { "name": room } },
            "Capsule": { "rich_text": [{ "text": { "content": capsule } }] },
            "Score": { "number": score },
            "Decision": { "select": { "name": decision } },
            "Date": { "date": { "start": date_str } },
            "Memory": { "rich_text": [{ "text": { "content": memory } }] }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200 or response.status_code == 201

st.title("🧹 Declutter Decider v2")

st.sidebar.header("🕒 15-Min Declutter Challenge")
start_challenge = st.sidebar.button("Start Challenge")
if start_challenge:
    st.session_state['challenge_start'] = time.time()
    st.session_state['challenge_items'] = 0

if 'challenge_start' in st.session_state:
    elapsed = time.time() - st.session_state['challenge_start']
    remaining = max(0, 900 - elapsed)
    st.sidebar.write(f"⏱️ Time left: {int(remaining // 60)}m {int(remaining % 60)}s")
    st.sidebar.write(f"📦 Items logged: {st.session_state['challenge_items']}")

st.header("Log an Item")
item = st.text_input("Item name")
category = st.selectbox("Category", ['Supplies', 'Spare Parts', 'Memory', 'Collectible', 'Tool', 'Decor', 'Personal', 'Functional'])
room = st.selectbox("Room", ['Kitchen', 'Lanai', 'Playroom', "Banning's Bedroom", "Finley's Bedroom", 'Master Bedroom', 'Family Room', 'Living Room'])
capsule = st.text_input("Capsule Collection (optional)")
memory = st.text_area("Memory / Sentimental Note (optional)")

q1 = st.checkbox("Used in last 6 months?")
q2 = st.checkbox("Would buy again today?")
q3 = st.checkbox("Fits a real plan or purpose?")
q4 = st.checkbox("Would miss it if gone?")
q5 = st.checkbox("Improves space, time, or peace?")

score = sum([q1, q2, q3, q4, q5])
if score >= 4:
    decision = "✅ Keep"
elif 2 <= score <= 3:
    decision = "🤔 Re-evaluate"
else:
    decision = "🚮 Toss"

st.subheader(f"Suggested Decision: {decision}")

if st.button("Log this decision"):
    if item:
        date_str = datetime.now().isoformat()
        success = add_to_notion(item, category, room, capsule, score, decision, memory, date_str)
        if success:
            st.success("✅ Item logged to Notion!")
            if 'challenge_start' in st.session_state:
                st.session_state['challenge_items'] += 1
        else:
            st.error("❌ Failed to log item. Check Notion settings.")
    else:
        st.warning("Please enter an item name.")
