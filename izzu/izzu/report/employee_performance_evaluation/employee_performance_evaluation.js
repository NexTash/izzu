// Copyright (c) 2024, izzu.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Performance Evaluation"] = {
    "filters": [
        {
            "fieldname": "employee_name",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Employee" 
        }
    ]
};