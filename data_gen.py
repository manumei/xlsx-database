import db_utils as db

# Parameters
N_USERS = 10
N_SPREADSHEETS = 20
N_RUNS = 30
FEATURES = ["Conversion", "Merge", "Clean-Up"]

# 1. Generate Users
db.generate_users(N_USERS, "users.csv")

# 2. Generate Spreadsheets
user_ids = list(range(1, N_USERS+1))
db.generate_spreadsheets(N_SPREADSHEETS, user_ids, "spreadsheets.csv")

# 3. Generate Features
db.generate_features(FEATURES, "features.csv")

# 4. Generate Feature Runs
sheet_ids = list(range(1, N_SPREADSHEETS+1))
feature_ids = list(range(1, len(FEATURES)+1))
db.generate_feature_runs(N_RUNS, user_ids, sheet_ids, feature_ids, "feature_runs.csv")

# 5. Generate Feature Run Details
run_ids = list(range(1, N_RUNS+1))
db.generate_feature_run_details(run_ids, "feature_run_details.csv")

print("CSV mock data generated successfully.")
