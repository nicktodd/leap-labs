import { Component, inject } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { Holdings } from '../holdings';

@Component({
  selector: 'app-holdings-summary',
  imports: [DecimalPipe],
  templateUrl: './holdings-summary.html',
  styleUrl: './holdings-summary.css',
})
export class HoldingsSummary {
  protected readonly svc = inject(Holdings);
}
