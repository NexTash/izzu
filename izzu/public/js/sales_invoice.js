frappe.ui.form.on('Sales Invoice', {
    after_save: function(frm, dt, dn) {
        frm.set_value("custom_barcode", frm.doc.name)
    }
});
