import { Component, inject } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { Holdings } from '../holdings';

@Component({
  selector: 'app-portfolio-badge',
  imports: [DecimalPipe],
  templateUrl: './portfolio-badge.html',
  styleUrl: './portfolio-badge.css',
})
export class PortfolioBadge {
  private readonly holdingsService = inject(Holdings);

  protected readonly totalValue = this.holdingsService.totalValue;
}
