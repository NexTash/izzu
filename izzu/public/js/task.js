// Copyright (c) 2024, izzu.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.ui.form.on('Task', {
    validate: function(frm) {
        frappe.db.get_list('ToDo', {
            fields: ['*'],
            filters: {
                reference_name: frm.doc.name
            }
            
        }).then(todo_records => {
            console.log(todo_records)
            if (todo_records && todo_records.length > 0) {
                frm.doc.custom_employee_child = []
                for (let row of todo_records) {
                    frm.add_child('custom_employee_child', {
                        user: row.allocated_to,
                        employee: row.custom_employee
                    });
                }
                frm.refresh_field("custom_employee_child")
            }

        });
    }
});
