import frappe
from frappe import _, whitelist

@frappe.whitelist(allow_guest=True)
def get_dashboard_data(from_date=None, to_date=None):
    data = {}

    # Convert dates if provided
    if from_date:
        from_date = frappe.utils.getdate(from_date)
    if to_date:
        to_date = frappe.utils.getdate(to_date)

    # 🏥 **General Statistics (Graph Data)**
    data_list = []
    
    # Hospitals and Beds Count
    hospitals = frappe.db.sql("""
        SELECT count(name) as hospitals, sum(total_no_of_beds) as beds 
        FROM `tabHospital`
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

    # Patients Admitted
    patients = frappe.db.sql("""
        SELECT count(*) as patients_admitted 
        FROM `tabBurn Admission Assessment`
        WHERE (%s IS NULL OR date_of_hospital_admission >= %s)
          AND (%s IS NULL OR date_of_hospital_admission <= %s)
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data_list.append({
        "title": "Admitted",
        "data": patients[0]["patients_admitted"],
        "index": 3
    })

    # Patients Discharged
    patients_discharged = frappe.db.sql("""
        SELECT count(*) as patients_discharged 
        FROM `tabHospital Discharge Detail`
        WHERE (%s IS NULL OR date_of_discharge >= %s)
          AND (%s IS NULL OR date_of_discharge <= %s)
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data_list.append({
        "title": "Discharged",
        "data": patients_discharged[0]["patients_discharged"],
        "index": 4
    })

    # Gender Statistics
    male_patients = frappe.db.sql("""
        SELECT count(*) as male_patients 
        FROM `tabBurn Admission Assessment` 
        WHERE sex = 'Male'
          AND (%s IS NULL OR date_of_hospital_admission >= %s)
          AND (%s IS NULL OR date_of_hospital_admission <= %s)
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data_list.append({
        "title": "Male",
        "data": male_patients[0]["male_patients"],
        "index": 5
    })

    female_patients = frappe.db.sql("""
        SELECT count(*) as female_patients 
        FROM `tabBurn Admission Assessment` 
        WHERE sex = 'Female'
          AND (%s IS NULL OR date_of_hospital_admission >= %s)
          AND (%s IS NULL OR date_of_hospital_admission <= %s)
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data_list.append({
        "title": "Female",
        "data": female_patients[0]["female_patients"],
        "index": 6
    })

    # Age Group Statistics
    zero_to_four_patients = frappe.db.sql("""
        SELECT COUNT(*) as zero_to_four
        FROM `tabBurn Admission Assessment`
        WHERE TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 0 AND 4
          AND (%s IS NULL OR date_of_hospital_admission >= %s)
          AND (%s IS NULL OR date_of_hospital_admission <= %s)
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data_list.append({
        "title": "0-4 Years",
        "data": zero_to_four_patients[0]["zero_to_four"],
        "index": 7
    })

    five_to_eleven_patients = frappe.db.sql("""
        SELECT COUNT(*) as five_to_eleven
        FROM `tabBurn Admission Assessment`
        WHERE TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 5 AND 11
          AND (%s IS NULL OR date_of_hospital_admission >= %s)
          AND (%s IS NULL OR date_of_hospital_admission <= %s)
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data_list.append({
        "title": "5-11 Years",
        "data": five_to_eleven_patients[0]["five_to_eleven"],
        "index": 8
    })

    twelve_to_eighteen_patients = frappe.db.sql("""
        SELECT COUNT(*) as twelve_to_eighteen
        FROM `tabBurn Admission Assessment`
        WHERE TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 12 AND 18
          AND (%s IS NULL OR date_of_hospital_admission >= %s)
          AND (%s IS NULL OR date_of_hospital_admission <= %s)
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data_list.append({
        "title": "12-18 Years",
        "data": twelve_to_eighteen_patients[0]["twelve_to_eighteen"],
        "index": 9
    })

    above_eighteen_patients = frappe.db.sql("""
        SELECT COUNT(*) as above_eighteen
        FROM `tabBurn Admission Assessment`
        WHERE TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) > 18
          AND (%s IS NULL OR date_of_hospital_admission >= %s)
          AND (%s IS NULL OR date_of_hospital_admission <= %s)
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data_list.append({
        "title": "Above 18 Years",
        "data": above_eighteen_patients[0]["above_eighteen"],
        "index": 10
    })

    # Add graph data to the response
    data["graph_data"] = data_list

    # 📝 **Charts Data** (Admission Reasons, Burn Causes, Patients in Hospital)
    # Admission Reasons
    admission_reasons = frappe.db.sql("""
        SELECT how_was_the_burn_caused, COUNT(*) as admission_reasons_count
        FROM `tabBurn Admission Assessment`
        WHERE (%s IS NULL OR date_of_hospital_admission >= %s)
          AND (%s IS NULL OR date_of_hospital_admission <= %s)
        GROUP BY how_was_the_burn_caused
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data["admission_reasons"] = admission_reasons

    # Burn Causes
    burn_cause = frappe.db.sql("""
        SELECT burn_cause, COUNT(*) as burn_cause_count
        FROM `tabBurn Admission Assessment`
        WHERE (%s IS NULL OR date_of_hospital_admission >= %s)
          AND (%s IS NULL OR date_of_hospital_admission <= %s)
        GROUP BY burn_cause
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data["burn_cause"] = burn_cause

    # Patients in Hospital
    patients_in_hospital = frappe.db.sql("""
        SELECT COUNT(*) as patients_in_hospital, hospital
        FROM `tabBurn Admission Assessment`
        WHERE discharge_status = 'Admitted'
          AND (%s IS NULL OR date_of_hospital_admission >= %s)
          AND (%s IS NULL OR date_of_hospital_admission <= %s)
        GROUP BY hospital
    """, (from_date, from_date, to_date, to_date), as_dict=True)
    data["patients_in_hospital"] = patients_in_hospital

    # Hospitals Map Data
    hospitals_map_data = frappe.db.sql("""
        SELECT city, latitude, longitude
        FROM `tabHospital`
    """, as_dict=True)
    data["hospitals_map_data"] = hospitals_map_data

    return data
