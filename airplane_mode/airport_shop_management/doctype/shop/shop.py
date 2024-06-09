# Copyright (c) 2024, mania@navari.co.ke and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class Shop(WebsiteGenerator):
	pass
	def before_save(self):
		if not self.rent_fee:
			default_rent_fee = frappe.db.get_single_value('Airplane Mode settings', 'default_rent_fee')
			self.rent_fee = default_rent_fee
