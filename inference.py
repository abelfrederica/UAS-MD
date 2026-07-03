import streamlit as st
import pandas as pd
import joblib
import time

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Credit Score Prediction",
    page_icon="💳",
    layout="wide"
)

# =====================================================
# CUSTOM CSS (DARK MODE OPTIMIZED)
# =====================================================
st.markdown("""
<style>
/* Background Utama */
.stApp {
    background-color: #0F172A !important;
}

/* Menyembunyikan elemen bawaan Streamlit */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Judul Utama (Header) */
.main-title {
    background: linear-gradient(90deg, #1E40AF, #0369A1);
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 5px 25px rgba(0,0,0,0.4);
}
.main-title h1 {
    font-size: 42px;
    margin-bottom: 10px;
    color: #FFFFFF !important;
}
.main-title p {
    font-size: 18px;
    color: #E2E8F0 !important;
}

/* Kartu Penampung Form (Kontras Tinggi) */
.card {
    background-color: #1E293B !important;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 5px 18px rgba(0,0,0,0.3);
    margin-bottom: 20px;
    border: 1px solid #334155;
}

/* Memaksa teks input Streamlit berwarna putih agar kontras */
.card label, .card p, .card span {
    color: #F8FAFC !important;
}

/* Tombol Prediksi */
div.stButton > button {
    width: 100%;
    height: 60px;
    border: none;
    border-radius: 12px;
    background: #2563EB;
    color: #FFFFFF !important;
    font-size: 20px;
    font-weight: bold;
    transition: 0.3s;
    box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.4);
}
div.stButton > button:hover {
    background: #1D4ED8;
    color: #FFFFFF !important;
    box-shadow: 0px 4px 20px rgba(29, 78, 216, 0.6);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617 !important;
    border-right: 1px solid #1E293B;
}
section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD MODEL
# =====================================================
@st.cache_resource
def load_model():
    return joblib.load("best_model.pkl")

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"Gagal memuat model 'best_model.pkl'. Pastikan file berada di direktori yang sama. Error: {e}")

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.title("💳 Credit Score")
    st.markdown("---")
    st.write("""
    This application predicts a customer's credit score using a Machine Learning model.

    ### Credit Categories
    🟢 Good
    🟡 Standard
    🔴 Poor
    """)
    st.markdown("---")
    
    if model_loaded:
        st.success("✅ Model Loaded")
    else:
        st.error("❌ Model Missing")

    st.info("""
    Created using:
    • Streamlit
    • Scikit-Learn
    • Pandas
    """)

# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="main-title">
    <h1>💳 Credit Score Prediction System</h1>
    <p>Machine Learning Deployment using Streamlit</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# FORM INPUT
# =====================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("👤 Customer Information")
st.caption("Please fill all customer information below.")

col1, col2 = st.columns(2)

with col1:
    Age = st.number_input("Age", min_value=18, max_value=100, value=30)
    Occupation = st.selectbox("Occupation", [
        "Scientist", "Teacher", "Engineer", "Doctor", "Lawyer",
        "Media_Manager", "Manager", "Entrepreneur", "Mechanic",
        "Developer", "Writer", "Architect", "Musician", "Accountant", "Journalist"
    ])
    Annual_Income = st.number_input("Annual Income", value=50000.0)
    Monthly_Inhand_Salary = st.number_input("Monthly Inhand Salary", value=4000.0)
    Num_Bank_Accounts = st.number_input("Number of Bank Accounts", value=3)
    Num_Credit_Card = st.number_input("Number of Credit Cards", value=2)
    Interest_Rate = st.number_input("Interest Rate", value=8)
    Num_of_Loan = st.number_input("Number of Loans", value=2)
    Delay_from_due_date = st.number_input("Delay from Due Date", value=5)
    Num_of_Delayed_Payment = st.number_input("Delayed Payments", value=2)

with col2:
    Changed_Credit_Limit = st.number_input("Changed Credit Limit", value=5.0)
    Num_Credit_Inquiries = st.number_input("Credit Inquiries", value=2)
    Credit_Mix = st.selectbox("Credit Mix", ["Good", "Standard", "Bad"])
    Outstanding_Debt = st.number_input("Outstanding Debt", value=1000.0)
    Credit_Utilization_Ratio = st.number_input("Credit Utilization Ratio (%)", value=30.0)
    Credit_History_Age = st.number_input("Credit History Age (Months)", value=120)
    Payment_of_Min_Amount = st.selectbox("Payment of Minimum Amount", ["Yes", "No"])
    Total_EMI_per_month = st.number_input("Total EMI per Month", value=120.0)
    Amount_invested_monthly = st.number_input("Amount Invested Monthly", value=150.0)
    Payment_Behaviour = st.selectbox("Payment Behaviour", [
        "High_spent_Small_value_payments", "High_spent_Medium_value_payments",
        "High_spent_Large_value_payments", "Low_spent_Small_value_payments",
        "Low_spent_Medium_value_payments", "Low_spent_Large_value_payments"
    ])
    Monthly_Balance = st.number_input("Monthly Balance", value=400.0)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# DATAFRAME CREATION
# =====================================================
input_df = pd.DataFrame({
    "Age": [Age], "Occupation": [Occupation], "Annual_Income": [Annual_Income],
    "Monthly_Inhand_Salary": [Monthly_Inhand_Salary], "Num_Bank_Accounts": [Num_Bank_Accounts],
    "Num_Credit_Card": [Num_Credit_Card], "Interest_Rate": [Interest_Rate],
    "Num_of_Loan": [Num_of_Loan], "Delay_from_due_date": [Delay_from_due_date],
    "Num_of_Delayed_Payment": [Num_of_Delayed_Payment], "Changed_Credit_Limit": [Changed_Credit_Limit],
    "Num_Credit_Inquiries": [Num_Credit_Inquiries], "Credit_Mix": [Credit_Mix],
    "Outstanding_Debt": [Outstanding_Debt], "Credit_Utilization_Ratio": [Credit_Utilization_Ratio],
    "Credit_History_Age": [Credit_History_Age], "Payment_of_Min_Amount": [Payment_of_Min_Amount],
    "Total_EMI_per_month": [Total_EMI_per_month], "Amount_invested_monthly": [Amount_invested_monthly],
    "Payment_Behaviour": [Payment_Behaviour], "Monthly_Balance": [Monthly_Balance]
})

with st.expander("📋 Customer Input Summary"):
    st.dataframe(input_df, use_container_width=True)

st.write("")

# =====================================================
# PREDICTION LOGIC
# =====================================================
if st.button("🔍 Predict Credit Score", use_container_width=True):
    if model_loaded:
        with st.spinner("Analyzing customer data..."):
            time.sleep(1) 
            prediction = model.predict(input_df)[0]

        labels = {0: "Poor", 1: "Standard", 2: "Good"}
        result = labels.get(prediction, "Unknown")

        st.write("")
        st.markdown("---")
        st.subheader("🎯 Prediction Result")

        if result == "Good":
            color = "#10B981"  # Hijau Emerald cerah
            icon = "🟢"
            score_target = 0.90
            description = """
            The customer demonstrates excellent credit behavior.
            - **Low** financial risk
            - **High** repayment reliability
            - **Highly suitable** for credit approval
            """
        elif result == "Standard":
            color = "#F59E0B"  # Amber/Kuning cerah
            icon = "🟡"
            score_target = 0.60
            description = """
            The customer demonstrates average credit behavior.
            - **Moderate** financial risk
            - **Acceptable** repayment history
            - Credit approval requires **further consideration**
            """
        else:
            color = "#EF4444"  # Merah terang
            icon = "🔴"
            score_target = 0.25
            description = """
            The customer demonstrates poor credit behavior.
            - **High** financial risk
            - **Frequent** payment issues/delays
            - Credit approval is **not recommended**
            """

        # HTML Banner Result (Dipaksa warna teks putih)
        st.markdown(f"""
        <div style="
            background:{color};
            padding:30px;
            border-radius:20px;
            text-align:center;
            box-shadow:0px 8px 25px rgba(0,0,0,0.3);
            margin-top:20px;
        ">
            <h1 style="font-size:60px; margin:0;">{icon}</h1>
            <h2 style="color:#FFFFFF !important; margin:10px 0; font-weight:bold;">Predicted Credit Score</h2>
            <h1 style="font-size:46px; color:#FFFFFF !important; margin:0; font-weight:black;">{result}</h1>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.info(description)
        st.write("")

        # Progress Bar Indicator
        st.subheader("📊 Credit Quality Indicator")
        progress_bar = st.progress(0.0)
        
        for percent_complete in range(int(score_target * 100) + 1):
            time.sleep(0.01)
            progress_bar.progress(percent_complete / 100.0)
    else:
        st.error("Cannot make prediction because the machine learning model file is missing.")

# =====================================================
# CREDIT SCORE GUIDE
# =====================================================
st.write("")
st.markdown("---")
st.subheader("📘 Credit Score Categories Reference")

col1, col2, col3 = st.columns(3)
with col1:
    st.success("""
    ### 🟢 Good
    Excellent repayment behavior
    - ✔ Low risk
    - ✔ Stable financial condition
    - ✔ High creditworthiness
    """)
with col2:
    st.warning("""
    ### 🟡 Standard
    Average repayment behavior
    - ✔ Moderate risk
    - ✔ Requires monitoring
    - ✔ Fair creditworthiness
    """)
with col3:
    st.error("""
    ### 🔴 Poor
    Poor repayment behavior
    - ✔ High risk
    - ✔ Frequent payment delays
    - ✔ Low creditworthiness
    """)

# =====================================================
# FOOTER
# =====================================================
st.write("")
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#94A3B8; padding:10px;">
    <b>💳 Credit Score Prediction System</b><br>
    Machine Learning Deployment using Streamlit<br>
    <small style="color:#64748B;">Annabelle Frederica Suryana / 2802412351</small>
</div>
""", unsafe_allow_html=True)
