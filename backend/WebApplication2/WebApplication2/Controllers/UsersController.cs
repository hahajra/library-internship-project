using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using WebApplication2.Data;
using Week2LibraryApi.Models;

namespace Week2LibraryApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class UsersController : ControllerBase
    {
        private readonly LibraryDbContext dbContext;
        private readonly IConfiguration configuration;

        public UsersController(
            LibraryDbContext dbContext,
            IConfiguration configuration)
        {
            this.dbContext = dbContext;
            this.configuration = configuration;
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register(
            RegisterRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.Username) ||
                string.IsNullOrWhiteSpace(request.Password))
            {
                return BadRequest(
                    "Username and password are required."
                );
            }

            bool exists = await dbContext.Users
                .AnyAsync(u =>
                    u.Username == request.Username);

            if (exists)
            {
                return BadRequest(
                    "Username already exists."
                );
            }

            User user = new User
            {
                Username = request.Username,
                Role = "User"
            };

            PasswordHasher<User> hasher =
                new PasswordHasher<User>();

            user.PasswordHash =
                hasher.HashPassword(
                    user,
                    request.Password
                );

            dbContext.Users.Add(user);
            await dbContext.SaveChangesAsync();

            return Ok(new
            {
                message = "User registered successfully."
            });
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login(
            LoginRequest request)
        {
            User? user = await dbContext.Users
                .FirstOrDefaultAsync(u =>
                    u.Username == request.Username);

            if (user == null)
            {
                return Unauthorized(
                    "Invalid username or password."
                );
            }

            PasswordHasher<User> hasher =
                new PasswordHasher<User>();

            PasswordVerificationResult result =
                hasher.VerifyHashedPassword(
                    user,
                    user.PasswordHash,
                    request.Password
                );

            if (result ==
                PasswordVerificationResult.Failed)
            {
                return Unauthorized(
                    "Invalid username or password."
                );
            }

            string token = GenerateJwtToken(user);

            return Ok(new
            {
                token,
                userId = user.UserId,
                username = user.Username,
                role = user.Role
            });
        }

        private string GenerateJwtToken(User user)
        {
            string key =
                configuration["Jwt:Key"]
                ?? throw new InvalidOperationException(
                    "JWT key is missing."
                );

            List<Claim> claims = new List<Claim>
            {
                new Claim(
                    ClaimTypes.NameIdentifier,
                    user.UserId.ToString()
                ),

                new Claim(
                    ClaimTypes.Name,
                    user.Username
                ),

                new Claim(
                    ClaimTypes.Role,
                    user.Role
                )
            };

            SymmetricSecurityKey securityKey =
                new SymmetricSecurityKey(
                    Encoding.UTF8.GetBytes(key)
                );

            SigningCredentials credentials =
                new SigningCredentials(
                    securityKey,
                    SecurityAlgorithms.HmacSha256
                );

            JwtSecurityToken token =
                new JwtSecurityToken(
                    issuer:
                        configuration["Jwt:Issuer"],

                    audience:
                        configuration["Jwt:Audience"],

                    claims: claims,

                    expires:
                        DateTime.UtcNow.AddMinutes(
                            double.Parse(
                                configuration[
                                    "Jwt:ExpiryMinutes"
                                ] ?? "60"
                            )
                        ),

                    signingCredentials:
                        credentials
                );

            return new JwtSecurityTokenHandler()
                .WriteToken(token);
        }
    }
}