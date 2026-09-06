export interface Book {
  bookId?: number;
  id?: number;
  title: string;
  authorId?: number;
  author: string;
  category: string;
  categories?: unknown[];
}