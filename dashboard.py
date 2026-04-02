import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
import hmac

# 1. PAGE SETUP
st.set_page_config(page_title="IAM SOC Dashboard", page_icon="🔒", layout="wide")

def check_password():
    def password_entered():
        if hmac.compare_digest(
            st.session_state["dashboard_password"], "Admin@123!"
        ):
            st.session_state["auth_ok"] = True
        else:
            st.session_state["auth_ok"] = False
            st.session_state["dashboard_password"] = ""

    if st.session_state.get("auth_ok", False):
        return True

    st.markdown("## 🔒 IAM SOC Dashboard")
    st.markdown("This dashboard is restricted to authorized administrators.")
    st.text_input(
        "Enter dashboard password",
        type="password",
        on_change=password_entered,
        key="dashboard_password"
    )
    if "auth_ok" in st.session_state and not st.session_state["auth_ok"]:
        st.error("Incorrect password.")
    return False

if not check_password():
    st.stop()

# 2. DATABASE LOGIC (Live - No Cache)
def get_data():
    conn = sqlite3.connect('users.db')
    # Note: Using password_hash to match your specific schema
    df = pd.read_sql_query("SELECT id, username, role, status, failed_attempts FROM users", conn)
    conn.close()
    return df

def perform_unlock(username):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("UPDATE users SET status='active', failed_attempts=0 WHERE username=?", (username,))
    conn.commit()
    success = cur.rowcount > 0
    conn.close()
    return success

# 3. SIDEBAR (Admin Controls)
with st.sidebar:
    st.title("🛡️ Admin Portal")
    if st.button("🔄 Force Refresh"):
        st.rerun()
    
    st.markdown("---")
    df = get_data()
    locked_users = df[df['status'] == 'locked']['username'].tolist()
    
    if locked_users:
        target = st.selectbox("Select user to unlock:", locked_users)
        if st.button("Confirm Unlock"):
            if perform_unlock(target):
                st.success(f"{target} is now Active.")
                st.rerun() # Refresh UI immediately
    else:
        st.info("No accounts currently locked.")

# 4. MAIN DASHBOARD (The "Vibe")
st.title("🔒 Identity Security Operations Center")

# KPI Cards
c1, c2, c3 = st.columns(3)
c1.metric("Total Identities", len(df))
c2.metric("Locked", len(df[df['status'] == 'locked']))
c3.metric("High Risk (Attempts > 2)", len(df[df['failed_attempts'] > 2]))

# Data Table with Highlighting
st.subheader("Real-Time Identity Registry")
def highlight_risk(row):
    return ['background-color: #721c24; color: white' if row.failed_attempts >= 3 else '' for _ in row]

st.dataframe(df.style.apply(highlight_risk, axis=1), use_container_width=True)

# Role Distribution (JML Visualization)
st.subheader("Identity Distribution by Role")
fig = px.bar(df['role'].value_counts(), labels={'value':'Count', 'index':'Role'}, color_discrete_sequence=['#00CC96'])
st.plotly_chart(fig)

# Audit Logs
st.subheader("📜 Recent Security Events")
if os.path.exists('audit.log'):
    with open('audit.log', 'r') as f:
        st.code("".join(f.readlines()[-10:]))