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
            "fieldname": "team_work",
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
    emp_filters = {}

    # Applying filter based on employee name
    if filters.get("employee_name"):
        emp_filters["name"] = filters.get("employee_name")

    # Fetch and append data from Task doctype
    data = []
    employee_data = {}
    task_data = frappe.get_all('Employee', filters=emp_filters, fields=["*"])

    for task in task_data:
        # Initialize employee data if not already present
        if task.name not in employee_data:
            employee_data[task.name] = {
                "employee_name": task.employee_name,
                "company": task.company,
                "department": task.department,
                "employee_task": [],
                "attendance_records": [],
                "feedback_ratings": [],
                "employee_eco": [],
                "employee_skill": []
            }
            task_docs = frappe.get_all("Task", {"user": task.user_id}, ["*"])
        for tas in task_docs:
            employee_data[task.name]["employee_task"].append({
                "status": tas.status,
                "project": tas.project,
                "priority": tas.priority,

            })

        # Fetch and append attendance documents for the employee
        att_docs = frappe.get_all("Attendance", {"employee": task.name}, ["*"])
        for att in att_docs:
            employee_data[task.name]["attendance_records"].append({
                "attendance_status": att.status,
                "attendance_date": att.attendance_date,
            })

        # Fetch and append feedback documents for the employee
        feed_docs = frappe.get_all("Employee Performance Feedback", {"employee": task.name}, ["*"])
        for row in feed_docs:
            doc = frappe.get_doc("Employee Performance Feedback", row.name)
            for child in doc.feedback_ratings:
                employee_data[task.name]["feedback_ratings"].append({
                    "feedback_criteria": child.criteria,
                    "feedback_weightage": child.per_weightage,
                    "total_score": doc.total_score,
                })

        # Fetch and append ECO documents for the employee
        eco_docs = frappe.get_all("Employee Performance on ECO", {"employee": task.name}, ["*"])
        for eco in eco_docs:
            employee_data[task.name]["employee_eco"].append({
                "team_work": eco.team_work,
                "communication_skills": eco.communication_skills,  # Corrected typo
                "positive_attitude_overall": eco.positive_attitude_overall,
            })

        # Fetch and append skill documents for the employee
        skill_docs = frappe.get_all("Employee Skill Map", {"employee": task.name}, ["*"])
        for skills in skill_docs:
            skill_doc = frappe.get_doc("Employee Skill Map", skills.name)
            for skill in skill_doc.employee_skills:
                employee_data[task.name]["employee_skill"].append({
                    "skill": skill.skill,
                    "evaluation_date": skill.evaluation_date,
                })
            for training in skill_doc.trainings:
                employee_data[task.name]["employee_skill"].append({
                    "training": training.training,
                    "training_date": training.training_date,
                })

    # Debugging message to check the final employee data structure
    # frappe.msgprint(f"{employee_data[task.name]['employee_skill']}")

    # Convert the dictionary to a list of rows
    for emp, emp_data in employee_data.items():
        for tas in emp_data["employee_task"]:
            row = {
                "status": tas["status"],
                "project": tas["project"],
                "priority": tas["priority"],
            }

        for att in emp_data["attendance_records"]:
            row.update ({
                "employee_name": emp_data["employee_name"],
                "company": emp_data["company"],
                "department": emp_data["department"],
                "attendance_status": att["attendance_status"],
                "attendance_date": att["attendance_date"],
            })

            if emp_data["feedback_ratings"]:
                for feedback in emp_data["feedback_ratings"]:
                    row.update({
                        "feedback_criteria": feedback["feedback_criteria"],
                        "feedback_weightage": feedback["feedback_weightage"],
                        "total_score": feedback["total_score"],
                    })

            if emp_data["employee_eco"]:
                for eco in emp_data["employee_eco"]:
                    row.update({
                        "team_work": eco["team_work"],
                        "communication_skills": eco["communication_skills"],
                        "positive_attitude_overall": eco["positive_attitude_overall"],
                    })

            # frappe.msgprint(f"{emp_data['employee_skill']}")
            if emp_data["employee_skill"]:
                for skill in emp_data["employee_skill"]:
                    if "skill" in skill and "evaluation_date" in skill:
                        row.update({
                            "skill": skill["skill"],
                            "evaluation_date": skill["evaluation_date"],
                        })
                    if "training" in skill and "training_date" in skill:
                        row.update({
                            "training": skill["training"],
                            "training_date": skill["training_date"],
                        })
                    

            data.append(row.copy())

    return data








    # frappe.msgprint(f"{data}")
        # for row in data:
    # Initialize variables to store concatenated attendance and feedback data
        # attendance_statuses = []
        # attendance_dates = []
        # feedback_criteria_list = []
        # feedback_weightages = []
        # total_scores = []
        
        # # Process attendance records
        # for row in att_docs:
        #     attendance_statuses.append(row.status)
        #     attendance_dates.append(str(row.attendance_date))
        
        # # Process feedback records
        
        # # Concatenate the lists into single strings
        # concatenated_attendance_statuses = ', '.join(attendance_statuses)
        # concatenated_attendance_dates = ', '.join(attendance_dates)
        # concatenated_feedback_criteria = ', '.join(feedback_criteria_list)
        # concatenated_feedback_weightages = ', '.join(feedback_weightages)
        # concatenated_total_scores = ', '.join(total_scores)
        
        # # Append the aggregated data to the data list
        # data.append({
        #     "employee_name": task.employee_name,
        #     "company": task.company,
        #     "department": task.department,
        #     "attendance_statuses": concatenated_attendance_statuses,
        #     "attendance_dates": concatenated_attendance_dates,
        #     "feedback_criteria": concatenated_feedback_criteria,
        #     "feedback_weightages": concatenated_feedback_weightages,
        #     "total_scores": concatenated_total_scores
        # })


















    # for task in task_data:
    #     my_dict = {}
    #     att_status = ''
    #     att_date = ''
    #     att_docs = frappe.get_all("Attendance", {"employee": task.name}, ["*"])
    #     for row in att_docs:
    #         frappe.msgprint(f"{row}")
    #         att_status = row.status
    #         att_date = row.attendance_date
    #         my_dict.update({
    #             "attendance_status" : att_status,
    #             "attendance_date" : att_date
    #         })
    #     feedback_criteria = ''
    #     feedback_weightage = ''
    #     total_score = ''
    #     feed_docs = frappe.get_all("Employee Performance Feedback", {"employee" : task.name}, ["*"])
    #     for row in feed_docs:
    #         doc = frappe.get_doc("Employee Performance Feedback", row.name)
    #         for child in doc.feedback_ratings:
    #             feedback_criteria = child.criteria
    #             feedback_weightage = child.per_weightage
    #             total_score = doc.total_score
    #     data.append({
    #         "employee_name": task.employee_name,
    #         # "status": task.status,
    #         # "project": task.project,
    #         # "priority": task.priority,
    #         "company": task.company,
    #         "department": task.department,
    #         "attendance_status": att_status,
    #         "attendance_date": att_date,
    #         "feedback_criteria": feedback_criteria,
    #         "feedback_weightage": feedback_weightage,
    #         "total_score": total_score,
    #         # "team_works": eco.team_works,
    #         # "comunication_skills": eco.comunication_skills,
    #         # "positive_attitude_overall": eco.positive_attitude_overall,
    #         # "skill": skill.skill,
    #         # "evaluation_date": skill.evaluation_date,
    #         # "training": training.training,
    #         # "training_date": training.training_date
    #     })           
        # attendance_data = frappe.get_all('Attendance', {"employee" : task.name}, fields=["*"])
        # for attendance in attendance_data:
        #     performance_feedback = frappe.get_all('Employee Performance Feedback', filters=emp_filters, fields=["*"])

        #     for feedback in performance_feedback:
        #         feedback_ratings = frappe.get_all('Employee Feedback Rating', filters={'parent': feedback.name}, fields=["*"])
        
        #         criteria_list = [rating.criteria for rating in feedback_ratings]
        #         weightage_list = [rating.per_weightage for rating in feedback_ratings]

        #         criteria_str = ", ".join(criteria_list)
        #         weightage_str = ", ".join(map(str, weightage_list))
        #         eco_data = frappe.get_list('Employee Performance on ECO', filters=emp_filters, fields=["*"])
    
        #         for eco in eco_data:
        #              employee_skill_maps = frappe.get_all('Employee Skill Map', filters=emp_filters, fields=["*"])

        #         for skill_map in employee_skill_maps:
        #             skills = frappe.get_all('Employee Skill', filters={'parent': skill_map.name}, fields=["*"])
        #             trainings = frappe.get_all('Employee Training', filters={'parent': skill_map.name}, fields=["*"])
        #             for skill in skills:
        #                 for training in trainings:
        #                     data.append({
        #                     "employee_name": attendance.employee_name,
        #                     "status": task.status,
        #                     "project": task.project,
        #                     "priority": task.priority,
        #                     "company": attendance.company,
        #                     "department": attendance.department,
        #                     "attendance_status": attendance.status,
        #                     "attendance_date": attendance.attendance_date,
        #                     "feedback_criteria": criteria_str,
        #                     "feedback_weightage": weightage_str,
        #                     "total_score": feedback.total_score,
        #                     "team_works": eco.team_works,
        #                     "comunication_skills": eco.comunication_skills,
        #                     "positive_attitude_overall": eco.positive_attitude_overall,
        #                     "skill": skill.skill,
        #                     "evaluation_date": skill.evaluation_date,
        #                     "training": training.training,
        #                     "training_date": training.training_date
        #                 })    
    return data
