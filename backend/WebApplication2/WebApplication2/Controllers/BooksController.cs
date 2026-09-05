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
        public IActionResult GetAllBooks()
        {
            return Ok(bookService.GetAllBooks());
        }

        [HttpGet("{id}")]
        public IActionResult GetBookById(int id)
        {
            Book? book = bookService.GetBookById(id);

            if (book == null)
            {
                return NotFound("Book not found.");
            }

            return Ok(book);
        }

        [HttpPost]
        public IActionResult AddBook(Book book)
        {
            if (string.IsNullOrWhiteSpace(book.Title) ||
                string.IsNullOrWhiteSpace(book.Author) ||
                string.IsNullOrWhiteSpace(book.Category))
            {
                return BadRequest("Title, Author, and Category are required.");
            }

            Book createdBook = bookService.AddBook(book);

            return CreatedAtAction(
                nameof(GetBookById),
                new { id = createdBook.Id },
                createdBook
            );
        }

        [HttpPut("{id}")]
        public IActionResult UpdateBook(int id, Book book)
        {
            if (string.IsNullOrWhiteSpace(book.Title) ||
                string.IsNullOrWhiteSpace(book.Author) ||
                string.IsNullOrWhiteSpace(book.Category))
            {
                return BadRequest("Title, Author, and Category are required.");
            }

            book.Id = id;

            bool updated = bookService.UpdateBook(book);

            if (!updated)
            {
                return NotFound("Book not found.");
            }

            return Ok("Book updated successfully.");
        }

        [HttpDelete("{id}")]
        public IActionResult DeleteBook(int id)
        {
            bool deleted = bookService.DeleteBook(id);

            if (!deleted)
            {
                return NotFound("Book not found.");
            }

            return Ok("Book deleted successfully.");
        }
    }
}