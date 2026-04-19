import streamlit as st
import json
from datetime import datetime

# ─────────────────────────────────────────────
# 1. DATA HELPERS
# ─────────────────────────────────────────────
def load_all_accounts():
    try:
        with open("oakstone_users.json", "r") as f:
            return json.load(f)
    except:
        return {
            "111": {
                "name": "Bhavya Malik",
                "pin": "1234",
                "balance": 100000,
                "history": []
            }
        }

def save_all_accounts(data):
    with open("oakstone_users.json", "w") as f:
        json.dump(data, f)

# Each transaction is now a dict:
# { "type": "credit"/"debit", "amount": 500, "desc": "Salary", "category": "Income", "date": "2024-06-01" }

def make_txn(txn_type, amount, desc, category):
    return {
        "type": txn_type,
        "amount": amount,
        "desc": desc,
        "category": category,
        "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
    }

# ─────────────────────────────────────────────
# 2. SESSION & PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Oakstone Bank", page_icon="🏦", layout="centered")

if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

all_users = load_all_accounts()

# ─────────────────────────────────────────────
# 3. STYLES — Navy/White banking palette
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* ── Base ── */
.stApp {
    background-color: #F0F4F8;
    color: #1A2332;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
}

/* ── Make main content use full width on mobile ── */
.block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-top: 1rem !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0F2044;
}
[data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 1rem;          /* bigger tap targets on mobile */
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #94A3B8 !important;
    padding: 0.4rem 0;        /* easier to tap */
}

/* ── Headings ── */
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600;
    color: #0F2044 !important;
}
h1 { font-size: 1.6rem !important; }   /* slightly smaller so it fits mobile */
h2 { font-size: 1.3rem !important; }
h3 { font-size: 1.05rem !important; }

/* ── Buttons — tall enough to tap comfortably ── */
.stButton > button {
    background-color: #1E40AF;
    border: none;
    border-radius: 8px;
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 1rem;          /* readable on small screens */
    letter-spacing: 0.03em;
    padding: 0.75rem 1.5rem;  /* min 48px height for touch */
    transition: background 0.2s ease;
    width: 100%;
    min-height: 48px;         /* Apple/Google touch target guideline */
}
.stButton > button:hover {
    background-color: #1E3A8A;
    color: #FFFFFF;
}

/* ── Inputs — large enough to type on mobile ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    color: #1A2332;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;          /* prevents iOS auto-zoom (must be ≥16px) */
    padding: 0.65rem 0.85rem;
    min-height: 48px;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #1E40AF;
    box-shadow: 0 0 0 2px rgba(30, 64, 175, 0.15);
}
.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-size: 0.8rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #64748B !important;
    font-weight: 500;
}

/* ── Tabs — scrollable on small screens ── */
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent;
    border-bottom: 2px solid #E2E8F0;
    gap: 0;
    overflow-x: auto;         /* tabs scroll horizontally on mobile */
    -webkit-overflow-scrolling: touch;
    flex-wrap: nowrap;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border: none;
    color: #64748B;
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-weight: 500;
    padding: 0.75rem 1rem;    /* taller for touch */
    white-space: nowrap;      /* stop tab text wrapping */
    min-height: 44px;
}
.stTabs [aria-selected="true"] {
    color: #1E40AF !important;
    border-bottom: 2px solid #1E40AF !important;
}

/* ── Metric ── */
[data-testid="stMetric"] {
    background-color: #0F2044;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
}
[data-testid="stMetricLabel"] {
    font-size: 0.72rem;
    letter-spacing, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 4. LANDING PAGE
# ─────────────────────────────────────────────
def show_landing():
    st.markdown("<h1>Oakstone Bank</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#64748B; font-size:0.95rem; margin-top:-0.5rem; margin-bottom:1.5rem;'>
        Trusted banking, built for everyone.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    features = [
        ("🔒", "Secure", "PIN-protected accounts and encrypted local storage."),
        ("⚡", "Instant", "Real-time balance updates and live transfer receipts."),
        ("📊", "Insightful", "Spending chart and categorised transaction history."),
    ]
    for col, (icon, title, body) in zip([col1, col2, col3], features):
        with col:
            st.markdown(f"""
            <div class='card' style='text-align:center;'>
                <div style='font-size:1.6rem;'>{icon}</div>
                <div style='font-weight:600; font-size:0.95rem; margin:0.4rem 0 0.3rem;'>{title}</div>
                <div style='font-size:0.78rem; color:#64748B; line-height:1.6;'>{body}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Use the sidebar to log in or open a new account.")


# ─────────────────────────────────────────────
# 5. SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.markdown("""
<div class='sb-brand'>🏦 Oakstone</div>
<div class='sb-tag'>Private Banking</div>
<hr style='border-color:#1E3A8A; margin-bottom:1rem;'>
""", unsafe_allow_html=True)

page = st.sidebar.radio("", ["Home", "Login", "Open Account"])


# ─────────────────────────────────────────────
# 6. PAGE ROUTING
# ─────────────────────────────────────────────

# ── HOME ──
if page == "Home":
    show_landing()


# ── OPEN ACCOUNT ──
elif page == "Open Account":
    st.markdown("<h2>Open a New Account</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    new_name = st.text_input("Full Name")
    new_pin  = st.text_input("Choose a 4-Digit PIN", type="password", max_chars=4)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Create Account"):
        if new_name and len(new_pin) == 4 and new_pin.isdigit():
            new_id = str(int(max(all_users.keys())) + 1)
            all_users[new_id] = {
                "name": new_name,
                "pin":  new_pin,
                "balance": 100000,
                "history": []
            }
            save_all_accounts(all_users)
            st.success(f"✅ Account created! Your Account Number is **{new_id}**. Please save it.")
        else:
            st.error("Enter a valid name and a 4-digit numeric PIN.")


# ── LOGIN & DASHBOARD ──
elif page == "Login":

    # ── Not logged in: show login form ──
    if st.session_state.authenticated_user is None:
        st.markdown("<h2>Login to Your Account</h2>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Login"):
            if acc in all_users and pin == all_users[acc]["pin"]:
                st.session_state.authenticated_user = acc
                st.rerun()
            else:
                st.error("Incorrect account number or PIN.")

    # ── Logged in: show dashboard ──
    else:
        acc  = st.session_state.authenticated_user
        user = all_users[acc]

        # Welcome strip + logout
        col_l, col_r = st.columns([4, 1])
        with col_l:
            st.markdown(f"""
            <div class='welcome-strip'>
                <div class='name'>Hello, {user['name']} 👋</div>
                <div class='sub'>Account No. {acc} &nbsp;|&nbsp; Oakstone Private Banking</div>
            </div>
            """, unsafe_allow_html=True)
        with col_r:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("Logout"):
                st.session_state.authenticated_user = None
                st.rerun()

        # ── TABS ──
        tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Deposit / Withdraw", "Transfer", "History"])


        # ══ TAB 1 – DASHBOARD ══
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric("Available Balance", f"₹{user['balance']:,.2f}")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Recent activity")

            history = user["history"]

            if not history:
                st.markdown("<p style='color:#94A3B8; font-size:0.85rem;'>No transactions yet.</p>", unsafe_allow_html=True)
            else:
                # Show last 5 as a quick summary
                recent = list(reversed(history))[:5]
                for txn in recent:
                    # Support old string-format history entries gracefully
                    if isinstance(txn, str):
                        st.markdown(f"<div class='txn-row'><span>{txn}</span></div>", unsafe_allow_html=True)
                        continue

                    sign  = "+" if txn["type"] == "credit" else "−"
                    cls   = "txn-credit" if txn["type"] == "credit" else "txn-debit"
                    label = txn.get("desc", txn["category"])
                    st.markdown(f"""
                    <div class='txn-row'>
                        <div>
                            <div style='font-weight:500;'>{label}</div>
                            <div style='font-size:0.75rem; color:#94A3B8;'>{txn.get('category','')} · {txn.get('date','')}</div>
                        </div>
                        <span class='{cls}'>{sign}₹{txn['amount']:,.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Simple spending bar chart ──
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### Spending by category")

                # Tally debits by category
                from collections import defaultdict
                cat_totals = defaultdict(float)
                for txn in history:
                    if isinstance(txn, dict) and txn["type"] == "debit":
                        cat_totals[txn.get("category", "Other")] += txn["amount"]

                if cat_totals:
                    # st.bar_chart expects a dict or DataFrame
                    st.bar_chart(cat_totals)
                else:
                    st.markdown("<p style='color:#94A3B8; font-size:0.85rem;'>No spending data yet.</p>", unsafe_allow_html=True)


        # ══ TAB 2 – DEPOSIT / WITHDRAW ══
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)

            CATEGORIES = ["Food & Dining", "Shopping", "Bills & Utilities", "Transport", "Healthcare", "Entertainment", "Income", "Other"]

            amount   = st.number_input("Amount (₹)", min_value=0.0, step=100.0, format="%.2f")
            note     = st.text_input("Description (optional)", placeholder="e.g. Grocery run")
            category = st.selectbox("Category", CATEGORIES)

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                if st.button("⬇ Withdraw"):
                    if amount <= 0:
                        st.error("Enter an amount greater than 0.")
                    elif amount > user["balance"]:
                        st.error("Insufficient balance.")
                    else:
                        user["balance"] -= amount
                        user["history"].append(make_txn("debit", amount, note or f"Withdrawal – {category}", category))
                        save_all_accounts(all_users)
                        st.success(f"₹{amount:,.2f} withdrawn.")
                        st.rerun()

            with col2:
                if st.button("⬆ Deposit"):
                    if amount <= 0:
                        st.error("Enter an amount greater than 0.")
                    else:
                        user["balance"] += amount
                        user["history"].append(make_txn("credit", amount, note or f"Deposit – {category}", category))
                        save_all_accounts(all_users)
                        st.success(f"₹{amount:,.2f} deposited.")
                        st.rerun()


        # ══ TAB 3 – TRANSFER ══
        with tab3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class='card' style='border-left: 4px solid #1E40AF;'>
                <b>How it works:</b> Enter the recipient's Oakstone account number and the amount.
                Both accounts update instantly.
            </div>
            """, unsafe_allow_html=True)

            recipient_id = st.text_input("Recipient Account Number")
            transfer_amt = st.number_input("Amount to Transfer (₹)", min_value=0.0, step=100.0, format="%.2f", key="tf_amt")
            transfer_note = st.text_input("Note (optional)", placeholder="e.g. Rent for June", key="tf_note")

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Send Money →"):
                if recipient_id == acc:
                    st.error("You cannot transfer to your own account.")
                elif recipient_id not in all_users:
                    st.error("Recipient account not found.")
                elif transfer_amt <= 0:
                    st.error("Enter a valid transfer amount.")
                elif transfer_amt > user["balance"]:
                    st.error("Insufficient balance.")
                else:
                    recipient = all_users[recipient_id]

                    # Debit sender
                    user["balance"] -= transfer_amt
                    user["history"].append(make_txn(
                        "debit", transfer_amt,
                        transfer_note or f"Transfer to {recipient['name']}",
                        "Transfer"
                    ))

                    # Credit recipient
                    recipient["balance"] += transfer_amt
                    recipient["history"].append(make_txn(
                        "credit", transfer_amt,
                        transfer_note or f"Transfer from {user['name']}",
                        "Transfer"
                    ))

                    save_all_accounts(all_users)
                    st.success(f"✅ ₹{transfer_amt:,.2f} sent to **{recipient['name']}** (Acc. {recipient_id}).")
                    st.rerun()


        # ══ TAB 4 – HISTORY ══
        with tab4:
            st.markdown("<br>", unsafe_allow_html=True)

            history = user["history"]
            if not history:
                st.markdown("<p style='color:#94A3B8; font-size:0.85rem;'>No transaction history yet.</p>", unsafe_allow_html=True)
            else:
                for txn in reversed(history):
                    # Gracefully handle old string entries
                    if isinstance(txn, str):
                        st.markdown(f"<div class='txn-row'><span>{txn}</span></div>", unsafe_allow_html=True)
                        continue

                    sign = "+" if txn["type"] == "credit" else "−"
                    cls  = "txn-credit" if txn["type"] == "credit" else "txn-debit"

                    st.markdown(f"""
                    <div class='txn-row'>
                        <div>
                            <div style='font-weight:500; font-size:0.9rem;'>{txn.get('desc', '')}</div>
                            <div style='font-size:0.75rem; color:#94A3B8;'>{txn.get('category','')} · {txn.get('date','')}</div>
                        </div>
                        <span class='{cls}' style='font-size:0.95rem;'>{sign}₹{txn['amount']:,.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
