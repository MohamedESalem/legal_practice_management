from odoo import models, fields, api, _

class ProjectProject(models.Model):
    _inherit = 'project.project'
    _description = 'Legal Case Project'

    office_file_number = fields.Char(
        string=_("File Number in the Office"),
        required=True,
        help=_("Internal reference number used by the law firm")
    )
    court_name = fields.Char(
        string=_("Court Name"),
        help=_("Court Name")
    )
    court_circle = fields.Char(
        string=_("Court Circle"),
        help=_("Court circle")
    )
    lawsuit_filing_date = fields.Date(
        string=_("Case Filing Date"),
        help=_("The date on which the lawsuit was filed in court")
    )
    first_degree_case_number_year = fields.Char(
        string=_("First Degree Case Number"),
        help=_("Number of the first degree case in court")
    )
    second_degree_case_number_year = fields.Char(
        string=_("Second Degree Case Number"),
        help=_("Number of the appeal or second degree case in court")
    )
    client_status = fields.Char(
        string=_("Client Status"),
        help=_("The client's status in the case e.g(Plaintiff, Defendant, Third Party, etc.)")
    )
    opponent_status = fields.Char(
        string=_("Opponent Status"),
        help=_("The opponent's status in the case e.g(Plaintiff, Defendant, Third Party, etc.)")
    )
    opponent_name = fields.Char(
        string=_("Opponent's Name"),
        help=_("Name of the opposing party")
    )
    opponent_address = fields.Text(
        string=_("Opponent's Address"),
        help=_("Address of the opposing party")
    )
    opponent_phone = fields.Char(
        string=_("Opponent's Phone Number"),
        help=_("Contact number of the opposing party")
    )
    opponent_attorney_name = fields.Char(
        string=_("Opponent's Attorney's Name"),
        help=_("Name of the opposing attorney")
    )
    opponent_attorney_phone = fields.Char(
        string=_("Opponent's Attorney's Phone"),
        help=_("Contact number of the opposing attorney")
    ) 