import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { TokenStore } from './token-store';

const MISSION_SERVICE_BASE = 'http://localhost:8090';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const tokenStore = inject(TokenStore);
  const token = tokenStore.getToken();

  // Only attach the header for requests to the mission service -
  // never to the auth service's own /auth/login, which is how the
  // token is obtained in the first place.
  if (token && req.url.startsWith(MISSION_SERVICE_BASE)) {
    const authedReq = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    });
    return next(authedReq);
  }

  return next(req);
};
