using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Polly.CircuitBreaker;
using Week2LibraryApi.Models;
using Week2LibraryApi.Services;

namespace Week2LibraryApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class AssistantController : ControllerBase
    {
        private readonly IAiServiceClient aiServiceClient;

        public AssistantController(
            IAiServiceClient aiServiceClient)
        {
            this.aiServiceClient = aiServiceClient;
        }

        [HttpPost("ask")]
        public async Task<IActionResult> Ask(
            AskDto request,
            CancellationToken cancellationToken)
        {
            if (string.IsNullOrWhiteSpace(
                request.Question))
            {
                return BadRequest(new
                {
                    message =
                        "Question is required."
                });
            }

            try
            {
                AiAskResponse? result =
                    await aiServiceClient.AskAsync(
                        request.Question,
                        cancellationToken
                    );

                if (result == null)
                {
                    return StatusCode(
                        StatusCodes
                            .Status502BadGateway,
                        new
                        {
                            message =
                                "The AI service returned an empty response."
                        }
                    );
                }

                return Ok(result);
            }
            catch (BrokenCircuitException)
            {
                Console.WriteLine(
                    "AI service circuit breaker is open."
                );

                return StatusCode(
                    StatusCodes
                        .Status503ServiceUnavailable,
                    new
                    {
                        message =
                            "The AI assistant is temporarily unavailable. Please try again shortly."
                    }
                );
            }
            catch (TaskCanceledException)
            {
                Console.WriteLine(
                    "AI service request timed out."
                );

                return StatusCode(
                    StatusCodes
                        .Status503ServiceUnavailable,
                    new
                    {
                        message =
                            "The AI assistant request timed out. Please try again shortly."
                    }
                );
            }
            catch (HttpRequestException error)
            {
                Console.WriteLine(
                    $"AI service request failed: {error.Message}"
                );

                return StatusCode(
                    StatusCodes
                        .Status503ServiceUnavailable,
                    new
                    {
                        message =
                            "The AI assistant is temporarily unavailable. Please try again shortly."
                    }
                );
            }
        }
    }
}