import db_utils as db

# Parameters
N_USERS = 50
N_SPREADSHEETS = 125
N_RUNS = 160
FEATURES = [
    "inspect", "merge", "split", "append", "clean-up",
    "convert csv", "convert pdf", "convert-json",
    "fill-series", "password-protect", "summary-stats", "correlation-matrix"
]

# 1. Users
emails = db.generate_users(N_USERS, "data/users.csv")

# 2. Spreadsheets
sheet_ids = db.generate_spreadsheets(N_SPREADSHEETS, emails, "data/spreadsheets.csv")

# 3. Features
features = db.generate_features(FEATURES, "data/features.csv")
feature_map = {f["feature_id"]: f["feature_name"] for f in features}

# 4. Feature Runs
runs = db.generate_feature_runs(N_RUNS, sheet_ids, features, "data/feature_runs.csv")

# 5. Feature Run Details
db.generate_feature_run_details(runs, feature_map, "data/feature_run_details.csv")

print("CSV mock data generated successfully.")
