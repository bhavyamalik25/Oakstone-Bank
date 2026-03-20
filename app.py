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

# Initialize Session State
if 'authenticated_user' not in st.session_state:
    st.session_state.authenticated_user = None

all_users = load_all_accounts()

# --- 2. THEME & UI ---
st.set_page_config(page_title="Oakstone Bank", page_icon="🏦", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap');

    /* Base */
    .stApp {
        background-color: #F5F0E8;
        color: #3B3530;
        font-family: 'Jost', sans-serif;
        font-weight: 300;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #EDE6D6;
        border-right: 1px solid #D6CBBA;
    }
    [data-testid="stSidebar"] * {
        color: #3B3530 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-family: 'Jost', sans-serif;
        font-weight: 300;
        letter-spacing: 0.08em;
        font-size: 0.85rem;
        text-transform: uppercase;
        color: #6B5E52 !important;
    }

    /* Headings */
    h1, h2, h3, h4 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 400;
        color: #3B3530 !important;
        letter-spacing: 0.03em;
    }
    h1 { font-size: 2.8rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }

    /* Subheader override */
    .stSubheader, [data-testid="stHeading"] {
        font-family: 'Cormorant Garamond', serif !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: transparent;
        border: 1px solid #9C8672;
        border-radius: 0px;
        color: #6B5E52;
        font-family: 'Jost', sans-serif;
        font-weight: 400;
        font-size: 0.78rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        padding: 0.55rem 1.6rem;
        transition: all 0.25s ease;
    }
    .stButton > button:hover {
        background-color: #9C8672;
        color: #F5F0E8;
        border-color: #9C8672;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #EDE6D6;
        border: none;
        border-bottom: 1px solid #C4B8A8;
        border-radius: 0px;
        color: #3B3530;
        font-family: 'Jost', sans-serif;
        font-weight: 300;
        font-size: 0.92rem;
        padding: 0.5rem 0.3rem;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-bottom: 1px solid #9C8672;
        box-shadow: none;
    }
    .stTextInput label, .stNumberInput label {
        font-family: 'Jost', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #9C8672 !important;
        font-weight: 400;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 1px solid #D6CBBA;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        color: #9C8672;
        font-family: 'Jost', sans-serif;
        font-size: 0.75rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        font-weight: 400;
        padding: 0.6rem 1.4rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #3B3530 !important;
        border-bottom: 2px solid #9C8672 !important;
    }

    /* Metric */
    [data-testid="stMetric"] {
        background-color: #EDE6D6;
        border: 1px solid #D6CBBA;
        padding: 1.5rem 2rem;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Jost', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #9C8672 !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 2.4rem !important;
        color: #3B3530 !important;
        font-weight: 400;
    }

    /* Alerts */
    .stSuccess, .stError {
        border-radius: 0px;
        font-family: 'Jost', sans-serif;
        font-size: 0.85rem;
        letter-spacing: 0.04em;
    }
    .stSuccess {
        background-color: #E8E2D5;
        border-left: 3px solid #9C8672;
        color: #3B3530;
    }
    .stError {
        background-color: #EDE0D4;
        border-left: 3px solid #C4896A;
        color: #3B3530;
    }

    /* Divider */
    hr { border-color: #D6CBBA; }

    /* Sidebar title */
    .sidebar-brand {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.4rem;
        font-weight: 400;
        letter-spacing: 0.12em;
        color: #3B3530;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }
    .sidebar-tagline {
        font-family: 'Jost', sans-serif;
        font-size: 0.68rem;
        letter-spacing: 0.2em;
        color: #9C8672;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }

    /* Transaction items */
    .txn-item {
        font-family: 'Jost', sans-serif;
        font-size: 0.85rem;
        font-weight: 300;
        color: #6B5E52;
        padding: 0.6rem 0;
        border-bottom: 1px solid #E8E2D5;
        letter-spacing: 0.04em;
    }

    /* Account ID display */
    .account-id {
        font-family: 'Jost', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 0.2em;
        color: #9C8672;
        text-transform: uppercase;
    }

    /* Welcome text */
    .welcome-name {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.6rem;
        font-weight: 300;
        font-style: italic;
        color: #6B5E52;
    }

    /* Hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)


# --- LANDING PAGE ---
def show_landing_page():
    st.markdown("<h1>Oakstone</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-family: Cormorant Garamond, serif; font-size: 1.15rem; font-style: italic; color: #9C8672; letter-spacing: 0.06em; margin-top: -0.8rem;'>
        Heritage Banking, Refined for Today
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <p style='font-family: Jost, sans-serif; font-size: 0.92rem; font-weight: 300; color: #6B5E52; line-height: 1.9; letter-spacing: 0.04em;'>
        At Oakstone, we bridge the timeless values of traditional integrity with the clarity of modern digital banking.
        Your wealth, your legacy — held with the quiet confidence of the oak.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='border-top: 2px solid #9C8672; padding-top: 1rem;'>
            <p style='font-family: Cormorant Garamond, serif; font-size: 1.1rem; color: #3B3530; margin-bottom: 0.3rem;'>Secure</p>
            <p style='font-family: Jost, sans-serif; font-size: 0.78rem; font-weight: 300; color: #9C8672; line-height: 1.7;'>Industry-standard encryption guards every asset.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='border-top: 2px solid #C4B8A8; padding-top: 1rem;'>
            <p style='font-family: Cormorant Garamond, serif; font-size: 1.1rem; color: #3B3530; margin-bottom: 0.3rem;'>Efficient</p>
            <p style='font-family: Jost, sans-serif; font-size: 0.78rem; font-weight: 300; color: #9C8672; line-height: 1.7;'>Real-time balances and instant transaction logging.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='border-top: 2px solid #D6CBBA; padding-top: 1rem;'>
            <p style='font-family: Cormorant Garamond, serif; font-size: 1.1rem; color: #3B3530; margin-bottom: 0.3rem;'>Legacy</p>
            <p style='font-family: Jost, sans-serif; font-size: 0.78rem; font-weight: 300; color: #9C8672; line-height: 1.7;'>We don't just bank — we build financial histories.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-family: Jost, sans-serif; font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase; color: #C4B8A8;'>
        Use the sidebar to access your vault or begin your journey with us.
    </p>
    """, unsafe_allow_html=True)


# --- SIDEBAR ---
st.sidebar.markdown("""
    <div class='sidebar-brand'>🏦 Oakstone</div>
    <div class='sidebar-tagline'>Private Banking</div>
    <hr style='border-color: #D6CBBA; margin-bottom: 1.2rem;'>
""", unsafe_allow_html=True)

access_type = st.sidebar.radio("", ["Our Story", "Login", "Open New Account"])


# --- 3. LOGIC FLOW ---
if access_type == "Our Story":
    show_landing_page()

elif access_type == "Open New Account":
    st.markdown("<h2>Begin Your Journey</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-family: Jost, sans-serif; font-size: 0.8rem; letter-spacing: 0.1em; text-transform: uppercase; color: #9C8672; margin-bottom: 1.5rem;'>
        Open a new Oakstone account
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    with st.container():
        new_name = st.text_input("Full Name")
        new_pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Create My Account"):
            if new_name and len(new_pin) == 4:
                new_acc_num = str(len(all_users) + 111)
                all_users[new_acc_num] = {"name": new_name, "pin": new_pin, "balance": 100000, "history": []}
                save_all_accounts(all_users)
                st.success(f"Account created. Your Account ID: {new_acc_num}")
            else:
                st.error("Please provide a valid name and a 4-digit PIN.")

elif access_type == "Login":
    if st.session_state.authenticated_user is None:
        st.markdown("<h2>Access Your Vault</h2>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        acc_num = st.text_input("Account Number")
        pin_input = st.text_input("PIN", type="password")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Authenticate"):
            if acc_num in all_users and pin_input == all_users[acc_num]["pin"]:
                st.session_state.authenticated_user = acc_num
                st.rerun()
            else:
                st.error("Invalid Account Number or PIN.")

    else:
        acc_num = st.session_state.authenticated_user
        user = all_users[acc_num]

        # Header row
        col_left, col_right = st.columns([3, 1])
        with col_left:
            st.markdown(f"<div class='welcome-name'>Welcome back, {user['name']}.</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='account-id'>Account No. {acc_num}</div>", unsafe_allow_html=True)
        with col_right:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Logout"):
                st.session_state.authenticated_user = None
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["Dashboard", "Payments", "Statement"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric("Current Balance", f"₹{user['balance']:,.2f}")

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            amt = st.number_input("Enter Amount", min_value=0)
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            if col1.button("Withdraw"):
                if 0 < amt <= user['balance']:
                    user['balance'] -= amt
                    user['history'].append(f"Withdrew ₹{amt:,.2f}")
                    save_all_accounts(all_users)
                    st.rerun()
                else:
                    st.error("Insufficient funds.")
            if col2.button("Deposit"):
                if amt > 0:
                    user['balance'] += amt
                    user['history'].append(f"Deposited ₹{amt:,.2f}")
                    save_all_accounts(all_users)
                    st.rerun()
                else:
                    st.error("Please enter a valid amount.")

        with tab3:
            st.markdown("<br>", unsafe_allow_html=True)
            if user['history']:
                for h in reversed(user['history']):
                    st.markdown(f"<div class='txn-item'>— {h}</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <p style='font-family: Jost, sans-serif; font-size: 0.82rem; color: #C4B8A8; font-style: italic; letter-spacing: 0.06em;'>
                    No transactions recorded yet.
                </p>
                """, unsafe_allow_html=True)
