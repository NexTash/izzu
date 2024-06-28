import frappe
from izzu.event.clone import clone_document

def all_events_task():
    # Example: Cloning a specific document every day
    clone_document("Student2", "STUD0001")
