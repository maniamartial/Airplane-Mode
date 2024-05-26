# Copyright (c) 2024, mania@navari.co.ke and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random

class AirplaneTicket(Document):
	pass
	def validate(self):
		self.remove_duplicate_add_on_items()
  
	def before_save(self):
		self.generate_seat_no()
		self.get_total_amount()
  
	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw(f"Cannot submit ticket no {self.name}. Passenger is not on board")
   
	# def after_submit(self):
	# 	self.status="Completed"
  
	def get_total_amount(self):
		total=0 +self.flight_price
		for addon in self.add_ons:
			if addon.amount:
				total += addon.amount
	
		self.total_amount = total
  
	def remove_duplicate_add_on_items(self):
		unique_add_on_types = []
		seen_add_on_types = set()

		for x in self.add_ons:
			if x.item not in seen_add_on_types:
				seen_add_on_types.add(x.item)
				unique_add_on_types.append(x)

		self.add_ons = unique_add_on_types
  
	def generate_seat_no(self):
		if not self.seat:
			random_integer = random.randint(1, 99)  # Adjust the range as needed
			random_letter = random.choice('ABCDE')
			self.seat = f"{random_integer}{random_letter}"
	def on_submit(self):
		
		available_seats = self.show_available_seats()
		frappe.publish_realtime(
			"show_available_seats", {"available_seats": available_seats}
		)
		self.check_plane_capacity()
	
   
	def check_plane_capacity(self):
		plane_capacity = frappe.db.get_all(
			"Airplane Flight",
			filters={"name": self.flight},
			fields=["airplane.capacity"],
		)[0].get("capacity", 0)

		number_of_tickets = frappe.db.get_all(
			"Airplane Ticket",
			filters={"flight": self.flight, "docstatus":1},
			fields=["COUNT(name) AS number_of_tickets"],
		)[0].get("number_of_tickets")

		if int(number_of_tickets) >= int(plane_capacity):
			frappe.throw("Flight is fully booked")
			
	@frappe.whitelist()
	def show_available_seats(self):
		plane_capacity = frappe.db.get_all(
			"Airplane Flight",
			filters={"name": self.flight},
			fields=["airplane.capacity"],
		)[0].get("capacity", 0)

		number_of_tickets = frappe.db.get_all(
			"Airplane Ticket",
			filters={"flight": self.flight, "docstatus":1},
			fields=["COUNT(name) AS number_of_tickets"],
		)[0].get("number_of_tickets")
		seats_available=plane_capacity - number_of_tickets
  
		if seats_available<0:
			seats_available=0
		return seats_available