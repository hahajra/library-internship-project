using Week2LibraryApi.Models;

namespace Week2LibraryApi.Repositories
{
    public interface IBookRepository
    {
        List<Book> GetAll();
        Book? GetById(int id);
        Book Add(Book book);
        bool Update(Book book);
        bool Delete(int id);
    }
}