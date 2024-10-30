from . import __version__ as app_version

app_name = "assignments"
app_title = "Assignments"
app_publisher = "Saisudha"
app_description = "to solve assignments"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "asignments.sudha@gmail.com"
app_license = "MIT"

# fixtures = [
#     "User", "Custom Field", "Workflow", "Workflow State", "Workflow Action Master"
#     "Workflow Transition", "Website Settings",
#     {"dt": "Role", "or_filters": [["name", "=", "Timesheet Manager"],["name", "=", "Timesheet User"]]},
# ]
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/assignments/css/assignments.css"
# app_include_js = "/assets/assignments/js/assignments.js"

# include js, css files in header of web template
# web_include_css = "/assets/assignments/css/assignments.css"
# web_include_js = "/assets/assignments/js/assignments.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "assignments/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "assignments.utils.jinja_methods",
# 	"filters": "assignments.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "assignments.install.before_install"
# after_install = "assignments.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "assignments.uninstall.before_uninstall"
# after_uninstall = "assignments.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "assignments.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"assignments.tasks.all"
# 	],
# 	"daily": [
# 		"assignments.tasks.daily"
# 	],
# 	"hourly": [
# 		"assignments.tasks.hourly"
# 	],
# 	"weekly": [
# 		"assignments.tasks.weekly"
# 	],
# 	"monthly": [
# 		"assignments.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "assignments.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "assignments.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "assignments.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"assignments.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []