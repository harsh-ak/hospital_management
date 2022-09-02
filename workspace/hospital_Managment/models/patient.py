from odoo import fields, models,api,_
from datetime import date
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name="hospital.patient" #This will be the table name.
    _description="Hospital Patient Tablee "
    _inherit=['mail.thread','mail.activity.mixin']

    #This all will be the columns of the table.
    name=fields.Char(string='Name',tracking=True)
    age=fields.Integer(string='Age',compute="_compute_age",inverse="_inverse_type_of_pat", store=True)
    birthdate=fields.Date(string='Birthdate')
    weight=fields.Float(string='Weight(kgs)')
    refdoctor_id=fields.Many2one(comodel_name='hospital.doctor', string="Referred By")
    doctor_id=fields.Many2one(comodel_name='hospital.doctor', string="Responsible Doctor")
    type_of_patient=fields.Char(string='type')
    image=fields.Image(string='Image')
    no_of_appo=fields.Integer(string="Appointments",compute="get_no_of_appo")
    med_presc_ids=fields.Many2many(string="Medicines Prescribed",comodel_name="hospital.medicine")
    no_of_meds=fields.Integer(string="Medicines",compute="get_no_of_meds")
    room_id=fields.Many2one(string="Room Alloted",comodel_name="hospital.room")

    city_id=fields.Many2one(comodel_name='hospital.city',string='City')

    @api.model
    def create(self,vals):
        res = super(HospitalPatient, self).create(vals)
        if vals.get('refdoctor_id', False):
            self.env['hospital.reference'].create({
                'name': "%s -> %s" % (res.name, res.doctor_id.name),
                'patient_id': res.id,
                'referer_id': vals.get('refdoctor_id', False),
                'refered_to_id': vals.get('doctor_id', False),
            })
        
        return res



    def write(self, vals):
        x = vals.get('x')
        if vals.get('refdoctor_id', False):
            old_refdoctor = self.refdoctor_id
            res = super(HospitalPatient, self).write(vals)

            if old_refdoctor:
                print("update relation of rec")
            else:
                self.env['hospital.reference'].create({
                    'name': "%s -> %s -> %s" % (self.refdoctor_id.name,self.doctor_id.name,self.name),
                    'patient_id': self.id,
                    'referer_id': self.refdoctor_id.id,
                    'refered_to_id': self.doctor_id.id,
                })
            return res
        else:
            return super(HospitalPatient, self).write(vals)

    def unlink(self):
        """Override method to unlink hospital references that is linked to patient"""
        for record in self:
            hospital_references = self.env['hospital.reference'].search([('patient_id','=',record.id)])
            print(hospital_references,"-------------hospital_references------\n\n")
            res = super(HospitalPatient,self).unlink()
            hospital_references.unlink()
            return res

    
    # *** Search ***
    # hospital_references = self.env['hospital.reference'].search([('patient_id','=',record.id)],limit=4)
    # print(hospital_references,"---------without limit---------\n\n")
    # hospital_references = self.env['hospital.reference'].search([('patient_id','=',record.id)],limit=4,order='refered_to_id')
    # print(hospital_references,"-----------with limit-----------\n\n")

    # *** Browse ***
    # hospital_references = self.env['hospital.reference'].search([('patient_id','=',record.id)]).ids
    # browse_hr = self.env['hospital.reference'].browse(hospital_references)
    # print(browse_hr.refered_to_id,"-----------browse_hr-------")
    # res = super(HospitalPatient,self).unlink()

    @api.depends('birthdate')
    def _compute_age(self):
        for rec in self:
            rec.age =0
            
            if rec.birthdate:
                birthDate = rec.birthdate
                today = date.today()
                age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day))

                
                rec.age = age
    @api.depends('age')
    def _inverse_type_of_pat(self):
        for rec in self:
            type_of_patient = " "
            if rec.age:
                if rec.age>18:
                    type_of_patient="Major"
                else:
                    type_of_patient="Minor"
            rec.type_of_patient = type_of_patient 


    def get_no_of_appo(self):
        for rec in self:
            res=self.env["hospital.appointments"].search_count([('patient_name_id','=',rec.id)])
            rec.no_of_appo=res

    def co_appointment(self):
        print("inside smart button_____________")

        return {
        'type':'ir.actions.act_window',
        'name':'Appointments',
        'res_model':'hospital.appointments',
        'domain':[('patient_name_id','=',self.id)],
        'view_mode':'tree,form',
        'target':'current'
        }              
    def get_no_of_meds(self):
        for rec in self:
            rec.no_of_meds=0
            res=len(rec.med_presc_ids.ids)
            rec.no_of_meds=res

    def co_medicines(self):
        print("________meds",self.med_presc_ids.ids) 
        return {
        'type':'ir.actions.act_window',
        'name':'Medicines',
        'res_model':'hospital.medicine',
        'domain':[('id','=',self.med_presc_ids.ids)],
        'view_mode':'tree,form',
        'target':'current'
        }

    @api.onchange('room_id')    
    def cal_room(self):
        for rec in self:
            print("_____________________________________")
            if rec.room_id.name=="Unavailable":
                print("______________________mde che")    