import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def register_hr_manager(full_name, email, password):
    # Check if the email already exists
    if frappe.db.exists("User", email):
        return {"status": "error", "message": _("Email already exists")}

    # Create a new User
    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": full_name,
        "enabled": 1,
        "new_password": password
    })
    user.insert()

    # Assign the "HR Officer" role
    role = "HR Officer"
    user.add_roles(role)

    return {"status": "success", "message": _("User registered successfully")}