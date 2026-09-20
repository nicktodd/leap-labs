import { TestBed } from '@angular/core/testing';
import { TokenStore } from './token-store';

describe('TokenStore', () => {
  let store: TokenStore;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    store = TestBed.inject(TokenStore);
  });

  it('should be created', () => {
    expect(store).toBeTruthy();
  });

  it('starts unauthenticated with no token', () => {
    expect(store.isAuthenticated()).toBeFalsy();
    expect(store.getToken()).toBeNull();
  });

  it('becomes authenticated after setToken', () => {
    store.setToken('my-jwt', 'alice');
    expect(store.isAuthenticated()).toBeTruthy();
    expect(store.getToken()).toBe('my-jwt');
  });

  it('clears token and becomes unauthenticated after clear()', () => {
    store.setToken('my-jwt', 'alice');
    store.clear();
    expect(store.isAuthenticated()).toBeFalsy();
    expect(store.getToken()).toBeNull();
  });
});
