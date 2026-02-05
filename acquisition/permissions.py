# path: acquisition/acquisition/permissions.py
import frappe

def po_permission_query(user=None):
    """
    LIST FILTER: Filters the Purchase Order list view.
    Ensures 'Acquisitions' role can only see records where custom_acquisition is 1.
    """
    if not user:
        user = frappe.session.user

    # Safety: check if column exists to prevent 500 error if DB hasn't migrated
    if not frappe.db.has_column("Purchase Order", "custom_acquisition"):
        return ""

    roles = frappe.get_roles(user)

    if "Acquisitions" in roles and "System Manager" not in roles:
        return "(`tabPurchase Order`.custom_acquisition = 1)"

    return ""

def has_po_permission(doc, ptype=None, user=None):
    """
    DOCUMENT ACCESS: Prevents users from bypassing the list filter via direct URL.
    """
    if not user:
        user = frappe.session.user
        
    roles = frappe.get_roles(user)
    
    if "Acquisitions" in roles and "System Manager" not in roles:
        # Use .get() to avoid AttributeError if the field isn't in the current view
        is_acq = doc.get("custom_acquisition")
        if not is_acq:
            return False
            
    return True

def auto_check_acquisition(doc, method=None):
    """
    AUTOMATION: Logic triggered via 'before_insert' in hooks.py.
    Checks the acquisition box if the PO is pulled from a Supplier Quotation.
    """
    # Use .get("items", []) to safely iterate even if items list is missing
    for item in doc.get("items", []):
        if item.get("supplier_quotation"):
            doc.custom_acquisition = 1
            break
