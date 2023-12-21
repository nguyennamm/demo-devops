using DevOpsTrainingDotnet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System;

namespace DevOpsTrainingDotnet.Controllers
{
   
        public class UserController : Controller
        {
            private readonly AppDbContext _context;

            public UserController(AppDbContext context)
            {
                _context = context;
            }

            [HttpGet("api/v1/ping")]
            public IActionResult Ping()
            {
                return Ok("Pong");
            }

            [HttpGet("api/v1/user/{id}")]
            public async Task<IActionResult> GetUser(int id)
            {
                var user = await _context.users.FindAsync(id);

                if (user == null)
                {
                    return NotFound($"User with ID {id} not found.");
                }

                return Ok(user);
            }

            [HttpGet("api/v1/users")]
            public async Task<IActionResult> GetAllUsers()
            {
                var users = await _context.users.ToListAsync();
                return Ok(users);
            }

            [HttpPost("api/v1/user")]
            public async Task<IActionResult> EditUser([FromBody] User editedUser)
            {
                var userToUpdate = await _context.users.FindAsync(editedUser.Id);
                if (userToUpdate != null)
                {
                    userToUpdate.Username = editedUser.Username;
                    userToUpdate.Email = editedUser.Email;
                    userToUpdate.Password = editedUser.Password;

                    await _context.SaveChangesAsync();
                    return Ok(userToUpdate);
                }

                return NotFound("No user found to edit.");
            }

            [HttpPost("api/v1/auth/login")]
            public IActionResult Login([FromBody] LoginRequest loginRequest)
            {
                // Logic to handle user authentication
                // For simplicity, let's just check if the username and password are not empty
                if (!string.IsNullOrWhiteSpace(loginRequest.Username) && !string.IsNullOrWhiteSpace(loginRequest.Password))
                {
                    return Ok("Login successful");
                }

                return BadRequest("Invalid username or password");
            }
        }
    
}
