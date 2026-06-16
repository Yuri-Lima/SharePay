import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'sp-root',
  standalone: true,
  imports: [RouterModule],
  template: `
    <nav style="padding:8px;background:#111;color:#fff">SharePay (Angular)</nav>
    <router-outlet></router-outlet>
    <footer style="padding:8px;font-size:12px">Migrated • pnpm + Nx • Nest + Angular • 100% calc parity</footer>
  `,
})
export class AppComponent {}
