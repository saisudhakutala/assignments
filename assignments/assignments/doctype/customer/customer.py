# Copyright (c) 2024, Saisudha and contributors
# For license information, please see license.txt

"""
There are two ways of writing rest apis in frappe
1. Resource apis which are profided by frappe can be handled through hooks
    a. eg: manage_customer: http://site_name/api/resource/Customer
        Post request creates a new customer
        Put request updates an existing customer
    b. this requires authentication by creating a token and passing it in the header
    c. tokens can be created for a user

2. Custom apis which are written in python a method can become an api by adding a decorator @frappe.whitelist(allow_guest=True)
    a. eg: manage_customer: http://site_name/api/method/assignments.assignments.doctype.customer.customer.manage_customer
    b. this does not require authentication as we are allowing guest to access the api
    c. this can be used for public apis
    d. We can also add authentication by checking the token in the header by making allow_guest=False in the decorator

Note: We can solve the given problem by both the ways for now I am choosing custom api
"""
import frappe
from frappe.model.document import Document
from frappe.utils import cint, validate_email_address, validate_phone_number
from frappe.exceptions import UniqueValidationError, ValidationError, DoesNotExistError, DuplicateEntryError

class Customer(Document):
    def validate(self):
        # Check if the email address is valid
        for email in self.email:
            if not validate_email_address(email.email):
                frappe.throw("Invalid email address: {}".format(email.email_address))

        # Check if the phone number is valid
        for phone in self.phone_number:
            if not validate_phone_number(phone.phone_number):
                frappe.throw("Invalid phone number: {}".format(phone.phone_number))

        # Check if the address is valid
        for address in self.address:
            if not address.address_line:
                frappe.throw("Address line is required")
            if not address.city:
                frappe.throw("City is required")
            if not address.state:
                frappe.throw("State is required")
            if not address.country:
                frappe.throw("Country is required")
            if not address.pincode:
                frappe.throw("Pincode is required")


def create_customer(payload={}):
    try:
        # Ensure customer_name and mandatory fields are provided
        if not payload.get("customer_name"):
            frappe.throw("Customer name is mandatory")

        # Create new customer document
        customer_doc = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": payload.get("customer_name"),
            "salutation": payload.get("salutation"),
            "sales_person": payload.get("sales_person"),
        })
        customer_doc.email = []
        customer_doc.phone_number = []
        customer_doc.address = []

        # Validate and add emails
        emails = payload.get("emails", [])
        for email in emails:
            email_address = email.get("email_address")
            if email_address:
                customer_doc.append("email", {
                    "doctype": "Customer Email",
                    "email": email_address,
                    "is_primary": cint(email.get("is_primary", 0))
                })
            else:
                frappe.throw("Email address is required for each entry in emails", ValidationError)
        
        # Validate and add phone numbers
        phone_numbers = payload.get("phone_numbers", [])
        for phone in phone_numbers:
            phone_number = phone.get("phone_number")
            if phone_number:
                customer_doc.append("phone_number", {
                    "doctype": "Customer Phone",
                    "phone_number": phone_number,
                    "is_primary": cint(phone.get("is_primary", 0))
                })
            else:
                frappe.throw("Phone number is required for each entry in phone numbers", ValidationError)

        # Validate and add addresses
        addresses = payload.get("addresses", [])
        for address in addresses:
            if address.get("address_line") and address.get("city") and address.get("pincode"):
                customer_doc.append("address", {
                    "doctype": "Customer Address",
                    "address_line": address.get("address_line"),
                    "city": address.get("city"),
                    "state": address.get("state"),
                    "country": address.get("country"),
                    "pincode": address.get("pincode")
                })
            else:
                frappe.throw("Address line, city, and pincode are required for each address entry")

        # Insert the customer document
        customer_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return {"message": "Customer created successfully", "customer_id": customer_doc.name}
    
    except ValidationError as e:
        frappe.throw("An error occurred while creating customer information.", exc=e)
    
    except UniqueValidationError as e:
        frappe.throw("An error occurred while creating customer information.", exc=e)
    
    except DuplicateEntryError as e:
        frappe.throw("Customer already existis", exc=e)
    
    except Exception as e:
        frappe.throw(str(e), frappe.ValidationError)
 
    return {"message": "Customer created successfully", "customer_name": customer_doc.name}
    

def update_customer(payload):
    customer_name = payload.get("customer_name")
    try:
        if not frappe.db.exists("Customer", customer_name):
            frappe.throw("Customer does not exist", DoesNotExistError)
        
        customer_doc = frappe.get_doc("Customer", customer_name)

        # Update or delete existing emails
        emails_payload = {email.get("email_address"): email for email in payload.get("emails", [])}
        existing_emails = {email.email: email for email in customer_doc.email}
        
        # Process emails in payload
        for email_address, email_data in emails_payload.items():
            if email_address in existing_emails:
                existing_email = existing_emails[email_address]
                existing_email.is_primary = cint(email_data.get("is_primary", 0))
            else:
                customer_doc.append("email", {
                    "doctype": "Customer Email",
                    "email": email_address,
                    "is_primary": cint(email_data.get("is_primary", 0))
                })

        # Delete emails not in payload
        for email_address in list(existing_emails):
            if email_address not in emails_payload:
                customer_doc.remove(existing_emails[email_address])

        # Update or delete existing phone numbers
        phones_payload = {phone.get("phone_number"): phone for phone in payload.get("phone_numbers", [])}
        existing_phone_numbers = {phone.phone_number: phone for phone in customer_doc.phone_number}
        
        # Process phones in payload
        for phone_number, phone_data in phones_payload.items():
            if phone_number in existing_phone_numbers:
                existing_phone = existing_phone_numbers[phone_number]
                existing_phone.is_primary = cint(phone_data.get("is_primary", 0))
            else:
                customer_doc.append("phone_number", {
                    "doctype": "Customer Phone",
                    "phone_number": phone_number,
                    "is_primary": cint(phone_data.get("is_primary", 0))
                })

        # Delete phones not in payload
        for phone_number in list(existing_phone_numbers):
            if phone_number not in phones_payload:
                customer_doc.remove(existing_phone_numbers[phone_number])

        # Update or delete existing addresses
        addresses_payload = {(addr.get("address_line"), addr.get("city"), addr.get("pincode")): addr for addr in payload.get("addresses", [])}
        existing_addresses = {(address.address_line, address.city, address.pincode): address for address in customer_doc.address}
        
        # Process addresses in payload
        for address_key, address_data in addresses_payload.items():
            if address_key in existing_addresses:
                existing_address = existing_addresses[address_key]
                existing_address.state = address_data.get("state")
                existing_address.country = address_data.get("country")
            else:
                customer_doc.append("address", {
                    "doctype": "Address",
                    "address_line": address_data.get("address_line"),
                    "city": address_data.get("city"),
                    "pincode": address_data.get("pincode"),
                    "state": address_data.get("state"),
                    "country": address_data.get("country"),
                })

        # Delete addresses not in payload
        for address_key in list(existing_addresses):
            if address_key not in addresses_payload:
                customer_doc.remove(existing_addresses[address_key])

        # Save updates
        customer_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"message": "Customer updated successfully", "customer_name": customer_doc.name}
    
    except DoesNotExistError as e:
        frappe.throw("Customer does not exist", exc=e)
    
    except ValidationError as e:
        if "Duplicate entry" in str(e) or "IntegrityError" in str(e):
            frappe.throw("One of the given email already presnet for another customer", exc=e)
        
        frappe.throw("An error occurred while updating customer information.", exc=e)
    
    except UniqueValidationError as e:
        frappe.throw("An error occurred while updating customer information.", exc=e)
    
    except Exception as e:
        frappe.throw(str(e), frappe.ValidationError)

@frappe.whitelist(allow_guest=True)
def manage_customer(data=None):
    payload = frappe.parse_json(data)
    if not payload:
        frappe.throw("Data is required", frappe.ValidationError)
    
    if frappe.request.method == "POST":
        result = create_customer(payload)
    elif frappe.request.method == "PUT":
        result = update_customer(payload)
    else:
        frappe.throw("Invalid method", frappe.ValidationError)
    return result

# sample payload for create_customer
data = {
    "customer_name": "John Doe",
    "salutation": "Mr",
    "sales_person": "Jane Doe",
    "emails": [
        {"email_address": "john@gmail.com", "is_primary": 1},
        {"email_address": "jane@gmail.com", "is_primary": 0}
    ],
    "phone_numbers": [
        {"phone_number": "123456789", "is_primary": 1},
        {"phone_number": "987654321", "is_primary": 0}
    ],
    "addresses": [
        {"address_line": "123, Main Street", "city": "New York", "state": "New York", "country": "USA", "pincode": "10001"},
        {"address_line": "456, Main Street", "city": "Los Angeles", "state": "California", "country": "USA", "pincode": "90001"}
    ]
}
