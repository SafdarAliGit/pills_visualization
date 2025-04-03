# app/api.py
import frappe
from frappe import _, whitelist

@frappe.whitelist(allow_guest=True)
def get_graph_data():
    data_list = []
    hospitals = frappe.db.sql("""
        SELECT count(name) as hospitals, sum(total_no_of_beds) as beds FROM `tabHospital`
    """, as_dict=True)
    data_list.append({
        "title": "Hospitals",
        "data": hospitals[0]["hospitals"],
        "index": 1
    })

    data_list.append({
        "title": "Beds",
        "data": hospitals[0]["beds"],
        "index": 2
    })

    patients = frappe.db.sql("""
        SELECT count(*) as patients_admitted FROM `tabBurn Admission Assessment`
    """, as_dict=True)
    data_list.append({
        "title": "Patients Admitted",
        "data": patients[0]["patients_admitted"],
        "index": 3
    })

    patients_discharged = frappe.db.sql("""
        SELECT count(*) as patients_discharged FROM `tabHospital Discharge Detail`
    """, as_dict=True)

    data_list.append({
        "title": "Patients Discharged",
        "data": patients_discharged[0]["patients_discharged"],
        "index": 4
    })

    male_patients = frappe.db.sql("""
        SELECT count(*) as male_patients FROM `tabBurn Admission Assessment` WHERE sex = 'Male'
    """, as_dict=True)

    data_list.append({
        "title": "Male Patients",
        "data": male_patients[0]["male_patients"],
        "index": 5
    })

    female_patients = frappe.db.sql("""
        SELECT count(*) as female_patients FROM `tabBurn Admission Assessment` WHERE sex = 'Female'
    """, as_dict=True)

    data_list.append({
        "title": "Female Patients",
        "data": female_patients[0]["female_patients"],
        "index": 6
    })

    zero_to_four_patients = frappe.db.sql("""
        SELECT COUNT(*) as zero_to_four
        FROM `tabBurn Admission Assessment`
        WHERE TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 0 AND 4
    """, as_dict=True)

    data_list.append({
        "title": "0-4 Years Patients",
        "data": zero_to_four_patients[0]["zero_to_four"],
        "index": 7
    })

    five_to_eleven_patients = frappe.db.sql("""
        SELECT COUNT(*) as five_to_eleven
        FROM `tabBurn Admission Assessment`
        WHERE TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 5 AND 11
    """, as_dict=True)

    data_list.append({
        "title": "5-11 Years Patients",
        "data": five_to_eleven_patients[0]["five_to_eleven"],
        "index": 8
    })

    twelve_to_eighteen_patients = frappe.db.sql("""
        SELECT COUNT(*) as twelve_to_eighteen
        FROM `tabBurn Admission Assessment`
        WHERE TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 12 AND 18
    """, as_dict=True)

    data_list.append({
        "title": "12-18 Years Patients",
        "data": twelve_to_eighteen_patients[0]["twelve_to_eighteen"],
        "index": 9
    })

    above_eighteen_patients = frappe.db.sql("""
        SELECT COUNT(*) as above_eighteen
        FROM `tabBurn Admission Assessment`
        WHERE TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) > 18
    """, as_dict=True)

    data_list.append({
        "title": "Above 18 Years Patients",
        "data": above_eighteen_patients[0]["above_eighteen"],
        "index": 10
    })

    return data_list

@frappe.whitelist(allow_guest=True)
def get_charts_data():
    data = {
        
    }
    admission_reasons = frappe.db.sql("""
        SELECT how_was_the_burn_caused, COUNT(*) as admission_reasons_count
        FROM `tabBurn Admission Assessment`
        GROUP BY how_was_the_burn_caused
    """, as_dict=True)
    data["admission_reasons"] = admission_reasons

    burn_cause = frappe.db.sql("""
    SELECT burn_cause, COUNT(*) as burn_cause_count
    FROM `tabBurn Admission Assessment`
    GROUP BY burn_cause
    """, as_dict=True)
    data["burn_cause"] = burn_cause
    patients_in_hospital = frappe.db.sql("""
    SELECT COUNT(*) as patients_in_hospital, hospital
    FROM `tabBurn Admission Assessment`
    WHERE discharge_status = 'Admitted'
    GROUP BY hospital
    """, as_dict=True)
    data["patients_in_hospital"] = patients_in_hospital

    hospitals_map_data = frappe.db.sql("""
    SELECT city,latitude,longitude
    FROM `tabHospital`
    """, as_dict=True)

    data["hospitals_map_data"] = hospitals_map_data
    return data