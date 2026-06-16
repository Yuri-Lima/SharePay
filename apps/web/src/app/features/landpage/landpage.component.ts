import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'sp-landpage',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
  <!-- Navigation + Masthead from index.html + features list -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container px-5">
      <a class="navbar-brand" routerLink="/">SharePay</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link" href="#features">Features</a></li>
          <li class="nav-item"><a class="nav-link" routerLink="/login">Login</a></li>
          <li class="nav-item"><a class="nav-link" routerLink="/signup">Sign Up</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <header class="bg-dark py-5">
    <div class="container px-5">
      <div class="row gx-5 align-items-center justify-content-center">
        <div class="col-lg-8 col-xl-7">
          <div class="my-5 text-center text-xl-start text-white">
            <h1 class="display-5 fw-bolder mb-2">SharePay helps you split bills among the tenants.</h1>
            <p class="lead fw-normal text-white-50 mb-4">If you don't like spreadsheets or math, we're here to help you. Come meet us!</p>
            <div class="d-grid gap-3 d-sm-flex justify-content-sm-center justify-content-xl-start">
              <a class="btn btn-primary btn-lg px-4" routerLink="/signup">Get Started</a>
              <a class="btn btn-outline-light btn-lg px-4" href="#features">Learn More</a>
            </div>
          </div>
        </div>
        <div class="col-xl-5 d-none d-xl-block">
          <div class="ratio ratio-16x9 bg-secondary rounded">
            <div class="d-flex align-items-center justify-content-center text-white">Demo Video Placeholder</div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- Features from index/about/pricing/faq condensed -->
  <section id="features" class="py-5">
    <div class="container px-5 my-5">
      <div class="row gx-5">
        <div class="col-lg-4 mb-5"><h2 class="fw-bolder">A better way to start sharing.</h2></div>
        <div class="col-lg-8">
          <div class="row gx-5 row-cols-1 row-cols-md-2">
            <div class="col mb-5"><div class="feature bg-primary text-white rounded-3 mb-3 p-3 d-inline-block"><i class="bi bi-collection"></i></div><h5>Paper Bill</h5><p>All details you will find out in your Bill.</p></div>
            <div class="col mb-5"><div class="feature bg-primary text-white rounded-3 mb-3 p-3 d-inline-block"><i class="bi bi-calendar-date"></i></div><h5>Period of the bill</h5><p>Make sure that you have all range of the period bill.</p></div>
            <div class="col mb-5"><div class="feature bg-primary text-white rounded-3 mb-3 p-3 d-inline-block"><i class="bi bi-cash-coin"></i></div><h5>Amount</h5><p>Check out the correct amount of the bill came from.</p></div>
            <div class="col"><div class="feature bg-primary text-white rounded-3 mb-3 p-3 d-inline-block"><i class="bi bi-clipboard-check"></i></div><h5>Tenants Names and Periods</h5><p>List all tenants name and period which they are/were living at house.</p></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="py-5 bg-light">
    <div class="container px-5">
      <div class="text-center">
        <div class="fs-4 mb-4 fst-italic">"Working with SharePay has saved me tons of time when I want to split the bill with Tenants who live in my houses!"</div>
        <div><strong>Yuri Lima</strong> / Owner, SharePay</div>
      </div>
    </div>
  </div>

  <section class="py-5">
    <div class="container px-5 text-center">
      <h2 class="fw-bolder mb-3">Pricing &amp; FAQ Highlights</h2>
      <p class="lead text-muted">Fair, transparent splitting. Free for core use. No spreadsheets needed. Supports main house + sub-houses with or without separate kWh meters.</p>
      <ul class="list-unstyled mt-4">
        <li>✓ Exact day-based proration and kWh-aware allocation</li>
        <li>✓ Handles tenant move-in/out ranges and empty days (left-overs)</li>
        <li>✓ Sub-house kWh reads supported; leftover calculations per original rules</li>
      </ul>
      <a routerLink="/signup" class="btn btn-primary mt-3">Create your first house</a>
    </div>
  </section>

  <footer class="bg-dark py-4 mt-auto text-white-50">
    <div class="container px-5 small d-flex justify-content-between">
      <div>© SharePay</div>
      <div>Privacy · Terms</div>
    </div>
  </footer>
  `
})
export class LandpageComponent {}
