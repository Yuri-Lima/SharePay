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
      <h3 class="text-center mb-4">Sign Up</h3>
      <form [formGroup]="form" (ngSubmit)="onSubmit()">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input class="form-control" formControlName="username" />
          <div class="text-danger small" *ngIf="form.get('username')?.errors?.['required'] && form.get('username')?.touched">Username required</div>
        </div>
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input type="email" class="form-control" formControlName="email" />
          <div class="text-danger small" *ngIf="form.get('email')?.errors?.['required'] && form.get('email')?.touched">Email required</div>
          <div class="text-danger small" *ngIf="form.get('email')?.errors?.['email']">Valid email required</div>
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" formControlName="password" />
          <div class="text-danger small" *ngIf="form.get('password')?.errors?.['minlength']">Min 4 characters</div>
        </div>
        <button class="btn btn-primary w-100" [disabled]="form.invalid || loading" type="submit">Sign Up</button>
        <div class="text-danger mt-2 small" *ngIf="error">{{error}}</div>
      </form>
      <div class="text-center mt-3"><small>Already have an account? <a routerLink="/login">Log In</a></small></div>
    </div>
  </div>
  `
})
export class SignupComponent {
  form!: ReturnType<FormBuilder['group']>;
  loading = false; error = '';
  constructor(private fb: FormBuilder, private auth: AuthService, private router: Router) {
    this.form = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(4)]]
    });
  }
  async onSubmit() {
    if (this.form.invalid) return;
    this.loading = true; this.error = '';
    const ok = await this.auth.signup(this.form.value.username!, this.form.value.email!, this.form.value.password!);
    this.loading = false;
    if (ok) this.router.navigate(['/houses']); else this.error = 'Signup failed (validation).';
  }
}
