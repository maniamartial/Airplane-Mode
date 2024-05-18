import frappe
@frappe.whitelist(allow_guest=True)
def get_mania():
    return dict(mania="Helo")