# path: your_custom_app/your_custom_app/permissions.py
import frappe

def po_permission_query(user):
    if not user:
        user = frappe.session.user

    roles = frappe.get_roles(user)

    # Apply restriction: If they have 'Acquisitions' but are not a 'System Manager'
    if "Acquisitions" in roles and "System Manager" not in roles:
        # We use the internal database name: custom_acquisition
        return "(`tabPurchase Order`.custom_acquisition = 1)"

    return ""

def has_po_permission(doc, ptype, user):
    """
    Prevents direct access via URL or API if the user doesn't meet the criteria.
    """
    roles = frappe.get_roles(user)
    
    if "Acquisitions" in roles and "System Manager" not in roles:
        # If the document is NOT marked as custom_acquisition, deny access
        if not doc.get("custom_acquisition"):
            return False
    return True
