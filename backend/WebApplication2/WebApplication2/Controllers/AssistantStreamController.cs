using System.Net.Http.Json;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Week2LibraryApi.Controllers
{
    [ApiController]
    [Route("api/assistant")]
    [Authorize]
    public class AssistantStreamController : ControllerBase
    {
        private readonly IHttpClientFactory httpClientFactory;

        public AssistantStreamController(
            IHttpClientFactory httpClientFactory)
        {
            this.httpClientFactory =
                httpClientFactory;
        }

        [HttpPost("ask/stream")]
        public async Task AskStream(
            StreamAskRequest request,
            CancellationToken cancellationToken)
        {
            HttpClient client =
                httpClientFactory.CreateClient(
                    "AiStreamingClient"
                );

            using HttpRequestMessage aiRequest =
                new HttpRequestMessage(
                    HttpMethod.Post,
                    "ask/stream"
                );

            aiRequest.Content =
                JsonContent.Create(
                    new
                    {
                        question =
                            request.Question,

                        delay_ms =
                            request.DelayMs
                    }
                );

            Response.StatusCode =
                StatusCodes.Status200OK;

            Response.ContentType =
                "text/event-stream";

            Response.Headers[
                "Cache-Control"
            ] = "no-cache";

            Response.Headers[
                "X-Accel-Buffering"
            ] = "no";

            try
            {
                using HttpResponseMessage aiResponse =
                    await client.SendAsync(
                        aiRequest,
                        HttpCompletionOption
                            .ResponseHeadersRead,
                        cancellationToken
                    );

                if (!aiResponse.IsSuccessStatusCode)
                {
                    Response.StatusCode =
                        (int)aiResponse.StatusCode;

                    await Response.WriteAsync(
                        "data: " +
                        "{\"type\":\"error\"," +
                        "\"message\":\"AI service request failed.\"}" +
                        "\n\n",
                        cancellationToken
                    );

                    await Response.Body.FlushAsync(
                        cancellationToken
                    );

                    return;
                }

                await using Stream stream =
                    await aiResponse.Content
                        .ReadAsStreamAsync(
                            cancellationToken
                        );

                using StreamReader reader =
                    new StreamReader(
                        stream
                    );

                while (!cancellationToken
                    .IsCancellationRequested)
                {
                    string? line =
                        await reader.ReadLineAsync(
                            cancellationToken
                        );

                    if (line == null)
                    {
                        break;
                    }

                    await Response.WriteAsync(
                        line + "\n",
                        cancellationToken
                    );

                    if (
    string.IsNullOrEmpty(
        line
    )
)
{
     await Response.Body
        .FlushAsync(
            cancellationToken
        );
}                }
            }
            catch (
                OperationCanceledException
            )
            {
                Console.WriteLine(
                    "Streaming request was cancelled."
                );
            }
            catch (
                HttpRequestException error
            )
            {
                Console.WriteLine(
                    "Streaming AI request failed: "
                    + error.Message
                );

                if (!Response.HasStarted)
                {
                    Response.StatusCode =
                        StatusCodes
                            .Status503ServiceUnavailable;
                }
            }
        }
    }


    public class StreamAskRequest
    {
        public string Question
        {
            get;
            set;
        } = string.Empty;

        public int DelayMs
        {
            get;
            set;
        } = 0;
    }
}