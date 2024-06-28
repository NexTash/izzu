import frappe

def before_save(doc, method):
    frappe.msgprint(("Document has been saved"))