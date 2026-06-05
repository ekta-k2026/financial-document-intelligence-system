import streamlit as st
import pandas as pd
import plotly.express as px
from fintech.pdf_report_generator import (
    generate_pdf_report
)





from fintech.fraud_detection import (
    detect_suspicious_transactions,
    detect_spending_spikes,
    detect_recurring_transactions,
    generate_fraud_explanations,
    calculate_financial_risk_score
)












def render_dashboard(df, kpis):

    st.divider()

    st.header("📊 Financial Analytics Dashboard")
    

    # ---------------- KPI CARDS ----------------
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "💰 Income",
        f"₹{kpis['Total Income']:,}"
    )

    col2.metric(
        "💸 Expenses",
        f"₹{kpis['Total Expenses']:,}"
    )

    col3.metric(
        "📈 Net Cash Flow",
        f"₹{kpis['Net Cash Flow']:,}"
    )

    col4.metric(
        "⚠️ Suspicious",
        kpis["Suspicious Transactions"]
    )

    col5.metric(
        "🔥 Largest Expense",
        kpis["Largest Expense"]
    )
    st.divider()

    # ---------------- EXPENSE PIE CHART ----------------
    expense_df = df[
        df["Type"].str.lower() == "debit"
    ]

    category_spending = (
        expense_df.groupby("AI_Category")["Amount"]
        .sum()
        .reset_index()
    )

    pie_chart = px.pie(
        category_spending,
        names="AI_Category",
        values="Amount",
        title="Expense Distribution"
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )
    st.divider()

    # ---------------- INCOME VS EXPENSE ----------------
    comparison_df = pd.DataFrame({
        "Type": ["Income", "Expenses"],
        "Amount": [
            kpis["Total Income"],
            kpis["Total Expenses"]
        ]
    })

    bar_chart = px.bar(
        comparison_df,
        x="Type",
        y="Amount",
        title="Income vs Expenses"
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )
    st.divider()

    # ---------------- SUSPICIOUS TRANSACTIONS ----------------
    suspicious_df = df[
        df["Category"]
        .astype(str)
        .str.lower()
        .str.contains("suspicious")
    ]

    if not suspicious_df.empty:

        st.subheader(
            "🚨 Suspicious Transactions"
        )

        st.dataframe(suspicious_df)
        st.divider()

    # ---------------- BALANCE TREND ----------------
    if "Date" in df.columns:

        trend_chart = px.line(
            df,
            x="Date",
            y="Balance",
            title="Account Balance Trend",
            markers=True
        )

        st.plotly_chart(
            trend_chart,
            use_container_width=True
        )
        st.divider()

    # ---------------- HIGH VALUE TRANSACTIONS ----------------
    high_value_df = df[
        df["Amount"] >= 10000
    ]

    if not high_value_df.empty:

        st.subheader(
            "💎 High Value Transactions"
        )

        st.dataframe(high_value_df)
        
    # ---------------- FRAUD DETECTION ----------------
    st.subheader("🚨 Fraud Detection Engine")

    fraud_df = detect_suspicious_transactions(df)

    if not fraud_df.empty:

        st.error(
            f"⚠️ {len(fraud_df)} suspicious transactions detected"
        )

        st.dataframe(fraud_df)

    else:

        st.success(
            "✅ No suspicious transactions detected"
        )
    
    # ---------------- SPENDING SPIKES ----------------
    st.subheader("📈 Spending Spike Detection")

    spike_df = detect_spending_spikes(df)

    if not spike_df.empty:

        st.warning(
            f"⚠️ {len(spike_df)} unusual spending spikes detected"
        )

        st.dataframe(spike_df)

    else:

        st.success(
            "✅ No abnormal spending spikes detected"
        )
    
    # ---------------- RECURRING TRANSACTIONS ----------------
    st.subheader("🔁 Recurring Transaction Intelligence")

    recurring_df = detect_recurring_transactions(df)

    if not recurring_df.empty:

        st.info(
            f"ℹ️ {len(recurring_df)} recurring transaction patterns detected"
        )

        st.dataframe(recurring_df)

    else:

        st.success(
            "✅ No recurring transaction patterns detected"
        )
    
    # ---------------- AI FRAUD EXPLANATIONS ----------------
    st.subheader("🧠 AI Fraud Explanations")

    explanation_df = generate_fraud_explanations(df)

    if not explanation_df.empty:

        st.warning(
            f"⚠️ {len(explanation_df)} transactions require review"
        )

        st.dataframe(explanation_df)

    else:

        st.success(
            "✅ No fraud explanations generated"
        )
    
    # ---------------- AI RISK ENGINE ----------------
    st.subheader("🛡️ AI Financial Risk Engine")

    risk_result = calculate_financial_risk_score(
        df,
        kpis
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Risk Score",
            f"{risk_result['Risk Score']}/100"
        )

    with col2:

        st.metric(
            "Risk Level",
            risk_result["Risk Level"]
        )

    # -------- RISK VISUALIZATION --------
    st.progress(
        risk_result["Risk Score"] / 100
    )
    # ---------------- PDF REPORT ----------------
    pdf_file = generate_pdf_report(
        kpis,
        risk_result
)

    with open(pdf_file, "rb") as file:

     st.download_button(
        label="📄 Download PDF Report",
        data=file,
        file_name="financial_report.pdf",
        mime="application/pdf"
    )





