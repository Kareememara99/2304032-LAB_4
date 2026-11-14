USE library_lab4;
GO

-- F2.1 Search Books

DECLARE @keyword VARCHAR(100) = '';
DECLARE @min_price DECIMAL(10,2) = 10;
DECLARE @max_price DECIMAL(10,2) = 20;
DECLARE @category_id INT = NULL;

SELECT
    b.book_id,
    b.title,
    b.price,
    b.publish_year,
    c.name AS category
FROM BOOK b
JOIN CATEGORY c
    ON b.category_id = c.category_id
WHERE
    b.title LIKE '%' + @keyword + '%'
    AND b.price BETWEEN @min_price AND @max_price
    AND (@category_id IS NULL OR b.category_id = @category_id)
ORDER BY b.price ASC;
GO

-- F2.2 Catalogue

SELECT
    b.book_id,
    b.title,
    b.price,
    b.publish_year,
    a.name AS author_name,
    p.name AS publisher_name,
    c.name AS category_name
FROM BOOK b
INNER JOIN AUTHOR a
    ON b.author_id = a.author_id
INNER JOIN PUBLISHER p
    ON b.publisher_id = p.publisher_id
INNER JOIN CATEGORY c
    ON b.category_id = c.category_id
ORDER BY b.title;
GO


-- F2.3 A: Books count and average price per category

SELECT
    c.name AS category_name,
    COUNT(b.book_id) AS books_count,
    AVG(b.price) AS average_price
FROM CATEGORY c
LEFT JOIN BOOK b
    ON c.category_id = b.category_id
GROUP BY c.category_id, c.name;
GO

-- F2.3 B: Authors with at least 2 books

SELECT
    a.author_id,
    a.name,
    COUNT(b.book_id) AS books_count
FROM AUTHOR a
JOIN BOOK b
    ON a.author_id = b.author_id
GROUP BY a.author_id, a.name
HAVING COUNT(b.book_id) >= 2;
GO

-- F2.3 C: Library price statistics

SELECT
    SUM(price) AS total_price,
    MIN(price) AS minimum_price,
    MAX(price) AS maximum_price
FROM BOOK;
GO

-- F2.4 A: Outstanding loans

SELECT
    l.loan_id,
    b.title,
    m.name AS member_name,
    l.loan_date
FROM LOAN l
JOIN BOOK b
    ON l.book_id = b.book_id
JOIN MEMBER m
    ON l.member_id = m.member_id
WHERE l.return_date IS NULL;
GO

-- F2.4 B: Members who never borrowed

SELECT
    m.member_id,
    m.name,
    m.email
FROM MEMBER m
LEFT JOIN LOAN l
    ON m.member_id = l.member_id
WHERE l.loan_id IS NULL;
GO

-- F2.4 C: Books never borrowed

SELECT
    b.book_id,
    b.title
FROM BOOK b
LEFT JOIN LOAN l
    ON b.book_id = l.book_id
WHERE l.loan_id IS NULL;
GO

-- F2.5 A: Top 3 most borrowed books

SELECT TOP 3
    b.book_id,
    b.title,
    COUNT(l.loan_id) AS loans_count
FROM BOOK b
JOIN LOAN l
    ON b.book_id = l.book_id
GROUP BY b.book_id, b.title
ORDER BY loans_count DESC;
GO

-- F2.5 B: Member with the most loans

SELECT TOP 1
    m.member_id,
    m.name,
    COUNT(l.loan_id) AS loans_count
FROM MEMBER m
JOIN LOAN l
    ON m.member_id = l.member_id
GROUP BY m.member_id, m.name
ORDER BY loans_count DESC;
GO


-- F2.6 A: All authors including authors with zero books

SELECT
    a.author_id,
    a.name,
    COUNT(b.book_id) AS books_count
FROM AUTHOR a
LEFT JOIN BOOK b
    ON a.author_id = b.author_id
GROUP BY a.author_id, a.name
ORDER BY books_count DESC;
GO


-- F2.6 B: Books whose author and publisher share the same country

SELECT
    b.title,
    a.name AS author_name,
    a.country AS author_country,
    p.name AS publisher_name,
    p.country AS publisher_country
FROM BOOK b
JOIN AUTHOR a
    ON b.author_id = a.author_id
JOIN PUBLISHER p
    ON b.publisher_id = p.publisher_id
WHERE a.country = p.country;
GO

