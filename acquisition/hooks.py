# path: your_custom_app/your_custom_app/hooks.py

doc_events = {
    "Purchase Order": {
        "before_insert": "your_custom_app.permissions.auto_check_acquisition"
    }
}
