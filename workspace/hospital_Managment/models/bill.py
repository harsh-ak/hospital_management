from odoo import fields, models,api,_
from datetime import date


class Bill(models.Model):
    _name = "hospital.bill" #This will be the table name.
    _description = "Hospital Bill"

    patient_id=fields.Many2one(string="Patient name",comodel_name="hospital.patient")
    medicine_ids=fields.Many2many(comodel_name="hospital.medicine",string="Medicines Prescribed")


    # @api.onchange('patient_id')
    # def 