import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    df = dict(fieldname="section_break", fieldtype="Section Break", label="Barcode", insert_after="scan_barcode")
    df2 = dict(fieldname="barcode", fieldtype="Data", label="Barcode", insert_after="section_break")
    create_custom_field("Sales Invoice", df)
    create_custom_field("Sales Invoice", df2)

    frappe.db.commit()