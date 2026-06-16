import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'sp-landpage',
  standalone: true,
  imports: [RouterLink],
  template: `
  <!-- Professional Nav with Tailwind + Prime ready -->
  <nav class="bg-zinc-950 border-b border-white/10 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
      <a routerLink="/" class="flex items-center gap-3 text-white font-semibold tracking-tight text-2xl">
        <span class="inline-block w-8 h-8 rounded bg-emerald-500"></span>
        SharePay
      </a>
      <div class="flex items-center gap-3 text-sm">
        <a href="#features" class="px-4 py-2 text-zinc-300 hover:text-white transition">Features</a>
        <a href="#how" class="px-4 py-2 text-zinc-300 hover:text-white transition">How it works</a>
        <a routerLink="/login" class="px-4 py-2 text-zinc-300 hover:text-white transition">Log in</a>
        <a routerLink="/signup" class="inline-flex items-center rounded-md bg-emerald-500 hover:bg-emerald-600 active:bg-emerald-700 text-white text-sm font-medium px-4 py-2 transition">Get started free</a>
      </div>
    </div>
  </nav>

  <!-- Hero: modern, clean, professional -->
  <header class="relative bg-zinc-950 text-white pt-16 pb-20 overflow-hidden">
    <div class="absolute inset-0 bg-[radial-gradient(#27272a_0.8px,transparent_1px)] bg-[length:4px_4px] opacity-60"></div>
    <div class="max-w-5xl mx-auto px-6 relative">
      <div class="flex flex-col items-center text-center">
        <div class="inline-flex items-center gap-2 rounded-full bg-white/5 px-3 py-1 text-xs tracking-[2px] text-emerald-400 mb-6 border border-white/10">FAIR • TRANSPARENT • EXACT</div>
        <h1 class="text-6xl md:text-7xl font-semibold tracking-tighter leading-none mb-6 max-w-4xl">
          Split energy bills fairly.<br>No spreadsheets. No stress.
        </h1>
        <p class="max-w-xl text-xl text-zinc-400 mb-10">
          SharePay calculates exact day-by-day + kWh prorations for main houses and sub-houses — the same trusted logic used by property managers.
        </p>
        <div class="flex flex-col sm:flex-row gap-3">
          <p-button routerLink="/signup" label="Create your first house" styleClass="!px-8 !py-3 !text-base !bg-white !text-zinc-950 hover:!bg-zinc-100 !border-white" />
          <a href="#features" class="inline-flex items-center justify-center rounded-md border border-white/20 hover:bg-white/5 px-8 py-3 text-base font-medium transition">See how it works</a>
        </div>
        <div class="mt-8 text-xs text-zinc-500 flex items-center gap-4">
          <div>✓ 100% parity with authoritative calculator</div>
          <div>✓ Works offline + real API</div>
        </div>
      </div>
    </div>
    <div class="mt-14 max-w-4xl mx-auto px-6">
      <div class="rounded-2xl border border-white/10 bg-zinc-900/70 p-4 text-left text-sm text-zinc-400 flex items-center gap-3">
        <i class="pi pi-check-circle text-emerald-400 text-lg"></i>
        <span>Trusted day-count, left-over, and sub-kWh allocation — identical to the original coresharepay engine.</span>
      </div>
    </div>
  </header>

  <!-- Trust / logos bar -->
  <div class="border-b border-white/10 bg-zinc-950 py-4">
    <div class="max-w-5xl mx-auto px-6 flex flex-wrap items-center justify-center gap-x-10 gap-y-3 text-xs tracking-widest text-zinc-500">
      <div>DAY-EXACT PRORATION</div>
      <div>SUB-HOUSES + KWH</div>
      <div>LEFT-OVER HANDLING</div>
      <div>NO MATH REQUIRED</div>
    </div>
  </div>

  <!-- Features -->
  <section id="features" class="max-w-6xl mx-auto px-6 py-20">
    <div class="flex flex-col items-center text-center mb-12">
      <div class="uppercase text-emerald-400 text-xs tracking-[3px] mb-2">Built for real houses</div>
      <h2 class="text-4xl font-semibold tracking-tight">Everything you need to split fairly</h2>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-5">
      <div class="rounded-2xl border border-white/10 bg-zinc-900 p-6">
        <i class="pi pi-file text-2xl text-emerald-400 mb-4 block"></i>
        <div class="font-semibold mb-1.5">Paper bill details</div>
        <div class="text-sm text-zinc-400">Capture total amount, exact period and days. Validations match the original forms.</div>
      </div>
      <div class="rounded-2xl border border-white/10 bg-zinc-900 p-6">
        <i class="pi pi-calendar text-2xl text-emerald-400 mb-4 block"></i>
        <div class="font-semibold mb-1.5">Precise periods</div>
        <div class="text-sm text-zinc-400">Tenant move-in/out ranges, inclusive day counts, and empty-day (left-over) allocation.</div>
      </div>
      <div class="rounded-2xl border border-white/10 bg-zinc-900 p-6">
        <i class="pi pi-bolt text-2xl text-emerald-400 mb-4 block"></i>
        <div class="font-semibold mb-1.5">kWh aware splits</div>
        <div class="text-sm text-zinc-400">Main house kWh + optional per-sub-house meter reads. Leftover kWh correctly redistributed.</div>
      </div>
      <div class="rounded-2xl border border-white/10 bg-zinc-900 p-6">
        <i class="pi pi-users text-2xl text-emerald-400 mb-4 block"></i>
        <div class="font-semibold mb-1.5">Main + sub-houses</div>
        <div class="text-sm text-zinc-400">Unlimited sub-houses, per-sub tenants, and separate kWh or proportional without kWh.</div>
      </div>
    </div>
  </section>

  <!-- How it works -->
  <section id="how" class="bg-zinc-900 border-y border-white/10 py-16">
    <div class="max-w-5xl mx-auto px-6">
      <div class="grid md:grid-cols-3 gap-8 text-sm">
        <div>
          <div class="text-emerald-400 text-xs mb-2 tracking-widest">01</div>
          <div class="font-semibold text-lg mb-2 text-white">Enter the bill</div>
          <p class="text-zinc-400">Amount, start and end dates. We compute days and validate ranges exactly as the legacy system.</p>
        </div>
        <div>
          <div class="text-emerald-400 text-xs mb-2 tracking-widest">02</div>
          <div class="font-semibold text-lg mb-2 text-white">Add kWh + tenants</div>
          <p class="text-zinc-400">Record main kWh (or last/present reads). Add tenants with their exact stay windows for both main and subs.</p>
        </div>
        <div>
          <div class="text-emerald-400 text-xs mb-2 tracking-widest">03</div>
          <div class="font-semibold text-lg mb-2 text-white">Get the authoritative report</div>
          <p class="text-zinc-400">One click produces the full breakdown with € values, left-overs, and per-tenant due — 100% parity guaranteed.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Testimonial / social proof -->
  <div class="py-16 border-b border-white/10">
    <div class="max-w-3xl mx-auto px-6 text-center">
      <div class="text-2xl font-medium tracking-tight text-white">"SharePay removed hours of painful reconciliation every month. The sub-house + kWh logic is perfect."</div>
      <div class="mt-6 text-sm text-zinc-400">— Yuri Lima, founder • used on dozens of shared houses</div>
    </div>
  </div>

  <!-- Final CTA -->
  <section class="py-16">
    <div class="max-w-xl mx-auto px-6 text-center">
      <h3 class="text-3xl font-semibold tracking-tight mb-3">Ready to stop fighting over bills?</h3>
      <p class="text-zinc-400 mb-8">Free core features. Exact math. Beautiful reports.</p>
      <a routerLink="/signup" class="inline-block rounded-lg bg-emerald-500 hover:bg-emerald-600 active:bg-emerald-700 text-white font-medium px-10 py-3 text-base transition">Start your first house in 30 seconds</a>
      <div class="text-[10px] text-zinc-500 mt-4">No credit card • Works fully offline • Real backend available</div>
    </div>
  </section>

  <footer class="border-t border-white/10 py-10 text-xs text-zinc-500">
    <div class="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
      <div>© SharePay • Fair splits for shared homes</div>
      <div class="flex gap-6">
        <a href="#" class="hover:text-zinc-300">Privacy</a>
        <a href="#" class="hover:text-zinc-300">Terms</a>
        <a routerLink="/login" class="hover:text-zinc-300">Log in</a>
      </div>
    </div>
  </footer>
  `
})
export class LandpageComponent {}
