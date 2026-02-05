# path: your_custom_app/your_custom_app/permissions.py
import frappe

def po_permission_query(user):
    """
    LIST FILTER: Filters the Purchase Order list view.
    Ensures 'Acquisitions' role can only see records where custom_acquisition is 1.
    """
    if not user:
        user = frappe.session.user

    roles = frappe.get_roles(user)

    # If the user has 'Acquisitions' role but NOT 'System Manager'
    if "Acquisitions" in roles and "System Manager" not in roles:
        return "(`tabPurchase Order`.custom_acquisition = 1)"

    # Everyone else sees everything (no additional SQL filter)
    return ""

def has_po_permission(doc, ptype, user):
    """
    DOCUMENT ACCESS: Prevents users from bypassing the list filter via direct URL.
    Returns False if an Acquisitions user tries to access a non-acquisition PO.
    """
    if not user:
        user = frappe.session.user
        
    roles = frappe.get_roles(user)
    
    if "Acquisitions" in roles and "System Manager" not in roles:
        # doc can be a dict (from API) or a Document object
        is_acq = doc.get("custom_acquisition")
        if not is_acq:
            return False
            
    return True

def auto_check_acquisition(doc, method):
    """
    AUTOMATION: Logic triggered via 'before_insert' in hooks.py.
    Checks the acquisition box if the PO is pulled from a Supplier Quotation.
    """
    # Loop through items to find a reference to a Supplier Quotation
    for item in doc.get("items"):
        if item.supplier_quotation:
            doc.custom_acquisition = 1
            break # Stop searching once we find a match
