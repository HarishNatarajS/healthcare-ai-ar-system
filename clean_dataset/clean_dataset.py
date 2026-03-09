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

print("Starting dataset generation...")

for i in range(NUM_RECORDS):
    claim_id = f"C{i+1}"
    patient_id = f"P{random.randint(1000, 9999)}"
    patient_age = random.randint(18, 90)
    patient_gender = random.choice(genders)
    service_type = random.choice(service_types)
    department = random.choice(departments)
    payer_type = random.choice(payer_types)
    
    insurance_company = random.choice(insurance_companies) if "Insurance" in payer_type else "None"
    
    claim_amount = random.randint(500, 20000)
    approved_amount = round(claim_amount * random.uniform(0.65, 0.95), 2)
    
    payment_type = random.choice(["full", "partial", "pending"])
    if payment_type == "full":
        payment_received = approved_amount
    elif payment_type == "partial":
        payment_received = round(approved_amount * random.uniform(0.2, 0.8), 2)
    else:
        payment_received = 0.0
    
    balance_due = round(approved_amount - payment_received, 2)
    
    days_in_ar = random.randint(30, 120) if payment_received == 0 else random.randint(1, 25)
    followup_count = days_in_ar // 15
    last_followup_days = random.randint(1, 20)
    denial_flag = random.choice([0, 1])
    
    priority_label = "High" if days_in_ar > 60 else ("Medium" if days_in_ar > 30 else "Low")
    claim_status = "Paid" if balance_due == 0 else ("Pending" if payment_received == 0 else "Partial")
    
    city = random.choice(cities)
    
    row = [
        claim_id, patient_id, patient_age, patient_gender, city,
        service_type, department, payer_type, insurance_company,
        claim_amount, approved_amount, payment_received, balance_due,
        claim_status, days_in_ar, followup_count, last_followup_days,
        denial_flag, priority_label
    ]
    data.append(row)
    
    if (i + 1) % 10000 == 0:
        print(f"{i + 1} records generated...")

print("Dataset generation finished.")

# Create DataFrame
columns = [
    "claim_id", "patient_id", "patient_age", "patient_gender", "patient_city",
    "service_type", "department", "payer_type", "insurance_company",
    "claim_amount", "approved_amount", "payment_received", "balance_due",
    "claim_status", "days_in_ar", "followup_count", "last_followup_days",
    "denial_flag", "priority_label"
]

df = pd.DataFrame(data, columns=columns)

# Data cleaning
df['patient_age'] = df['patient_age'].astype('int16')
df['claim_amount'] = df['claim_amount'].astype('float32')
df['approved_amount'] = df['approved_amount'].astype('float32')
df['payment_received'] = df['payment_received'].astype('float32')
df['balance_due'] = df['balance_due'].astype('float32')
df['days_in_ar'] = df['days_in_ar'].astype('int16')
df['followup_count'] = df['followup_count'].astype('int8')
df['last_followup_days'] = df['last_followup_days'].astype('int8')
df['denial_flag'] = df['denial_flag'].astype('int8')

# Check for nulls
print("\nNull values check:")
print(df.isnull().sum())

# Remove duplicates
df = df.drop_duplicates(subset=['claim_id'], keep='first')

# Validate data integrity
print(f"\nData validation:")
print(f"Total rows after deduplication: {len(df)}")
print(f"Claim amount range: ${df['claim_amount'].min():.2f} - ${df['claim_amount'].max():.2f}")
print(f"Balance due range: ${df['balance_due'].min():.2f} - ${df['balance_due'].max():.2f}")
print(f"\nClaim status distribution:\n{df['claim_status'].value_counts()}")
print(f"\nPriority distribution:\n{df['priority_label'].value_counts()}")

# Save CSV
file_name = "healthcare_claims_dataset_100k.csv"
df.to_csv(file_name, index=False)

print(f"\nCSV file saved as: {file_name}")
print("Dataset generation completed successfully!")