using Week2LibraryApi.Models;

namespace Week2LibraryApi.Services
{
    public interface IBookService
    {
        List<Book> GetAllBooks();
        Book? GetBookById(int id);
        Book AddBook(Book book);
        bool UpdateBook(Book book);
        bool DeleteBook(int id);
    }
}