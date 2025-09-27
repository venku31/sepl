# Copyright (c) 2025, SEPL and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Expense Approver", "fieldname": "expense_approver", "fieldtype": "Data", "width": 180},
        {"label": "Expense Type", "fieldname": "expense_type", "fieldtype": "Data", "width": 150},
        {"label": "Description", "fieldname": "description", "fieldtype": "Data", "width": 250},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Sanctioned Amount", "fieldname": "sanctioned_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Status", "fieldname": "approval_status", "fieldtype": "Data", "width": 50},
    ]

    data = frappe.db.sql("""
        SELECT 
            ecd.expense_date AS date,
            ec.employee_name AS employee_name,
            ec.expense_approver AS expense_approver,
            ecd.expense_type AS expense_type,
            ecd.description AS description,
            ecd.amount AS amount,approval_status,
            ecd.sanctioned_amount AS sanctioned_amount
        FROM 
            `tabExpense Claim Detail` ecd
        JOIN 
            `tabExpense Claim` ec ON ec.name = ecd.parent
        WHERE
            ecd.expense_date BETWEEN %(from_date)s AND %(to_date)s
        ORDER BY
            ecd.expense_date DESC
    """, {"from_date": from_date, "to_date": to_date}, as_dict=True)

    return columns, data
