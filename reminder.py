import streamlit as st
import calendar
import datetime
import json
import os
import pandas as pd

st.set_page_config(page_title="Reminder App", layout="centered")
st.title("Monthly Calendar & Reminder App")

# Hide Streamlit branding elements
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.markdown("""
    <style>
    html, body, [class*="st-"] {
        font-family: 'Segoe UI', sans-serif;
    }

    .stButton > button {
        border-radius: 10px;
        padding: 0.5rem 1rem;
        background-color: #0099ff;
        color: white;
        font-weight: 500;
    }

    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #d0eaff;
    }

    .stNumberInput input {
        border-radius: 6px;
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    .stMarkdown h3 {
        color: #006bb3;
    }

    .stApp {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)


# ---------- Config ----------
REMINDER_FILE = "reminders.json"

# ---------- Utils ----------
def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reminders(data):
    with open(REMINDER_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Streamlit App ----------


# Today's date
today = datetime.date.today()

# Sidebar: Year & Month selection
year = st.sidebar.number_input("Select Year", value=today.year, min_value=2000, max_value=2100)
month_name = st.sidebar.selectbox("Select Month", list(calendar.month_name)[1:], index=today.month - 1)
month_index = list(calendar.month_name).index(month_name)

# Calendar grid using DataFrame
st.markdown(f"### {month_name} {year}")

# Get raw matrix and clean
month_matrix = calendar.monthcalendar(year, month_index)

# Get today's info
today = datetime.date.today()
is_current_month = today.year == year and today.month == month_index

# Weekday headers
st.markdown("<div style='display: flex; justify-content: space-between; font-weight: bold;'>"
            + "".join(f"<div style='width: 13%; text-align: center;'>{day}</div>" for day in ['Mo','Tu','We','Th','Fr','Sa','Su'])
            + "</div>", unsafe_allow_html=True)

# Render grid
for week in month_matrix:
    cols = st.columns(7)
    for i, day in enumerate(week):
        with cols[i]:
            if day == 0:
                st.markdown(" ")
            else:
                is_today = (is_current_month and day == today.day)
                st.markdown(
                    f"""
                    <div style="
                        text-align: center;
                        padding: 10px;
                        margin: 2px;
                        border-radius: 10px;
                        background-color: {'#cceeff' if is_today else '#f2f2f2'};
                        border: 1px solid #d3d3d3;
                        font-weight: {'bold' if is_today else 'normal'};
                        color: {'#003366' if is_today else '#000000'};
                    ">
                        {day}
                    </div>
                    """, unsafe_allow_html=True)

# Day selection & formatting
selected_day = st.number_input("Select Day", min_value=1, max_value=31, value=today.day)
selected_date = f"{year}-{month_index:02d}-{selected_day:02d}"

# Load reminders
reminders = load_reminders()

# Add Reminder Form
st.markdown("### Add Reminder")
with st.form("add_reminder"):
    reminder_text = st.text_input("Enter your reminder:")
    submitted = st.form_submit_button("Add")
    if submitted:
        if selected_date not in reminders:
            reminders[selected_date] = []
        reminders[selected_date].append(reminder_text)
        save_reminders(reminders)
        st.success(f"✅ Reminder added for {selected_date}")

# Show Reminders for Selected Date
st.markdown(f"### Reminders on {selected_date}")
if selected_date in reminders and reminders[selected_date]:
    for i, r in enumerate(reminders[selected_date]):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"{i+1}. {r}")
        with col2:
            if st.button("❌", key=f"{selected_date}_{i}"):
                reminders[selected_date].pop(i)
                if not reminders[selected_date]:
                    del reminders[selected_date]
                save_reminders(reminders)
                st.experimental_rerun()
else:
    st.info("No reminders for this date.")

# Expandable section to show all reminders
with st.expander("📂 View All Saved Reminders"):
    if reminders:
        for date in sorted(reminders):
            st.write(f"📅 **{date}**")
            for r in reminders[date]:
                st.write(f"– {r}")
    else:
        st.write("No reminders saved.")
