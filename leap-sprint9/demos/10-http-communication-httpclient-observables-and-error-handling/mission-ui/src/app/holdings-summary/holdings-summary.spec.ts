import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HoldingsSummary } from './holdings-summary';

describe('HoldingsSummary', () => {
  let component: HoldingsSummary;
  let fixture: ComponentFixture<HoldingsSummary>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HoldingsSummary],
    }).compileComponents();

    fixture = TestBed.createComponent(HoldingsSummary);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
