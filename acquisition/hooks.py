app_name = "acquisition"
app_title = "Acquisition"
app_publisher = "SurgiShop"
app_description = "Control Acquisition Role Access"
app_email = "gary.starr@surgishop.com"
app_license = "MIT"


# ─────────────────────────────
# Permissions
# ─────────────────────────────

permission_query_conditions = {
    "Purchase Order": "acquisition.permissions.po_permission_query"
}

has_permission = {
    "Purchase Order": "acquisition.permissions.has_po_permission"
}


# ─────────────────────────────
# Document Events
# ─────────────────────────────

doc_events = {
    "Purchase Order": {
        "before_insert": "acquisition.permissions.auto_check_acquisition",
        "validate": "acquisition.permissions.prevent_price_edit"
    }
}


# ─────────────────────────────
# Client-side UI logic
# ─────────────────────────────

doctype_js = {
    "Purchase Order": "public/js/purchase_order.js"
}
