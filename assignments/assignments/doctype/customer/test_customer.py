# Copyright (c) 2024, Saisudha and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.exceptions import ValidationError, DoesNotExistError
from assignments.assignments.doctype.customer.customer import create_customer, update_customer, manage_customer

class TestCustomer(FrappeTestCase):

    def setUp(self):
        # Set up a new customer for tests
        self.valid_payload = {
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

        # Clean up any existing customers before tests
        if frappe.db.exists("Customer", "John Doe"):
            frappe.delete_doc("Customer", "John Doe")

    def tearDown(self):
        # Clean up after tests
        if frappe.db.exists("Customer", "John Doe"):
            frappe.delete_doc("Customer", "John Doe")

    def test_create_customer_success(self):
        response = create_customer(self.valid_payload)
        self.assertEqual(response['message'], "Customer created successfully")
        self.assertTrue(frappe.db.exists("Customer", "John Doe"))

    def test_create_customer_invalid_email(self):
        invalid_payload = {
            "customer_name": "Jane Doe",
            "emails": [
                {"email_address": "invalid-email", "is_primary": 1}
            ]
        }
        with self.assertRaises(ValidationError):
            create_customer(invalid_payload)

    def test_update_customer_success(self):
        create_customer(self.valid_payload)  # Create the customer first

        update_payload = {
            "customer_name": "John Doe",
            "emails": [
                {"email_address": "john.updated@gmail.com", "is_primary": 1}
            ],
            "phone_numbers": [  # Include mandatory fields
                {"phone_number": "123456789", "is_primary": 1}
            ],
            "addresses": [  # Include mandatory fields
                {
                    "address_line": "123, Main Street",
                    "city": "New York",
                    "state": "New York",
                    "country": "USA",
                    "pincode": "10001"
                }
            ]
        }

        response = update_customer(update_payload)
        self.assertEqual(response['message'], "Customer updated successfully")

        # Verify the email was updated
        customer = frappe.get_doc("Customer", "John Doe")
        self.assertEqual(customer.email[0].email, "john.updated@gmail.com")

    def test_manage_customer_post(self):
        frappe.local.request = frappe._dict()  
        frappe.local.request.method = "POST"  # Set the request method
        response = manage_customer(data=frappe.as_json(self.valid_payload))
        self.assertEqual(response['message'], "Customer created successfully")

    def test_manage_customer_put(self):
        create_customer(self.valid_payload)  # Create the customer first

        update_payload = {
            "customer_name": "John Doe",
            "emails": [
                {"email_address": "john.updated@gmail.com", "is_primary": 1}
            ],
            "phone_numbers": [  # Include mandatory fields
                {"phone_number": "123456789", "is_primary": 1}
            ],
            "addresses": [  # Include mandatory fields
                {
                    "address_line": "123, Main Street",
                    "city": "New York",
                    "state": "New York",
                    "country": "USA",
                    "pincode": "10001"
                }
            ]
        }
        frappe.local.request = frappe._dict()
        frappe.local.request.method = "PUT"  # Set the request method
        response = manage_customer(data=frappe.as_json(update_payload))
        self.assertEqual(response['message'], "Customer updated successfully")

    def test_manage_customer_invalid_method(self):
        with self.assertRaises(ValidationError):
            manage_customer(data=None)

