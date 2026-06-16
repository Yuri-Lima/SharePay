import { Component, inject, signal, effect } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { HousesService, House } from '../../core/houses.service';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  template: `
  <div class="masthead"><div class="masthead-bg"></div>
  <div class="container">
    @if (house(); as h) {
      <div class="masthead-content text-white py-4">
        <h3>Details from {{h.house_name}}</h3>

        <!-- Messages / feedback -->
        @for (m of messages(); track m) {
          <div class="alert alert-info py-1 small">{{m}}</div>
        }

        <!-- Edit House Name -->
        <a class="btn btn-outline-primary text-white w-100 mb-2" (click)="toggleEditingName()">Edit House Name</a>
        @if (editingName()) {
          <div class="form-section mb-3">
            <form [formGroup]="nameForm" (ngSubmit)="saveName()">
              <input class="form-control mb-2" formControlName="name" />
              <button class="btn btn-sm btn-primary" type="submit">Save</button>
            </form>
          </div>
        }

        <!-- BILL SECTION -->
        <div class="form-section">
          <div class="section-title">Bill</div>
          @if (h.bill) {
            <div><strong>€{{h.bill.amount_bill}}</strong> | {{h.bill.start_date_bill}} → {{h.bill.end_date_bill}} ({{h.bill.days_bill}} days)</div>
          } @else {
            <em>No bill yet</em>
          }
          <form [formGroup]="billForm" (ngSubmit)="saveBill()" class="row g-2 mt-2">
            <div class="col-md-3"><input type="text" class="form-control" placeholder="Amount e.g. 124.50" formControlName="amount" /></div>
            <div class="col-md-3"><input type="date" class="form-control" formControlName="start" /></div>
            <div class="col-md-3"><input type="date" class="form-control" formControlName="end" /></div>
            <div class="col-md-3"><button class="btn btn-primary w-100" type="submit">Save Bill</button></div>
          </form>
          @for (e of billErrors(); track e) {
            <div class="text-danger small">{{e}}</div>
          }
        </div>

        <!-- KWH SECTION (only after bill) -->
        @if (h.bill) {
          <div class="form-section">
            <div class="section-title">Kilowatts</div>
            @if (h.kwh) {
              <div><strong>{{h.kwh.kwh}} kwh</strong> <span class="small">(reads: {{h.kwh.last_read_kwh}} / {{h.kwh.read_kwh}})</span></div>
            } @else {
              <em>Add kilowatts (direct or last+present read)</em>
            }

            <form [formGroup]="kwhForm" (ngSubmit)="saveKwh()" class="row g-2 mt-2">
              <div class="col-md-2"><input type="number" class="form-control" placeholder="kWh direct" formControlName="kwh" /></div>
              <div class="col-md-2"><input type="number" class="form-control" placeholder="Last read" formControlName="last" /></div>
              <div class="col-md-2"><input type="number" class="form-control" placeholder="Present read" formControlName="read" /></div>
              <div class="col-md-3"><button class="btn btn-primary w-100" type="submit">Save KWH</button></div>
            </form>
            @for (e of kwhErrors(); track e) {
              <div class="text-danger small">{{e}}</div>
            }
          </div>
        }

        <!-- TENANTS SECTION (after bill + kwh) -->
        @if (h.bill && h.kwh) {
          <div class="form-section">
            <div class="section-title">Tenants (Main House) — {{h.tenants.length}} total</div>
            @for (t of h.tenants; track t.id) {
              <div class="d-flex justify-content-between border-bottom py-1 small">
                <span>{{t.house_tenant}} — {{t.start_date}} to {{t.end_date}} ({{t.days}}d)
                  <button class="btn btn-sm btn-link text-danger p-0 ms-2" (click)="removeTenant(t.id)">×</button>
                </span>
              </div>
            }
            <form [formGroup]="tenantForm" (ngSubmit)="addTenant()" class="row g-2 mt-2">
              <div class="col-md-4"><input class="form-control" placeholder="Tenant Name" formControlName="name" /></div>
              <div class="col-md-3"><input type="date" class="form-control" formControlName="start" /></div>
              <div class="col-md-3"><input type="date" class="form-control" formControlName="end" /></div>
              <div class="col-md-2"><button class="btn btn-success w-100" type="submit">Add Tenant</button></div>
            </form>
            @for (e of tenantErrors(); track e) {
              <div class="text-danger small">{{e}}</div>
            }
          </div>
        }

        <!-- SUB HOUSES -->
        @if (h.bill && h.kwh) {
          <div class="form-section">
            <div class="section-title">Sub Houses</div>
            @if (h.subHouses.length) {
              @for (sh of h.subHouses; track sh.id) {
                <div class="mb-3 border p-2 rounded bg-dark bg-opacity-25">
                  <div class="d-flex justify-content-between">
                    <strong>{{sh.sub_house_name}}</strong>
                    <button class="btn btn-sm btn-outline-danger" (click)="deleteSub(sh.id)">Delete Sub</button>
                  </div>

                  <!-- Sub KWH (signal-driven, no ngModel) -->
                  <div class="mt-1 small">KWH: {{sh.sub_kwh?.sub_kwh || '—'}}</div>
                  <form class="row g-1 mt-1" (ngSubmit)="saveSubKwh(sh.id)">
                    <div class="col-auto">
                      <input
                        type="number"
                        class="form-control form-control-sm"
                        placeholder="Sub kWh"
                        [value]="subKwhVal()[sh.id] || ''"
                        (input)="updateSubKwhVal(sh.id, $any($event.target).value)"
                      />
                    </div>
                    <div class="col-auto"><button class="btn btn-sm btn-primary" type="submit">Save Sub KWH</button></div>
                  </form>

                  <!-- Sub Tenants -->
                  <div class="mt-2 small">Sub Tenants:</div>
                  @for (st of sh.sub_tenants; track st.id) {
                    <div class="small">{{st.sub_house_tenant}} ({{st.sub_start_date}}–{{st.sub_end_date}} {{st.sub_days}}d)
                      <span class="text-danger" style="cursor:pointer" (click)="removeSubTenant(sh.id, st.id)">×</span>
                    </div>
                  }

                  <!-- Add sub tenant (signal-driven) -->
                  <form class="row g-1 mt-1" (ngSubmit)="addSubTenant(sh.id)">
                    <div class="col-5">
                      <input
                        class="form-control form-control-sm"
                        placeholder="Sub Tenant"
                        [value]="newSubTenant()[sh.id] || ''"
                        (input)="updateNewSubTenant(sh.id, $any($event.target).value)"
                      />
                    </div>
                    <div class="col-3">
                      <input
                        type="date"
                        class="form-control form-control-sm"
                        [value]="newSubStart()[sh.id] || ''"
                        (input)="updateNewSubStart(sh.id, $any($event.target).value)"
                      />
                    </div>
                    <div class="col-3">
                      <input
                        type="date"
                        class="form-control form-control-sm"
                        [value]="newSubEnd()[sh.id] || ''"
                        (input)="updateNewSubEnd(sh.id, $any($event.target).value)"
                      />
                    </div>
                    <div class="col-1"><button class="btn btn-sm btn-success">Add</button></div>
                  </form>
                </div>
              }
            } @else {
              <em>No sub-houses.</em>
            }

            <!-- New sub house (signal) -->
            <form (ngSubmit)="addSub()" class="mt-2 d-flex gap-2">
              <input
                class="form-control"
                placeholder="New Sub House Name"
                [value]="newSubName()"
                (input)="newSubName.set($any($event.target).value)"
              />
              <button class="btn btn-success" type="submit">Add Sub House</button>
            </form>
          </div>
        }

        <!-- ACTIONS: Reports / Calc / Back -->
        @if (h.bill && h.kwh) {
          <div class="mt-3">
            <a [routerLink]="['/houses', h.id, 'calc']" class="btn btn-success w-100 mb-2">Calculate / Report</a>
            <a routerLink="/houses" class="btn btn-secondary w-100">Back to Houses List</a>
          </div>
        } @else {
          <a routerLink="/houses" class="btn btn-secondary w-100">Back</a>
        }
      </div>
    }
  </div></div>
  `
})
export class HouseDetailComponent {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private svc = inject(HousesService);
  private fb = inject(FormBuilder);

  id!: number;

  // Local UI state as signals (modern)
  house = signal<House | undefined>(undefined);
  messages = signal<string[]>([]);
  editingName = signal(false);

  // Reactive forms (kept for main entities)
  billForm = this.fb.group({ amount: [''], start: [''], end: [''] });
  kwhForm = this.fb.group({ kwh: [''], last: [''], read: [''] });
  tenantForm = this.fb.group({ name: [''], start: [''], end: [''] });
  nameForm = this.fb.group({ name: [''] });

  // Transient per-sub-house UI state (replaces the old Record + ngModel standalone pattern)
  subKwhVal = signal<Record<number, number>>({});
  newSubTenant = signal<Record<number, string>>({});
  newSubStart = signal<Record<number, string>>({});
  newSubEnd = signal<Record<number, string>>({});
  newSubName = signal('');

  // Error arrays as signals
  billErrors = signal<string[]>([]);
  kwhErrors = signal<string[]>([]);
  tenantErrors = signal<string[]>([]);

  constructor() {
    this.id = +this.route.snapshot.paramMap.get('id')!;

    // React to any house list changes (modern effect instead of observable subscribe)
    effect(() => {
      // Depend on the signal
      this.svc.houses();
      this.reload();
    });

    // Initial load
    this.reload();
  }

  private pushMessage(msg: string) {
    this.messages.update(m => [...m, msg]);
  }
  private setMessages(msgs: string[]) {
    this.messages.set(msgs);
  }

  toggleEditingName() {
    this.editingName.update(v => !v);
  }

  reload() {
    const h = this.svc.getById(this.id);
    this.house.set(h);
    if (h) {
      this.nameForm.patchValue({ name: h.house_name });
      if (h.bill) {
        this.billForm.patchValue({
          amount: h.bill.amount_bill,
          start: h.bill.start_date_bill,
          end: h.bill.end_date_bill
        });
      }
    }
  }

  saveName() {
    const h = this.house();
    if (!h) return;
    const nm = this.nameForm.value.name?.trim();
    if (nm) this.svc.updateHouseName(h.id, nm);
    this.editingName.set(false);
    this.setMessages(['House name updated.']);
  }

  saveBill() {
    const h = this.house();
    if (!h) return;
    this.billErrors.set([]);
    const v = this.billForm.value;
    const res = this.svc.setBill(h.id, v.amount ?? '', v.start ?? '', v.end ?? '');
    if (!res.ok) {
      this.billErrors.set(res.errors || []);
    } else {
      this.setMessages(['Bill saved (tenants cleared per original rules).']);
      this.reload();
    }
  }

  saveKwh() {
    const h = this.house();
    if (!h) return;
    this.kwhErrors.set([]);
    const v = this.kwhForm.value;
    const res = this.svc.setKwh(
      h.id,
      v.kwh ? +v.kwh : undefined,
      v.last ? +v.last : undefined,
      v.read ? +v.read : undefined
    );
    if (!res.ok) {
      this.kwhErrors.set(res.errors || []);
    } else {
      this.setMessages(['Kilowatts saved.']);
      this.reload();
    }
  }

  addTenant() {
    const h = this.house();
    if (!h) return;
    this.tenantErrors.set([]);
    const v = this.tenantForm.value;
    const res = this.svc.addTenant(h.id, v.name ?? '', v.start ?? '', v.end ?? '');
    if (!res.ok) {
      this.tenantErrors.set(res.errors || []);
    } else {
      this.setMessages(['Tenant added.']);
      this.tenantForm.reset();
      this.reload();
    }
  }

  removeTenant(tid: number) {
    this.svc.removeTenant(this.id, tid);
    this.reload();
  }

  addSub() {
    const h = this.house();
    const name = this.newSubName().trim();
    if (!h || !name) return;
    const res = this.svc.addSubHouse(h.id, name);
    if (res.ok) {
      this.newSubName.set('');
      this.setMessages(['Sub house added.']);
      this.reload();
    }
  }

  deleteSub(sid: number) {
    this.svc.deleteSubHouse(this.id, sid);
    this.reload();
  }

  // --- Signal-backed helpers for sub-house transient fields (modern replacement for ngModel maps) ---
  updateSubKwhVal(subId: number, val: string) {
    const num = val === '' ? NaN : parseFloat(val);
    this.subKwhVal.update(map => ({ ...map, [subId]: isNaN(num) ? (map[subId] ?? 0) : num }));
  }

  saveSubKwh(subId: number) {
    const h = this.house();
    const val = this.subKwhVal()[subId];
    if (!h || !val) return;
    const res = this.svc.setSubKwh(h.id, subId, +val);
    if (res.ok) {
      this.setMessages(['Sub KWH saved.']);
      this.reload();
    } else {
      this.setMessages(res.errors || []);
    }
  }

  updateNewSubTenant(subId: number, val: string) {
    this.newSubTenant.update(map => ({ ...map, [subId]: val }));
  }
  updateNewSubStart(subId: number, val: string) {
    this.newSubStart.update(map => ({ ...map, [subId]: val }));
  }
  updateNewSubEnd(subId: number, val: string) {
    this.newSubEnd.update(map => ({ ...map, [subId]: val }));
  }

  addSubTenant(subId: number) {
    const h = this.house();
    if (!h) return;
    const name = this.newSubTenant()[subId];
    const st = this.newSubStart()[subId];
    const en = this.newSubEnd()[subId];
    if (!name || !st || !en) return;

    const res = this.svc.addSubTenant(h.id, subId, name, st, en);
    if (res.ok) {
      // clear only this sub's fields
      this.newSubTenant.update(m => { const c = { ...m }; delete c[subId]; return c; });
      this.newSubStart.update(m => { const c = { ...m }; delete c[subId]; return c; });
      this.newSubEnd.update(m => { const c = { ...m }; delete c[subId]; return c; });
      this.setMessages(['Sub tenant added.']);
      this.reload();
    } else {
      this.setMessages(res.errors || []);
    }
  }

  removeSubTenant(subId: number, tid: number) {
    this.svc.removeSubTenant(this.id, subId, tid);
    this.reload();
  }
}
