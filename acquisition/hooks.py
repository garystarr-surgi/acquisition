app_name = "acquisition"
app_title = "Acquisition"
app_publisher = "SurgiShop"
app_description = "Control Acquisition Role Access"
app_email = "gary.starr@surgishop.com"
app_license = "MIT"


# Permission query hooks
permission_query_conditions = {
    "Purchase Order": "acquisition.permissions.po_permission_query",
    "Purchase Receipt": "acquisition.permissions.pr_permission_query"
}

# Permission check hooks
has_permission = {
    "Purchase Order": "acquisition.permissions.has_po_permission",
    "Purchase Receipt": "acquisition.permissions.has_pr_permission"
}

# Doc events
doc_events = {
    "Purchase Order": {
        "before_insert": "acquisition.permissions.auto_check_acquisition",
    },
    "Purchase Receipt": {
        "before_insert": "acquisition.permissions.auto_check_pr_acquisition",
    }
}


# ─────────────────────────────
# Client-side UI logic
# ─────────────────────────────

doctype_js = {
    "Purchase Order": "public/js/purchase_order.js"
}
