import streamlit as st
import json

# --- 1. DATA VAULT ---
def load_all_accounts():
    try:
        with open("oakstone_users.json", "r") as file:
            return json.load(file)
    except:
        return {"111": {"name": "Bhavya Malik", "pin": "1234", "balance": 100000, "history": []}}

def save_all_accounts(all_data):
    with open("oakstone_users.json", "w") as file:
        json.dump(all_data, file)

# Initialize Session State to remember the user
if 'authenticated_user' not in st.session_state:
    st.session_state.authenticated_user = None

all_users = load_all_accounts()

# --- 2. THEME & UI ---
st.set_page_config(page_title="Oakstone Bank", page_icon="🏦")

# Permanent Obsidian Theme
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1A; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #262626; color: #FFFFFF; }
    h1, h2, h3 { color: #E0E0E0; }
    .stButton>button { border: 1px solid #E0E0E0; border-radius: 5px; color: #E0E0E0; }
    </style>
""", unsafe_allow_html=True)

def show_landing_page():
    st.title("🏦 Oakstone: Heritage Banking")
    st.markdown("""
    ---
    ### Welcome to the shade of the Oak.
    At **Oakstone**, we bridge the gap between traditional integrity and modern digital efficiency. 
    
    * **Secure:** Your assets are guarded by industry-standard encryption.
    * **Efficient:** Real-time balance updates and instant transaction logging.
    * **Legacy:** We don't just bank; we build financial histories.
    
    *Use the sidebar to access your vault or begin your journey with us.*
    """)

# Sidebar Navigation
st.sidebar.title("🏦 Oakstone Bank")
access_type = st.sidebar.radio("Navigate", ["Our Story", "Login", "Open New Account"])

# --- 3. LOGIC FLOW ---
if access_type == "Our Story":
    show_landing_page()

elif access_type == "Open New Account":
    st.subheader("Be a member of Oakstone")
    with st.container():
        new_name = st.text_input("Full Name")
        new_pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4)
        if st.button("Create My Account"):
            if new_name and len(new_pin) == 4:
                new_acc_num = str(len(all_users) + 111)
                all_users[new_acc_num] = {"name": new_name, "pin": new_pin, "balance": 100000, "history": []}
                save_all_accounts(all_users)
                st.success(f"Account Created! Your ID: {new_acc_num}")
            else:
                st.error("Please provide a valid name and a 4-digit PIN.")

elif access_type == "Login":
    st.subheader("Access Your Vault")
    
    # Check if user is logged in
    if st.session_state.authenticated_user is None:
        acc_num = st.text_input("Account Number")
        pin_input = st.text_input("PIN", type="password")

        if st.button("Authenticate"):
            if acc_num in all_users and pin_input == all_users[acc_num]["pin"]:
                st.session_state.authenticated_user = acc_num
                st.rerun()
            else:
                st.error("Invalid Account Number or PIN.")
    
    # If logged in, show the banking interface
    else:
        acc_num = st.session_state.authenticated_user
        user = all_users[acc_num]
        
        # Logout button logic
        if st.button("Logout"):
            st.session_state.authenticated_user = None
            st.rerun()
            
        st.success(f"Welcome back, {user['name']}!")
        
        tab1, tab2, tab3 = st.tabs(["Dashboard", "Payments", "Statement"])
        
        with tab1:
            st.header("Account Overview")
            st.metric("Current Balance", f"₹{user['balance']}")

        with tab2:
            amt = st.number_input("Enter Amount", min_value=0)
            col1, col2 = st.columns(2)
            if col1.button("Withdraw"):
                if 0 < amt <= user['balance']:
                    user['balance'] -= amt
                    user['history'].append(f"Withdrew ₹{amt}")
                    save_all_accounts(all_users)
                    st.rerun()
                else:
                    st.error("Insufficient Funds!")
            if col2.button("Deposit"):
                user['balance'] += amt
                user['history'].append(f"Deposited ₹{amt}")
                save_all_accounts(all_users)
                st.rerun()

        with tab3:
            st.subheader("Transaction History")
            for h in reversed(user['history']):
                st.text(f"• {h}")
