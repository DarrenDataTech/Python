# SQL Cheat Sheet

```sql
-- SELECT statements
SELECT column1, column2 FROM table;
SELECT * FROM table;

-- DISTINCT
SELECT DISTINCT column FROM table;

-- WHERE clause
SELECT * FROM table WHERE condition;
-- Operators: =, !=, <>, <, >, <=, >=, BETWEEN, IN, LIKE, IS NULL

-- AND, OR, NOT
SELECT * FROM table WHERE column1 = 'value' AND column2 > 5;
SELECT * FROM table WHERE NOT column IS NULL;

-- ORDER BY
SELECT * FROM table ORDER BY column ASC;
SELECT * FROM table ORDER BY column DESC;

-- LIMIT / OFFSET
SELECT * FROM table LIMIT 10 OFFSET 20;

-- INSERT
INSERT INTO table (column1, column2) VALUES (value1, value2);

-- UPDATE
UPDATE table SET column1 = value1 WHERE condition;

-- DELETE
DELETE FROM table WHERE condition;

-- CREATE TABLE
CREATE TABLE table_name (
    id SERIAL PRIMARY KEY,
    column1 datatype,
    column2 datatype
);

-- DROP TABLE
DROP TABLE table_name;

-- ALTER TABLE
ALTER TABLE table_name ADD column_name datatype;
ALTER TABLE table_name DROP COLUMN column_name;
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;

-- JOINS
SELECT * FROM table1
JOIN table2 ON table1.id = table2.fk_id;

SELECT * FROM table1
LEFT JOIN table2 ON table1.id = table2.fk_id;

SELECT * FROM table1
RIGHT JOIN table2 ON table1.id = table2.fk_id;

SELECT * FROM table1
FULL OUTER JOIN table2 ON table1.id = table2.fk_id;

-- GROUP BY + Aggregate Functions
SELECT column, COUNT(*) FROM table GROUP BY column;
SELECT column, SUM(amount) FROM table GROUP BY column;

-- HAVING (filters grouped results)
SELECT column, COUNT(*) FROM table GROUP BY column HAVING COUNT(*) > 1;

-- Subqueries
SELECT * FROM table WHERE column IN (
    SELECT column FROM another_table WHERE condition
);

-- CASE statements
SELECT name,
    CASE
        WHEN score >= 90 THEN 'A'
        WHEN score >= 80 THEN 'B'
        ELSE 'F'
    END AS grade
FROM students;

-- Views
CREATE VIEW view_name AS
SELECT column1, column2 FROM table WHERE condition;

-- Indexes
CREATE INDEX idx_name ON table (column);

-- Transactions
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT; -- or ROLLBACK;

-- Comments
-- Single-line comment
/* Multi-line
   comment */
```
