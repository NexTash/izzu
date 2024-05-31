// Copyright (c) 2024, izzu.com and contributors
// For license information, please see license.txt

frappe.query_reports["Sales invoice"] = {
    onload: function (report) {
    
        var defaultCustomer = frappe.defaults.get_default("customer");
        
        frappe.db.get_list('Sales Invoice', {
            fields: ['name'],
            filters: { 'customer': defaultCustomer },
            limit: 6,
        }).then(salesInvoices => {
            if (salesInvoices.length > 0) {
                let salesInvoice = salesInvoices[0];
                
                frappe.db.get_doc('Sales Invoice', salesInvoice.name)
                    .then(doc => {
                        if (doc.items && doc.items.length > 0) {
                            let item = doc.items[0];
                            
                            localStorage.setItem("customer", JSON.stringify({ 
                                customer: doc.customer,
                                item_name: item.item_name,
                                item_code: item.item_code,
                                amount: item.amount
                            }));
                        }
                    });
            }
        });
    },
    
    

    "filters": [
        {
            "fieldname": "start_date",
            "label": "Start Date",
            "fieldtype": "Date",
            "width": 250
        },
        {
            "fieldname": "end_date",
            "label": "End Date",
            "fieldtype": "Date",
            "width": 250
        },
        {
            "fieldname": "customer",
            "label": "Customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 250
        },
        {
            "fieldname": "amount",
            "label": __("Amount"),
            "fieldtype": "Data",
            "width": 250
        }
    ]
};
