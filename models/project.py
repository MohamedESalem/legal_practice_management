import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from .constants import (
    DEFAULT_PIPELINE_TYPE,
    MATTER_TO_PIPELINE,
    PIPELINE_TO_MATTER,
    PIPELINE_TYPE_SELECTION,
)

_logger = logging.getLogger(__name__)

class ProjectProject(models.Model):
    _inherit = 'project.project'
    _description = 'Legal Case Project'

    # ========== Field Overrides ==========
    partner_id = fields.Many2one(required=False)
    allow_billable = fields.Boolean(default=True)

    # ========== ORM Overrides ==========
    @api.model
    def _get_context_pipeline_type(self):
        """Get the pipeline type from context in a backward-compatible way."""
        pipeline_type = (
            self.env.context.get('pipeline_board_type')
            or self.env.context.get('default_pipeline_type')
        )
        if pipeline_type in dict(PIPELINE_TYPE_SELECTION):
            return pipeline_type
        if self.env.context.get('create_from_cases'):
            return 'litigation'
        if self.env.context.get('create_from_matters'):
            return 'legal_subject'
        return False

    @api.model
    def _default_pipeline_type(self):
        return self._get_context_pipeline_type() or DEFAULT_PIPELINE_TYPE

    @api.model
    def _sync_pipeline_and_matter_vals(self, vals):
        """Keep pipeline_type and matter_type synchronized in both directions."""
        vals = dict(vals)

        if vals.get('pipeline_type') in PIPELINE_TO_MATTER:
            vals['matter_type'] = PIPELINE_TO_MATTER[vals['pipeline_type']]
            return vals

        if vals.get('matter_type') in MATTER_TO_PIPELINE:
            vals['pipeline_type'] = MATTER_TO_PIPELINE[vals['matter_type']]
            return vals

        context_pipeline = self._get_context_pipeline_type()
        if context_pipeline:
            vals.setdefault('pipeline_type', context_pipeline)
            vals.setdefault('matter_type', PIPELINE_TO_MATTER[context_pipeline])
            return vals

        context_matter = self.env.context.get('default_matter_type')
        if context_matter in MATTER_TO_PIPELINE:
            vals.setdefault('matter_type', context_matter)
            vals.setdefault('pipeline_type', MATTER_TO_PIPELINE[context_matter])
            return vals

        vals.setdefault('pipeline_type', DEFAULT_PIPELINE_TYPE)
        vals.setdefault('matter_type', PIPELINE_TO_MATTER[vals['pipeline_type']])
        return vals

    def _get_first_stage_for_pipeline(self, pipeline_type, company_id=False):
        """Return the first available board stage for a pipeline."""
        if not pipeline_type:
            return self.env['project.project.stage']

        domain = [('pipeline_type', '=', pipeline_type)]
        if company_id:
            domain += ['|', ('company_id', '=', False), ('company_id', '=', company_id)]
        return self.env['project.project.stage'].search(domain, order='sequence, id', limit=1)

    @api.model
    def _default_stage_id(self):
        """Default stage should match the chosen pipeline whenever possible."""
        pipeline_type = self._get_context_pipeline_type() or DEFAULT_PIPELINE_TYPE
        company_id = self.env.context.get('default_company_id')
        stage = self._get_first_stage_for_pipeline(pipeline_type, company_id=company_id)
        return stage or super()._default_stage_id()

    @api.model
    def _read_group_expand_full(self, groups, domain):
        """Filter stage columns by pipeline in pipeline-specific Kanban actions."""
        pipeline_type = (
            self.env.context.get('pipeline_board_type')
            or self.env.context.get('default_pipeline_type')
        )
        if groups._name == 'project.project.stage' and pipeline_type in dict(PIPELINE_TYPE_SELECTION):
            allowed_company_ids = self.env.context.get('allowed_company_ids') or [self.env.company.id]
            stage_domain = [
                ('pipeline_type', '=', pipeline_type),
                ('company_id', 'in', [False, *allowed_company_ids]),
            ]
            return groups.search(stage_domain, order=f"sequence asc, {groups._order}")
        return super()._read_group_expand_full(groups, domain)

    def write(self, vals):
        """Override write to handle file number locking."""
        vals = dict(vals)

        if 'office_file_number' in vals and any(rec.is_file_number_locked for rec in self):
            raise UserError(_(
                "File number cannot be modified once it has been set and saved."
            ))
        
        # Set the lock if office_file_number is being set
        if 'office_file_number' in vals and vals.get('office_file_number') and not self._context.get('skip_lock_update'):
            vals['is_file_number_locked'] = True

        if 'pipeline_type' in vals or 'matter_type' in vals:
            vals = self._sync_pipeline_and_matter_vals(vals)

        if 'pipeline_type' in vals and 'stage_id' not in vals:
            for record in self:
                record_vals = dict(vals)
                if record.stage_id and record.stage_id.pipeline_type != record_vals['pipeline_type']:
                    stage = self._get_first_stage_for_pipeline(
                        record_vals['pipeline_type'],
                        company_id=record_vals.get('company_id', record.company_id.id),
                    )
                    record_vals['stage_id'] = stage.id if stage else False
                super(ProjectProject, record).write(record_vals)
            return True
            
        return super().write(vals)
    
    # ========== Field Definitions ==========
    pipeline_type = fields.Selection(
        PIPELINE_TYPE_SELECTION,
        required=True,
        default=_default_pipeline_type,
        tracking=True,
        index=True,
    )

    matter_type = fields.Selection(
        [
            ('case', 'Legal Case'),
            ('subject', 'Legal Subject')
        ],
        required=True,
        default='subject',
        tracking=True
    )

    stage_id = fields.Many2one(
        domain="['&', ('pipeline_type', '=', pipeline_type), '|', ('company_id', '=', False), ('company_id', '=?', company_id)]"
    )
    
    office_file_number = fields.Integer(
        string=_("File Number in the Office"),
        # required=True,
        help=_("Internal reference number used by the law firm (positive integers only)"),
        readonly=False,
        copy=False,
        index=True  # For faster lookups
    )
    
    is_file_number_locked = fields.Boolean(
        string="File Number Locked",
        default=False,
        copy=False,
        help="Indicates if the file number is locked from editing"
    )
    
    # Legal Case Information
    court_name = fields.Char(string=_("Court Name"))
    court_circle = fields.Char(string=_("Court Circle"))
    lawsuit_filing_date = fields.Date(string=_("Lawsuit Filing Date"))
    first_degree_case_number_year = fields.Char(
        string=_("First Degree Case Number/Year")
    )
    second_degree_case_number_year = fields.Char(
        string=_("Second Degree Case Number/Year")
    )
    
    # Client Information
    client_status = fields.Selection(
        [('plaintiff', _('Plaintiff')), ('defendant', _('Defendant'))],
        string=_("Client Status")
    )
    
    # Opponent Information
    opponent_status = fields.Selection(
        [('plaintiff', _('Plaintiff')), ('defendant', _('Defendant'))],
        string=_("Opponent Status")
    )
    opponent_name = fields.Char(string=_("Opponent Name"))
    opponent_address = fields.Text(string=_("Opponent Address"))
    opponent_phone = fields.Char(string=_("Opponent Phone"))
    opponent_attorney_name = fields.Char(string=_("Opponent Attorney Name"))
    opponent_attorney_phone = fields.Char(string=_("Opponent Attorney Phone"))

    # ========== File Number Generation Methods ==========
    
    def _get_next_file_number(self):
        """Get the next available file number with proper concurrency handling.
        
        Returns:
            int: The next available file number
            
        Raises:
            UserError: If unable to generate a valid file number
        """
        # Use a more targeted lock approach for better performance
        try:
            with self.env.cr.savepoint():
                # Lock only the records we're interested in
                self.env.cr.execute("""
                    SELECT office_file_number 
                    FROM project_project 
                    WHERE office_file_number IS NOT NULL 
                    AND office_file_number > 0
                    ORDER BY office_file_number DESC
                    LIMIT 1
                    FOR UPDATE
                """)
                
                result = self.env.cr.fetchone()
                max_number = result[0] if result else 0
                next_number = max_number + 1
                
                # Double-check that the next number doesn't exist (extra safety)
                self.env.cr.execute("""
                    SELECT id FROM project_project 
                    WHERE office_file_number = %s 
                    LIMIT 1
                """, (next_number,))
                
                if self.env.cr.fetchone():
                    # This should rarely happen, but if it does, try a few more numbers
                    for i in range(1, 11):  # Try up to 10 more numbers
                        candidate = max_number + 1 + i
                        self.env.cr.execute("""
                            SELECT id FROM project_project 
                            WHERE office_file_number = %s 
                            LIMIT 1
                        """, (candidate,))
                        
                        if not self.env.cr.fetchone():
                            return candidate
                    
                    # If we still can't find a number, raise an error
                    raise UserError(_(
                        "Unable to generate a valid file number. "
                        "Please contact your system administrator."
                    ))
                
                return next_number
                
        except Exception as e:
            _logger.error("Error generating next file number: %s", str(e), exc_info=True)
            raise UserError(_(
                "Could not generate the next file number. "
                "Please try again or contact your system administrator."
            ))
    
    def _get_current_max_file_number(self):
        """Get the current maximum file number from the database.
        
        Returns:
            int: The maximum file number found, or 0 if none exist
        """
        try:
            # Use raw SQL for better performance and reliability
            self.env.cr.execute("""
                SELECT COALESCE(MAX(office_file_number), 0) 
                FROM project_project 
                WHERE office_file_number IS NOT NULL 
                AND office_file_number > 0
            """)
            result = self.env.cr.fetchone()
            return result[0] if result else 0
            
        except Exception as e:
            _logger.error("Error getting max file number: %s", str(e), exc_info=True)
            return 0
    
    def action_get_next_office_file_number(self):
        """Button action to get the next available office file number.
        
        Returns:
            dict: Action result to update the view
        """
        self.ensure_one()
        
        try:
            # Get the next available file number
            next_number = self._get_next_file_number()
            
            # Update the field with proper context to skip validations
            self.with_context(
                skip_lock_update=True,
                skip_sequence_validation=True
            ).write({
                'office_file_number': next_number,
                'is_file_number_locked': True
            })
            
            # Reload the form to show the updated file number
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'project.project',
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'current',
                'context': dict(self.env.context),
            }
            
        except Exception as e:
            _logger.error("Error getting next file number: %s", str(e), exc_info=True)
            raise UserError(_(
                "Could not generate the next file number. "
                "Please try again or contact your system administrator."
            ))

    # ========== Validation Methods ==========
    
    @api.constrains('office_file_number')
    def _validate_office_file_number(self):
        """Validate office file number meets all requirements:
        - Must be a positive integer
        - Must be unique across all projects
        - Cannot be more than 1 greater than the current maximum (unless generated by system)
        """
        for record in self:
            if not record.office_file_number:
                continue
                
            # Check if it's a positive integer
            if not isinstance(record.office_file_number, int) or record.office_file_number <= 0:
                raise ValidationError(_(
                    "File number must be a positive integer. "
                    "Current value: %s" % record.office_file_number
                ))
            
            # Check for duplicates
            duplicate = self.search([
                ('office_file_number', '=', record.office_file_number),
                ('id', '!=', record.id)
            ], limit=1)
            
            if duplicate:
                raise ValidationError(_(
                    "File number %s already exists in another case." % 
                    record.office_file_number
                ))
            
            # Skip max+1 validation if this was generated by the system or during import
            if self._context.get('skip_sequence_validation') or self._context.get('install_mode'):
                continue
                
            # Get current maximum number (excluding this record)
            max_number = self._get_current_max_file_number_excluding(record.id)
            
            # If there are existing numbers, enforce the max+1 rule for manual entries
            if max_number > 0 and record.office_file_number > max_number + 1:
                raise ValidationError(_(
                    "File number cannot be more than 1 greater than the "
                    "highest existing number (%s). Current value: %s. "
                    "Use the 'Get Next Number' button for automatic numbering." % 
                    (max_number, record.office_file_number)
                ))
    
    def _get_current_max_file_number_excluding(self, exclude_record_id):
        """Get the current maximum file number, excluding a specific record.
        
        Args:
            exclude_record_id (int): ID of the record to exclude
            
        Returns:
            int: The maximum file number found, or 0 if none exist
        """
        try:
            self.env.cr.execute("""
                SELECT COALESCE(MAX(office_file_number), 0) 
                FROM project_project 
                WHERE office_file_number IS NOT NULL 
                AND office_file_number > 0
                AND id != %s
            """, (exclude_record_id,))
            result = self.env.cr.fetchone()
            return result[0] if result else 0
            
        except Exception as e:
            _logger.error("Error getting max file number excluding record: %s", str(e), exc_info=True)
            return 0

    @api.constrains('pipeline_type', 'matter_type')
    def _check_pipeline_matter_alignment(self):
        """Ensure legacy matter_type and new pipeline_type are always aligned."""
        for record in self:
            if (
                record.pipeline_type
                and record.matter_type
                and PIPELINE_TO_MATTER.get(record.pipeline_type) != record.matter_type
            ):
                raise ValidationError(_(
                    "Pipeline type and matter type are inconsistent. "
                    "Please choose matching values."
                ))

    @api.constrains('stage_id', 'pipeline_type')
    def _check_stage_pipeline_alignment(self):
        """Ensure the selected board stage belongs to the same pipeline."""
        for record in self:
            if (
                record.stage_id
                and record.pipeline_type
                and record.stage_id.pipeline_type != record.pipeline_type
            ):
                raise ValidationError(_(
                    "Stage '%(stage)s' belongs to pipeline '%(stage_pipeline)s' "
                    "and cannot be used for a '%(project_pipeline)s' project.",
                    stage=record.stage_id.display_name,
                    stage_pipeline=record.stage_id.pipeline_type,
                    project_pipeline=record.pipeline_type,
                ))

    @api.onchange('pipeline_type')
    def _onchange_pipeline_type(self):
        """Update matter type and stage suggestion when pipeline changes in UI."""
        if self.pipeline_type in PIPELINE_TO_MATTER:
            self.matter_type = PIPELINE_TO_MATTER[self.pipeline_type]

        if self.stage_id and self.stage_id.pipeline_type == self.pipeline_type:
            return

        stage = self._get_first_stage_for_pipeline(
            self.pipeline_type,
            company_id=self.company_id.id if self.company_id else False,
        )
        self.stage_id = stage or False

    @api.onchange('matter_type')
    def _onchange_matter_type(self):
        """Keep pipeline type aligned when users manually edit matter type."""
        if self.matter_type in MATTER_TO_PIPELINE:
            self.pipeline_type = MATTER_TO_PIPELINE[self.matter_type]

    @api.constrains('partner_id', 'is_template', 'matter_type')
    def _check_partner_required_for_non_template(self):
        """Ensure partner_id is required only for real legal entities (not templates)."""
        for record in self:
            if (
                not record.is_template
                and record.matter_type in ['case', 'subject']
                and not record.partner_id
            ):
                raise ValidationError(_(
                    "Customer is required for legal entities."
                ))

    @api.model
    def generate_missing_file_numbers(self):
        """Administrative method to generate file numbers for records that don't have them.
        
        This method can be used to fix data inconsistencies or during migration.
        It only affects records that don't already have a file number.
        
        Returns:
            dict: Summary of the operation
        """
        try:
            # Find records without file numbers
            records_without_numbers = self.search([
                ('office_file_number', '=', False)
            ])
            
            if not records_without_numbers:
                return {
                    'success': True,
                    'message': 'No records found without file numbers.',
                    'updated_count': 0
                }
            
            # Get the current maximum to continue sequence
            max_number = self._get_current_max_file_number()
            
            updated_count = 0
            for record in records_without_numbers:
                max_number += 1
                record.with_context(
                    skip_sequence_validation=True,
                    skip_lock_update=True
                ).write({
                    'office_file_number': max_number,
                    'is_file_number_locked': True
                })
                updated_count += 1
                
            return {
                'success': True,
                'message': f'Successfully assigned file numbers to {updated_count} records.',
                'updated_count': updated_count
            }
            
        except Exception as e:
            _logger.error("Error in bulk file number generation: %s", str(e), exc_info=True)
            return {
                'success': False,
                'message': f'Error occurred: {str(e)}',
                'updated_count': 0
            }

    # ==================== TAG MANAGEMENT ====================
    
    def _get_context_tag(self):
        """
        Determine which tag to add based on the current context.
        
        Returns:
            project.tags record or None: The appropriate tag based on context
        """
        if self.env.context.get('create_from_cases'):
            return self.env.ref('legal_practice_management.project_tag_case', raise_if_not_found=False)
        if self.env.context.get('create_from_matters'):
            return self.env.ref('legal_practice_management.project_tag_matter', raise_if_not_found=False)
        return None
    
    def _default_tag_ids(self):
        """
        Default method to add appropriate tag based on context.
        
        Returns:
            list: List of tag commands for the tag_ids field
        """
        tag = self._get_context_tag()
        if tag:
            return [(4, tag.id)]
        return []
    
    tag_ids = fields.Many2many(
        'project.tags',
        string='Tags',
        default=_default_tag_ids,
        help='Tags for categorizing legal entities'
    )
    
    # ==================== OVERRIDE METHODS ====================
    
    def _apply_template_based_on_matter_type(self):
        """Apply template configuration based on matter type after project creation.
        
        This method is called after project creation to copy stages and tasks from the appropriate
        template if configured by the administrator.
        """
        for record in self:
            template_id = False
            
            if record.matter_type == 'case':
                template_id = self.env['ir.config_parameter'].sudo().get_param(
                    'legal_practice_management.litigation_template_id'
                )
            elif record.matter_type == 'subject':
                template_id = self.env['ir.config_parameter'].sudo().get_param(
                    'legal_practice_management.advisory_template_id'
                )
            
            if template_id:
                try:
                    template = self.browse(int(template_id))
                    if template and template.exists():
                        # Copy stages from template and create mapping
                        stage_mapping = {}
                        for stage in template.type_ids:
                            new_stage = stage.copy({'project_ids': [(4, record.id)]})
                            stage_mapping[stage.id] = new_stage.id
                        
                        # Copy tasks from template, updating project and stage
                        for task in template.task_ids:
                            new_stage_id = stage_mapping.get(task.stage_id.id, task.stage_id.id)
                            task.copy({
                                'project_id': record.id,
                                'stage_id': new_stage_id,
                            })
                        
                        _logger.info(
                            "Applied template %s to project %s (matter_type: %s) - copied %d stages and %d tasks",
                            template.name, record.name, record.matter_type, len(stage_mapping), len(template.task_ids)
                        )
                except (ValueError, TypeError) as e:
                    _logger.warning(
                        "Failed to apply template for project %s: %s",
                        record.name, str(e)
                    )
    
    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to handle file number locking, pipeline mapping, tags, and templates.
        
        Args:
            vals_list (list): List of values for creating records
            
        Returns:
            project.project: Created records
        """
        normalized_vals_list = []
        for vals in vals_list:
            vals = self._sync_pipeline_and_matter_vals(vals)

            # Handle file number locking
            if 'office_file_number' in vals and vals.get('office_file_number'):
                vals['is_file_number_locked'] = True

            # If stage is not provided, suggest first stage for that pipeline
            if 'stage_id' not in vals and vals.get('pipeline_type'):
                stage = self._get_first_stage_for_pipeline(
                    vals['pipeline_type'],
                    company_id=vals.get('company_id'),
                )
                if stage:
                    vals['stage_id'] = stage.id
            
            # Handle tag assignment based on context
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

            normalized_vals_list.append(vals)
        
        # Create the projects
        records = super().create(normalized_vals_list)
        
        # Apply template-based stage copying after creation
        records._apply_template_based_on_matter_type()
        
        return records
