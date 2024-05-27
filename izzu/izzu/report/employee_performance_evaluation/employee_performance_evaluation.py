import frappe
from datetime import datetime

def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
        {
            "fieldname": "employee_name",
            "label": "Employee Name",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 250
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "project",
            "label": "Project",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "priority",
            "label": "Priority",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "company",
            "label": "Company",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "department",
            "label": "Department",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "attendance_status",
            "label": "Attendance Status",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "attendance_date",
            "label": "Date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "feedback_criteria",
            "label": "Feedback Criteria",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "feedback_weightage",
            "label": "Feedback Weightage",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "total_score",
            "label": "Total Score",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "team_works",
            "label": "Team Works",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "comunication_skills",
            "label": "Comunication Skills",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "positive_attitude_overall",
            "label": "Positive Attitude Overall",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "skill",
            "label": "Skill",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "evaluation_date",
            "label": "Evaluation Date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "training",
            "label": "Training",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "training_date",
            "label": "Training Date",
            "fieldtype": "Date",
            "width": 100
        }
    ]
    return columns

def get_data(filters):
    data = []
    emp_filters = {}

    if filters.get('employee_name'):
        emp_filters['employee_name'] = filters.get('employee_name')

    # Fetch and append data from Task doctype
    task_data = frappe.get_list('Task', filters=emp_filters, fields=["*"])
    for task in task_data:
        attendance_data = frappe.get_list('Attendance', filters=emp_filters, fields=["*"])
        for attendance in attendance_data:
            performance_feedback = frappe.get_list('Employee Performance Feedback', filters=emp_filters, fields=["*"])

            for feedback in performance_feedback:
                feedback_ratings = frappe.get_list('Employee Feedback Rating', filters={'parent': feedback.name}, fields=["*"])
        
                criteria_list = [rating.criteria for rating in feedback_ratings]
                weightage_list = [rating.per_weightage for rating in feedback_ratings]

                criteria_str = ", ".join(criteria_list)
                weightage_str = ", ".join(map(str, weightage_list))
                eco_data = frappe.get_list('Employee Performance on ECO', filters=emp_filters, fields=["*"])
    
                for eco in eco_data:
                     employee_skill_maps = frappe.get_list('Employee Skill Map', filters=emp_filters, fields=["*"])

                for skill_map in employee_skill_maps:
                    skills = frappe.get_list('Employee Skill', filters={'parent': skill_map.name}, fields=["*"])
                    trainings = frappe.get_list('Employee Training', filters={'parent': skill_map.name}, fields=["*"])
                    for skill in skills:
                        for training in trainings:
                            data.append({
                            "employee": task.employee_name,
                            "status": task.status,
                            "project": task.project,
                            "priority": task.priority,
                            "company": attendance.company,
                            "department": attendance.department,
                            "attendance_status": attendance.status,
                            "attendance_date": attendance.attendance_date,
                            "feedback_criteria": criteria_str,
                            "feedback_weightage": weightage_str,
                            "total_score": feedback.total_score,
                            "team_works": eco.team_works,
                            "comunication_skills": eco.comunication_skills,
                            "positive_attitude_overall": eco.positive_attitude_overall,
                            "skill": skill.skill,
                            "evaluation_date": skill.evaluation_date,
                            "training": training.training,
                            "training_date": training.training_date
                        })    
    return data

