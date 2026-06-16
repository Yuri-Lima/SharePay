import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';

export interface User { id: number; username: string; email: string; }

@Injectable({ providedIn: 'root' })
export class AuthService {
  private tokenKey = 'sharepay_jwt';
  private userKey = 'sharepay_user';
  currentUser = signal<User | null>(this.loadUser());
  private token = signal<string | null>(localStorage.getItem(this.tokenKey));

  constructor(private http: HttpClient, private router: Router) {}

  isLoggedIn(): boolean { return !!this.token(); }

  getToken(): string | null { return this.token(); }

  // Simulate API calls to /auth/* as required. In real would be this.http.post(`${environment.apiUrl}/auth/login`...
  // Store JWT. Simple client validation performed in components; here basic.
  async login(usernameOrEmail: string, password: string): Promise<boolean> {
    // Client side validation is done in form; here call simulated /auth/login
    if (!usernameOrEmail || !password) return false;

    // Fake API response - generate JWT-like token. For demo SPA full parity we persist user.
    const fakeJwt = btoa(JSON.stringify({ sub: usernameOrEmail, exp: Date.now() + 86400000 }));
    const user: User = { id: 1, username: usernameOrEmail.split('@')[0], email: usernameOrEmail.includes('@') ? usernameOrEmail : usernameOrEmail + '@example.com' };

    localStorage.setItem(this.tokenKey, fakeJwt);
    localStorage.setItem(this.userKey, JSON.stringify(user));
    this.token.set(fakeJwt);
    this.currentUser.set(user);
    return true;
  }

  async signup(username: string, email: string, password: string): Promise<boolean> {
    // Simulate /auth/signup . Client validation in component (required fields, basic email, pw len)
    if (!username || !email || !password || password.length < 4) return false;

    const fakeJwt = btoa(JSON.stringify({ sub: username, exp: Date.now() + 86400000 }));
    const user: User = { id: Date.now(), username, email };

    localStorage.setItem(this.tokenKey, fakeJwt);
    localStorage.setItem(this.userKey, JSON.stringify(user));
    this.token.set(fakeJwt);
    this.currentUser.set(user);
    return true;
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
    this.token.set(null);
    this.currentUser.set(null);
    this.router.navigate(['/']);
  }

  private loadUser(): User | null {
    try { return JSON.parse(localStorage.getItem(this.userKey) || 'null'); } catch { return null; }
  }
}
