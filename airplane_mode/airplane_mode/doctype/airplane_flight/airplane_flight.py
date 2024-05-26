# Copyright (c) 2024, mania@navari.co.ke and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.document import Document


class AirplaneFlight(WebsiteGenerator, Document):
	pass
	def on_submit(self):
		self.status = "Completed"

	@frappe.whitelist()
	def show_remaining_seats(self):
		plane_capacity = frappe.db.get_all(
			"Airplane Flight", filters={"name": self.name}, fields=["airplane.capacity"]
		)[0].get("capacity", 0)
		number_of_tickets = frappe.db.get_all(
			"Airplane Ticket",
			filters={"flight": self.name},
			fields=["COUNT(name) AS number_of_tickets"],
		)[0].get("number_of_tickets")

		return plane_capacity - number_of_tickets



