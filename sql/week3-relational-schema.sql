CREATE DATABASE LibraryDb_Week3;
GO

USE LibraryDb_Week3;
GO

CREATE TABLE Authors
(
    AuthorId INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(100) NOT NULL
);
GO

CREATE TABLE Books
(
    BookId INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(150) NOT NULL,
    AuthorId INT NOT NULL,

    CONSTRAINT FK_Books_Authors
        FOREIGN KEY (AuthorId)
        REFERENCES Authors(AuthorId)
);
GO

CREATE TABLE Categories
(
    CategoryId INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName NVARCHAR(100) NOT NULL
);
GO

CREATE TABLE BookCategories
(
    BookId INT NOT NULL,
    CategoryId INT NOT NULL,

    CONSTRAINT PK_BookCategories
        PRIMARY KEY (BookId, CategoryId),

    CONSTRAINT FK_BookCategories_Books
        FOREIGN KEY (BookId)
        REFERENCES Books(BookId),

    CONSTRAINT FK_BookCategories_Categories
        FOREIGN KEY (CategoryId)
        REFERENCES Categories(CategoryId)
);
GO

INSERT INTO Authors (FullName)
VALUES
('ali'),
('mustafa'),
('hashim');
GO

INSERT INTO Books (Title, AuthorId)
VALUES
('C# Fundamentals', 1),
('Modern JavaScript', 2),
('ASP.NET Core Basics', 3),
('Angular Essentials', 2),
('SQL Server Guide', 1),
('Software Engineering Basics', 3);
GO

INSERT INTO Categories (CategoryName)
VALUES
('Programming'),
('Web Development'),
('Database'),
('Software Engineering');
GO

INSERT INTO BookCategories (BookId, CategoryId)
VALUES
(1, 1),
(2, 1),
(2, 2),
(3, 1),
(3, 2),
(4, 2),
(5, 3),
(6, 4);
GO

SELECT * FROM Authors;
GO

SELECT * FROM Books;
GO

SELECT * FROM Categories;
GO

SELECT * FROM BookCategories;
GO

SELECT
    Books.BookId,
    Books.Title,
    Authors.FullName AS AuthorName
FROM Books
INNER JOIN Authors
    ON Books.AuthorId = Authors.AuthorId;
GO

SELECT
    Books.Title,
    Categories.CategoryName
FROM BookCategories
INNER JOIN Books
    ON BookCategories.BookId = Books.BookId
INNER JOIN Categories
    ON BookCategories.CategoryId = Categories.CategoryId;
GO

DELETE FROM Authors
WHERE AuthorId = 1;
GO