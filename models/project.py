import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)

class ProjectProject(models.Model):
    _inherit = 'project.project'
    _description = 'Legal Case Project'

    # ========== ORM Overrides ==========
    def write(self, vals):
        """Override write to handle file number locking."""
        if 'office_file_number' in vals and any(rec.is_file_number_locked for rec in self):
            raise UserError(_(
                "File number cannot be modified once it has been set and saved."
            ))
        
        # Set the lock if office_file_number is being set
        if 'office_file_number' in vals and vals.get('office_file_number') and not self._context.get('skip_lock_update'):
            vals['is_file_number_locked'] = True
            
        return super().write(vals)
    
    # ========== Field Definitions ==========
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
    
    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to handle file number locking and tag management.
        
        Args:
            vals_list (list): List of values for creating records
            
        Returns:
            project.project: Created records
        """
        for vals in vals_list:
            # Handle file number locking
            if 'office_file_number' in vals and vals.get('office_file_number'):
                vals['is_file_number_locked'] = True
            
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
        
        return super().create(vals_list)