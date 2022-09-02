from odoo import fields, models,api,_
from datetime import date


class Bill(models.Model):
    _name = "hospital.bill" #This will be the table name.
    _description = "Hospital Bill"
    _rec_name="patient_id"

    patient_id=fields.Many2one(string="Patient name",comodel_name="hospital.patient")
    medicine_ids=fields.Many2many(comodel_name="hospital.medicine",string="Medicines To Buy",compute="cal_meds")
    price=fields.Char(string="Total Bill(Rs)",store=True,compute="cal_bill")
    vis_charge=fields.Integer(string="Visiting Charge",compute="cal_doc")
    visited_doctor=fields.Char(string="Visited Doctor",compute="cal_meds")
    med_charge=fields.Integer(string="Medicine Charge")


    @api.depends('patient_id')
    def cal_meds(self):
        for rec in self:
            rec.medicine_ids = False
            rec.visited_doctor = False
            if rec.patient_id:
                print("computing medicine_ids for---",rec)
                # res=self.env['hospital.patient'].search([('id','=',rec.patient_id.id)])
                rec.medicine_ids = rec.patient_id.med_presc_ids
                rec.visited_doctor = rec.patient_id.doctor_id.name


    @api.depends('visited_doctor')
    def cal_doc(self):
        for rec in self:
            res=self.env['hospital.doctor'].search([('name','=',rec.visited_doctor)])
            rec.vis_charge=res.visiting_charge



    @api.depends('medicine_ids')
    def cal_bill(self):
        summ=0
        for rec in self:
            print("computing bill for---",rec)
            rec.price=""
            # rec.vis_charge=0
            for meds in rec.medicine_ids:
                summ+=meds.strip_price
            print("_________",rec.vis_charge)
            rec.med_charge=summ    
            summ+=rec.vis_charge   
            rec.price=str(summ)+".00 ₹"

    # @api.depends('medicine_ids')
    # def cal_bill(self):
    #     summ=0
    #     for rec in self: 
    #         rec.price=""
    #         # rec.vis_charge=0
    #         for meds in rec.medicine_ids:
    #             summ+=meds.strip_price
    #         #print("_________",rec.vis_charge)    
    #         #summ+=rec.vis_charge   
    #         rec.med_charge=summ          

            

                       
