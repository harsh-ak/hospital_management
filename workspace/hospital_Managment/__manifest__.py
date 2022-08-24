
{
    'name': 'Hospital Management',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'This is Hospital Management System',
    'description': """
    This is Hospital Management System.
    """,
    'sequence':-500,
    'depends': ['base'],
    'data': [
    'security/ir.model.access.csv',
    'views/patients.xml',
    'views/menu.xml',
    'views/degree.xml',
    'views/doctor.xml',
    'views/doctor_type.xml',
    ],
    'installable':True,
    'auto_install':False,
    'images':['static/description/icon.png'],
    'application':True,
    'license': 'LGPL-3',
}