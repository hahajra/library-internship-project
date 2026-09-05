using Week2LibraryApi.Models;
using Week2LibraryApi.Repositories;

namespace Week2LibraryApi.Services
{
    public class BookService : IBookService
    {
        private readonly IBookRepository bookRepository;

        public BookService(IBookRepository bookRepository)
        {
            this.bookRepository = bookRepository;
        }

        public List<Book> GetAllBooks()
        {
            return bookRepository.GetAll();
        }

        public Book? GetBookById(int id)
        {
            return bookRepository.GetById(id);
        }

        public Book AddBook(Book book)
        {
            return bookRepository.Add(book);
        }

        public bool UpdateBook(Book book)
        {
            return bookRepository.Update(book);
        }

        public bool DeleteBook(int id)
        {
            return bookRepository.Delete(id);
        }
    }
}