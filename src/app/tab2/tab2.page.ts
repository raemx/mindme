
import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from "@angular/core";
import { Chart } from "chart.js";
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ApiService } from "../api.service";

import { Observable } from "rxjs";
import { PostProvider } from 'src/providers/post-provider';
import { IonicModule, ToastController } from '@ionic/angular';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import {  NavController, NavParams, LoadingController } from '@ionic/angular';
import { RouterOutlet,  ActivationStart } from '@angular/router';
import { Tab3Page } from "../tab3/tab3.page";

// import { pandas } from pandas;

// activitydf = pd.read_csv('../csv/activity.csv')
// sleepdf = pd.read_csv('../csv/sleep.csv')
// datadf = pd.read_csv('../csv/data.csv')

// sleepdf['day'] = pd.to_datetime(sleepdf['End']).dt.date #day finished sleeping
// sleepdf['day'] = sleepdf['day'].to_string()
// sleepdf['starttime'] = pd.to_datetime(sleepdf['Start']).dt.time #time began sleeping
// sleepdf.rename(columns={'Sleep quality': 'sleepquality','Time in bed': 'timeinbed','Wake up': 'wakeup','Sleep Notes': 'sleepnotes', 'Heart rate':'heartrate', 'Activity (steps)':'steps'}, inplace=True)


// activitydf.rename(columns={'Minutes Sedentary': 'minsed', 'Steps': 'steps', 'Day': 'day'}


@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss'],
  providers: [NavParams]
})

export class Tab2Page implements OnInit {
  @ViewChild("barCanvas", {static: true}) barCanvas: ElementRef;
  @ViewChild("doughnutCanvas",  {static: true}) doughnutCanvas: ElementRef;
  @ViewChild("lineCanvas", {static: true}) lineCanvas: ElementRef;
  @ViewChild(RouterOutlet) outlet: RouterOutlet;

  private barChart: Chart;
  private doughnutChart: Chart;
  private lineChart: Chart;
  users: any = [];
  pyths: any = [];
  recomsS: any = [];
  recomsW: any = [];
  data: any;
  email:any;
  id: any;
  msgs: any = [];


  // private todo : FormGroup;

  // constructor( private formBuilder: FormBuilder ) {
  //   this.todo = this.formBuilder.group({
  //     title: ['', Validators.required],
  //     description: [''],
  // });
  // }
  // logForm(){
  //   console.log(this.todo.value)
  // }
  
  constructor(public navCtrl: NavController, 
    public http   : HttpClient,
    private router: Router, 
    private postPvdr: PostProvider, 
    public toastCtrl: ToastController, 
    public apiservice: ApiService,
    private route: ActivatedRoute,
    public navParams: NavParams,
    public loadingCtrl: LoadingController){}

  async ngOnInit() {
    this.router.events.subscribe(e => {
      if (e instanceof ActivationStart && e.snapshot.outlet === "administration")
        this.outlet.deactivate();
    });

    this.email = this.navParams.get('email');
    this.id = 1
    
    var headers = new Headers();
    headers.append("Accept", 'application/json');
    headers.append('Content-Type', 'application/json' );
    let options = ({ headers: headers });

    let data = {
     // email: this.email
     id: this.id
  };

  let loader = this.loadingCtrl.create({
    message: 'Processing please wait...',
    });    

  (await loader).present().then(() => {
  this.http.post('http://localhost/project/api/config/retrieveuser.php',data)
  .subscribe(async res => {
    console.log(res);
  (await loader).dismiss()
     
    this.users=res
    
    console.log(this.users);
    });
    });


  (await loader).present().then(() => {
    this.http.post('http://localhost/project/api/config/retrieverecomS.php',data)
    .subscribe(async res => {
      console.log(res);
    (await loader).dismiss()
        
      this.recomsS=res
      
      console.log(this.recomsS);
      });
      });

  (await loader).present().then(() => {
    this.http.post('http://localhost/project/api/config/retrieverecomW.php',data)
    .subscribe(async res => {
      console.log(res);
    (await loader).dismiss()
        
      this.recomsW=res
      
      console.log(this.recomsW);
      });
      });

  (await loader).present().then(() => {
    this.http.post('http://localhost/project/api/config/retrievemsg.php',data)
    .subscribe(async res => {
      console.log(res);
    (await loader).dismiss()
        
      this.msgs=res
      
      console.log(this.msgs);
      });
      });


}


nextpage() {
  this.navCtrl.navigateRoot(['/tabs/tab3']);
}

}