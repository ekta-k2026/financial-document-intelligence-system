
import pandas as pd


def detect_suspicious_transactions(df):

    suspicious = []

    suspicious_keywords = [
        "international",
        "crypto",
        "bitcoin",
        "unknown",
        "offshore",
        "wire",
        "transfer"
    ]

    for _, row in df.iterrows():

        description = str(
            row.get("Description", "")
        ).lower()

        amount = abs(
            float(row.get("Amount", 0))
        )

        risk_score = 0

        # -------- KEYWORD RISK --------
        for word in suspicious_keywords:

            if word in description:
                risk_score += 50

        # -------- HIGH VALUE RISK --------
        if amount > 50000:
            risk_score += 40

        elif amount > 20000:
            risk_score += 20

        # -------- FINAL FLAG --------
        if risk_score >= 50:

            suspicious.append({
                "Description": row.get(
                    "Description",
                    ""
                ),
                "Amount": amount,
                "Risk Score": risk_score
            })

    return pd.DataFrame(suspicious)

def detect_spending_spikes(df):

    debit_df = df[
        df["Type"].astype(str).str.lower() == "debit"
    ].copy()

    if debit_df.empty:
        return pd.DataFrame()

    avg_spending = debit_df["Amount"].mean()

    spike_threshold = avg_spending * 2

    spikes = debit_df[
        debit_df["Amount"] > spike_threshold
    ][[
        "Description",
        "Amount"
    ]].copy()

    spikes["Average Spending"] = round(
        avg_spending,
        2
    )

    spikes["Spike Level"] = round(
        spikes["Amount"] / avg_spending,
        2
    )

    return spikes

def detect_recurring_transactions(df):

    recurring = []

    grouped = df.groupby(
        "Description"
    ).size().reset_index(name="Count")

    recurring_df = grouped[
        grouped["Count"] >= 2
    ]

    for _, row in recurring_df.iterrows():

        recurring.append({
            "Description": row["Description"],
            "Occurrences": row["Count"]
        })

    return pd.DataFrame(recurring)

def generate_fraud_explanations(df):

    explanations = []

    suspicious_keywords = [
        "international",
        "crypto",
        "bitcoin",
        "unknown",
        "offshore",
        "wire",
        "transfer"
    ]

    for _, row in df.iterrows():

        description = str(
            row.get("Description", "")
        ).lower()

        amount = abs(
            float(row.get("Amount", 0))
        )

        reasons = []

        # -------- KEYWORD ANALYSIS --------
        for word in suspicious_keywords:

            if word in description:

                reasons.append(
                    f"Suspicious keyword detected: '{word}'"
                )

        # -------- HIGH VALUE ANALYSIS --------
        if amount > 50000:

            reasons.append(
                "Very high transaction amount detected"
            )

        elif amount > 20000:

            reasons.append(
                "Unusually high spending detected"
            )

        # -------- FINAL OUTPUT --------
        if reasons:

            explanations.append({

                "Description": row.get(
                    "Description",
                    ""
                ),

                "Amount": amount,

                "Fraud Explanation": " | ".join(reasons)
            })

    return pd.DataFrame(explanations)

def calculate_financial_risk_score(df, kpis):

    risk_score = 0

    # -------- LOW CASH FLOW --------
    net_cash_flow = kpis.get(
        "Net Cash Flow",
        0
    )

    if isinstance(net_cash_flow, str):

        net_cash_flow = (
            net_cash_flow
            .replace("₹", "")
            .replace(",", "")
        )

        try:
            net_cash_flow = float(net_cash_flow)
        except:
            net_cash_flow = 0

    if net_cash_flow < 5000:
        risk_score += 25

    # -------- HIGH VALUE TRANSACTIONS --------
    high_value = kpis.get(
        "High Value Transactions",
        0
    )

    risk_score += int(high_value) * 10

    # -------- SUSPICIOUS TRANSACTIONS --------
    suspicious = kpis.get(
        "Suspicious Transactions",
        0
    )

    risk_score += int(suspicious) * 20

    # -------- SPENDING SPIKES --------
    spikes = detect_spending_spikes(df)

    risk_score += len(spikes) * 10

    # -------- NORMALIZE --------
    risk_score = min(risk_score, 100)

    # -------- RISK LEVEL --------
    if risk_score >= 75:
        level = "CRITICAL"

    elif risk_score >= 50:
        level = "HIGH"

    elif risk_score >= 25:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "Risk Score": risk_score,
        "Risk Level": level
    }









