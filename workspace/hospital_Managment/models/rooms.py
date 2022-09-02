from odoo import fields, models,api,_
from datetime import date
from odoo.exceptions import ValidationError


class Room(models.Model):
    _name="hospital.room" #This will be the table name.
    _description="Rooms "


    name = fields.Selection([
        ('No Room Alloted','No Room Alloted'),
        ('101','101'),
        ('102','102'),
        ('103','103'),('104','104'),('105','105'),('201','201'),('202','202'),('203','203'),('204','204'),('205','205'),('301','301'),('302','302'),('303','303'),('304','304'),('305','305')],string="Room No")
    availability=fields.Selection([('Available','Available'),('Unavailable','Unavailable')],string="Availability",compute="_compute_avail")
    floor=fields.Selection([('1st','1st'),('2nd','2nd'),('3rd','3rd')],string=" On Which Floor")
    type_of=fields.Selection([('ICU','ICU'),('Normal','Normal')],string="Room Type")
    alloted_to=fields.Char(string="Alloted To",compute="_compute_patient")


    def _compute_patient(self):
        for rec in self:
            rec.alloted_to=""
            res=self.env['hospital.patient'].search([('room_id','=',rec.name)])
            for a in res:
                rec.alloted_to=a.name

        for rec in self:
            if rec.alloted_to:
                pass
            else:
                rec.alloted_to="No Room Alloted"



    def _compute_avail(self):
        for rec in self:
            rec.availability=""
            res=self.env['hospital.patient'].search([('room_id','=',rec.name)])
            for a in res:
                rec.availability="Unavailable"

        for rec in self:
            if rec.availability:
                pass
            else:
                rec.availability="Available"            




                            
                

            



