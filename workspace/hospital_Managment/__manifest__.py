
{
    'name': 'Hospital Management',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'This is Hospital Management System',
    'description': """
    This is Hospital Management System.
    """,
    'sequence':-500,
    'depends': ['base','mail'],
    'data': [
    "data/doctor_type_data.xml",
    'security/ir.model.access.csv',
    'wizard/cancel_appointment.xml',
    'views/patients.xml',
    'views/menu.xml',
    'views/degree.xml',
    'views/doctor.xml',
    'views/doctor_type.xml',
    'views/appointments.xml',
    'views/medicine.xml',
    'views/bills.xml',
    'views/room.xml',

    ],
    'installable':True,
    'auto_install':False,
    'images':['static/description/icon.png'],
    'application':True,
    'license': 'LGPL-3',
}