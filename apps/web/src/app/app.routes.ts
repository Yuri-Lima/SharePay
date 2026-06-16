import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';
import { LandpageComponent } from './features/landpage/landpage.component';
import { LoginComponent } from './features/auth/login.component';
import { SignupComponent } from './features/auth/signup.component';
import { HouseListComponent } from './features/houses/house-list.component';
import { HouseCreateComponent } from './features/houses/house-create.component';
import { HouseDetailComponent } from './features/houses/house-detail.component';
import { CalcReportComponent } from './features/houses/calc-report.component';

export const routes: Routes = [
  { path: '', component: LandpageComponent },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'houses', component: HouseListComponent, canActivate: [authGuard] },
  { path: 'houses/new', component: HouseCreateComponent, canActivate: [authGuard] },
  { path: 'houses/:id', component: HouseDetailComponent, canActivate: [authGuard] },
  { path: 'houses/:id/calc', component: CalcReportComponent, canActivate: [authGuard] },
  { path: '**', redirectTo: '' }
];
