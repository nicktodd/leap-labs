import { Component, inject } from '@angular/core';
import { MissionApi } from '../mission-api';

@Component({
  selector: 'app-place-order',
  imports: [],
  templateUrl: './place-order.html',
  styleUrl: './place-order.css',
})
export class PlaceOrder {
  private readonly missionApi = inject(MissionApi);

  protected readonly lastOrder = this.missionApi.lastOrder;
  protected readonly error = this.missionApi.error;

  protected submitTestOrder(): void {
    this.missionApi.submitOrder({
      ticker: 'ULVR.L',
      instrumentType: 'EQUITY',
      quantity: 1,
      price: 40.0,
      side: 'BUY',
    });
  }
}
