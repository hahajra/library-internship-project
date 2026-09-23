import {
  ChangeDetectorRef,
  Component,
  OnInit
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { finalize } from 'rxjs';

import { Book } from '../book';
import { BookService } from '../book.service';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-library-page',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './library-page.html',
  styleUrl: './library-page.css'
})
export class LibraryPage implements OnInit {
  books: Book[] = [];

  newBook: Book = {
    title: '',
    author: '',
    category: ''
  };

  loading = false;
  errorMessage = '';

  editingBookId: number | null = null;

  constructor(
    private bookService: BookService,
    public authService: AuthService,
    private changeDetector: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadBooks();
  }

  loadBooks(): void {
    this.loading = true;
    this.errorMessage = '';

    this.bookService
      .getBooks()
      .pipe(
        finalize(() => {
          this.loading = false;
          this.changeDetector.detectChanges();
        })
      )
      .subscribe({
        next: (books) => {
          this.books = books;

          this.changeDetector.detectChanges();
        },

        error: (error) => {
          console.error(
            'Unable to load books:',
            error
          );

          this.errorMessage =
            'Unable to load books.';

          this.changeDetector.detectChanges();
        }
      });
  }

  saveBook(): void {
    if (
      !this.newBook.title.trim() ||
      !this.newBook.author.trim() ||
      !this.newBook.category.trim()
    ) {
      this.errorMessage =
        'Please fill in all fields.';

      return;
    }

    this.errorMessage = '';

    if (this.editingBookId !== null) {
      this.bookService
        .updateBook(
          this.editingBookId,
          this.newBook
        )
        .subscribe({
          next: () => {
            this.resetForm();
            this.loadBooks();
          },

          error: (error) => {
            console.error(
              'Unable to update book:',
              error
            );

            this.errorMessage =
              'Unable to update book.';

            this.changeDetector.detectChanges();
          }
        });

      return;
    }

    this.bookService
      .addBook(this.newBook)
      .subscribe({
        next: () => {
          this.resetForm();
          this.loadBooks();
        },

        error: (error) => {
          console.error(
            'Unable to add book:',
            error
          );

          this.errorMessage =
            'Unable to add book.';

          this.changeDetector.detectChanges();
        }
      });
  }

  editBook(book: Book): void {
    const id =
      book.bookId ?? book.id;

    if (id === undefined) {
      return;
    }

    this.editingBookId = id;

    this.newBook = {
      title: book.title,
      author: book.author,
      category: book.category
    };

    this.changeDetector.detectChanges();

    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  }

  cancelEdit(): void {
    this.resetForm();
  }

  deleteBook(book: Book): void {
    const id =
      book.bookId ?? book.id;

    if (id === undefined) {
      return;
    }

    this.bookService
      .deleteBook(id)
      .subscribe({
        next: () => {
          if (
            this.editingBookId === id
          ) {
            this.resetForm();
          }

          this.loadBooks();
        },

        error: (error) => {
          console.error(
            'Unable to delete book:',
            error
          );

          if (error.status === 403) {
            this.errorMessage =
              'Only Admin users can delete books.';
          } else {
            this.errorMessage =
              'Unable to delete book.';
          }

          this.changeDetector.detectChanges();
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

    this.changeDetector.detectChanges();
  }
}