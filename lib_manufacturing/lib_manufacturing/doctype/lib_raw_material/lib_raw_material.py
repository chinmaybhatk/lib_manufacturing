import frappe
from frappe.model.document import Document
import re
from datetime import datetime, timedelta

class LIBRawMaterial(Document):
    def validate(self):
        """
        Validate raw material data before saving
        """
        # Validate material name
        if not self.material_name:
            frappe.throw("Material Name is required")
        
        # Validate material type
        valid_types = [
            "Cathode Material", 
            "Anode Material", 
            "Separator", 
            "Electrolyte", 
            "Current Collector", 
            "Other"
        ]
        if self.material_type not in valid_types:
            frappe.throw(f"Invalid Material Type. Must be one of {', '.join(valid_types)}")
        
        # Validate purity percentage
        if self.purity_percentage is not None:
            if self.purity_percentage < 90 or self.purity_percentage > 99.99:
                frappe.throw("Purity Percentage must be between 90% and 99.99%")
        
        # Validate manufacturing date
        if self.manufacturing_date:
            if self.manufacturing_date > datetime.now().date():
                frappe.throw("Manufacturing Date cannot be in the future")
            
            # Warn if material is older than 2 years
            expiry_date = self.manufacturing_date + timedelta(days=730)
            if expiry_date < datetime.now().date():
                frappe.msgprint("Warning: This raw material is over 2 years old and may be expired")
        
        # Validate batch number format
        if self.batch_number:
            # Batch number should be alphanumeric with optional hyphens
            if not re.match(r'^[A-Z0-9-]+$', self.batch_number):
                frappe.throw("Batch Number must contain only uppercase letters, numbers, and hyphens")
    
    def before_insert(self):
        """
        Generate a batch number if not provided
        """
        if not self.batch_number:
            # Generate a unique batch number based on material type and current timestamp
            prefix = self.material_type[:3].upper()
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            self.batch_number = f"{prefix}-{timestamp}"
    
    def on_update(self):
        """
        Log any updates to the raw material
        """
        frappe.log_activity(f"Updated Raw Material: {self.name}")
