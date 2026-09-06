using Microsoft.EntityFrameworkCore;
using WebApplication2.Data;
using Week2LibraryApi.Models;

namespace Week2LibraryApi.Repositories
{
    public class BookRepository : IBookRepository
    {
        private readonly LibraryDbContext dbContext;

        public BookRepository(LibraryDbContext dbContext)
        {
            this.dbContext = dbContext;
        }

        public async Task<List<Book>> GetAllAsync()
        {
            List<Book> books = await dbContext.Books
                .Include(book => book.AuthorEntity)
                .Include(book => book.Categories)
                .ToListAsync();

            foreach (Book book in books)
            {
                book.Author = book.AuthorEntity?.FullName ?? string.Empty;
                book.Category = string.Join(
                    ", ",
                    book.Categories.Select(category => category.CategoryName)
                );
            }

            return books;
        }

        public async Task<Book?> GetByIdAsync(int id)
        {
            Book? book = await dbContext.Books
                .Include(book => book.AuthorEntity)
                .Include(book => book.Categories)
                .FirstOrDefaultAsync(book => book.BookId == id);

            if (book != null)
            {
                book.Author = book.AuthorEntity?.FullName ?? string.Empty;
                book.Category = string.Join(
                    ", ",
                    book.Categories.Select(category => category.CategoryName)
                );
            }

            return book;
        }

        public async Task<Book> AddAsync(Book book)
        {
            Author? author = await dbContext.Authors
                .FirstOrDefaultAsync(author =>
                    author.FullName.ToLower() == book.Author.ToLower());

            if (author == null)
            {
                author = new Author
                {
                    FullName = book.Author
                };

                dbContext.Authors.Add(author);
            }

            Category? category = await dbContext.Categories
                .FirstOrDefaultAsync(category =>
                    category.CategoryName.ToLower() == book.Category.ToLower());

            if (category == null)
            {
                category = new Category
                {
                    CategoryName = book.Category
                };

                dbContext.Categories.Add(category);
            }

            book.AuthorEntity = author;
            book.Categories.Add(category);

            dbContext.Books.Add(book);

            await dbContext.SaveChangesAsync();

            book.AuthorId = author.AuthorId;

            return book;
        }

        public async Task<bool> UpdateAsync(Book book)
        {
            Book? existingBook = await dbContext.Books
                .Include(existing => existing.AuthorEntity)
                .Include(existing => existing.Categories)
                .FirstOrDefaultAsync(existing => existing.BookId == book.BookId);

            if (existingBook == null)
            {
                return false;
            }

            Author? author = await dbContext.Authors
                .FirstOrDefaultAsync(author =>
                    author.FullName.ToLower() == book.Author.ToLower());

            if (author == null)
            {
                author = new Author
                {
                    FullName = book.Author
                };

                dbContext.Authors.Add(author);
            }

            Category? category = await dbContext.Categories
                .FirstOrDefaultAsync(category =>
                    category.CategoryName.ToLower() == book.Category.ToLower());

            if (category == null)
            {
                category = new Category
                {
                    CategoryName = book.Category
                };

                dbContext.Categories.Add(category);
            }

            existingBook.Title = book.Title;
            existingBook.AuthorEntity = author;

            existingBook.Categories.Clear();
            existingBook.Categories.Add(category);

            await dbContext.SaveChangesAsync();

            return true;
        }

        public async Task<bool> DeleteAsync(int id)
        {
            Book? book = await dbContext.Books.FindAsync(id);

            if (book == null)
            {
                return false;
            }

            dbContext.Books.Remove(book);

            await dbContext.SaveChangesAsync();

            return true;
        }
    }
}