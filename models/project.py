from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    office_file_number = fields.Char(
        string="File Number in the Office",
        required=True,
        help="Internal reference number used by the law firm"
    )
    court_name = fields.Char(
        string="Court Name",
        required=True,
        help="Court Name"
    )
    court_circle = fields.Char(
        string="Court Circle",
        help="Court circle"
    )
    lawsuit_filing_date = fields.Date(
        string="Case Filing Date",
        required=True,
        help="The date on which the lawsuit was filed in court"
    )
    first_degree_case_number_year = fields.Char(
        string="First Degree Case Number",
        help="Number of the first degree case in court"
    )
    second_degree_case_number_year = fields.Char(
        string="Second Degree Case Number",
        help="Number of the appeal or second degree case in court"
    )
    client_status = fields.Char(
        string="Client Status",
        required=True,
        help="The client's status in the case e.g(Plaintiff, Defendant, Third Party, etc.)"
    )
    opponent_status = fields.Char(
        string="Opponent Status",
        required=True,
        help="The opponent's status in the case e.g(Plaintiff, Defendant, Third Party, etc.)"
    )
    opponent_name = fields.Char(
        string="Opponent's Name",
        required=True,
        help="Name of the opposing party"
    )
    opponent_address = fields.Text(
        string="Opponent's Address",
        help="Address of the opposing party"
    )
    opponent_phone = fields.Char(
        string="Opponent's Phone Number",
        help="Contact number of the opposing party"
    )
    opponent_attorney_name = fields.Char(
        string="Opponent's Attorney's Name",
        help="Name of the opposing attorney"
    )
    opponent_attorney_phone = fields.Char(
        string="Opponent's Attorney's Phone",
        help="Contact number of the opposing attorney"
    ) 