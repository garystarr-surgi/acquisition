import frappe

def po_permission_query(user=None):
    """
    LIST FILTER: Filters the Purchase Order list view.
    Ensures 'Acquisitions' role can only see records where custom_acquisition is 1.
    """
    if not user:
        user = frappe.session.user

    roles = frappe.get_roles(user)

    # Safety: If field doesn't exist yet, don't crash, just show everything
    if not frappe.db.has_column("Purchase Order", "custom_acquisition"):
        return ""

    # If the user has 'Acquisitions' role but NOT 'System Manager'
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
        # Safely get the value to avoid AttributeError
        is_acq = doc.get("custom_acquisition")
        if not is_acq:
            return False
            
    return True

def auto_check_acquisition(doc, method=None):
    """
    AUTOMATION: Logic triggered via 'before_insert' in hooks.py.
    Checks the acquisition box if the PO is pulled from a Supplier Quotation.
    """
    # Safely iterate through items
    items = doc.get("items") or []
    for item in items:
        # Check if the item originated from a Supplier Quotation
        if item.get("supplier_quotation"):
            doc.custom_acquisition = 1
            break
