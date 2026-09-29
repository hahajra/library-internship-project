using Week2LibraryApi.Models;

namespace Week2LibraryApi.Services
{
    public interface IAiServiceClient
    {
        Task<AiAskResponse?> AskAsync(
            string question,
            CancellationToken cancellationToken = default
        );
    }
}