# Context-Aware Automatic Tag Assignment

## Overview

The Legal Case Management module now automatically assigns tags to newly created projects based on the context from which they are created. This ensures proper categorization and organization:

- **"Case" tag** is added when creating projects from the **Cases app**
- **"Matter" tag** is added when creating projects from the **Matters app**
- **No default tags** are added when creating projects from other contexts

## How It Works

### Context Detection

The system automatically detects the source context when creating new projects:

1. **Cases Context**: Projects created from the Legal Cases menu get the "Case" tag
2. **Matters Context**: Projects created from the Matters menu get the "Matter" tag
3. **Other Contexts**: Projects created from other sources (like regular Projects) get no default tags

### Implementation Details

The feature uses context detection to determine which tag to assign:

#### 1. Context Detection Method
```python
@api.model
def _get_context_tag(self):
    """Determine which tag to add based on the current context."""
    # Check for specific context keys
    if self.env.context.get('create_from_cases'):
        return self.env.ref('legal_case_management.project_tag_case', raise_if_not_found=False)
    
    if self.env.context.get('create_from_matters'):
        return self.env.ref('legal_matter_management.project_tag_matter', raise_if_not_found=False)
    
    return None
```

#### 2. Default Value Method
```python
@api.model
def _default_tag_ids(self):
    """Default method to add appropriate tag based on context."""
    tag = self._get_context_tag()
    if tag:
        return [(4, tag.id)]
    return []
```

#### 3. Create Method Override
```python
@api.model
def create(self, vals):
    """Override create method to automatically add appropriate tag based on context."""
    tag = self._get_context_tag()
    # Add tag logic...
    return super().create(vals)
```

## Benefits

1. **Intelligent Categorization**: Projects are automatically tagged based on their creation context
2. **Proper Organization**: Cases and Matters are clearly distinguished
3. **No Manual Work**: Users don't need to remember to add the correct tag
4. **Context Awareness**: The system understands where the project is being created from
5. **Flexible**: Users can still add additional tags as needed
6. **Backward Compatibility**: Existing projects and other contexts are unaffected

## Configuration

### Case Tag Definition
```xml
<record id="project_tag_case" model="project.tags">
    <field name="name">Case</field>
    <field name="color">5</field>
</record>
```

### Matter Tag Definition
```xml
<record id="project_tag_matter" model="project.tags">
    <field name="name">Matter</field>
    <field name="color">8</field>
</record>
```

### Context Configuration
The actions are configured with specific context keys:

**Cases Action:**
```xml
<record id="action_view_project_cases_strict" model="ir.actions.act_window">
    <field name="context">{'group_by': 'stage_id', 'create_from_cases': True}</field>
</record>
```

**Matters Action:**
```xml
<record id="action_view_project_matters" model="ir.actions.act_window">
    <field name="context">{'group_by': 'stage_id', 'create_from_matters': True}</field>
</record>
```

## Testing

The feature includes comprehensive tests in `tests/test_project_tags.py` that verify:

- Projects created from Cases context get the "Case" tag
- Projects created from Matters context get the "Matter" tag
- Projects created without context get no default tags
- Projects with existing tags still get the appropriate context tag
- No duplicate tags are created
- Form defaults work correctly for both contexts
- Multiple projects can be created successfully from each context

## Usage

### For End Users

#### Creating Cases
1. Navigate to **Legal Cases** → **All Cases**
2. Click **Create** to add a new case
3. The "Case" tag will automatically appear as selected
4. Add any additional tags as needed
5. Save the case

#### Creating Matters
1. Navigate to  **Matters** → **All Matters**
2. Click **Create** to add a new matter
3. The "Matter" tag will automatically appear as selected
4. Add any additional tags as needed
5. Save the matter

#### Creating Regular Projects
1. Navigate to **Projects** (regular project menu)
2. Click **Create** to add a new project
3. No default tags will be assigned
4. Add tags manually as needed
5. Save the project

### For Developers

The feature works transparently based on context:

```python
# This project will get the "Case" tag
project = self.env['project.project'].with_context(create_from_cases=True).create({
    'name': 'New Legal Case',
    'partner_id': client.id,
})

# This project will get the "Matter" tag
project = self.env['project.project'].with_context(create_from_matters=True).create({
    'name': 'New Legal Matter',
    'partner_id': client.id,
})

# This project will get no default tags
project = self.env['project.project'].create({
    'name': 'Regular Project',
    'partner_id': client.id,
})
```

## Troubleshooting

### Wrong Tag Assigned

If the wrong tag is being assigned:

1. **Check context**: Verify the project is being created from the correct menu
2. **Check action configuration**: Ensure the action has the correct context key
3. **Clear browser cache**: Refresh the page to ensure latest context is used

### No Tag Assigned

If no tag is being assigned:

1. **Check menu navigation**: Ensure you're creating from the correct menu
2. **Check module installation**: Ensure both modules are properly installed
3. **Check tag references**: Verify the tag references exist in the data files

### Duplicate Tags

If duplicate tags appear:

1. **Check for multiple tag definitions**: Ensure there's only one tag with each name
2. **Clear cache**: Restart the Odoo server to clear any cached data
3. **Check for conflicting modules**: Ensure no other modules are creating similar tags

## Best Practices

1. **Use the correct menu**: Always create cases from the Cases menu and matters from the Matters menu
2. **Don't remove context tags manually**: The system will re-add them on the next project creation
3. **Use additional tags**: Add specific tags for case types, urgency, or other classifications
4. **Leverage filtering**: Use the respective menus to filter and manage cases and matters
5. **Regular maintenance**: Periodically review and clean up unused tags

## Future Enhancements

Potential improvements for future versions:

1. **Configurable default tags**: Allow administrators to configure which tags are added by default
2. **Case type tags**: Automatically add tags based on case type (Civil, Criminal, etc.)
3. **Client-specific tags**: Add tags based on client information
4. **Template-based tags**: Allow project templates to define default tags
5. **Workflow-based tags**: Add tags based on project stage or workflow
6. **User preference tags**: Allow users to set their preferred default tags 