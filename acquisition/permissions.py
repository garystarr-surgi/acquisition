import frappe


def po_permission_query(user=None):
    """
    Filters Purchase Order list, reports, searches.
    Acquisitions only see acquisition POs.
    """
    if not user:
        user = frappe.session.user

    if not frappe.db.has_column("Purchase Order", "custom_acquisition"):
        return ""

    roles = frappe.get_roles(user)

    if "Acquisitions" in roles and "System Manager" not in roles:
        return "`tabPurchase Order`.custom_acquisition = 1"

    return ""


def has_po_permission(doc, ptype=None, user=None):
    """
    Controls direct access (URL, API, background jobs).
    REQUIRED explicit True in v16.
    """
    if not user:
        user = frappe.session.user

    roles = frappe.get_roles(user)

    if "Acquisitions" in roles and "System Manager" not in roles:
        if not doc.get("custom_acquisition"):
            return False

    return True

def has_pr_permission(doc, ptype=None, user=None):
    """
    Controls direct access (URL, API, background jobs).
    """
    if not user:
        user = frappe.session.user

    roles = frappe.get_roles(user)

    if "Acquisitions" in roles and "System Manager" not in roles:
        if not doc.get("custom_acquisition"):
            return False

    return True





def pr_permission_query(user=None):
    """
    Filters Purchase Receipt list, reports, searches.
    Acquisitions only see acquisition PRs.
    """
    if not user:
        user = frappe.session.user

    if not frappe.db.has_column("Purchase Receipt", "custom_acquisition"):
        return ""

    roles = frappe.get_roles(user)

    if "Acquisitions" in roles and "System Manager" not in roles:
        return "`tabPurchase Receipt`.custom_acquisition = 1"

    return ""




def auto_check_acquisition(doc, method=None):
    """
    Automatically mark PO as acquisition
    when created by Acquisition role.
    """
    user = frappe.session.user
    roles = frappe.get_roles(user)

    if "Acquisitions" in roles and "System Manager" not in roles:
        doc.custom_acquisition = 1


def prevent_price_edit(doc, method=None):
    """
    Server-side protection.
    Acquisition users cannot change pricing.
    """
    user = frappe.session.user
    roles = frappe.get_roles(user)

    if "Acquisitions" not in roles or "System Manager" in roles:
        return

    for item in doc.items:
        db_rate = item.get_db_value("rate")
        if db_rate is not None and item.rate != db_rate:
            frappe.throw(
                "Acquisitions are not allowed to modify item pricing."
            )
