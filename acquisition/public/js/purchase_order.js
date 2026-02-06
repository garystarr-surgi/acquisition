frappe.ui.form.on("Purchase Order", {
    refresh(frm) {
        if (frappe.user.has_role("Acquisitions")) {

            // Fields Acquisition should NOT see
            const hide_fields = [
                "rate",
                "amount",
                "base_rate",
                "base_amount",
                "price_list_rate"
            ];

            hide_fields.forEach(field => {
                if (frm.fields_dict.items?.grid) {
                    frm.fields_dict.items.grid.toggle_display(field, false);
                }
            });

        } else {
            // Procurement / managers see everything
            const show_fields = [
                "rate",
                "amount",
                "base_rate",
                "base_amount",
                "price_list_rate"
            ];

            show_fields.forEach(field => {
                if (frm.fields_dict.items?.grid) {
                    frm.fields_dict.items.grid.toggle_display(field, true);
                }
            });
        }
    }
});
