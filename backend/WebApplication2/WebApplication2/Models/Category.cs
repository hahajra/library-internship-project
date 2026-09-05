using System.Text.Json.Serialization;

namespace Week2LibraryApi.Models
{
    public class Category
    {
        public int CategoryId { get; set; }

        public string CategoryName { get; set; } = string.Empty;

        [JsonIgnore]
        public List<Book> Books { get; set; } = new List<Book>();
    }
}
