import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { HousesService, House } from '../../core/houses.service';

@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
  <div class="masthead"><div class="masthead-bg"></div>
  <div class="container">
    <div class="masthead-content text-white py-4" *ngIf="house as h">
      <h3>Details from {{h.house_name}}</h3>

      <!-- Messages / feedback -->
      <div class="alert alert-info py-1 small" *ngFor="let m of messages">{{m}}</div>

      <!-- Edit House Name -->
      <a class="btn btn-outline-primary text-white w-100 mb-2" (click)="editingName=!editingName">Edit House Name</a>
      <div *ngIf="editingName" class="form-section mb-3">
        <form [formGroup]="nameForm" (ngSubmit)="saveName()">
          <input class="form-control mb-2" formControlName="name" />
          <button class="btn btn-sm btn-primary" type="submit">Save</button>
        </form>
      </div>

      <!-- BILL SECTION -->
      <div class="form-section">
        <div class="section-title">Bill</div>
        <div *ngIf="h.bill; else noBill"><strong>€{{h.bill.amount_bill}}</strong> | {{h.bill.start_date_bill}} → {{h.bill.end_date_bill}} ({{h.bill.days_bill}} days)</div>
        <ng-template #noBill><em>No bill yet</em></ng-template>
        <form [formGroup]="billForm" (ngSubmit)="saveBill()" class="row g-2 mt-2">
          <div class="col-md-3"><input type="text" class="form-control" placeholder="Amount e.g. 124.50" formControlName="amount" /></div>
          <div class="col-md-3"><input type="date" class="form-control" formControlName="start" /></div>
          <div class="col-md-3"><input type="date" class="form-control" formControlName="end" /></div>
          <div class="col-md-3"><button class="btn btn-primary w-100" type="submit">Save Bill</button></div>
        </form>
        <div class="text-danger small" *ngFor="let e of billErrors">{{e}}</div>
      </div>

      <!-- KWH SECTION (only after bill) -->
      <div class="form-section" *ngIf="h.bill">
        <div class="section-title">Kilowatts</div>
        <div *ngIf="h.kwh; else noKwh"><strong>{{h.kwh.kwh}} kwh</strong> <span class="small">(reads: {{h.kwh.last_read_kwh}} / {{h.kwh.read_kwh}})</span></div>
        <ng-template #noKwh><em>Add kilowatts (direct or last+present read)</em></ng-template>

        <form [formGroup]="kwhForm" (ngSubmit)="saveKwh()" class="row g-2 mt-2">
          <div class="col-md-2"><input type="number" class="form-control" placeholder="kWh direct" formControlName="kwh" /></div>
          <div class="col-md-2"><input type="number" class="form-control" placeholder="Last read" formControlName="last" /></div>
          <div class="col-md-2"><input type="number" class="form-control" placeholder="Present read" formControlName="read" /></div>
          <div class="col-md-3"><button class="btn btn-primary w-100" type="submit">Save KWH</button></div>
        </form>
        <div class="text-danger small" *ngFor="let e of kwhErrors">{{e}}</div>
      </div>

      <!-- TENANTS SECTION (after bill + kwh) -->
      <div class="form-section" *ngIf="h.bill && h.kwh">
        <div class="section-title">Tenants (Main House) — {{h.tenants.length}} total</div>
        <div *ngFor="let t of h.tenants" class="d-flex justify-content-between border-bottom py-1 small">
          <span>{{t.house_tenant}} — {{t.start_date}} to {{t.end_date}} ({{t.days}}d) <button class="btn btn-sm btn-link text-danger p-0 ms-2" (click)="removeTenant(t.id)">×</button></span>
        </div>
        <form [formGroup]="tenantForm" (ngSubmit)="addTenant()" class="row g-2 mt-2">
          <div class="col-md-4"><input class="form-control" placeholder="Tenant Name" formControlName="name" /></div>
          <div class="col-md-3"><input type="date" class="form-control" formControlName="start" /></div>
          <div class="col-md-3"><input type="date" class="form-control" formControlName="end" /></div>
          <div class="col-md-2"><button class="btn btn-success w-100" type="submit">Add Tenant</button></div>
        </form>
        <div class="text-danger small" *ngFor="let e of tenantErrors">{{e}}</div>
      </div>

      <!-- SUB HOUSES -->
      <div class="form-section" *ngIf="h.bill && h.kwh">
        <div class="section-title">Sub Houses</div>
        <div *ngIf="h.subHouses.length; else noSub">
          <div *ngFor="let sh of h.subHouses" class="mb-3 border p-2 rounded bg-dark bg-opacity-25">
            <div class="d-flex justify-content-between">
              <strong>{{sh.sub_house_name}}</strong>
              <button class="btn btn-sm btn-outline-danger" (click)="deleteSub(sh.id)">Delete Sub</button>
            </div>

            <!-- Sub KWH -->
            <div class="mt-1 small">KWH: {{sh.sub_kwh?.sub_kwh || '—'}}</div>
            <form class="row g-1 mt-1" (ngSubmit)="saveSubKwh(sh.id, subKwhVal[sh.id])">
              <div class="col-auto"><input type="number" class="form-control form-control-sm" placeholder="Sub kWh" [(ngModel)]="subKwhVal[sh.id]" [ngModelOptions]="{standalone:true}" /></div>
              <div class="col-auto"><button class="btn btn-sm btn-primary" type="submit">Save Sub KWH</button></div>
            </form>

            <!-- Sub Tenants -->
            <div class="mt-2 small">Sub Tenants:</div>
            <div *ngFor="let st of sh.sub_tenants" class="small">{{st.sub_house_tenant}} ({{st.sub_start_date}}–{{st.sub_end_date}} {{st.sub_days}}d) <span class="text-danger" style="cursor:pointer" (click)="removeSubTenant(sh.id, st.id)">×</span></div>
            <form class="row g-1 mt-1" (ngSubmit)="addSubTenant(sh.id)">
              <div class="col-5"><input class="form-control form-control-sm" placeholder="Sub Tenant" [(ngModel)]="newSubTenant[sh.id]" [ngModelOptions]="{standalone:true}" /></div>
              <div class="col-3"><input type="date" class="form-control form-control-sm" [(ngModel)]="newSubStart[sh.id]" [ngModelOptions]="{standalone:true}" /></div>
              <div class="col-3"><input type="date" class="form-control form-control-sm" [(ngModel)]="newSubEnd[sh.id]" [ngModelOptions]="{standalone:true}" /></div>
              <div class="col-1"><button class="btn btn-sm btn-success">Add</button></div>
            </form>
          </div>
        </div>
        <ng-template #noSub><em>No sub-houses.</em></ng-template>

        <form (ngSubmit)="addSub()" class="mt-2 d-flex gap-2">
          <input class="form-control" placeholder="New Sub House Name" [(ngModel)]="newSubName" [ngModelOptions]="{standalone:true}" />
          <button class="btn btn-success" type="submit">Add Sub House</button>
        </form>
      </div>

      <!-- ACTIONS: Reports / Calc / Back -->
      <div class="mt-3" *ngIf="h.bill && h.kwh">
        <a [routerLink]="['/houses', h.id, 'calc']" class="btn btn-success w-100 mb-2">Calculate / Report</a>
        <a routerLink="/houses" class="btn btn-secondary w-100">Back to Houses List</a>
      </div>
      <a *ngIf="!(h.bill && h.kwh)" routerLink="/houses" class="btn btn-secondary w-100">Back</a>
    </div>
  </div></div>
  `
})
export class HouseDetailComponent implements OnInit {
  house?: House; id!: number;
  messages: string[] = [];
  editingName = false;

  billForm: FormGroup; billErrors: string[] = [];
  kwhForm: FormGroup; kwhErrors: string[] = [];
  tenantForm: FormGroup; tenantErrors: string[] = [];
  nameForm: FormGroup;

  newSubName = '';
  subKwhVal: Record<number, number> = {};
  newSubTenant: Record<number, string> = {};
  newSubStart: Record<number, string> = {};
  newSubEnd: Record<number, string> = {};

  constructor(private route: ActivatedRoute, private router: Router, private svc: HousesService, private fb: FormBuilder) {
    this.billForm = this.fb.group({ amount: [''], start: [''], end: [''] });
    this.kwhForm = this.fb.group({ kwh: [''], last: [''], read: [''] });
    this.tenantForm = this.fb.group({ name: [''], start: [''], end: [''] });
    this.nameForm = this.fb.group({ name: [''] });
  }

  ngOnInit() {
    this.id = +this.route.snapshot.paramMap.get('id')!;
    this.reload();
    this.svc.houses$.subscribe(() => this.reload());
  }

  reload() {
    this.house = this.svc.getById(this.id);
    if (this.house) {
      this.nameForm.patchValue({ name: this.house.house_name });
      if (this.house.bill) this.billForm.patchValue({ amount: this.house.bill.amount_bill, start: this.house.bill.start_date_bill, end: this.house.bill.end_date_bill });
    }
  }

  saveName() {
    if (!this.house) return;
    const nm = this.nameForm.value.name?.trim();
    if (nm) this.svc.updateHouseName(this.house.id, nm);
    this.editingName = false; this.messages = ['House name updated.'];
  }

  saveBill() {
    if (!this.house) return;
    this.billErrors = [];
    const v = this.billForm.value;
    const res = this.svc.setBill(this.house.id, v.amount, v.start, v.end);
    if (!res.ok) this.billErrors = res.errors || [];
    else { this.messages = ['Bill saved (tenants cleared per original rules).']; this.reload(); }
  }

  saveKwh() {
    if (!this.house) return;
    this.kwhErrors = [];
    const v = this.kwhForm.value;
    const res = this.svc.setKwh(this.house.id, v.kwh ? +v.kwh : undefined, v.last ? +v.last : undefined, v.read ? +v.read : undefined);
    if (!res.ok) this.kwhErrors = res.errors || [];
    else { this.messages = ['Kilowatts saved.']; this.reload(); }
  }

  addTenant() {
    if (!this.house) return;
    this.tenantErrors = [];
    const v = this.tenantForm.value;
    const res = this.svc.addTenant(this.house.id, v.name, v.start, v.end);
    if (!res.ok) this.tenantErrors = res.errors || [];
    else { this.messages = ['Tenant added.']; this.tenantForm.reset(); this.reload(); }
  }
  removeTenant(tid: number) { this.svc.removeTenant(this.id, tid); this.reload(); }

  addSub() {
    if (!this.house || !this.newSubName) return;
    const res = this.svc.addSubHouse(this.house.id, this.newSubName);
    if (res.ok) { this.newSubName = ''; this.messages = ['Sub house added.']; this.reload(); }
  }
  deleteSub(sid: number) { this.svc.deleteSubHouse(this.id, sid); this.reload(); }

  saveSubKwh(subId: number, val?: number) {
    if (!this.house || !val) return;
    const res = this.svc.setSubKwh(this.house.id, subId, +val);
    if (res.ok) { this.messages = ['Sub KWH saved.']; this.reload(); } else this.messages = res.errors || [];
  }

  addSubTenant(subId: number) {
    if (!this.house) return;
    const name = this.newSubTenant[subId]; const st = this.newSubStart[subId]; const en = this.newSubEnd[subId];
    if (!name || !st || !en) return;
    const res = this.svc.addSubTenant(this.house.id, subId, name, st, en);
    if (res.ok) {
      this.newSubTenant[subId] = ''; this.newSubStart[subId] = ''; this.newSubEnd[subId] = '';
      this.messages = ['Sub tenant added.']; this.reload();
    } else this.messages = res.errors || [];
  }
  removeSubTenant(subId: number, tid: number) { this.svc.removeSubTenant(this.id, subId, tid); this.reload(); }
}
