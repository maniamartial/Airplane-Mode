# Copyright (c) 2024, mania@navari.co.ke and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CrewMember(Document):
	pass

	def before_save(self):
		if self.last_name:
			self.full_name =f"{self.first_name} {self.last_name}"
		else:
			self.full_name = self.first_name
