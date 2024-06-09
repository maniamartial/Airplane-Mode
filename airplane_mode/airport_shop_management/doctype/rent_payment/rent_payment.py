# Copyright (c) 2024, mania@navari.co.ke and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):
	pass
	def before_submit(self):
		send_email_to_shop_owner(self.shop, self.amount)
		update_contract_status(self.contract, self.to)
		
def send_email_to_shop_owner(shop, amount):
	shop_owner = frappe.get_doc("Shop", shop)
	shop_owner_email = shop_owner.email
	if shop_owner_email:
		frappe.sendmail(
			recipients=shop_owner_email,
			subject="Rent Payment",
			message=f"Dear {shop_owner},\n\nWe have received a payment of {amount} for your shop {shop}.\n\Tenants name: {frappe.session.user}\n\nThank you for your business.\n\nRegards,\n\nAirplane Mode Team",
		)
	frappe.msgprint(f"Email sent to {shop_owner_email}")
 
def update_contract_status(contract, to_date):
	contract_doc=frappe.get_doc("Shop Contract", contract)
	contract_doc.status="Active"
	contract_doc.expiry_date=to_date
	contract_doc.save()
	
def schedular_update_status_contract_expire():
	contracts=frappe.get_all("Shop Contract", filters={"status":"Active"})
	for contract in contracts:
		contract_doc=frappe.get_doc("Shop Contract", contract)
		
		difference=frappe.utils.date_diff(contract_doc.expiry_date, frappe.utils.nowdate())
		if difference <=0:
			contract_doc.status="Expired"
			contract_doc.save()
			tenant_email=get_tenant_email(contract_doc)
			enable_notifications=frappe.db.get_single_value("Airplane Mode Settings", "enable_due_rent_reminder")
			if enable_notifications:
				frappe.sendmail(
					recipients=tenant_email,
					subject="Contract Expired",
					message=f"Dear {contract_doc.tenant},\n\nYour contract for shop {contract_doc.shop} has expired.\n\nRegards,\n\nAirplane Mode Team",
				)
	change_shop_status(contract_doc)
 
 
def get_tenant_email(contract_doc):
	tenant=contract_doc.tenant
	tenant_doc=frappe.get_doc("Tenant", tenant)
	tenant_email=tenant_doc.email
	return tenant_email

def change_shop_status(contract_doc):
	shop=contract_doc.shop
	shop_doc=frappe.get_doc("Shop", shop)
	if contract_doc.status=="Active":
		shop_doc.status="Occupied"
	elif contract_doc.status=="Expired":
		shop_doc.status="Vacant"
	shop_doc.save()
			
		