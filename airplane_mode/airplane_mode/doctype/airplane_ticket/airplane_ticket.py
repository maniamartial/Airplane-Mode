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
   
	def after_submit(self):
		self.status="Completed"
  
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