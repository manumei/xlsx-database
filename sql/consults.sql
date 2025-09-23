-- Me habia dicho Nacho que mejor mantener consistencia en el idioma asi que como estan las tablas y entities y todo en ingles, dejo los
-- comentarios en ingles tambien, porque tiene mas sentido usar los nombres reales de las relaciones y entidades en su contexto (ya despues para el informe los traduzco)

-- Q1: Count users per email domain
SELECT split_part(email, '@', 2) AS domain, COUNT(*) AS users
FROM Users
GROUP BY domain
ORDER BY users DESC;

-- Q2: List spreadsheets per user
SELECT u.email, COUNT(s.sheet_id) AS total_sheets
FROM Users u
LEFT JOIN Spreadsheets s ON u.email = s.email
GROUP BY u.email;

-- Q3: Average file size of spreadsheets per user
SELECT u.email,
        ROUND(AVG(s.file_size),2) AS avg_file_size
FROM Users u
JOIN Spreadsheets s ON u.email = s.email
GROUP BY u.email
ORDER BY avg_file_size DESC;

-- Q4: Find the largest spreadsheet(s) by file size
SELECT s.sheet_id,
        s.sheet_name,
        u.email,
        s.file_size
FROM Spreadsheets s
JOIN Users u ON s.email = u.email
WHERE s.file_size = (SELECT MAX(file_size) FROM Spreadsheets);

-- Q5: Total number of distinct features
SELECT COUNT(*) AS total_features
FROM Features;

-- Q6: How many times each feature was run
SELECT f.feature_name,
        COUNT(fr.feat_run_id) AS run_count
FROM Features f
LEFT JOIN FeatureRuns fr ON f.feature_id = fr.feature_id
GROUP BY f.feature_name
ORDER BY run_count DESC;

-- Q7: Average output_weight per feature
SELECT f.feature_name,
        ROUND(AVG(fr.output_weight),2) AS avg_output_weight
FROM Features f
JOIN FeatureRuns fr ON f.feature_id = fr.feature_id
GROUP BY f.feature_name
ORDER BY avg_output_weight DESC;

-- Q8: Average output_weight per user
SELECT u.email,
        ROUND(AVG(fr.output_weight),2) AS avg_output_weight
FROM Users u
JOIN Spreadsheets s ON u.email = s.email
JOIN FeatureRuns fr ON s.sheet_id = fr.sheet_id
GROUP BY u.email
ORDER BY avg_output_weight DESC;

-- Q9: Longest-running feature run (based on start and end date)
SELECT fr.feat_run_id,
        f.feature_name,
        u.email,
        (fr.run_end_date - fr.run_start_date) AS duration
FROM FeatureRuns fr
JOIN Features f ON fr.feature_id = f.feature_id
JOIN Spreadsheets s ON fr.sheet_id = s.sheet_id
JOIN Users u ON s.email = u.email
WHERE fr.run_end_date IS NOT NULL
    AND fr.run_start_date IS NOT NULL
ORDER BY duration DESC
LIMIT 1;

-- Q10: Feature run counts grouped by run_status
SELECT fr.run_status,
        COUNT(*) AS total_runs
FROM FeatureRuns fr
GROUP BY fr.run_status
ORDER BY total_runs DESC;

-- Q11: Features ranked by most fails (run_status = 'False')
SELECT f.feature_name,
        COUNT(fr.feat_run_id) AS fail_count
FROM Features f
JOIN FeatureRuns fr ON f.feature_id = fr.feature_id
WHERE fr.run_status = 'False'
GROUP BY f.feature_name
ORDER BY fail_count DESC;

-- Q12: Users who never uploaded a spreadsheet
SELECT u.email
FROM Users u
LEFT JOIN Spreadsheets s ON u.email = s.email
WHERE s.sheet_id IS NULL;

-- Q13: Users who uploaded more than 2 spreadsheets
SELECT u.email,
        COUNT(s.sheet_id) AS total_sheets
FROM Users u
JOIN Spreadsheets s ON u.email = s.email
GROUP BY u.email
HAVING COUNT(s.sheet_id) > 2
ORDER BY total_sheets DESC;

-- Q14: FeatureRuns per month
SELECT TO_CHAR(fr.run_start_date, 'YYYY-MM') AS month,
        COUNT(*) AS runs_in_month
FROM FeatureRuns fr
WHERE fr.run_start_date IS NOT NULL
GROUP BY TO_CHAR(fr.run_start_date, 'YYYY-MM')
ORDER BY month;

-- Q15: Features that have never been used in any run
SELECT f.feature_name
FROM Features f
LEFT JOIN FeatureRuns fr ON f.feature_id = fr.feature_id
WHERE fr.feat_run_id IS NULL;

-- Q16: Top 5 users by total feature runs
SELECT u.email,
        COUNT(fr.feat_run_id) AS total_runs
FROM Users u
JOIN Spreadsheets s ON u.email = s.email
JOIN FeatureRuns fr ON s.sheet_id = fr.sheet_id
GROUP BY u.email
ORDER BY total_runs DESC
LIMIT 5;

-- Q17: General distribution of attributes stored in FeatureRunDetails
SELECT attr_name,
        COUNT(*) AS occurrences
FROM FeatureRunDetails
GROUP BY attr_name
ORDER BY occurrences DESC;

-- Q18: For 'merge' feature, average amount_of_sheets merged
SELECT ROUND(AVG(CAST(d.attr_value AS INT)),2) AS avg_sheets_merged
FROM FeatureRunDetails d
JOIN FeatureRuns fr ON d.feat_run_id = fr.feat_run_id
JOIN Features f ON fr.feature_id = f.feature_id
WHERE f.feature_name = 'merge'
    AND d.attr_name = 'amount_of_sheets';

-- Q19: For 'split' feature, average percent_kept
SELECT ROUND(AVG(CAST(d.attr_value AS NUMERIC)),2) AS avg_percent_kept
FROM FeatureRunDetails d
JOIN FeatureRuns fr ON d.feat_run_id = fr.feat_run_id
JOIN Features f ON fr.feature_id = f.feature_id
WHERE f.feature_name = 'split'
    AND d.attr_name = 'percent_kept';

-- Q20: For 'clean-up' feature, total cells_cleaned across all runs
SELECT SUM(CAST(d.attr_value AS INT)) AS total_cells_cleaned
FROM FeatureRunDetails d
JOIN FeatureRuns fr ON d.feat_run_id = fr.feat_run_id
JOIN Features f ON fr.feature_id = f.feature_id
WHERE f.feature_name = 'clean-up'
    AND d.attr_name = 'cells_cleaned';

-- Q21: Total final sum of total_rows_appended from the 'append' feature
SELECT SUM(CAST(d.attr_value AS INT)) AS total_rows_appended
FROM FeatureRunDetails d
JOIN FeatureRuns fr ON d.feat_run_id = fr.feat_run_id
JOIN Features f ON fr.feature_id = f.feature_id
WHERE f.feature_name = 'append'
    AND d.attr_name = 'total_rows_appended';

-- Q22: Months with the most cells_counted for 'correlation-matrix' feature
SELECT TO_CHAR(fr.run_start_date, 'YYYY-MM') AS month,
        SUM(CAST(d.attr_value AS INT)) AS total_cells_counted
FROM FeatureRunDetails d
JOIN FeatureRuns fr ON d.feat_run_id = fr.feat_run_id
JOIN Features f ON fr.feature_id = f.feature_id
WHERE f.feature_name = 'correlation-matrix'
    AND d.attr_name = 'cells_counted'
GROUP BY TO_CHAR(fr.run_start_date, 'YYYY-MM')
ORDER BY total_cells_counted DESC;

-- Q23: User with the most final_pages in the 'convert pdf' feature
SELECT u.email,
        SUM(CAST(d.attr_value AS INT)) AS total_final_pages
FROM FeatureRunDetails d
JOIN FeatureRuns fr ON d.feat_run_id = fr.feat_run_id
JOIN Features f ON fr.feature_id = f.feature_id
JOIN Spreadsheets s ON fr.sheet_id = s.sheet_id
JOIN Users u ON s.email = u.email
WHERE f.feature_name = 'convert pdf'
    AND d.attr_name = 'final_pages'
GROUP BY u.email
ORDER BY total_final_pages DESC
LIMIT 1;

-- Q24: Feature with the most cells_filled in the 'fill-series' feature
SELECT f.feature_name,
        SUM(CAST(d.attr_value AS INT)) AS total_cells_filled
FROM FeatureRunDetails d
JOIN FeatureRuns fr ON d.feat_run_id = fr.feat_run_id
JOIN Features f ON fr.feature_id = f.feature_id
WHERE f.feature_name = 'fill-series'
    AND d.attr_name = 'cells_filled'
GROUP BY f.feature_name
ORDER BY total_cells_filled DESC;
