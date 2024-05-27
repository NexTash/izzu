import frappe

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

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
    ]
    return columns

def get_data(filters):
    data = []
    emp_filters = {}

    if filters and filters.get('customer'):
        emp_filters['customer'] = filters.get('customer')

    if filters.get('start_date') and filters.get('end_date'):
        emp_filters['posting_date'] = ['between', [filters.get('start_date'), filters.get('end_date')]]


    sales_invoices = frappe.get_list('Sales Invoice', filters=emp_filters, fields=["name", "customer"])

    for invoice in sales_invoices:
        items = frappe.get_list('Sales Invoice Item', filters={'parent': invoice.name}, fields=["item_code","item_name"])
        
        item_codes = [item.item_code for item in items]
        item_names = [item.item_name for item in items]

        item_codes_str = ", ".join(item_codes)
        item_names_str = ", ".join(item_names)
        
        data.append({
            "customer": invoice.customer,
            "item_code": item_codes_str,
            "item_name": item_names_str,
        })

    return data



# Combine the data into a single list
# combined_data = task_data + attendance_data + performance_feedback + eco_data + employee_skill_maps + skills + trainings

# Process each entry in the combined data
# for entry in combined_data: