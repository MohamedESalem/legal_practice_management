from odoo import models, fields, api, _

class ProjectProject(models.Model):
    _inherit = 'project.project'
    _description = 'Legal Case Project'

    office_file_number = fields.Char(
        string=_("File Number in the Office"),
        # required=True,
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

    @api.model
    def _get_context_tag(self):
        """Determine which tag to add based on the current context."""
        # Check if we're in the Cases context
        if self.env.context.get('default_tag_ids') or self.env.context.get('tag_ids'):
            # If tags are already specified in context, don't add defaults
            return None
            
        # Check if we're creating from Cases app (action_view_project_cases_strict)
        if self.env.context.get('params', {}).get('action') == self.env.ref('legal_case_management.action_view_project_cases_strict', raise_if_not_found=False).id:
            return self.env.ref('legal_case_management.project_tag_case', raise_if_not_found=False)
        
        # Check if we're creating from Matters app (action_view_project_matters)
        if self.env.context.get('params', {}).get('action') == self.env.ref('legal_matter_management.action_view_project_matters', raise_if_not_found=False).id:
            return self.env.ref('legal_matter_management.project_tag_matter', raise_if_not_found=False)
        
        # Check for specific context keys that might indicate the source
        if self.env.context.get('create_from_cases'):
            return self.env.ref('legal_case_management.project_tag_case', raise_if_not_found=False)
        
        if self.env.context.get('create_from_matters'):
            return self.env.ref('legal_matter_management.project_tag_matter', raise_if_not_found=False)
        
        return None

    @api.model
    def _default_tag_ids(self):
        """Default method to add appropriate tag based on context."""
        tag = self._get_context_tag()
        if tag:
            return [(4, tag.id)]
        return []

    tag_ids = fields.Many2many(
        'project.tags',
        string='Tags',
        default=_default_tag_ids,
        help=_("Tags for categorizing projects")
    )

    @api.model
    def create(self, vals):
        """Override create method to automatically add appropriate tag based on context."""
        # Get the appropriate tag based on context
        tag = self._get_context_tag()
        
        if tag:
            # Initialize tag_ids if not present
            if 'tag_ids' not in vals:
                vals['tag_ids'] = []
            
            # Add the tag if it's not already in the list
            if isinstance(vals['tag_ids'], list):
                # Handle list of commands format
                tag_ids = vals['tag_ids']
                tag_id = tag.id
                
                # Check if tag is already in the list
                tag_exists = any(
                    isinstance(cmd, tuple) and len(cmd) >= 2 and cmd[1] == tag_id
                    for cmd in tag_ids
                )
                
                if not tag_exists:
                    vals['tag_ids'].append((4, tag_id))
            else:
                # Handle direct list of IDs format
                if isinstance(vals['tag_ids'], (list, tuple)):
                    if tag.id not in vals['tag_ids']:
                        vals['tag_ids'].append(tag.id)
        
        return super().create(vals) 