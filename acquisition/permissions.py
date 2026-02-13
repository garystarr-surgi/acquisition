import frappe

# -----------------------------
# Reusable helpers
# -----------------------------
def is_acquisition(user=None):
    if not user:
        user = frappe.session.user
    roles = frappe.get_roles(user)
    return "Acquisitions" in roles and "System Manager" not in roles

def get_acquisition_condition(doctype, user=None):
    """
    Returns SQL condition to restrict records to acquisitions.
    Assumes 'custom_acquisition' exists on the doctype.
    """
    if not user:
        user = frappe.session.user

    if is_acquisition(user):
        if frappe.db.has_column(doctype, "custom_acquisition"):
            return f"`tab{doctype}`.custom_acquisition = 1"
    return ""

def check_acquisition_permission(doc, user=None):
    """
    Returns True/False if user can access this doc
    """
    if not user:
        user = frappe.session.user

    if is_acquisition(user):
        if not doc.get("custom_acquisition"):
            return False
    return True

def auto_set_acquisition(doc, method=None):
    """
    Auto-check the custom_acquisition field for Acquisition users
    """
    if is_acquisition():
        doc.custom_acquisition = 1


# Add these to the bottom of your permissions.py

def po_permission_query(user):
    return get_acquisition_condition("Purchase Order", user)

def pr_permission_query(user):
    return get_acquisition_condition("Purchase Receipt", user)

def has_po_permission(doc, user):
    return check_acquisition_permission(doc, user)

def has_pr_permission(doc, user):
    return check_acquisition_permission(doc, user)

def auto_check_acquisition(doc, method=None):
    auto_set_acquisition(doc, method)

def auto_check_pr_acquisition(doc, method=None):
    auto_set_acquisition(doc, method)
