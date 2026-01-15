import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { TutorInterfaceComponent } from './components/tutor-interface/tutor-interface.component';

export const routes: Routes = [
    { path: '', redirectTo: 'home', pathMatch: 'full' },
    { path: 'home', component: HomeComponent },
    { path: 'tutor', component: TutorInterfaceComponent }
];
