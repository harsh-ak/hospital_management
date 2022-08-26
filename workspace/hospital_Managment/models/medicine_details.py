from odoo import fields, models,api,_
from datetime import date


class Medicine(models.Model):
    _name = "hospital.medicine" #This will be the table name.
    _description = "medicine"
    

    name=fields.Char(string="Medicine Name")
    med_type_id=fields.Many2one(comodel_name="hospital.medicinetype",string="Medicine Type")
    med_company_id=fields.Many2one(comodel_name="hospital.medicinecompany",string="Medicine Company")
    strips=fields.Integer(string="Strips Available")
