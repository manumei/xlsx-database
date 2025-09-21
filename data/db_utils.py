import csv, random, string, hashlib
from datetime import datetime, timedelta
from faker import Faker
import random
fake = Faker()

def random_string(n=8):
    return ''.join(random.choices(string.ascii_lowercase, k=n))

def random_username():
    first = fake.first_name()
    last = fake.last_name()
    options = [
        first,
        first + last,
        first + str(random.randint(1, 9999)),
        fake.user_name(),
        first + random.choice(["x", "y", "z"])
    ]
    return random.choice(options)

def random_email(username):
    domains = ["@gmail.com","@hotmail.com","@icloud.com",
                "@yahoo.com","@protonmail.com","@example.org"]
    # bias: 70% chance for gmail/hotmail/icloud
    if random.random() < 0.7:
        domain = random.choice(domains[:3])
    else:
        domain = random.choice(domains[3:])
    return f"{username.lower()}{random.randint(1,999)}{domain}"

def random_hash():
    return hashlib.sha256(random_string(16).encode()).hexdigest()

def random_date(start_year=2020, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

# USERS
def generate_users(n, path):
    rows = []
    usernames = set()
    for _ in range(n):
        while True:
            uname = random_username()
            if uname not in usernames:
                usernames.add(uname)
                break
        email = random_email(uname)
        rows.append({
            "email": email,
            "username": uname,
            "pfp_hash": random_hash(),
            "create_date": random_date().date(),
            "password_hash": random_hash()
        })
    write_csv(path, rows[0].keys(), rows)
    return [row["email"] for row in rows]

# SPREADSHEETS
def generate_spreadsheets(n, users, path):
    rows = []
    for i in range(1, n+1):
        owner = random.choice(users)  # must reference an existing user
        rows.append({
            "sheet_id": i,
            "email": owner,
            "sheet_name": f"sheet_{random_string(5)}",
            "file_size": random.randint(100, 5000),
            "sheet_pages": random.randint(1, 10),
            "upload_date": random_date().date()
        })
    write_csv(path, rows[0].keys(), rows)
    return [row["sheet_id"] for row in rows]

# FEATURES
def generate_features(features_list, path):
    rows = [{"feature_id": i+1, "feature_name": feat} for i, feat in enumerate(features_list)]
    write_csv(path, rows[0].keys(), rows)
    return rows

# FEATURE RUNS
def generate_feature_runs(n, sheets, features, path):
    rows = []
    for i in range(1, n+1):
        sheet = random.choice(sheets)  # must reference an existing sheet_id
        feat = random.choice(features)  # must reference an existing feature
        start = random_date()
        end = start + timedelta(milliseconds=random.randint(50, 25000))
        rows.append({
            "feat_run_id": i,
            "sheet_id": sheet,
            "feature_id": feat["feature_id"],
            "output_weight": random.randint(80, 4800),
            "run_status": random.choice([True, False]),
            "run_start_date": start,
            "run_end_date": end,
        })
    write_csv(path, rows[0].keys(), rows)
    return rows

# FEATURE RUN DETAILS
def generate_feature_run_details(runs, feature_map, path):
    detail_rows = []
    detail_id = 1
    for run in runs:
        feat_name = feature_map[run["feature_id"]]
        attr_value = None
        attr_name = None
        if feat_name == "merge":
            attr_name, attr_value = "amount_of_sheets", str(random.randint(2, 5))
        elif feat_name == "split":
            attr_name, attr_value = "percent_kept", str(random.randint(10, 90))
        elif feat_name == "append":
            attr_name, attr_value = "total_rows_appended", str(random.randint(100, 5000))
        elif feat_name == "clean-up":
            attr_name, attr_value = "cells_cleaned", str(random.randint(50, 10000))
        elif feat_name == "convert pdf":
            attr_name, attr_value = "final_pages", str(random.randint(1, 20))
        elif feat_name == "fill-series":
            attr_name, attr_value = "cells_filled", str(random.randint(5, 500))
        elif feat_name == "correlation-matrix":
            attr_name, attr_value = "cells_counted", str(random.randint(50, 5000))

        if attr_name:  # only add when feature has details
            detail_rows.append({
                "detail_id": detail_id,
                "feat_run_id": run["feat_run_id"],
                "attr_name": attr_name,
                "attr_value": attr_value
            })
            detail_id += 1
    if detail_rows:
        write_csv(path, detail_rows[0].keys(), detail_rows)
