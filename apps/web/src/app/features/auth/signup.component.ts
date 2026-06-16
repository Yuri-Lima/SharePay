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
      <h3 class="text-center mb-4">Sign Up</h3>
      <form [formGroup]="form" (ngSubmit)="onSubmit()">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input class="form-control" formControlName="username" />
          @if (form.get('username')?.errors?.['required'] && form.get('username')?.touched) {
            <div class="text-danger small">Username required</div>
          }
        </div>
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input type="email" class="form-control" formControlName="email" />
          @if (form.get('email')?.errors?.['required'] && form.get('email')?.touched) {
            <div class="text-danger small">Email required</div>
          }
          @if (form.get('email')?.errors?.['email']) {
            <div class="text-danger small">Valid email required</div>
          }
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" formControlName="password" />
          @if (form.get('password')?.errors?.['minlength']) {
            <div class="text-danger small">Min 4 characters</div>
          }
        </div>
        <button class="btn btn-primary w-100" [disabled]="form.invalid || loading()" type="submit">Sign Up</button>
        @if (error()) {
          <div class="text-danger mt-2 small">{{error()}}</div>
        }
      </form>
      <div class="text-center mt-3"><small>Already have an account? <a routerLink="/login">Log In</a></small></div>
    </div>
  </div>
  `
})
export class SignupComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);

  form = this.fb.group({
    username: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(4)]]
  });

  loading = signal(false);
  error = signal('');

  async onSubmit() {
    if (this.form.invalid) return;
    this.loading.set(true);
    this.error.set('');
    const ok = await this.auth.signup(this.form.value.username!, this.form.value.email!, this.form.value.password!);
    this.loading.set(false);
    if (ok) {
      this.router.navigate(['/houses']);
    } else {
      this.error.set('Signup failed (validation).');
    }
  }
}
