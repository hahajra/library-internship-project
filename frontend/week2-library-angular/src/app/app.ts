import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Book } from './book';
import { BookService } from './book.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  books: Book[] = [];

  newBook: Book = {
    title: '',
    author: '',
    category: ''
  };

  loading = false;
  errorMessage = '';
  editingBookId: number | null = null;

  constructor(private bookService: BookService) {}

  ngOnInit(): void {
    this.loadBooks();
  }

  loadBooks(): void {
    this.loading = true;
    this.errorMessage = '';

    this.bookService.getBooks().subscribe({
      next: (books) => {
        this.books = books;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Unable to load books.';
        this.loading = false;
      }
    });
  }

  saveBook(): void {
    if (
      !this.newBook.title.trim() ||
      !this.newBook.author.trim() ||
      !this.newBook.category.trim()
    ) {
      this.errorMessage = 'Please fill in all fields.';
      return;
    }

    this.errorMessage = '';

    if (this.editingBookId !== null) {
      this.bookService
        .updateBook(this.editingBookId, this.newBook)
        .subscribe({
          next: () => {
            this.resetForm();
            this.loadBooks();
          },
          error: () => {
            this.errorMessage = 'Unable to update book.';
          }
        });

      return;
    }

    this.bookService.addBook(this.newBook).subscribe({
      next: () => {
        this.resetForm();
        this.loadBooks();
      },
      error: () => {
        this.errorMessage = 'Unable to add book.';
      }
    });
  }

  editBook(book: Book): void {
    const id = book.bookId ?? book.id;

    if (id === undefined) {
      return;
    }

    this.editingBookId = id;

    this.newBook = {
      title: book.title,
      author: book.author,
      category: book.category
    };

    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  }

  cancelEdit(): void {
    this.resetForm();
  }

  deleteBook(book: Book): void {
    const id = book.bookId ?? book.id;

    if (id === undefined) {
      return;
    }

    this.bookService.deleteBook(id).subscribe({
      next: () => {
        if (this.editingBookId === id) {
          this.resetForm();
        }

        this.loadBooks();
      },
      error: () => {
        this.errorMessage = 'Unable to delete book.';
      }
    });
  }

  resetForm(): void {
    this.newBook = {
      title: '',
      author: '',
      category: ''
    };

    this.editingBookId = null;
  }
}