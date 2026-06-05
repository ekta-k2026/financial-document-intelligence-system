def detect_category(description):

    text = str(description).lower()

    # -------- FOOD --------
    if any(word in text for word in [
        "starbucks",
        "restaurant",
        "coffee",
        "cafe",
        "food",
        "swiggy",
        "zomato"
    ]):
        return "Food"

    # -------- TRAVEL --------
    elif any(word in text for word in [
        "flight",
        "uber",
        "ola",
        "travel",
        "hotel"
    ]):
        return "Travel"

    # -------- SHOPPING --------
    elif any(word in text for word in [
        "amazon",
        "watch",
        "shopping",
        "flipkart"
    ]):
        return "Shopping"

    # -------- INVESTMENT --------
    elif any(word in text for word in [
        "mutual fund",
        "investment",
        "stock",
        "sip"
    ]):
        return "Investment"

    # -------- UTILITIES --------
    elif any(word in text for word in [
        "electricity",
        "water",
        "insurance",
        "bill"
    ]):
        return "Utilities"
        # -------- HOUSING --------
    elif any(word in text for word in [
        "rent",
        "housing"
    ]):
        return "Housing"

    # -------- CASH / WITHDRAWAL --------
    elif any(word in text for word in [
        "atm",
        "withdrawal",
        "cash"
    ]):
        return "Cash Withdrawal"

    # -------- SALARY / INCOME --------
    elif any(word in text for word in [
        "salary",
        "bonus",
        "freelance",
        "credit"
    ]):
        return "Income"

    # -------- SUSPICIOUS --------
    elif any(word in text for word in [
        "international transfer",
        "unknown",
        "crypto"
    ]):
        return "Suspicious"

    return "Other"