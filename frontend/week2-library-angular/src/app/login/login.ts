import { Component } from '@angular/core';

import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

import { Router } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    ReactiveFormsModule
  ],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {
  loginForm: FormGroup;

  errorMessage = '';
  loading = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm =
      this.formBuilder.group({
        username: [
          '',
          Validators.required
        ],

        password: [
          '',
          Validators.required
        ]
      });
  }

  login(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    this.authService
      .login(
        this.loginForm.value.username,
        this.loginForm.value.password
      )
      .subscribe({
        next: () => {
          this.loading = false;

          this.router.navigate(['/']);
        },

        error: () => {
          this.loading = false;

          this.errorMessage =
            'Invalid username or password.';
        }
      });
  }
}