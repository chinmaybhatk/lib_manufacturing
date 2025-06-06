import frappe
from frappe.model.document import Document

class LIBRawMaterial(Document):
    def validate(self):
        # Ensure purity percentage is within acceptable range
        if self.purity_percentage and (self.purity_percentage < 95 or self.purity_percentage > 99.99):
            frappe.throw(f'Purity Percentage {self.purity_percentage}% is outside acceptable range (95-99.99%)')
        
        # Validate batch number format
        if self.batch_number and not frappe.utils.validate_regex(self.batch_number, r'^[A-Z0-9-]+$'):
            frappe.throw('Batch Number must contain only alphanumeric characters and hyphens')
    
    def before_insert(self):
        # Auto-generate unique identifier if no batch number
        if not self.batch_number:
            self.batch_number = frappe.generate_hash(length=10)