import frappe
import json
from frappe import _

@frappe.whitelist()
def myfunc(formData):
    data = json.loads(formData)
    # frappe.msgprint(f"{data['name']}")
    doc = frappe.new_doc("Order Request")
    frappe.msgprint(f"{data['bouquet_price']}")
    

    doc.name1 =  data['name']
    doc.phone = data['phone']
    doc.email = data['email']
    doc.address = data['address']
    doc.bouquet_type = data['bouquet_type']
    doc.gift_wrapping = data['gift_wrapping']
    doc.urgent_delivery = data['urgent_delivery']
    doc.bouquet_price = data['bouquet_price']
    doc.insert()
    # doc.save()
    