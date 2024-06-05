// Copyright (c) 2024, izzu.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stu Parent', {
	// 	refresh: function(frm) {
	// 		// Custom buttons
	// frm.add_custom_button('Open Reference form', () => {
	
	// 			frappe.call({
	// 				method: 'izzu.izzu.doctype.student.student.my_function',
	
	// 				args: {
	// 					// data: frm.doc.stu_child,
	// 					docname: frm.doc.one
	// 				},
	
	// 				callback: (r) => {
	// 					console.log(r.message)
	// 					frm.doc.stu_child=[]
	// 					for(let row of r.message){
	// 						frm.add_child("stu_child",{
	// 							name1:row.name1,
	// 							class1:row.class1,
	// 							address:row.address
	// 						})
	// 					}
	// 					frm.refresh_field('stu_child')
	
	// 				},
		
	// 			})
	// 		})
	
	// 	}
});
