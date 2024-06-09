// Copyright (c) 2024, mania@navari.co.ke and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    setup: function (frm) {
        frappe.realtime.on("show_available_seats", (data) => {
            frm.set_intro(`${data["available_seats"]} seats available`);
        });
    },
    refresh: function (frm) {
        frm.add_custom_button(
            __("Assign Seat"),
            function () {
                let dialog = new frappe.ui.Dialog({
                    title: "Select Seat",
                    fields: [
                        {
                            label: "Seat Number",
                            fieldname: "seat_number",
                            fieldtype: "Data",
                        },
                    ],
                    size: "small",
                    primary_action_label: "Assign",
                    primary_action(values) {
                        frm.set_value("seat", values.seat_number);
                        cur_frm.save();
                        dialog.hide();
                    },
                });
                dialog.show();
            },
            __("Actions")
        );
    },
    source_airport_code: function (frm) {
        frm.set_query("gate_number", function () {
            return {
                filters: {
                    airport_code: frm.doc.source_airport_code,
                },
            };
        });
    },
    
});
  