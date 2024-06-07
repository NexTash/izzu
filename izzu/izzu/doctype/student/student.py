# import json
import frappe
from frappe.model.document import Document

class Student(Document):
	pass
@frappe.whitelist()
def	send_data():
	email = "itxjutt008@gmail.com"
	sender = frappe.session.user
	subject = "Subject of the email"
	message = "This is the body of the email."
	frappe.sendmail(
	recipients=email,
	sender=None,
	subject=subject,
	message=message,
	header=[subject, "green"],
	delayed= False,
	retry=3,
)






# @frappe.whitelist()
# def my_function(docname):
# 		stu_child = []
# 		doc = frappe.get_doc("Student",  docname)
# 		for child in doc.stu_child:
# 			stu_child.append(child)
# 		return stu_child


# @frappe.whitelist()
# def my_function(docname):
# 	doc = frappe.get_doc("Student", docname)
# 	for row in doc.stu_child:

# 		new_doc = frappe.new_doc('Student2')
# 		new_doc.name1 = row.name1
# 		new_doc.class1 = row.class1
# 		new_doc.address = row.address
	
	
# 		new_doc.insert()