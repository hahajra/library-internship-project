import { Routes } from '@angular/router';
import { Login } from './login/login';
import { LibraryPage } from './library-page/library-page';
import { authGuard } from './auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    component: Login
  },

  {
    path: '',
    component: LibraryPage,
    canActivate: [
      authGuard
    ]
  },

  {
    path: '**',
    redirectTo: ''
  }
];