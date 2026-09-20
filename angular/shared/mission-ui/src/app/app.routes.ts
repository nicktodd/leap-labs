import { Routes } from '@angular/router';
import { authGuard } from './auth-guard';

export const routes: Routes = [
  { path: '', redirectTo: 'holdings', pathMatch: 'full' },
  { path: 'login', loadComponent: () => import('./login-page/login-page').then((m) => m.LoginPageComponent) },
  { path: 'holdings', canActivate: [authGuard], loadComponent: () => import('./holdings-summary/holdings-summary').then((m) => m.HoldingsSummary) },
  { path: 'orders', canActivate: [authGuard], loadComponent: () => import('./place-order/place-order').then((m) => m.PlaceOrderComponent) },
];
