import csv
import random
import string
from datetime import datetime, timedelta
import hashlib

def random_string(n=8):
    return ''.join(random.choices(string.ascii_lowercase, k=n))

def random_email():
    return f"{random_string(6)}@example.com"

def random_hash():
    return hashlib.sha256(random_string(16).encode()).hexdigest()

def random_date(start_year=2020, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def generate_users(n, path):
    rows = []
    for i in range(1, n+1):
        rows.append({
            "user_id": i,
            "username": random_string(8),
            "email": random_email(),
            "pfp_hash": random_hash(),
            "create_date": random_date().date(),
            "password_hash": random_hash()
        })
    write_csv(path, rows[0].keys(), rows)

def generate_spreadsheets(n, users, path):
    rows = []
    for i in range(1, n+1):
        user_id = random.choice(users)
        rows.append({
            "sheet_id": i,
            "user_id": user_id,
            "sheet_name": f"sheet_{random_string(5)}",
            "sheet_weight": random.randint(100, 5000),
            "sheet_pages": random.randint(1, 10),
            "upload_date": random_date().date()
        })
    write_csv(path, rows[0].keys(), rows)

def generate_features(features_list, path):
    rows = []
    for i, feat in enumerate(features_list, 1):
        rows.append({"feature_id": i, "feature_name": feat})
    write_csv(path, rows[0].keys(), rows)

def generate_feature_runs(n, users, sheets, features, path):
    rows = []
    for i in range(1, n+1):
        start = random_date()
        end = start + timedelta(seconds=random.randint(1, 5000))
        rows.append({
            "feat_run_id": i,
            "user_id": random.choice(users),
            "sheet_id": random.choice(sheets),
            "feature_id": random.choice(features),
            "input_weight": random.randint(100, 5000),
            "output_weight": random.randint(80, 4800),
            "run_status": random.choice([True, False]),
            "run_start_date": start,
            "run_end_date": end,
            "duration_ms": int((end - start).total_seconds() * 1000)
        })
    write_csv(path, rows[0].keys(), rows)

def generate_feature_run_details(runs, feature_map, path):
    attr_options = {
        "merge": ["join_type", "sort_order"],
        "inspect": ["cell_range", "preview_rows"],
        "split": ["split_column", "delimiter"],
        "clean-up": ["remove_duplicates", "trim_spaces"],
        "convert-csv": ["delimiter", "encoding"],
        "convert-pdf": ["page_size", "orientation"],
        "convert-json": ["indent", "flatten"],
        "fill-series": ["series_type", "start_value", "step"],
        "password-protect": ["password_strength", "hint"],
        "summary-stats": ["columns", "include_median"],
        "correlation-matrix": ["method", "columns"]
    }

    rows = []
    detail_id = 1
    for run_id, feature_id in runs:
        feature_name = feature_map[feature_id]
        possible_attrs = attr_options.get(feature_name, ["param"])
        attrs = random.sample(possible_attrs, random.randint(1, min(3, len(possible_attrs))))
        for attr in attrs:
            rows.append({
                "detail_id": detail_id,
                "feat_run_id": run_id,
                "attr_name": attr,
                "attr_value": random_string(5)
            })
            detail_id += 1
    write_csv(path, rows[0].keys(), rows)

def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
