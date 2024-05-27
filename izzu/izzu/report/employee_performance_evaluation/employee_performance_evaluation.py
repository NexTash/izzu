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
            "fieldtype": "Data",
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
            "fieldtype": "percent",
            "width": 300
        },
        {
            "fieldname": "comunication_skills",
            "label": "Communication Skills",
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
        },
        {
            "fieldname": "overall_score",
            "label": "Overall Score",
            "fieldtype": "Float",  # Changed fieldtype to Float
            "width": 100
        }
    ]
    return columns

def get_data(filters):
    data = []
    emp_filters = {}

    if filters.get('employee_name'):
        emp_filters['employee_name'] = filters.get('employee_name')
    
    task_data = frappe.get_all('Task', filters=emp_filters, fields=["*"])
    for task in task_data:
        # Assign numerical values to task priorities
        if task.priority.lower() == 'high':
            task_priority = 100
        elif task.priority.lower() == 'medium':
            task_priority = 50
        elif task.priority.lower() == 'low':
            task_priority = 10
        else:
            task_priority = 0  # Assign a default value for other cases
        
        attendance_data = frappe.get_all('Attendance', filters=emp_filters, fields=["*"])
        for attendance in attendance_data:
            performance_feedback = frappe.get_all('Employee Performance Feedback', filters=emp_filters, fields=["*"])
            for feedback in performance_feedback:
                feedback_ratings = frappe.get_all('Employee Feedback Rating', filters={'parent': feedback.name}, fields=["*"])
                criteria_list = [rating.criteria for rating in feedback_ratings]
                weightage_list = [rating.per_weightage for rating in feedback_ratings]
                criteria_str = ", ".join(criteria_list)
                weightage_str = ", ".join(map(str, weightage_list))
                eco_data = frappe.get_all('Employee Performance on ECO', filters=emp_filters, fields=["*"])
                for eco in eco_data:
                    employee_skill_maps = frappe.get_all('Employee Skill Map', filters=emp_filters, fields=["*"])
                    for skill_map in employee_skill_maps:
                        skills = frappe.get_all('Employee Skill', filters={'parent': skill_map.name}, fields=["*"])
                        trainings = frappe.get_all('Employee Training', filters={'parent': skill_map.name}, fields=["*"])
                        for skill in skills:
                            for training in trainings:
                                # Convert attendance status to binary
                                attendance_score = 1 if attendance.attendance_status == "Present" else 0
                                # Normalize task priority
                                task_score = int(task_priority) / 100
                                # Assuming team_works, positive_attitude_overall, and skill_score are out of 100
                                team_engagement_score = eco.team_works / 100 if eco.team_works is not None else 0
                                # Handle non-numeric values for positive_attitude_overall
                                try:
                                    environmental_behavior_score = int(eco.positive_attitude_overall) / 100
                                except ValueError:
                                    environmental_behavior_score = 0
                                # Calculate overall score
                                overall_score = (task_score * 0.5) + (attendance_score * 0.1) + (team_engagement_score * 0.1) + (environmental_behavior_score * 0.2)
                                # Append data to the dictionary
                                data.append({
                                    "employee_name": attendance.employee_name,
                                    "status": task.status,
                                    "project": task.project,
                                    "priority": task_priority,  # Use converted priority
                                    "company": attendance.company,
                                    "department": attendance.department,
                                    "attendance_status": attendance.status,
                                    "attendance_date": attendance.attendance_date,
                                    "feedback_criteria": criteria_str,
                                    "feedback_weightage": weightage_str,
                                    "total_score": feedback.total_score,
                                    "team_works": eco.team_works,
                                    "communication_skills": eco.communication_skills,  # Corrected field name
                                    "positive_attitude_overall": eco.positive_attitude_overall,
                                    "skill": skill.skill,
                                    "evaluation_date": skill.evaluation_date,
                                    "training": training.training,
                                    "training_date": training.training_date,
                                    "overall_score": overall_score  # Add overal  # Corrected
                                })
    return data