import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PortfolioBadge } from './portfolio-badge';

describe('PortfolioBadge', () => {
  let component: PortfolioBadge;
  let fixture: ComponentFixture<PortfolioBadge>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PortfolioBadge],
    }).compileComponents();

    fixture = TestBed.createComponent(PortfolioBadge);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
