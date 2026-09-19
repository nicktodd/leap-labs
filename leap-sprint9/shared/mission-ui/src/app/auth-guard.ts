import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { TokenStore } from './token-store';

export const authGuard: CanActivateFn = () => {
  const tokenStore = inject(TokenStore);
  if (tokenStore.isAuthenticated()) return true;
  inject(Router).navigate(['/login']);
  return false;
};
