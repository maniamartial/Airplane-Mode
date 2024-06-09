# Copyright (c) 2024, mania@navari.co.ke and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopContract(Document):
	pass

	def before_submit(self):
		active_contracts=frappe.get_all("Shop Contract", filters={"status":"Active"}, fields=["*"])
		for contract in active_contracts:
			if contract.shop==self.shop:
				frappe.throw(f"Shop {self.shop} already has an <strong>Active contract</strong>")
