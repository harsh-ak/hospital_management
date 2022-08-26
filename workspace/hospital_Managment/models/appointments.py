from odoo import fields, models,api,_
from datetime import date


class Appointments(models.Model):
    _name = "hospital.appointments" #This will be the table name.
    _description = "appointments"
    _rec_name = "patient_name_id"

    patient_name_id=fields.Many2one(comodel_name="hospital.patient",string="Patient Name")
    doctor_name=fields.Char(compute="_compute_doctor",string="Responsible Doctor",store=True)
    status_id=fields.Many2one(comodel_name="hospital.status",string="Status")

    @api.depends('patient_name_id')
    def _compute_doctor(self):
    	doctor_name=""
    	for rec in self:
    		res=self.env['hospital.patient'].search([('name','=',rec.patient_name_id.name)])
    		rec.doctor_name=res.doctor_id.name



    def count_app(self):
        # print("Button clicked_--------________________")
        # print("_________self_________",self)       		
        res=self.status_id.name
        a=""
        message="Appointment Status is:"+res
        if res=="DONE":
            a="success"
        else:
            a="warning"    

        print("_____",res)
        return{
        'type':'ir.actions.client',
        'tag':'display_notification',

        'params':{
        'message':message,
        'type':a,
        'sticky':False


        }



        }


    