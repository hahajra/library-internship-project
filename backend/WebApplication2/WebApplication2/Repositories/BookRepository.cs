using Week2LibraryApi.Models;

namespace Week2LibraryApi.Repositories
{
    public class BookRepository : IBookRepository
    {
        private readonly List<Book> books = new List<Book>
        {
            new Book
            {
                Id = 1,
                Title = "C# Basics",
                Author = "John Smith",
                Category = "Programming"
            },
            new Book
            {
                Id = 2,
                Title = "Learning Angular",
                Author = "Sarah Khan",
                Category = "Web Development"
            },
            new Book
            {
                Id = 3,
                Title = "Database Fundamentals",
                Author = "Ahmed Ali",
                Category = "Database"
            }
        };

        public List<Book> GetAll()
        {
            return books;
        }

        public Book? GetById(int id)
        {
            return books.FirstOrDefault(book => book.Id == id);
        }

        public Book Add(Book book)
        {
            int newId = books.Count == 0
                ? 1
                : books.Max(book => book.Id) + 1;

            book.Id = newId;

            books.Add(book);

            return book;
        }

        public bool Update(Book book)
        {
            Book? existingBook = GetById(book.Id);

            if (existingBook == null)
            {
                return false;
            }

            existingBook.Title = book.Title;
            existingBook.Author = book.Author;
            existingBook.Category = book.Category;

            return true;
        }

        public bool Delete(int id)
        {
            Book? book = GetById(id);

            if (book == null)
            {
                return false;
            }

            books.Remove(book);

            return true;
        }
    }
}