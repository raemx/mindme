import { IonicModule } from '@ionic/angular';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Tab1Page } from './tab1.page';
import { Chart } from 'chart.js';
import { Tab1PageRoutingModule } from './tab1-routing.module';
import { Papa } from 'ngx-papaparse';
//import { PapaParseModule } from 'ngx-papaparse';

@NgModule({
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    Tab1PageRoutingModule,
    //PapaParseModule,
    Chart
  ],
  declarations: [Tab1Page]
})
export class Tab1PageModule {}
