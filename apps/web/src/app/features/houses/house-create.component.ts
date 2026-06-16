import { Component, inject } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { HousesService } from '../../core/houses.service';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  template: `
  <div class="masthead"><div class="masthead-bg"></div>
  <div class="container"><div class="row"><div class="col-12 my-auto">
    <div class="masthead-content text-white py-5">
      <h3>New House Name</h3>
      <form [formGroup]="form" (ngSubmit)="submit()">
        <div class="mb-3">
          <label>House Name (max 25 chars)</label>
          <input class="form-control" formControlName="name" />
          @if (form.get('name')?.errors && form.get('name')?.touched) {
            <div class="text-warning small">Required, max 25 chars</div>
          }
        </div>
        <button class="btn btn-primary w-100 mb-2" [disabled]="form.invalid">Add House Name</button>
        <a routerLink="/houses" class="btn btn-outline-light w-100">Cancel</a>
      </form>
    </div>
  </div></div></div></div>
  `
})
export class HouseCreateComponent {
  private fb = inject(FormBuilder);
  private svc = inject(HousesService);
  private router = inject(Router);

  form = this.fb.group({
    name: ['', [Validators.required, Validators.maxLength(25)]]
  });

  submit() {
    if (this.form.invalid) return;
    const h = this.svc.createHouse(this.form.value.name!);
    this.router.navigate(['/houses', h.id]);
  }
}
