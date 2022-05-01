

import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from "@angular/core";
import { Chart } from "chart.js";
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ApiService } from "../api.service";
import { IonicModule, ToastController } from '@ionic/angular';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import {  NavController, NavParams,  } from '@ionic/angular';


@Component({
  selector: 'app-tab5',
  templateUrl: './tab5.page.html',
  styleUrls: ['./tab5.page.scss'],
  providers: [NavParams]
})
export class Tab5Page implements OnInit {

  constructor(public navCtrl: NavController, 
  ) { }

  ngOnInit() {
  }

logout(){
  this.navCtrl.navigateRoot(['/login']);
}

}
