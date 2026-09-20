import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HoldingsSummary } from './holdings-summary/holdings-summary';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HoldingsSummary],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('mission-ui');
}
