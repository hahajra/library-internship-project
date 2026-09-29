namespace Week2LibraryApi.Models
{
    public class AiAskResponse
    {
        public string Answer { get; set; } = string.Empty;

        public List<string> Sources { get; set; } = new List<string>();

        public string Model { get; set; } = string.Empty;
    }
}