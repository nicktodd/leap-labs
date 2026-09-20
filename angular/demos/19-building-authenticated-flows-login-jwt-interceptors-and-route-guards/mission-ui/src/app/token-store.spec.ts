import { TestBed } from '@angular/core/testing';

import { TokenStore } from './token-store';

describe('TokenStore', () => {
  let service: TokenStore;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TokenStore);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
