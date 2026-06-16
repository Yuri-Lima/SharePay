import { Component, inject, effect } from '@angular/core';
import { RouterLink } from '@angular/router';
import { HousesService, House } from '../../core/houses.service';

@Component({
  standalone: true,
  imports: [RouterLink],
  template: `
  <div class="masthead">
    <div class="masthead-bg"></div>
    <div class="container h-100">
      <div class="row h-100">
        <div class="col-12 my-auto">
          <div class="masthead-content text-white py-4">
            <h2 class="h3">Houses</h2>
            @if (houses().length) {
              @for (h of houses(); track h.id) {
                <div class="btn-toolbar mb-2">
                  <div class="btn-group me-2"><a class="btn btn-outline-primary text-white">{{h.house_name}}</a></div>
                  <div class="btn-group me-2"><a class="btn btn-outline-success text-white" [routerLink]="['/houses', h.id]">Edit / Detail</a></div>
                  <div class="btn-group"><button class="btn btn-outline-warning text-white" (click)="del(h.id)">Delete</button></div>
                </div>
              }
            } @else {
              <p class="text-white-50">No houses yet.</p>
            }

            <a routerLink="/houses/new" class="btn btn-secondary w-100 mb-2 mt-3">Add House</a>
            <a routerLink="/" class="btn btn-outline-light w-100">Back to Home</a>
          </div>
        </div>
      </div>
    </div>
  </div>
  `
})
export class HouseListComponent {
  private svc = inject(HousesService);

  // Direct signal consumption - modern and efficient
  houses = this.svc.houses;

  constructor() {
    // Trigger real API load if available (it updates the signal internally via persist)
    const listReal = (this.svc as any).listReal;
    if (typeof listReal === 'function') {
      listReal.call(this.svc).then(() => {
        // signal already updated inside listReal -> persist
      });
    }
  }

  del(id: number) {
    if (confirm('Delete house?')) {
      this.svc.deleteHouse(id);
    }
  }
}
