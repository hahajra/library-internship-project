import { Routes } from '@angular/router';
import { Login } from './login/login';
import { LibraryPage } from './library-page/library-page';
import { AssistantChat } from './assistant-chat/assistant-chat';
import { authGuard } from './auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    component: Login
  },

  {
    path: 'assistant',
    component: AssistantChat,
    canActivate: [
      authGuard
    ]
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