import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DecimalPipe, JsonPipe } from '@angular/common';
import { HousesService } from '../../core/houses.service';

@Component({
  standalone: true,
  imports: [RouterLink, DecimalPipe, JsonPipe],
  template: `
  @if (result(); as r) {
    <div class="container py-4">
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
      @for (mainEntry of mainHouseEntries(r); track mainEntry.name) {
        <div class="table-responsive">
          <table class="table table-hover">
            <caption>Main House</caption>
            <h5 class="m-2">{{mainEntry.name}}</h5>
            <div class="m-2"><strong>Kilowatts:</strong> {{r.new_main_kwh}} kwh</div>
            <div class="m-2"><strong>Bill Value:</strong> {{r.new_amount}}</div>
            <thead class="thead-dark"><tr>
              <th>#</th><th>Tenant Name</th><th>Tenant Period</th><th>Days</th><th>Due Value</th>
            </tr></thead>
            <tbody>
              @for (t of mainEntry.tenants; track t.key; let i = $index) {
                <tr class="table-success">
                  <th>{{i + 1}}</th>
                  <td>{{t.key}}</td>
                  <td>{{t.value.date}}</td>
                  <td>{{t.value.days}}</td>
                  <td>{{t.value.value}}</td>
                </tr>
              }
            </tbody>
          </table>
        </div>
      }

      <!-- SUB HOUSE WITHOUT -->
      @for (entry of subWithoutEntries(r); track entry.name) {
        <div class="table-responsive">
          <table class="table table-hover">
            <caption>Sub House Without Kilowatts</caption>
            <h5 class="m-2">{{entry.name}}</h5>
            <thead class="thead-dark"><tr>
              <th>#</th><th>Tenant Name</th><th>Tenant Period</th><th>Days</th><th>Due Value</th>
            </tr></thead>
            <tbody>
              @for (t of entry.tenants; track t.key; let i = $index) {
                <tr class="table-success">
                  <th>{{i + 1}}</th>
                  <td>{{t.key}}</td>
                  <td>{{t.value.date}}</td>
                  <td>{{t.value.days}}</td>
                  <td>{{t.value.value}}</td>
                </tr>
              }
            </tbody>
          </table>
        </div>
      }

      <!-- LEFT OVER 1 (collapsible) -->
      @if (r.left_over1) {
        <div>
          <p class="m-2">
            <a class="btn btn-primary" (click)="toggleLO1()">Details: Days of Empty House</a>
          </p>
          <div class="collapse" [class.show]="showLO1()">
            <div class="card card-body">
              <div class="table-responsive">
                @for (lo of leftOverEntries(r.left_over1); track lo.house) {
                  <table class="table table-hover">
                    <caption>Values which no one was living as a tenant.</caption>
                    <thead class="thead-dark"><tr><th>#</th><th>Main/Sub House_Name - Date</th><th>Left Over</th></tr></thead>
                    <tbody>
                      @for (d of lo.details; track d.key; let i = $index) {
                        <tr class="table-danger">
                          <th>{{i + 1}}</th>
                          <td>{{d.key}}</td>
                          <td>{{d.value | number:'1.3-3'}}</td>
                        </tr>
                      }
                    </tbody>
                    <thead class="thead-secondary"><tr><th>#</th><th>Total</th><th>{{lo.total}}</th></tr></thead>
                  </table>
                }
              </div>
            </div>
          </div>
          <!-- summary totals table -->
          @for (lo of leftOverEntries(r.left_over1); track lo.house) {
            <div class="table-responsive">
              <table class="table table-hover">
                <thead class="thead-dark">
                  <tr><th>#</th><th>Total Days of Empty House</th><th>{{lo.total}}</th></tr>
                  <tr><th>#</th><th>Total Days Left</th><th>{{lo.days}}</th></tr>
                </thead>
              </table>
            </div>
          }
        </div>
      }

      <!-- WITH KWH SECTION -->
      @if (hasWithKwh(r)) {
        <div>
          <div class="alert alert-danger text-center mt-4"><h5>Sub Houses With Kilowatts</h5></div>
          @for (entry of subWithEntries(r); track entry.name) {
            <div class="table-responsive">
              <table class="table table-hover">
                <caption>Sub_House with kilowatts registered</caption>
                <h5 class="m-2">{{entry.name}}</h5>
                <div class="m-2"><strong>Kilowatts:</strong> {{entry.first.kwh_infor | json}} kwh</div>
                <div class="m-2"><strong>Bill Value:</strong> {{entry.first.bill_value}}</div>
                <thead class="thead-dark"><tr>
                  <th>#</th><th>Tenant Name</th><th>Tenant Period</th><th>Days</th><th>Due Value</th>
                </tr></thead>
                <tbody>
                  @for (t of entry.tenants; track t.key; let i = $index) {
                    <tr class="table-secondary">
                      <th>{{i + 1}}</th>
                      <td>{{t.key}}</td>
                      <td>{{t.value.date}}</td>
                      <td>{{t.value.days}}</td>
                      <td>{{t.value.tenant_value}}</td>
                    </tr>
                  }
                </tbody>
              </table>
            </div>
          }

          <!-- left over with kwh collapsible -->
          @if (r.left_over_with || r.left_over1) {
            <div>
              <p class="m-2"><a class="btn btn-primary" (click)="toggleLO2()">Details: Days of Empty House (with kWh)</a></p>
              <div class="collapse" [class.show]="showLO2()">
                <div class="card card-body">
                  @for (lo of leftOverWithEntries(r); track lo.house) {
                    <div class="table-responsive">
                      <table class="table table-hover">
                        <caption>Values which no one was living as a tenant.</caption>
                        <thead class="thead-dark"><tr><th>#</th><th>Sub House_Name - Date</th><th>Value per Day</th></tr></thead>
                        <tbody>
                          @for (d of lo.details; track d.key; let ii = $index) {
                            <tr class="table-danger">
                              <th>{{ii + 1}}</th>
                              <td>{{d.key}}</td>
                              <td>{{d.value | number:'1.3-3'}}</td>
                            </tr>
                          }
                        </tbody>
                        <thead><tr class="table-secondary"><th>#</th><th>Total</th><th>{{lo.total}}</th></tr></thead>
                        <thead><tr class="table-secondary"><th>#</th><th>Empty Days</th><th>{{lo.days}}</th></tr></thead>
                      </table>
                    </div>
                  }
                </div>
              </div>
            </div>
          }
        </div>
      }

      <a class="btn btn-link mt-4" routerLink="..">Back to Reports / House</a>
    </div>
  } @else {
    <div class="container py-5">Loading calculation... (or missing bill/kwh data)</div>
  }
  `
})
export class CalcReportComponent {
  private route = inject(ActivatedRoute);
  private svc = inject(HousesService);

  result = signal<any>(null);
  showLO1 = signal(false);
  showLO2 = signal(false);

  id!: number;

  constructor() {
    this.id = +this.route.snapshot.paramMap.get('id')!;

    // Prefer real authoritative calculate
    const maybePromise = (this.svc as any).calculateReal
      ? (this.svc as any).calculateReal(this.id)
      : Promise.resolve(this.svc.calculate(this.id));

    maybePromise
      .then((r: any) => this.result.set(r))
      .catch(() => this.result.set(this.svc.calculate(this.id)));
  }

  toggleLO1() { this.showLO1.update(v => !v); }
  toggleLO2() { this.showLO2.update(v => !v); }

  // Helpers (kept for exact report structure parity)
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

  hasWithKwh(r: any) {
    return r.sub_house_with && Object.keys(r.sub_house_with).length > 0;
  }

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
