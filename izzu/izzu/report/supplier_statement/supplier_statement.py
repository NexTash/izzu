import frappe
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    supplier_filter = filters.get("supplier")

    # Get opening balances
    opening_balances = get_opening_balances(from_date, supplier_filter)

    # Get transactions
    transactions = get_transactions(from_date, to_date, supplier_filter)

    # Combine data
    data = []
    suppliers = set(opening_balances.keys()) | set(transactions.keys())

    for supplier in sorted(suppliers):
        opening = opening_balances.get(supplier, 0)
        txns = transactions.get(supplier, [])

        # Fetch supplier name
        supplier_name = frappe.db.get_value("Supplier", supplier, "supplier_name") or supplier

        if txns or opening != 0:
            data.append({
                "date": "",
                "supplier": supplier,
                "supplier_name": supplier_name,
                "voucher_subtype": "",
                "voucher_type": "",
                "voucher_no": "",
                "doc_ref": "<b>Opening Balance</b>",
                "opening_balance": opening,
                "debit": 0,
                "credit": 0,
                "balance": opening
            })

        total_debit = total_credit = 0
        balance = opening

        for txn in txns:
            balance += flt(txn["debit"]) - flt(txn["credit"])
            data.append({
                "date": txn.get("posting_date"),
                "supplier": supplier,
                "supplier_name": "",
                "voucher_subtype": txn["voucher_subtype"],
                "voucher_type": txn["voucher_type"],
                "voucher_no": txn["voucher_no"],
                "doc_ref": txn.get("doc_ref", ""),
                "opening_balance": "",
                "debit": txn["debit"],
                "credit": txn["credit"],
                "balance": balance
            })
            total_debit += flt(txn["debit"])
            total_credit += flt(txn["credit"])

        if txns or opening != 0:
            data.append({
                "date": "",
                "supplier": "",
                "supplier_name": "",
                "voucher_subtype": "",
                "voucher_type": "",
                "voucher_no": "",
                "doc_ref": "<b>Total</b>",
                "opening_balance": "",
                "debit": total_debit,
                "credit": total_credit,
                "balance": balance
            })
            data.append({"page_break": 0})

    return get_columns(), data

def get_opening_balances(from_date, supplier_filter):
    condition = "posting_date < %(from_date)s AND party_type = 'Supplier'"
    params = {"from_date": from_date}

    if supplier_filter:
        condition += " AND party = %(supplier)s"
        params["supplier"] = supplier_filter

    result = frappe.db.sql(f"""
        SELECT party, SUM(debit - credit) AS opening_balance
        FROM `tabGL Entry`
        WHERE {condition}
        GROUP BY party
    """, params, as_dict=1)

    return {row.party: flt(row.opening_balance) for row in result}

def get_transactions(from_date, to_date, supplier_filter):
    condition = "posting_date BETWEEN %(from_date)s AND %(to_date)s AND party_type = 'Supplier'"
    params = {"from_date": from_date, "to_date": to_date}

    if supplier_filter:
        condition += " AND party = %(supplier)s"
        params["supplier"] = supplier_filter

    result = frappe.db.sql(f"""
        SELECT party, voucher_type, voucher_subtype, voucher_no, posting_date,
               SUM(debit) AS debit, SUM(credit) AS credit
        FROM `tabGL Entry`
        WHERE {condition}
        GROUP BY voucher_type, voucher_no
        HAVING SUM(debit) != SUM(credit)
        ORDER BY party, posting_date
    """, params, as_dict=1)

    enriched = []
    for gle in result:
        details = ""
        p_name = ""

        if gle["voucher_type"] == "Purchase Invoice":
            pi = frappe.db.get_value(
                "Purchase Invoice", gle["voucher_no"],
                ["docstatus", "is_return", "bill_no", "remarks", "supplier_name"],
                as_dict=True
            )
            if not pi or pi.docstatus == 2:
                continue
            if pi.bill_no:
                details = f"Supp.Inv: {pi.bill_no}"
            elif pi.remarks:
                details = f"Remarks: {pi.remarks}"
            p_name = pi.supplier_name

        elif gle["voucher_type"] == "Payment Entry":
            pe = frappe.db.get_value(
                "Payment Entry", gle["voucher_no"],
                ["docstatus", "reference_no", "remarks", "party_name"],
                as_dict=True
            )
            if not pe or pe.docstatus == 2:
                continue
            if pe.reference_no:
                details = f"Ref: {pe.reference_no}"
            elif pe.remarks:
                details = f"Remarks: {pe.remarks}"
            p_name = pe.party_name

        elif gle["voucher_type"] == "Journal Entry":
            je = frappe.db.get_value("Journal Entry", gle["voucher_no"], "user_remark")
            if je:
                details = f"Remarks: {je}"

        gle["party_name"] = p_name
        gle["doc_ref"] = details or ""
        enriched.append(gle)

    # Group by supplier
    grouped = {}
    for row in enriched:
        grouped.setdefault(row.party, []).append(row)

    return grouped

def get_columns():
    return [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Supplier", "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 150},
        {"label": "Supplier Name", "fieldname": "supplier_name", "fieldtype": "Data", "width": 200},
        {"label": "Voucher Subtype", "fieldname": "voucher_subtype", "fieldtype": "Data", "width": 120},
        {"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},
        {"label": "Doc Ref", "fieldname": "doc_ref", "fieldtype": "Data", "width": 200},
        {"label": "Opening", "fieldname": "opening_balance", "fieldtype": "Currency", "width": 120},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 120},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 120},
        {"label": "Balance", "fieldname": "balance", "fieldtype": "Currency", "width": 120},
    ]
