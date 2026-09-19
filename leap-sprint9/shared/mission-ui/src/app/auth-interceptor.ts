import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { TokenStore } from './token-store';

const MISSION_SERVICE_BASE = 'http://localhost:8090';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(TokenStore).getToken();
  if (token && req.url.startsWith(MISSION_SERVICE_BASE)) {
    req = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
  }
  return next(req);
};
