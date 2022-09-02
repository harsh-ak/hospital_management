from odoo import fields, models,api,_
from datetime import date
from odoo.exceptions import ValidationError


class Doctor(models.Model):
    _name="hospital.doctor" #This will be the table name.
    _description="Hospital Doctor Table "

    f_name=fields.Char(string="First Name")
    l_name=fields.Char(string="Last Name")
    name=fields.Char(string='Name')
    age=fields.Integer(string='Age',compute="_computee_age",store=True)
    birthdate=fields.Date(string='Birthdate')
    image=fields.Image(string='Image')
    type_id=fields.Many2one(comodel_name='hospital.typesofdoc',string="Type of Doctor")
    degree_ids=fields.Many2many(comodel_name='hospital.degree',string='Degree')
    reference_ids = fields.One2many(comodel_name="hospital.reference", inverse_name="referer_id", string="References Provided")
    no_of_patients_count = fields.Integer(string=_('Patients Assigned'),compute='_compute_patients_count')
    no_degree_count = fields.Integer(string=_('Total Degrees'),compute='_compute_degree_count',store=True)
    visiting_charge=fields.Integer(string="Visiting Charge(Rs)")



    
    def _compute_patients_count(self):
        print('Self---------',self)
        for rec in self:
            print('Current record---Data computed for',rec)
            print('Doctor name---Data computed for',rec.name)
            rec.no_of_patients_count = 0
            patients = self.env['hospital.patient'].search_count([('doctor_id','=',rec.id)])
            # doctors = rec.search_count([('type_id','=',self.env.ref('hospital_Managment.type_oncologist').id)])
            # print(doctors,"---------doctors--------\n\n")
            rec.no_of_patients_count = patients
            print('Number of Patients-----',rec.no_of_patients_count)

    def _compute_degree_count(self):
        for rec in self:
            rec.no_degree_count=0
            rec.no_degree_count = len(rec.degree_ids.ids)
        


    @api.depends('birthdate')
    def _computee_age(self):
        for rec in self:
            #rec.age =0
            print("aaaaaaaaa",rec)
            if rec.birthdate:
                birthDate = rec.birthdate
                today = date.today()
                age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day))

                print ("SSSSSSSSSSSSSS",age)
                rec.age = age


    @api.model
    def create(self,vals):
        print(vals,"---------------------")
        vals['name']="Dr."+"  "+(vals['f_name'] or '')+"  "+ (vals['l_name'] or '')
        res=super(Doctor,self).create(vals)
        return res

    # def write(self,vals):
    #     if  self.f_name and self.l_name:
    #         vals['name']="Dr."+"  "+vals['f_name']+"  "+vals['l_name']
    #         res=super(Doctor,self).write(vals)
    #         return res
    #     else:
    #         res=super(Doctor,self).write(vals)
    #         return res

    def unlink(self):
        if self.type_id.name=='Cardiologists':
            raise ValidationError(_("You cannot delete an Cardiologists Doctor."))   
        else:
            return super(Doctor,self).unlink()