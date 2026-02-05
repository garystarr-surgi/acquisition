# path: your_custom_app/your_custom_app/hooks.py

permission_query_conditions = {
    "Purchase Order": "your_custom_app.permissions.po_permission_query"
}

has_permission = {
    "Purchase Order": "your_custom_app.permissions.has_po_permission"
}
