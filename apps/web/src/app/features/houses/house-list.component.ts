import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { HousesService, House } from '../../core/houses.service';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
  <div class="masthead">
    <div class="masthead-bg"></div>
    <div class="container h-100">
      <div class="row h-100">
        <div class="col-12 my-auto">
          <div class="masthead-content text-white py-4">
            <h2 class="h3">Houses</h2>
            <div *ngIf="houses.length; else none">
              <div class="btn-toolbar mb-2" *ngFor="let h of houses">
                <div class="btn-group me-2"><a class="btn btn-outline-primary text-white">{{h.house_name}}</a></div>
                <div class="btn-group me-2"><a class="btn btn-outline-success text-white" [routerLink]="['/houses', h.id]">Edit / Detail</a></div>
                <div class="btn-group"><button class="btn btn-outline-warning text-white" (click)="del(h.id)">Delete</button></div>
              </div>
            </div>
            <ng-template #none><p class="text-white-50">No houses yet.</p></ng-template>

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
  houses: House[] = [];
  constructor(private svc: HousesService) {
    this.svc.houses$.subscribe(hs => this.houses = hs);
    // Start of real API wiring: if token, load from Nest (persists to local cache for getById during transition)
    if ((this.svc as any).listReal) {
      (this.svc as any).listReal().then((hs: House[]) => { this.houses = hs; });
    }
  }
  del(id: number) { if (confirm('Delete house?')) this.svc.deleteHouse(id); }
}
