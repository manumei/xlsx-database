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
