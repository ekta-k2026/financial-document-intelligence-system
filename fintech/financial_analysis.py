def generate_financial_summary(
    question,
    selected_knowledge,
    client
):

    messages = [
        {
            "role": "system",
            "content": """
You are a Financial AI Analyst.

Your job:
- Analyze financial documents
- Summarize key insights
- Highlight risks
- Identify trends
- Detect anomalies
- Explain clearly

Rules:
- Use bullet points
- Be concise
- Mention important financial indicators
- If information is missing, say:
  'Not found in document'
"""
        },
        {
            "role": "user",
            "content": f"""
Financial Document Data:
{selected_knowledge}

Question:
{question}
"""
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    return response.choices[0].message.content