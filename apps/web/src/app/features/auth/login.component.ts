import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth.service';

@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
  <div class="container py-5" style="max-width:420px">
    <div class="card p-4 shadow-sm">
      <h3 class="text-center mb-4">Login</h3>
      <form [formGroup]="form" (ngSubmit)="onSubmit()">
        <div class="mb-3">
          <label class="form-label">Username or Email</label>
          <input class="form-control" formControlName="login" placeholder="yourname or email" />
          <div class="text-danger small" *ngIf="form.get('login')?.invalid && form.get('login')?.touched">Required</div>
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" formControlName="password" />
          <div class="text-danger small" *ngIf="form.get('password')?.invalid && form.get('password')?.touched">Required</div>
        </div>
        <button class="btn btn-primary w-100" type="submit" [disabled]="form.invalid || loading">Login</button>
        <div class="text-danger mt-2 small" *ngIf="error">{{error}}</div>
      </form>
      <div class="text-center mt-3"><small>Don't have an account? <a routerLink="/signup">Sign Up</a></small></div>
    </div>
  </div>
  `
})
export class LoginComponent {
  form!: ReturnType<FormBuilder['group']>;
  loading = false; error = '';
  constructor(private fb: FormBuilder, private auth: AuthService, private router: Router) {
    this.form = this.fb.group({ login: ['', Validators.required], password: ['', Validators.required] });
  }
  async onSubmit() {
    if (this.form.invalid) return;
    this.loading = true; this.error = '';
    const ok = await this.auth.login(this.form.value.login!, this.form.value.password!);
    this.loading = false;
    if (ok) this.router.navigate(['/houses']); else this.error = 'Login failed. Check credentials.';
  }
}
