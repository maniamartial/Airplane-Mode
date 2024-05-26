# Copyright (c) 2024, mania@navari.co.ke and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from pypika import Case


def execute(filters=None):

    columns = [
        {
            "fieldtype": "Link",
            "label": "Airline",
            "options": "Airline",
            "fieldname": "airline",
            "width": 300,
        },
        {
            "fieldtype": "Currency",
            "label": "Revenue",
            "fieldname": "revenue",
            "width": 200,
        },
    ]

    data = get_revenue_from_diff_airline()

    chart = {
        "type": "donut",
        "data": {
            "labels": [row.airline for row in data],
            "datasets": [{"values": [row.revenue for row in data]}],
        },
    }

    total_revenue = sum(row.revenue for row in data)

    report_summary = [
        {
            "value": total_revenue,
            "indicator": "green" if total_revenue > 0 else "red",
            "label": "Total Revenue",
            "datatype": "Currency",
        }
    ]

    return columns, data, None, chart, report_summary


def get_revenue_from_diff_airline():
    airline = frappe.qb.DocType("Airline")
    airplane = frappe.qb.DocType("Airplane")
    airplane_ticket = frappe.qb.DocType("Airplane Ticket")
    airplane_flight = frappe.qb.DocType("Airplane Flight")

    sum_total_amount = frappe.qb.functions("SUM", airplane_ticket.total_amount).as_(
        "revenue"
    )

    query = (
        frappe.qb.from_(airline)
        .left_join(airplane)
        .on(airline.name == airplane.airline)
        .left_join(airplane_flight)
        .on(airplane.name == airplane_flight.airplane)
        .left_join(airplane_ticket)
        .on(airplane_flight.name == airplane_ticket.flight)
        .select(
            airline.name.as_("airline"),
            sum_total_amount,
            Case()
            .when(sum_total_amount.isnull(), 0)
            .else_(sum_total_amount)
            .as_("revenue"),
        )
        .groupby(airline.name)
    )

    data = query.run(as_dict=True)
    return data