import { Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth.service';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  template: `
  <div class="container py-5" style="max-width:420px">
    <div class="card p-4 shadow-sm">
      <h3 class="text-center mb-4">Login</h3>
      <form [formGroup]="form" (ngSubmit)="onSubmit()">
        <div class="mb-3">
          <label class="form-label">Username or Email</label>
          <input class="form-control" formControlName="login" placeholder="yourname or email" />
          @if (form.get('login')?.invalid && form.get('login')?.touched) {
            <div class="text-danger small">Required</div>
          }
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" formControlName="password" />
          @if (form.get('password')?.invalid && form.get('password')?.touched) {
            <div class="text-danger small">Required</div>
          }
        </div>
        <button class="btn btn-primary w-100" type="submit" [disabled]="form.invalid || loading()">Login</button>
        @if (error()) {
          <div class="text-danger mt-2 small">{{error()}}</div>
        }
      </form>
      <div class="text-center mt-3"><small>Don't have an account? <a routerLink="/signup">Sign Up</a></small></div>
    </div>
  </div>
  `
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);

  form = this.fb.group({
    login: ['', Validators.required],
    password: ['', Validators.required]
  });

  loading = signal(false);
  error = signal('');

  async onSubmit() {
    if (this.form.invalid) return;
    this.loading.set(true);
    this.error.set('');
    const ok = await this.auth.login(this.form.value.login!, this.form.value.password!);
    this.loading.set(false);
    if (ok) {
      this.router.navigate(['/houses']);
    } else {
      this.error.set('Login failed. Check credentials.');
    }
  }
}
