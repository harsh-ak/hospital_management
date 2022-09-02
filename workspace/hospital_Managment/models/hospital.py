from odoo import fields, models,api,_
from datetime import date
from odoo.exceptions import ValidationError

class Degree(models.Model):
    _name = "hospital.degree" #This will be the table name.
    _description = "Degree"
    _rec_name = "degree"

    degree = fields.Char(string='Degree')

    

class HospitalReference(models.Model):
    _name="hospital.reference" #This will be the table name.
    _description="References"
    _order = 'id desc'

    name=fields.Char(string='Name')
    patient_id=fields.Many2one(comodel_name='hospital.patient',string='Patient')
    referer_id=fields.Many2one(comodel_name='hospital.doctor',string='Refered By')
    refered_to_id=fields.Many2one(comodel_name='hospital.doctor',string='Refered To')


class City(models.Model):
    _name="hospital.city" #This will be the table name.
    _description="Hospital City Table "


    name=fields.Char(string='City')
    zip_code=fields.Integer(string='Zip Code')

class TypeOfDoctor(models.Model):
    _name="hospital.typesofdoc" #This will be the table name.
    _description="Types Of Doctor Table"

    name=fields.Char(string="Doctor Types")



      




              




 











