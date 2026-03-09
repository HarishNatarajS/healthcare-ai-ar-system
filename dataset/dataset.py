import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------
# CONFIG
# -----------------------------

NUM_RECORDS = 100000   # 1 lakh records

# -----------------------------
# POSSIBLE VALUES
# -----------------------------

payer_types = [
    "Private Insurance",
    "Self Pay",
    "Government Medicare",
    "Government Medicaid",
    "Employer Health Plan",
    "Military Health",
    "Charity Program"
]

insurance_companies = [
    "Aetna",
    "BlueCross",
    "Cigna",
    "UnitedHealth",
    "Humana",
    "Kaiser Permanente",
    "Centene",
    "Molina Healthcare",
    "WellCare",
    "Anthem"
]

service_types = [
    "Consultation",
    "Surgery",
    "Lab Test",
    "Emergency Care",
    "Radiology",
    "Physiotherapy",
    "Dental Procedure",
    "Vaccination",
    "Health Checkup",
    "ICU Care"
]

departments = [
    "Cardiology",
    "Orthopedics",
    "Neurology",
    "General Medicine",
    "Pediatrics",
    "Dermatology",
    "Oncology",
    "Gynecology",
    "ENT",
    "Urology"
]

genders = ["Male", "Female", "Other"]

cities = [
    "New York",
    "Chicago",
    "Houston",
    "Los Angeles",
    "Dallas",
    "San Diego",
    "Boston",
    "Seattle",
    "Miami",
    "Atlanta"
]

claim_status_types = ["Paid", "Pending", "Partial", "Denied"]

# -----------------------------
# DATA STORAGE
# -----------------------------

data = []

# -----------------------------
# DATA GENERATION
# -----------------------------

print("Starting dataset generation...")

for i in range(NUM_RECORDS):

    claim_id = f"C{i+1}"
    patient_id = f"P{random.randint(1000,9999)}"

    patient_age = random.randint(18, 90)
    patient_gender = random.choice(genders)

    service_type = random.choice(service_types)
    department = random.choice(departments)

    payer_type = random.choice(payer_types)

    if "Insurance" in payer_type:
        insurance_company = random.choice(insurance_companies)
    else:
        insurance_company = "None"

    claim_amount = random.randint(500, 20000)

    approved_amount = claim_amount * random.uniform(0.65, 0.95)

    payment_type = random.choice(["full", "partial", "pending"])

    if payment_type == "full":
        payment_received = approved_amount
    elif payment_type == "partial":
        payment_received = approved_amount * random.uniform(0.2, 0.8)
    else:
        payment_received = 0

    balance_due = approved_amount - payment_received

    if payment_received == 0:
        days_in_ar = random.randint(30, 120)
    else:
        days_in_ar = random.randint(1, 25)

    followup_count = days_in_ar // 15

    last_followup_days = random.randint(1, 20)

    denial_flag = random.choice([0, 1])

    if days_in_ar > 60:
        priority_label = "High"
    elif days_in_ar > 30:
        priority_label = "Medium"
    else:
        priority_label = "Low"

    if balance_due == 0:
        claim_status = "Paid"
    elif payment_received == 0:
        claim_status = "Pending"
    else:
        claim_status = "Partial"

    city = random.choice(cities)

    row = [
        claim_id,
        patient_id,
        patient_age,
        patient_gender,
        city,
        service_type,
        department,
        payer_type,
        insurance_company,
        claim_amount,
        round(approved_amount,2),
        round(payment_received,2),
        round(balance_due,2),
        claim_status,
        days_in_ar,
        followup_count,
        last_followup_days,
        denial_flag,
        priority_label
    ]

    data.append(row)

    # progress debug
    if (i+1) % 10000 == 0:
        print(f"{i+1} records generated...")

print("Dataset generation finished.")

# -----------------------------
# CREATE DATAFRAME
# -----------------------------

columns = [
    "claim_id",
    "patient_id",
    "patient_age",
    "patient_gender",
    "patient_city",
    "service_type",
    "department",
    "payer_type",
    "insurance_company",
    "claim_amount",
    "approved_amount",
    "payment_received",
    "balance_due",
    "claim_status",
    "days_in_ar",
    "followup_count",
    "last_followup_days",
    "denial_flag",
    "priority_label"
]

df = pd.DataFrame(data, columns=columns)

print("Total rows created:", len(df))

# -----------------------------
# SAVE CSV
# -----------------------------

file_name = "healthcare_claims_dataset_100k.csv"

df.to_csv(file_name, index=False)

print("CSV file saved as:", file_name)
print("Dataset generation completed successfully!")