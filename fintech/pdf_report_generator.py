from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf_report(
    kpis,
    risk_result,
    filename="financial_report.pdf"
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "Financial Intelligence Report",
        styles["Title"]
    )

    content.append(title)
    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Key Performance Indicators",
            styles["Heading2"]
        )
    )

    for key, value in kpis.items():

        content.append(
            Paragraph(
                f"{key}: {value}",
                styles["BodyText"]
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "AI Risk Assessment",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Score: {risk_result['Risk Score']}/100",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Level: {risk_result['Risk Level']}",
            styles["BodyText"]
        )
    )

    doc.build(content)

    return filename

