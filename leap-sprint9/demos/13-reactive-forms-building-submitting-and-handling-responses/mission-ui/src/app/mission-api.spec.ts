import { TestBed } from '@angular/core/testing';

import { MissionApi } from './mission-api';

describe('MissionApi', () => {
  let service: MissionApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MissionApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
