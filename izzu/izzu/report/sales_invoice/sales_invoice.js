// Copyright (c) 2024, izzu.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales invoice"] = {
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
       
	]

	
};
