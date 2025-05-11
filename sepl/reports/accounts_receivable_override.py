import frappe
from frappe import _, qb, query_builder, scrub
from erpnext.accounts.report.accounts_receivable.accounts_receivable import ReceivablePayableReport as OriginalReceivablePayableReport
from collections import OrderedDict

from frappe.query_builder import Criterion
from frappe.query_builder.functions import Date, Substring, Sum
from frappe.utils import cint, cstr, flt, getdate, nowdate

from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
	get_dimension_with_children,
)
from erpnext.accounts.utils import get_currency_precision, get_party_types_from_account_type

def custom_execute(filters=None):
	args = {
		"account_type": "Receivable",
		"naming_by": ["Selling Settings", "cust_master_name"],
	}
	return CustomAccountsReceivable(filters).run(args)


class CustomAccountsReceivable(OriginalReceivablePayableReport):
	def __init__(self, filters):
		self.filters = filters
		super().__init__(filters)
		self.set_defaults()

	def run(self, args):
		super().run(args)

		self.get_columns()

		self.add_vessel_names()
		return self.columns, self.data

	def set_defaults(self):
		if not self.filters.get("company"):
			self.filters.company = frappe.db.get_single_value("Global Defaults", "default_company")

		self.company_currency = frappe.get_cached_value(
			"Company", self.filters.get("company"), "default_currency"
		)
		self.currency_precision = get_currency_precision() or 2
		self.dr_or_cr = "debit" if self.filters.account_type == "Receivable" else "credit"
		self.account_type = self.filters.account_type
		self.party_type = get_party_types_from_account_type(self.account_type)
		self.party_details = {}
		self.invoices = set()
		self.skip_total_row = 0

		if self.filters.get("group_by_party"):
			self.previous_party = ""
			self.total_row_map = {}
			self.skip_total_row = 1

		if self.filters.get("in_party_currency"):
			if self.filters.get("party") and len(self.filters.get("party")) == 1:
				self.skip_total_row = 0
			else:
				self.skip_total_row = 1

	def get_columns(self):
		self.columns = []
		# self.add_column("Posting Date", fieldtype="Date")
		# self.add_column(
		# 	label="Party Type",
		# 	fieldname="party_type",
		# 	fieldtype="Data",
		# 	width=100,
		# )
		# self.add_column(
		# 	label="Party",
		# 	fieldname="party",
		# 	fieldtype="Dynamic Link",
		# 	options="party_type",
		# 	width=180,
		# )
		# self.add_column(
		# 	label=self.account_type + " Account",
		# 	fieldname="party_account",
		# 	fieldtype="Link",
		# 	options="Account",
		# 	width=180,
		# )

		# if self.party_naming_by == "Naming Series":
		# 	if self.account_type == "Payable":
		# 		label = "Supplier Name"
		# 		fieldname = "supplier_name"
		# 	else:
		# 		label = "Customer Name"
		# 		fieldname = "customer_name"
		# 	self.add_column(
		# 		label=label,
		# 		fieldname=fieldname,
		# 		fieldtype="Data",
		# 	)

		# if self.account_type == "Receivable":
		# 	self.add_column(
		# 		_("Customer Contact"),
		# 		fieldname="customer_primary_contact",
		# 		fieldtype="Link",
		# 		options="Contact",
		# 	)

		# self.add_column(label=_("Cost Center"), fieldname="cost_center", fieldtype="Data")
		self.add_column(label=_("Voucher Type"), fieldname="voucher_type", fieldtype="Data")
		self.add_column(
			label=_("Voucher No"),
			fieldname="voucher_no",
			fieldtype="Dynamic Link",
			options="voucher_type",
			width=250,
		)
		self.add_column(
			label=_("Vessel name"),
			fieldname="custom_vessel_name",
			fieldtype="Data",
			width=120,
		)
		self.add_column(label="Due Date", fieldtype="Date")

		if self.account_type == "Payable":
			self.add_column(label=_("Bill No"), fieldname="bill_no", fieldtype="Data")
			self.add_column(label=_("Bill Date"), fieldname="bill_date", fieldtype="Date")

		if self.filters.based_on_payment_terms:
			self.add_column(label=_("Payment Term"), fieldname="payment_term", fieldtype="Data")
			self.add_column(label=_("Invoice Grand Total"), fieldname="invoice_grand_total")

		self.add_column(_("Invoiced Amount"), fieldname="invoiced")
		# self.add_column(_("Paid Amount"), fieldname="paid")
		# if self.account_type == "Receivable":
		# 	self.add_column(_("Credit Note"), fieldname="credit_note")
		# else:
		# 	# note: fieldname is still `credit_note`
		# 	self.add_column(_("Debit Note"), fieldname="credit_note")
		# self.add_column(_("Outstanding Amount"), fieldname="outstanding")

		self.setup_ageing_columns()

		# self.add_column(
		# 	label=_("Currency"), fieldname="currency", fieldtype="Link", options="Currency", width=80
		# )

		if self.filters.show_future_payments:
			self.add_column(label=_("Future Payment Ref"), fieldname="future_ref", fieldtype="Data")
			self.add_column(label=_("Future Payment Amount"), fieldname="future_amount")
			self.add_column(label=_("Remaining Balance"), fieldname="remaining_balance")

		if self.filters.account_type == "Receivable":
			self.add_column(label=_("Customer LPO"), fieldname="po_no", fieldtype="Data")

			# comma separated list of linked delivery notes
			if self.filters.show_delivery_notes:
				self.add_column(label=_("Delivery Notes"), fieldname="delivery_notes", fieldtype="Data")
			# self.add_column(
			# 	label=_("Territory"), fieldname="territory", fieldtype="Link", options="Territory"
			# )
			# self.add_column(
			# 	label=_("Customer Group"),
			# 	fieldname="customer_group",
			# 	fieldtype="Link",
			# 	options="Customer Group",
			# )
			if self.filters.show_sales_person:
				self.add_column(label=_("Sales Person"), fieldname="sales_person", fieldtype="Data")

			if self.filters.sales_partner:
				self.add_column(label=_("Sales Partner"), fieldname="default_sales_partner", fieldtype="Data")

		if self.filters.account_type == "Payable":
			self.add_column(
				label=_("Supplier Group"),
				fieldname="supplier_group",
				fieldtype="Link",
				options="Supplier Group",
			)

		if self.filters.show_remarks:
			self.add_column(label=_("Remarks"), fieldname="remarks", fieldtype="Text", width=200)

	# def add_column(self, label, fieldname=None, fieldtype="Currency", options=None, width=120):
	# 	if not fieldname:
	# 		fieldname = scrub(label)
	# 	if fieldtype == "Currency":
	# 		options = "currency"
	# 	if fieldtype == "Date":
	# 		width = 90

	# 	self.columns.append(
	# 		dict(label=label, fieldname=fieldname, fieldtype=fieldtype, options=options, width=width)
	# 	)

	def setup_ageing_columns(self):
		# for charts
		self.ageing_column_labels = []
		self.add_column(label=_("Age (Days)"), fieldname="age", fieldtype="Int", width=80)

		for i, label in enumerate(
			[
				"0-{range1}".format(range1=self.filters["range1"]),
				"{range1}-{range2}".format(
					range1=cint(self.filters["range1"]) + 1, range2=self.filters["range2"]
				),
				"{range2}-{range3}".format(
					range2=cint(self.filters["range2"]) + 1, range3=self.filters["range3"]
				),
				"{range3}-{range4}".format(
					range3=cint(self.filters["range3"]) + 1, range4=self.filters["range4"]
				),
				_("{range4}-Above").format(range4=cint(self.filters["range4"]) + 1),
			]
		):
			self.add_column(label=label, fieldname="range" + str(i + 1))
			self.ageing_column_labels.append(label)

	def get_invoice_details(self):
		self.invoice_details = frappe._dict()
		if self.account_type == "Receivable":
			si_list = frappe.db.sql(
				"""
				select name, due_date, po_no,custom_vessel_name
				from `tabSales Invoice`
				where posting_date <= %s
			""",
				self.filters.report_date,
				as_dict=1,
			)
			for d in si_list:
				self.invoice_details.setdefault(d.name, d)

			# Get Sales Team
			if self.filters.show_sales_person:
				sales_team = frappe.db.sql(
					"""
					select parent, sales_person
					from `tabSales Team`
					where parenttype = 'Sales Invoice'
				""",
					as_dict=1,
				)
				for d in sales_team:
					self.invoice_details.setdefault(d.parent, {}).setdefault("sales_team", []).append(
						d.sales_person
					)

		if self.account_type == "Payable":
			for pi in frappe.db.sql(
				"""
				select name, due_date, bill_no, bill_date
				from `tabPurchase Invoice`
				where posting_date <= %s
			""",
				self.filters.report_date,
				as_dict=1,
			):
				self.invoice_details.setdefault(pi.name, pi)

		# Invoices booked via Journal Entries
		journal_entries = frappe.db.sql(
			"""
			select name, due_date, bill_no, bill_date
			from `tabJournal Entry`
			where posting_date <= %s
		""",
			self.filters.report_date,
			as_dict=1,
		)

		for je in journal_entries:
			if je.bill_no:
				self.invoice_details.setdefault(je.name, je)

	def add_vessel_names(self):
		sinv_names = [row["voucher_no"] for row in self.data if row.get("voucher_type") == "Sales Invoice"]
		if not sinv_names:
			return

		vessel_map = frappe._dict({
			d.name: d.vessel_name
			for d in frappe.get_all("Sales Invoice", filters={"name": ["in", sinv_names]},
									fields=["name", "custom_vessel_name"])
		})

		for row in self.data:
			if row.get("voucher_type") == "Sales Invoice":
				row["vessel_name"] = vessel_map.get(row["voucher_no"], "")

	
