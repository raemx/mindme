import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { Tab3resourcePageRoutingModule } from './tab3resource-routing.module';

import { Tab3resourcePage } from './tab3resource.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    Tab3resourcePageRoutingModule
  ],
  declarations: [Tab3resourcePage]
})
export class Tab3resourcePageModule {}
