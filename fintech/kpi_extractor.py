import pandas as pd


def extract_kpis(df):

    insights = {}

    # -------------------- TOTAL INCOME --------------------
    income = df[
        df["Type"] == "Credit"
    ]["Amount"].sum()

    insights["Total Income"] = income

    # -------------------- TOTAL EXPENSE --------------------
    expenses = df[
        df["Type"] == "Debit"
    ]["Amount"].sum()

    insights["Total Expenses"] = expenses

    # -------------------- NET CASH FLOW --------------------
    insights["Net Cash Flow"] = income - expenses

    # -------------------- LARGEST EXPENSE --------------------
    debit_df = df[df["Type"] == "Debit"]

    if not debit_df.empty:

        largest = debit_df.loc[
            debit_df["Amount"].idxmax()
        ]

        insights["Largest Expense"] = (
            f"{largest['Description']} "
            f"(₹{largest['Amount']})"
        )

    # -------------------- SUSPICIOUS TRANSACTIONS --------------------
    suspicious = df[
        df["Category"]
        .str.contains(
            "Suspicious",
            case=False,
            na=False
        )
    ]

    insights["Suspicious Transactions"] = len(
        suspicious
    )

    # -------------------- HIGH VALUE TRANSACTIONS --------------------
    high_value = df[
        df["Amount"] > 50000
    ]

    insights["High Value Transactions"] = len(
        high_value
    )

    return insights