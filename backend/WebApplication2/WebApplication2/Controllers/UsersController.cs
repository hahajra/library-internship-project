using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebApplication2.Data;
using Week2LibraryApi.Models;

namespace Week2LibraryApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class UsersController : ControllerBase
    {
        private readonly LibraryDbContext dbContext;

        public UsersController(LibraryDbContext dbContext)
        {
            this.dbContext = dbContext;
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register(User user)
        {
            if (string.IsNullOrWhiteSpace(user.Username) ||
                string.IsNullOrWhiteSpace(user.Password))
            {
                return BadRequest("Username and password are required.");
            }

            bool userExists = await dbContext.Users
                .AnyAsync(existingUser =>
                    existingUser.Username == user.Username);

            if (userExists)
            {
                return BadRequest("Username already exists.");
            }

            dbContext.Users.Add(user);
            await dbContext.SaveChangesAsync();

            return Ok("User registered successfully.");
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login(LoginRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.Username) ||
                string.IsNullOrWhiteSpace(request.Password))
            {
                return BadRequest("Username and password are required.");
            }

            User? user = await dbContext.Users
                .FirstOrDefaultAsync(existingUser =>
                    existingUser.Username == request.Username &&
                    existingUser.Password == request.Password);

            if (user == null)
            {
                return Unauthorized("Invalid username or password.");
            }

            return Ok("Login successful.");
        }
    }
}