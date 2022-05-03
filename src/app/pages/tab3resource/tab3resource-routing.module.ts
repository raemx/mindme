import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { Tab3resourcePage } from './tab3resource.page';

const routes: Routes = [
  {
    path: '',
    component: Tab3resourcePage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class Tab3resourcePageRoutingModule {}
