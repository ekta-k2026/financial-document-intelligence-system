def generate_financial_report(kpis, question_answer=None):

    report = f"""
FINANCIAL ANALYSIS REPORT
=========================

KEY PERFORMANCE INDICATORS
--------------------------
Total Income: ₹{kpis['Total Income']}
Total Expenses: ₹{kpis['Total Expenses']}
Net Cash Flow: ₹{kpis['Net Cash Flow']}

Largest Expense:
{kpis['Largest Expense']}

Suspicious Transactions:
{kpis['Suspicious Transactions']}

High Value Transactions:
{kpis['High Value Transactions']}

=========================

AI FINANCIAL INSIGHTS
---------------------
"""

    insights = []

    # -------- CASH FLOW --------
    if kpis["Net Cash Flow"] < 5000:

        insights.append(
            "- Low net cash flow detected. Liquidity should be monitored carefully."
        )

    else:

        insights.append(
            "- Cash flow appears relatively stable."
        )

    # -------- SUSPICIOUS --------
    if kpis["Suspicious Transactions"] > 0:

        insights.append(
            "- Suspicious transactions detected. Manual review is recommended."
        )

    # -------- EXPENSE ANALYSIS --------
    if kpis["Total Expenses"] > kpis["Total Income"] * 0.8:

        insights.append(
            "- Expenses are consuming a large portion of income."
        )

    # -------- HIGH VALUE --------
    if kpis["High Value Transactions"] > 1:

        insights.append(
            "- Multiple high-value transactions detected."
        )

    # -------- LARGEST EXPENSE --------
    insights.append(
        f"- Largest recorded expense: {kpis['Largest Expense']}."
    )

    for item in insights:

        report += item + "\n"

    if question_answer:

        report += f"""

=========================

LATEST AI ANALYSIS
------------------

{question_answer}
"""

    return report