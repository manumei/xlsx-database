-- Load CSVs into iLoveXLSX tables

COPY Users(email, username, pfp_hash, create_date, password_hash)
FROM '/tmp/users.csv'
DELIMITER ',' CSV HEADER;

COPY Spreadsheets(sheet_id, email, sheet_name, file_size, sheet_pages, upload_date)
FROM '/tmp/spreadsheets.csv'
DELIMITER ',' CSV HEADER;

COPY Features(feature_id, feature_name)
FROM '/tmp/features.csv'
DELIMITER ',' CSV HEADER;

COPY FeatureRuns(feat_run_id, sheet_id, feature_id, output_weight, run_status, run_start_date, run_end_date)
FROM '/tmp/feature_runs.csv'
DELIMITER ',' CSV HEADER;

COPY FeatureRunDetails(detail_id, feat_run_id, attr_name, attr_value)
FROM '/tmp/feature_run_details.csv'
DELIMITER ',' CSV HEADER;
