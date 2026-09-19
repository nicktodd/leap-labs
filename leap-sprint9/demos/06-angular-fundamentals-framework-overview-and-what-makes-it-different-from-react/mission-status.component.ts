import { Component, signal, computed, input } from '@angular/core';

@Component({
  selector: 'app-mission-status',
  standalone: true,
  template: `
    <div class="status-card">
      <h2>{{ missionName() }}</h2>
      <p>Holdings: {{ holdingCount() }}</p>
      @if (holdingCount() > 0) {
        <button (click)="refresh()">Refresh</button>
      } @else {
        <p>No holdings yet.</p>
      }
    </div>
  `,
})
export class MissionStatusComponent {
  missionName = input.required<string>();
  private holdings = signal<number>(0);
  holdingCount = computed(() => this.holdings());

  refresh(): void {
    this.holdings.set(this.holdings() + 1);
  }
}
