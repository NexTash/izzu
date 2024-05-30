import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart

def get_columns(filters):
    columns = [
        {
            "fieldname": "customer",
            "label": "Customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 250
        },
        {
            "fieldname": "item_code",
            "label": "Item Code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 250
        },
        {
            "fieldname": "item_name",
            "label": "Item Name",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "amount",
            "label": "Amount",
            "fieldtype": "Currency",
            "width": 250
        },
    ]
    return columns

def get_data(filters):
    data = []
    emp_filters = {}

    if filters and filters.get('customer'):
        emp_filters['customer'] = filters.get('customer')
    if filters and filters.get('amount'):
        emp_filters['amount'] = filters.get('amount')

    if filters.get('start_date') and filters.get('end_date'):
        emp_filters['posting_date'] = ['between', [filters.get('start_date'), filters.get('end_date')]]

    sales_invoices = frappe.get_list('Sales Invoice', filters=emp_filters, fields=["*"])

    for invoice in sales_invoices:
        items = frappe.get_list('Sales Invoice Item', filters={'parent': invoice.name}, fields=["*"])
        
        for item in items:
                data.append({
                    "customer": invoice.customer,
                    "item_code": item.item_code,
                    "item_name": item.item_name,
                    "amount": item.amount,
                })

    return data

def get_chart(data):
    if not data:
        return None

    labels = [row["customer"] for row in data]
    values = [row["amount"] for row in data]

    chart = {
        "data": {
            "labels": labels,
            "datasets": [{
                "name": _("Amount"),
                "values": values,
                

            }]
        },
        "type": "pie",
        "title": "Sales Invoice",

    }
    return chart
