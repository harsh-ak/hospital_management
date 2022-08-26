from odoo import fields, models,api,_
from datetime import date


class MedicineType(models.Model):
    _name = "hospital.medicinetype" #This will be the table name.
    _description = "medicine type"

    name=fields.Char(string="Medicine Type")