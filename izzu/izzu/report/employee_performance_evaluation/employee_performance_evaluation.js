// Copyright (c) 2024, izzu.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.ui.form.on('Employee Performance Evaluation', {
    validate: function(frm) {
        frm.add_custom_button('Open', () => {
            // if(frm.doc.reference) {
            //     console.log(frm.doc.reference);

                // Fetch records from ToDo
                frappe.db.get_list('ToDo', {
                    fields: ['*'],
                    filters: {
                        reference_name: frm.doc.reference
                    }
                }).then(todo_records => {
                    console.log(todo_records)
                    if (todo_records && todo_records.length > 0) {
                        for (let row of todo_records) {
                            frm.add_child('employee_child', {
                                allocated_to: row.user
                            });
                        }
                    }

                    // Fetch records from Task
                    frappe.db.get_list('Task', {
                        fields: ['*'],
                        filters: {
                            reference_name: frm.doc.reference
                        }
                    }).then(task_records => {
                        if (task_records && task_records.length > 0) {
                            for (let row of task_records) {
                                frm.add_child('employee_child', {
                                    allocated_to: row.user
                                });
                            }
                        }

                        // Refresh the child table field after both fetches
                        frm.refresh_field('employee_child');
                    });
                });
            // }
        });
    }
});

frappe.query_reports["Employee Performance Evaluation"] = {
    "filters": [
        {
            "fieldname": "employee_name",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Employee" // Assuming Employee is a DocType
        }
    ]
};

// Example for an `onload` event for a specific DocType
// frappe.ui.form.on('Employee Performance Evaluation', {
// });
