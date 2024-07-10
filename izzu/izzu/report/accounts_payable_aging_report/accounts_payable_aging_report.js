// Copyright (c) 2024, izzu.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Accounts Payable Aging Report"] = {
    onload: function(report) {
        report.page.add_inner_button(__('Send Email'), function() {
            // frappe.msgprint(__('Custom Button Clicked!'));
            
            frappe.call({
                method: 'izzu.izzu.report.accounts_payable_aging_report.accounts_payable_aging_report.send_data',
                args: {
                    // Add necessary arguments here
                },
                callback: function(response) {
                    // Handle response if needed
                }
            });
        });
    },

    "filters": [
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier",
            "reqd": 0
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            // "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            // "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            // "default": frappe.datetime.get_today(),
            // "reqd": 1
        }
    ]
};
