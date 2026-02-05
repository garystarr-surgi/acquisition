app_name = "acquisition"
app_title = "Acquisition"
app_publisher = "SurgiShop"
app_description = "Control Acquisition Role Access"
app_email = "gary.starr@surgishop.com"
app_license = "MIT"

# path: your_custom_app/your_custom_app/hooks.py

# 1. Filters the list view
permission_query_conditions = {
    "Purchase Order": "your_custom_app.permissions.po_permission_query"
}

# 2. Controls direct access/API access
has_permission = {
    "Purchase Order": "your_custom_app.permissions.has_po_permission"
}

# 3. Runs the automation when creating the record
doc_events = {
    "Purchase Order": {
        "before_insert": "your_custom_app.permissions.auto_check_acquisition"
    }
}
