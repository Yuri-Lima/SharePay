import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HousesService } from '../../core/houses.service';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
  <div class="container py-4" *ngIf="result as r; else loading">
    <a class="btn btn-link mb-2" routerLink="..">← Back to House</a>
    <h4 class="mb-3">Reports SharePay — Calculate</h4>

    <!-- Info table EXACT same as calc_main_house.html -->
    <table class="table table-sm">
      <thead class="bg-info text-white">
        <tr>
          <th>Total Kilowatts/Hour</th>
          <th>Amount Bill</th>
          <th>Period</th>
          <th>User Name</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>{{r.kwh}}</th>
          <td>{{r.bill_value}}</td>
          <td>{{r.period_bill}}</td>
          <td>{{r.user}}</td>
        </tr>
      </tbody>
    </table>

    <div class="alert alert-danger text-center"><h5>Main House and Sub Houses Without Kilowatts</h5></div>

    <!-- MAIN HOUSE TABLE -->
    <div class="table-responsive" *ngFor="let mainEntry of mainHouseEntries(r)">
      <table class="table table-hover">
        <caption>Main House</caption>
        <h5 class="m-2">{{mainEntry.name}}</h5>
        <div class="m-2"><strong>Kilowatts:</strong> {{r.new_main_kwh}} kwh</div>
        <div class="m-2"><strong>Bill Value:</strong> {{r.new_amount}}</div>
        <thead class="thead-dark"><tr>
          <th>#</th><th>Tenant Name</th><th>Tenant Period</th><th>Days</th><th>Due Value</th>
        </tr></thead>
        <tbody>
          <tr class="table-success" *ngFor="let t of mainEntry.tenants; let i = index">
            <th>{{i+1}}</th>
            <td>{{t.key}}</td>
            <td>{{t.value.date}}</td>
            <td>{{t.value.days}}</td>
            <td>{{t.value.value}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- SUB HOUSE WITHOUT -->
    <div class="table-responsive" *ngFor="let entry of subWithoutEntries(r)">
      <table class="table table-hover">
        <caption>Sub House Without Kilowatts</caption>
        <h5 class="m-2">{{entry.name}}</h5>
        <thead class="thead-dark"><tr>
          <th>#</th><th>Tenant Name</th><th>Tenant Period</th><th>Days</th><th>Due Value</th>
        </tr></thead>
        <tbody>
          <tr class="table-success" *ngFor="let t of entry.tenants; let i=index">
            <th>{{i+1}}</th><td>{{t.key}}</td><td>{{t.value.date}}</td><td>{{t.value.days}}</td><td>{{t.value.value}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- LEFT OVER 1 (collapsible) - exact match structure from template -->
    <div *ngIf="r.left_over1">
      <p class="m-2">
        <a class="btn btn-primary" (click)="toggleLO1()">Details: Days of Empty House</a>
      </p>
      <div class="collapse" [class.show]="showLO1">
        <div class="card card-body">
          <div class="table-responsive">
            <table class="table table-hover" *ngFor="let lo of leftOverEntries(r.left_over1)">
              <caption>Values which no one was living as a tenant.</caption>
              <thead class="thead-dark"><tr><th>#</th><th>Main/Sub House_Name - Date</th><th>Left Over</th></tr></thead>
              <tbody>
                <tr class="table-danger" *ngFor="let d of lo.details; let i=index">
                  <th>{{i+1}}</th><td>{{d.key}}</td><td>{{d.value | number:'1.3-3'}}</td>
                </tr>
              </tbody>
              <thead class="thead-secondary"><tr><th>#</th><th>Total</th><th>{{lo.total}}</th></tr></thead>
            </table>
          </div>
        </div>
      </div>
      <!-- summary totals table -->
      <div class="table-responsive" *ngFor="let lo of leftOverEntries(r.left_over1)">
        <table class="table table-hover">
          <thead class="thead-dark">
            <tr><th>#</th><th>Total Days of Empty House</th><th>{{lo.total}}</th></tr>
            <tr><th>#</th><th>Total Days Left</th><th>{{lo.days}}</th></tr>
          </thead>
        </table>
      </div>
    </div>

    <!-- WITH KWH SECTION: include same structure as with_kwh.html -->
    <div *ngIf="hasWithKwh(r)">
      <div class="alert alert-danger text-center mt-4"><h5>Sub Houses With Kilowatts</h5></div>
      <div class="table-responsive" *ngFor="let entry of subWithEntries(r)">
        <table class="table table-hover">
          <caption>Sub_House with kilowatts registered</caption>
          <h5 class="m-2">{{entry.name}}</h5>
          <div class="m-2"><strong>Kilowatts:</strong> {{entry.first.kwh_infor | json}} kwh</div>
          <div class="m-2"><strong>Bill Value:</strong> {{entry.first.bill_value}}</div>
          <thead class="thead-dark"><tr>
            <th>#</th><th>Tenant Name</th><th>Tenant Period</th><th>Days</th><th>Due Value</th>
          </tr></thead>
          <tbody>
            <tr class="table-secondary" *ngFor="let t of entry.tenants; let i=index">
              <th>{{i+1}}</th><td>{{t.key}}</td><td>{{t.value.date}}</td><td>{{t.value.days}}</td><td>{{t.value.tenant_value}}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- left over with kwh collapsible -->
      <div *ngIf="r.left_over_with || r.left_over1">
        <p class="m-2"><a class="btn btn-primary" (click)="toggleLO2()">Details: Days of Empty House (with kWh)</a></p>
        <div class="collapse" [class.show]="showLO2">
          <div class="card card-body">
            <div class="table-responsive" *ngFor="let lo of leftOverWithEntries(r)">
              <table class="table table-hover">
                <caption>Values which no one was living as a tenant.</caption>
                <thead class="thead-dark"><tr><th>#</th><th>Sub House_Name - Date</th><th>Value per Day</th></tr></thead>
                <tbody>
                  <tr class="table-danger" *ngFor="let d of lo.details; let ii=index"><th>{{ii+1}}</th><td>{{d.key}}</td><td>{{d.value | number:'1.3-3'}}</td></tr>
                </tbody>
                <thead><tr class="table-secondary"><th>#</th><th>Total</th><th>{{lo.total}}</th></tr></thead>
                <thead><tr class="table-secondary"><th>#</th><th>Empty Days</th><th>{{lo.days}}</th></tr></thead>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <a class="btn btn-link mt-4" routerLink="..">Back to Reports / House</a>
  </div>
  <ng-template #loading>
    <div class="container py-5">Loading calculation... (or missing bill/kwh data)</div>
  </ng-template>
  `
})
export class CalcReportComponent implements OnInit {
  result: any; id!: number; showLO1 = false; showLO2 = false;

  constructor(private route: ActivatedRoute, private svc: HousesService) {}

  ngOnInit() {
    this.id = +this.route.snapshot.paramMap.get('id')!;
    // Prefer real authoritative calculate (POST /houses/:id/calculate via Nest -> pure BillCalculator)
    // for exact parity proof. Falls back to local mock (which is kept identical).
    const maybePromise = (this.svc as any).calculateReal ? (this.svc as any).calculateReal(this.id) : Promise.resolve(this.svc.calculate(this.id));
    maybePromise.then((r: any) => { this.result = r; }).catch(() => {
      this.result = this.svc.calculate(this.id);
    });
  }

  toggleLO1() { this.showLO1 = !this.showLO1; }
  toggleLO2() { this.showLO2 = !this.showLO2; }

  // Helpers to produce iterable data for exact template replication
  mainHouseEntries(r: any) {
    if (!r.main_house) return [];
    return Object.keys(r.main_house).map(name => ({
      name,
      tenants: Object.keys(r.main_house[name]).map(k => ({ key: k, value: r.main_house[name][k] }))
    }));
  }
  subWithoutEntries(r: any) {
    if (!r.sub_house_without) return [];
    return Object.keys(r.sub_house_without).map(name => ({
      name,
      tenants: Object.keys(r.sub_house_without[name]).map(k => ({ key: k, value: r.sub_house_without[name][k] }))
    }));
  }
  hasWithKwh(r: any) { return r.sub_house_with && Object.keys(r.sub_house_with).length > 0; }
  subWithEntries(r: any) {
    if (!r.sub_house_with) return [];
    return Object.keys(r.sub_house_with).map(name => {
      const tenantsObj = r.sub_house_with[name];
      const keys = Object.keys(tenantsObj);
      return {
        name,
        first: keys.length ? tenantsObj[keys[0]] : {},
        tenants: keys.map(k => ({ key: k, value: tenantsObj[k] }))
      };
    });
  }
  leftOverEntries(lo: any) {
    if (!lo) return [];
    return Object.keys(lo).map(house => ({
      house,
      total: lo[house].left_over1,
      days: lo[house].days_left_over,
      details: Object.keys(lo[house].details_date || {}).map(k => ({ key: k, value: lo[house].details_date[k] }))
    }));
  }
  leftOverWithEntries(r: any) {
    const lo = r.left_over_with || r.left_over1;
    return this.leftOverEntries(lo);
  }
}
