import { IonicModule} from '@ionic/angular';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Tab1Page } from './tab1.page';
import { Chart } from 'chart.js';
import { Tab1PageRoutingModule } from './tab1-routing.module';
import { Papa } from 'ngx-papaparse';
import { HttpClientModule, HttpClient } from '@angular/common/http';
//import { IonicPageModule } from 'ionic-angular';

//import { PapaParseModule } from 'ngx-papaparse';

@NgModule({
  imports: [
    IonicModule,
    //IonicPageModule.forChild(Tab1Page),
    CommonModule,
    FormsModule,
    HttpClientModule,
    Tab1PageRoutingModule,
    //PapaParseModule,
  ],
  declarations: [Tab1Page]
})
export class Tab1PageModule {}
