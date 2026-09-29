using System.Net.Http.Json;
using Week2LibraryApi.Models;

namespace Week2LibraryApi.Services
{
    public class AiServiceClient : IAiServiceClient
    {
        private readonly HttpClient httpClient;

        public AiServiceClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        public async Task<AiAskResponse?> AskAsync(
            string question,
            CancellationToken cancellationToken = default
        )
        {
            AskDto request = new AskDto
            {
                Question = question
            };

            using HttpResponseMessage response =
                await httpClient.PostAsJsonAsync(
                    "ask",
                    request,
                    cancellationToken
                );

            response.EnsureSuccessStatusCode();

            AiAskResponse? result =
                await response.Content
                    .ReadFromJsonAsync<AiAskResponse>(
                        cancellationToken:
                            cancellationToken
                    );

            return result;
        }
    }
}