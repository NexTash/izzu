// Copyright (c) 2024, izzu.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Performance Evaluation"] = {
    "filters": [
        // {
        //     "fieldname": "from_date",
        //     "label": __("From Date"),
        //     "fieldtype": "Date"
        // },
        // {
        //     "fieldname": "to_date",
        //     "label": __("To Date"),
        //     "fieldtype": "Date"
        // },
        {
            "fieldname": "employee_name",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Attendance" // Assuming Employee is a DocType
        },
        // {
        //     "fieldname": "task",
        //     "label": __("Task"),
        //     "fieldtype": "Link",
        //     "options": "Task" // Assuming Task is a DocType
        // },
        // {
        //     "fieldname": "attendance",
        //     "label": __("Attendance"),
        //     "fieldtype": "Link",
        //     "options": "Attendance" // Assuming Attendance is a DocType
        // },
        // {
        //     "fieldname": "employee_performance_feedback",
        //     "label": __("Employee Performance Feedback"),
        //     "fieldtype": "Link",
        //     "options": "Employee Performance Feedback" // Assuming Feedback is a DocType
        // },
        // {
        //     "fieldname": "employee_performance_on_eco",
        //     "label": __("Employee Performance on ECO"),
        //     "fieldtype": "Link",
        //     "options": "Employee Performance on ECO" // Assuming ECO is a DocType
        // },
        // {
        //     "fieldname": "employee_skill_map",
        //     "label": __("Employee Skill Map"),
        //     "fieldtype": "Link",
        //     "options": "Employee Skill Map" // Assuming Skill Map is a DocType
        // }
    ]
};


