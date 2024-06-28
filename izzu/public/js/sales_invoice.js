frappe.ui.form.on('Sales Invoice', {
    after_save: function(frm, dt, dn) {
        frm.set_value("barcode", frm.doc.name)
    }
});
