// Copyright (c) 2024, izzu.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student', {
    refresh: function(frm) {
        frm.add_custom_button(__('Send Email'), function() {
            // frappe.msgprint(__('Custom Button Clicked!'));
            
            frm.call({
                method: 'izzu.izzu.doctype.student.student.send_data',
                args: {
                    // doc: frm.doc  
                },
            });
        });
    }
});

