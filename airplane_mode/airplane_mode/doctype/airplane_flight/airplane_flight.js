// Copyright (c) 2024, mania@navari.co.ke and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
    setup: function (frm) {
        frappe.realtime.on("show_available_seats", (data) => {
            frm.set_intro(`${data["available_seats"]} seats available`);
        });
    },
    onload: function (frm) {
        frm.set_query("departure_gate", () => {
            return {
                filters: {
                    airport: frm.doc.source_airport,
                },
            };
        });

        if (!frm.doc.__unsaved) {
            frappe
                .call({
                    doc: frm.doc,
                    method: "show_remaining_seats",
                })
                .then((r) => {
                    frm.set_intro(`${r["message"]} seats available`);
                });
        }
    },
});