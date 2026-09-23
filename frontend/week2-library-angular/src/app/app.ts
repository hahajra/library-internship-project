import { Component } from '@angular/core';

import {
  Router,
  RouterOutlet
} from '@angular/router';

import { AuthService } from './auth.service';

@Component({
  selector: 'app-root',
  standalone: true,

  imports: [
    RouterOutlet
  ],

  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  constructor(
    public authService: AuthService,
    private router: Router
  ) {}

  logout(): void {
    this.authService.logout();

    this.router.navigate([
      '/login'
    ]);
  }
}