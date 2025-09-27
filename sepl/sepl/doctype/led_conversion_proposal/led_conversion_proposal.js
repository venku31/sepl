// Copyright (c) 2024, SEPL and contributors
// For license information, please see license.txt

frappe.ui.form.on('LED Conversion Proposal', {
	validate: function(frm) {
		(frm.doc.proposal_detals || []).forEach(function(d) {
			d.installed_bf_power_conversion = d.units * d.wattage;

			// Condition for DECK or Deck
			if (d.location === "DECK" || d.location === "Deck") {
				d.power_before_conversion_at_sea = 0;
                                d.power_after_conversion_at_sea = 0;
			} else {
				d.power_before_conversion_at_sea = d.installed_bf_power_conversion * d.usage_factor * 0.6;
                                d.power_after_conversion_at_sea = d.installed_power_af_conversion * d.usage_factor * 0.6;
			}

			d.installed_power_af_conversion = d.sepl_wattage * d.qty;
			// d.power_after_conversion_at_sea = d.installed_power_af_conversion * d.usage_factor * 0.6;
			d.power_before_conversion_at_port = d.units * d.wattage * d.usage_factor * 0.4;
			d.power_after_conversion_at_port = d.sepl_wattage * d.qty * d.usage_factor * 0.4;

			d.power_consumption_per_year_before_conversion_in_kwh =
				(d.power_before_conversion_at_sea + d.power_before_conversion_at_port) * 24 * 365 / 1000;

			d.power_consumption_per_year_after_conversion_in_kwh =
				(d.power_after_conversion_at_sea + d.power_after_conversion_at_port) * 24 * 365 / 1000;
		});

		// Call your total calculation function (make sure it's defined elsewhere)
		main_total_qty(frm);
	}
});

function main_total_qty(frm) {
	if (!frm.doc.proposal_detals) return;

	let installed_bf_power_conversion = 0;
	let power_before_conversion_at_sea = 0;
	let power_before_conversion_at_port = 0;
	let installed_power_af_conversion = 0;
	let power_after_conversion_at_sea = 0;
	let power_after_conversion_at_port = 0;
	let power_consumption_per_year_before_conversion_in_kwh = 0;
	let power_consumption_per_year_after_conversion_in_kwh = 0;

	frm.doc.proposal_detals.forEach(function(d) {
		installed_bf_power_conversion += flt(d.installed_bf_power_conversion);
		power_before_conversion_at_sea += flt(d.power_before_conversion_at_sea);
		power_before_conversion_at_port += flt(d.power_before_conversion_at_port);
		installed_power_af_conversion += flt(d.installed_power_af_conversion);
		power_after_conversion_at_sea += flt(d.power_after_conversion_at_sea);
		power_after_conversion_at_port += flt(d.power_after_conversion_at_port);
		power_consumption_per_year_before_conversion_in_kwh += flt(d.power_consumption_per_year_before_conversion_in_kwh);
		power_consumption_per_year_after_conversion_in_kwh += flt(d.power_consumption_per_year_after_conversion_in_kwh);
	});

	let power_savings = power_consumption_per_year_before_conversion_in_kwh - power_consumption_per_year_after_conversion_in_kwh;
	let fuel_saving_per_year = ((power_consumption_per_year_before_conversion_in_kwh - power_consumption_per_year_after_conversion_in_kwh) * 220) / 1000000;
	let fuel_cost_saving__per_year = fuel_saving_per_year * 650;
	let co2_saving_per_year = fuel_saving_per_year * 3.5;

	frm.set_value('installed_bf_power_conversion', installed_bf_power_conversion);
	frm.set_value('power_before_conversion_at_sea', power_before_conversion_at_sea);
	frm.set_value('power_before_conversion_at_port', power_before_conversion_at_port);
	frm.set_value('installed_power_af_conversion', installed_power_af_conversion);
	frm.set_value('power_after_conversion_at_sea', power_after_conversion_at_sea);
	frm.set_value('power_after_conversion_at_port', power_after_conversion_at_port);
	frm.set_value('power_consumption_per_year_before_conversion_in_kwh', power_consumption_per_year_before_conversion_in_kwh);
	frm.set_value('power_consumption_per_year_after_conversion_in_kwh', power_consumption_per_year_after_conversion_in_kwh);
	frm.set_value('power_savings', power_savings);
	frm.set_value('power_saving_per_year', power_after_conversion_at_port);
	frm.set_value('fuel_saving_per_year', fuel_saving_per_year);
	frm.set_value('fuel_cost_saving__per_year', fuel_cost_saving__per_year);
	frm.set_value('co2_saving_per_year', co2_saving_per_year);
}



frappe.ui.form.on("LED Conversion Proposal", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Create Quotation'), function() {
                frappe.call({
                    method: "sepl.sepl.doctype.led_conversion_proposal.led_conversion_proposal.create_quotation",
                    args: {
                        proposal: frm.doc.name
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.set_route("Form", "Quotation", r.message);
                        }
                    }
                });
            }, __("Create"));
        }
    }
});
