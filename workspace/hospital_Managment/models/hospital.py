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
        vals['name']="Dr."+"  "+vals['f_name']+"  "+ (vals['l_name'] or '')
        res=super(Doctor,self).create(vals)
        return res

    def write(self,vals):
        if  self.f_name and self.l_name:
            vals['name']="Dr."+"  "+vals['f_name']+"  "+vals['l_name']
            res=super(Doctor,self).write(vals)
            return res
        else:
            res=super(Doctor,self).write(vals)
            return res

    def unlink(self):
        if self.type_id.name=='Cardiologists':
            raise ValidationError(_("You cannot delete an Cardiologists Doctor."))   
        else:
            return super(Doctor,self).unlink()      




class HospitalPatient(models.Model):
    _name="hospital.patient" #This will be the table name.
    _description="Hospital Patient Table "

    #This all will be the columns of the table.
    name=fields.Char(string='Name')
    age=fields.Integer(string='Age',compute="_compute_age",inverse="_inverse_type_of_pat", store=True)
    birthdate=fields.Date(string='Birthdate')
    weight=fields.Float(string='Weight(kgs)')
    refdoctor_id=fields.Many2one(comodel_name='hospital.doctor', string="Referred By")
    doctor_id=fields.Many2one(comodel_name='hospital.doctor', string="Responsible Doctor")
    type_of_patient=fields.Char(string='type')
    image=fields.Image(string='Image')

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


class Status(models.Model):
    _name="hospital.status" #This will be the table name.
    _description="Status"

    name=fields.Char(string=("Status"))



 











