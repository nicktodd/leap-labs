import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'holdings', pathMatch: 'full' },
  {
    path: 'holdings',
    loadComponent: () =>
      import('./holdings-summary/holdings-summary').then((m) => m.HoldingsSummary),
  },
  {
    path: 'orders',
    loadComponent: () =>
      import('./place-order/place-order').then((m) => m.PlaceOrder),
  },
];
