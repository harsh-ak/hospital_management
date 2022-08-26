from odoo import fields, models,api,_
from datetime import date


class MedicineCompany(models.Model):
    _name = "hospital.medicinecompany" #This will be the table name.
    _description = "medicine company"

    name=fields.Char(string="Medicine Company")
