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

  it('starts unauthenticated, with no token and no username', () => {
    expect(service.isAuthenticated()).toBe(false);
    expect(service.getToken()).toBeNull();
    expect(service.currentUsername()).toBeNull();
  });

  it('becomes authenticated once a token is set, and exposes the username', () => {
    service.setToken('fake-jwt-token', 'alice');

    expect(service.isAuthenticated()).toBe(true);
    expect(service.getToken()).toBe('fake-jwt-token');
    expect(service.currentUsername()).toBe('alice');
  });

  it('returns to unauthenticated after clear()', () => {
    service.setToken('fake-jwt-token', 'alice');
    service.clear();

    expect(service.isAuthenticated()).toBe(false);
    expect(service.getToken()).toBeNull();
    expect(service.currentUsername()).toBeNull();
  });
});
