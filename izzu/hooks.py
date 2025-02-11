from . import __version__ as app_version

app_name = "izzu"
app_title = "izzu"
app_publisher = "izzu.com"
app_description = "this app is for whitelable"
app_email = "support@izzu.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_logo_url = "/assets/izzu/images/izzu-logo.png"

website_context = {
    "favicon": "/assets/izzu/images/izzu-login.png",
    "splash_image": "/assets/izzu/images/izzu-logo.png",
}


web_include_css = ["izzu_login.bundle.css"]
app_include_js = "toolbar.bundle.js"

# include js, css files in header of desk.html
# app_include_css = "/assets/aks_ui/css/aks_ui.css"
# app_include_js = "/assets/aks_ui/js/aks_ui.js"

# include js, css files in header of web template
# web_include_css = "/assets/aks_ui/css/aks_ui.css"
# web_include_js = "/assets/aks_ui/js/aks_ui.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "aks_ui/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Task" : "public/js/task.js",
            "Payment Entry" : "public/js/payment_entry.js",
            "Sales Invoice" : "public/js/sales_invoice.js",
            }
doctype_list_js = {"ToDo" : "public/js/todo.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "login"

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
#	"methods": "aks_ui.utils.jinja_methods",
#	"filters": "aks_ui.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "aks_ui.install.before_install"
# after_install = "aks_ui.install.after_install"

# Migrate
after_migrate = "izzu.migrate.after_migrate"
# Uninstallation
# ------------

# before_uninstall = "aks_ui.uninstall.before_uninstall"
# after_uninstall = "aks_ui.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "aks_ui.utils.before_app_install"
# after_app_install = "aks_ui.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "aks_ui.utils.before_app_uninstall"
# after_app_uninstall = "aks_ui.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "aks_ui.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Student": {
		"before_save": "izzu.event.student.before_save",
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"izzu.event.tasks.all_events_task"
	],
	"daily": [
		"izzu.event.tasks.all_events_task"
	],
	"hourly": [
		"izzu.event.tasks.all_events_task"
	],
	"weekly": [
		"izzu.event.tasks.all_events_task"
	],
	"monthly": [
		"izzu.event.tasks.all_events_task"
	],
    
	"cron": {
        "0 0 * * MON": [
            "izzu.izzu.report.accounts_payable_aging_report.accounts_payable_aging_report.send_data"
        ]
    }
}

# Testing
# -------

# before_tests = "aks_ui.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "aks_ui.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "aks_ui.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["aks_ui.utils.before_request"]
# after_request = ["aks_ui.utils.after_request"]

# Job Events
# ----------
# before_job = ["aks_ui.utils.before_job"]
# after_job = ["aks_ui.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"aks_ui.auth.validate"
# ]

fixtures = ["Custom Field"]