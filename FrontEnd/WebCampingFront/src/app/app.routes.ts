import { Routes } from '@angular/router';
import { AjoutClientComponent } from './ajout-client/ajout-client.component';
import { AuthentificationComponent } from './authentification/authentification.component';
import { StatCampingComponent } from './stat-camping/stat-camping.component';
import { StatGeneralComponent } from './stat-general/stat-general.component';

export const routes: Routes = [
    { path: '', component: AuthentificationComponent },
    { path: 'ajout-client', component: AjoutClientComponent },
    { path: 'stat-camping', component: StatCampingComponent },
    { path: 'stat-general', component: StatGeneralComponent }
    // { path: '**', component: PageNotFoundComponent }
];
