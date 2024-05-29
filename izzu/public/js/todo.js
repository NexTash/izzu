// Copyright (c) 2024, izzu.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.ui.form.on('ToDo', {
    validate: function(frm) {
        frappe.db.get_list('Employee', {
            fields: ['*'],
            filters: {
                user_id: frm.doc.allocated_to
            }
        }).then(employees => {
            if (employees && employees.length > 0) {
                frm.set_value('custom_employee', employees[0].name);
            }
            frm.refresh_field('custom_employee'); 
        });
    }
});
