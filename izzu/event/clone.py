import frappe

def clone_document(Student2 , STUD0001):
    try:
        doc = frappe.get_doc(Student2, STUD0001)
        new_doc = frappe.copy_doc(doc)
        new_doc.insert()
        frappe.db.commit()
        frappe.msgprint(f"Document {STUD0001} cloned successfully")
    except Exception as e:
        frappe.log_error(f"Error cloning document {STUD0001}: {str(e)}", "Clone Document Error")
