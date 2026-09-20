import { TestBed } from '@angular/core/testing';

import { Holdings } from './holdings';

describe('Holdings', () => {
  let service: Holdings;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Holdings);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
