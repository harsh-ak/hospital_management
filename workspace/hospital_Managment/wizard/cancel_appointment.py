from odoo import fields, models,api,_
from datetime import date


class CancelAppoinment(models.TransientModel):
    _name = "cancel.appointment.wizard" #This will be the table name.
    _description = "Cancel Appointment"
    

    appointment_id=fields.Many2many(comodel_name="hospital.appointments",string="Patient Name")

    def button_cancel_appo(self):
        for rec in self:
            for res in rec.appointment_id:
                res.status="CANCEL"
        return {
        'type':'ir.actions.act_window',
        'name':'Appointments',
        'res_model':'hospital.appointments',
        #'domain':[('patient_name_id','=',self.id)],
        'view_mode':'tree,form',
        'target':'current'
        }        

