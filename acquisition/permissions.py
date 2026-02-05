# path: acquisition/acquisition/permissions.py
import frappe

def po_permission_query(user=None):
    if not user:
        user = frappe.session.user

    # Safety: check if column exists
    if not frappe.db.has_column("Purchase Order", "custom_acquisition"):
        return ""

    roles = frappe.get_roles(user)

    if "Acquisitions" in roles and "System Manager" not in roles:
        return "(`tabPurchase Order`.custom_acquisition = 1)"

    return ""

def has_po_permission(doc, ptype=None, user=None):
    """
    V16 BREAKING CHANGE FIX: 
    Must return True explicitly if permission is allowed.
    """
    if not user:
        user = frappe.session.user
        
    roles = frappe.get_roles(user)
    
    if "Acquisitions" in roles and "System Manager" not in roles:
        is_acq = doc.get("custom_acquisition")
        if not is_acq:
            return False # Deny access
            
    # IMPORTANT: v16 requires an explicit True to allow the document to load
    return True

def auto_check_acquisition(doc, method=None):
    items = doc.get("items") or []
    for item in items:
        if item.get("supplier_quotation"):
            doc.custom_acquisition = 1
            break
