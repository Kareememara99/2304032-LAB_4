
USE library_lab4;
GO

-- =========================================
-- 1. INSERT AUTHORS (4 AUTHORS)
-- =========================================

INSERT INTO AUTHOR (name, country)
VALUES
('Naguib Mahfouz', 'Egypt'),
('Agatha Christie', 'UK'),
('Gabriel Garcia Marquez', 'Colombia'),
('Taha Hussein', 'Egypt');
GO


-- =========================================
-- 2. INSERT PUBLISHERS (3 PUBLISHERS)
-- =========================================

INSERT INTO PUBLISHER (name, country)
VALUES
('Dar El Shorouk', 'Egypt'),
('Penguin Books', 'UK'),
('Vintage Books', 'USA');
GO


-- =========================================
-- 3. INSERT CATEGORIES (3 CATEGORIES)
-- =========================================

INSERT INTO CATEGORY (name)
VALUES
('Fiction'),
('Mystery'),
('Historical');
GO


-- =========================================
-- 4. INSERT BOOKS (10 BOOKS)
-- =========================================

INSERT INTO BOOK
(title, price, publish_year, author_id, publisher_id, category_id)
VALUES
('Palace Walk', 18.50, 1956, 1, 1, 3),
('Midaq Alley', 12.00, 1947, 1, 1, 1),
('Children of the Alley', 16.75, 1959, 1, 1, 1),

('Murder on the Orient Express', 14.25, 1934, 2, 2, 2),
('And Then There Were None', 19.00, 1939, 2, 2, 2),
('Death on the Nile', 17.50, 1937, 2, 2, 2),

('One Hundred Years of Solitude', 20.00, 1967, 3, 3, 1),
('Love in the Time of Cholera', 15.50, 1985, 3, 3, 1),

('The Thief and the Dogs', 13.00, 1961, 1, 1, 1),
('The Autumn of the Patriarch', 22.00, 1975, 3, 3, 1);
GO


-- =========================================
-- 5. INSERT MEMBERS (5 MEMBERS)
-- =========================================

INSERT INTO MEMBER (name, email, join_date)
VALUES
('Ahmed Ali', 'ahmed@gmail.com', '2025-01-10'),
('Mohamed Hassan', 'mohamed@gmail.com', '2025-02-15'),
('Sara Mahmoud', 'sara@gmail.com', '2025-03-20'),
('Mariam Adel', 'mariam@gmail.com', '2025-04-05'),
('Omar Khaled', 'omar@gmail.com', '2025-05-12');
GO


-- =========================================
-- 6. INSERT LOANS (12 LOANS)
-- =========================================

INSERT INTO LOAN (book_id, member_id, loan_date, return_date)
VALUES
(1, 1, '2025-06-01', '2025-06-10'),
(2, 1, '2025-06-11', '2025-06-20'),
(3, 1, '2025-06-21', NULL),
(4, 1, '2025-07-01', '2025-07-10'),

(1, 2, '2025-07-05', '2025-07-15'),
(5, 2, '2025-07-16', NULL),
(6, 2, '2025-07-20', '2025-07-30'),

(2, 3, '2025-08-01', '2025-08-10'),
(7, 3, '2025-08-11', NULL),
(8, 3, '2025-08-20', '2025-08-30'),

(4, 4, '2025-09-01', '2025-09-10'),
(5, 4, '2025-09-15', NULL);
GO


-- =========================================
-- VERIFY INSERTED DATA
-- =========================================

SELECT * FROM AUTHOR;
SELECT * FROM PUBLISHER;
SELECT * FROM CATEGORY;
SELECT * FROM BOOK;
SELECT * FROM MEMBER;
SELECT * FROM LOAN;
GO
