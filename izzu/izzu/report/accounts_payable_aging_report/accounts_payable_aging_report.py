import frappe
from frappe.utils import today, getdate, flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": "Supplier",
            "fieldname": "supplier",
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 200
        },
        {
            "label": "Invoice Number",
            "fieldname": "invoice_number",
            "fieldtype": "Link",
            "options": "Purchase Invoice",
            "width": 150
        },
        {
            "label": "Posting Date",
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": "Due Date",
            "fieldname": "due_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": "Outstanding Amount",
            "fieldname": "outstanding_amount",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "0-30 Days",
            "fieldname": "age_0_30",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": "31-60 Days",
            "fieldname": "age_31_60",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": "61-90 Days",
            "fieldname": "age_61_90",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": "Over 90 Days",
            "fieldname": "age_over_90",
            "fieldtype": "Currency",
            "width": 100
        }
    ]

def get_data(filters):
    data = []
    today_date = getdate(today())
    
    conditions = [["status", "=", "Unpaid"]]
    
    if filters.get("supplier"):
        conditions.append(["supplier", "=", filters["supplier"]])
    
    if filters.get("from_date"):
        conditions.append(["posting_date", ">=", filters["from_date"]])
        
    if filters.get("to_date"):
        conditions.append(["posting_date", "<=", filters["to_date"]])

    invoices = frappe.get_all(
        "Purchase Invoice",
        filters=conditions,
        fields=["name", "supplier", "posting_date", "due_date", "outstanding_amount"]
    )

    for invoice in invoices:
        outstanding_amount = flt(invoice.outstanding_amount)
        due_date = getdate(invoice.due_date) if invoice.due_date else None
        age_0_30 = age_31_60 = age_61_90 = age_over_90 = 0

        if due_date:
            age = (today_date - due_date).days

            if 0 <= age <= 30:
                age_0_30 = outstanding_amount
            elif 31 <= age <= 60:
                age_31_60 = outstanding_amount
            elif 61 <= age <= 90:
                age_61_90 = outstanding_amount
            else:
                age_over_90 = outstanding_amount

        row = {
            "supplier": invoice.supplier,
            "invoice_number": invoice.name,
            "posting_date": invoice.posting_date,
            "due_date": invoice.due_date,
            "outstanding_amount": outstanding_amount,
            "age_0_30": age_0_30,
            "age_31_60": age_31_60,
            "age_61_90": age_61_90,
            "age_over_90": age_over_90
        }
        data.append(row)
    return data

@frappe.whitelist()
def send_data():
    filters = {}
    columns, data = execute(filters)
    
    # Prepare the email content
    email_content = "<h2>Weekly Accounts Payable Aging Report</h2>"
    email_content += "<table border='1' style='width:100%; border-collapse: collapse;'>"
    email_content += "<tr>"
    
    # Add column headers
    for col in columns:
        email_content += f"<th>{col['label']}</th>"
    email_content += "</tr>"
    
    # Add data rows
    for row in data:
        email_content += "<tr>"
        for col in columns:
            email_content += f"<td>{row.get(col['fieldname'], '')}</td>"
        email_content += "</tr>"
    
    email_content += "</table>"

    # Send the email
    recipients = ["itxjutt008@gmail.com"]  # List of recipients
    frappe.sendmail(
        recipients=recipients,
        subject="Weekly Accounts Payable Aging Report",
        message=email_content,
        delayed=False,
        retry=3,
    )
