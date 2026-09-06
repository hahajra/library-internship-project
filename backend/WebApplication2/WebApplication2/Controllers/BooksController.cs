using Microsoft.AspNetCore.Mvc;
using Week2LibraryApi.Models;
using Week2LibraryApi.Services;

namespace Week2LibraryApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class BooksController : ControllerBase
    {
        private readonly IBookService bookService;

        public BooksController(IBookService bookService)
        {
            this.bookService = bookService;
        }

        [HttpGet]
        public async Task<IActionResult> GetAllBooks()
        {
            List<Book> books = await bookService.GetAllBooksAsync();

            return Ok(books);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetBookById(int id)
        {
            Book? book = await bookService.GetBookByIdAsync(id);

            if (book == null)
            {
                return NotFound("Book not found.");
            }

            return Ok(book);
        }

        [HttpPost]
        public async Task<IActionResult> AddBook(Book book)
        {
            if (string.IsNullOrWhiteSpace(book.Title) ||
                string.IsNullOrWhiteSpace(book.Author) ||
                string.IsNullOrWhiteSpace(book.Category))
            {
                return BadRequest("Title, Author, and Category are required.");
            }

            Book createdBook = await bookService.AddBookAsync(book);

            return CreatedAtAction(
                nameof(GetBookById),
                new { id = createdBook.BookId },
                createdBook
            );
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateBook(int id, Book book)
        {
            if (string.IsNullOrWhiteSpace(book.Title) ||
                string.IsNullOrWhiteSpace(book.Author) ||
                string.IsNullOrWhiteSpace(book.Category))
            {
                return BadRequest("Title, Author, and Category are required.");
            }

            book.BookId = id;

            bool updated = await bookService.UpdateBookAsync(book);

            if (!updated)
            {
                return NotFound("Book not found.");
            }

            return Ok("Book updated successfully.");
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBook(int id)
        {
            bool deleted = await bookService.DeleteBookAsync(id);

            if (!deleted)
            {
                return NotFound("Book not found.");
            }

            return Ok("Book deleted successfully.");
        }
    }
}