import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from "@angular/core";
import { HttpClientModule } from '@angular/common/http';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ApiService } from "../api.service";
import { Tab1Service, Type } from '../services/tab1.service';
import { Observable } from "rxjs";
import { PostProvider } from 'src/providers/post-provider';
import { IonicModule, ToastController } from '@ionic/angular';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import {  NavController, NavParams, LoadingController } from '@ionic/angular';
import { RouterOutlet,  ActivationStart } from '@angular/router';
import { Push, PushObject, PushOptions } from '@awesome-cordova-plugins/push/ngx';
import { LocalNotifications } from '@awesome-cordova-plugins/local-notifications/ngx';


//@IonicPage()
@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss'],
  providers: [NavParams, LocalNotifications, Push]

})

export class Tab1Page implements OnInit {
  emot: any;
  users: any = [];
  pyths: any = [];
  recoms: any = [];
  data: any;
  email:any;
  id: any;
  

  @ViewChild("barCanvas", {static: true}) barCanvas: ElementRef;
  @ViewChild(RouterOutlet) outlet: RouterOutlet;

  private barChart: Chart;


  constructor(public navCtrl: NavController, 
              public http   : HttpClient,
              private tab1Service: Tab1Service,
              private router: Router, 
              private postPvdr: PostProvider, 
              public toastCtrl: ToastController, 
              public apiservice: ApiService,
              private route: ActivatedRoute,
              public navParams: NavParams,
              public loadingCtrl: LoadingController,
              private localNotif: LocalNotifications,
              private push: Push
  ) 
  {
    //this.getUser();
    this.email = this.navParams.get('email');
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad Tab1Page');
  }


  async ngOnInit() {
   

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
      this.http.post('http://localhost/project/api/config/retrieverecom.php',data)
      .subscribe(async res => {
        console.log(res);
      (await loader).dismiss()
         
        this.recoms=res
        
        console.log(this.recoms);
        });
        });

        (await loader).present().then(() => {
          this.http.post('http://localhost/project/api/config/retrievepoints.php',data)
          .subscribe(async res => {
            console.log(res);
          (await loader).dismiss()
             
            this.pyths=res
            
            console.log(this.pyths);
            });
            });

   }

addMood(){
  
  let data = {
  emot: this.emot 
  }
  
  this.apiservice.addMood(data).subscribe((res:any)=> {
    this.emot = "";
    console.log("SUCCESS===",res);
    //this.getUser();
  },(error: any) =>{
    console.log("ERROR ===",error);
  })
}

nextpage() {
  this.navCtrl.navigateRoot(['/tabs/tab2']);
}



  // getUser(){
   
  //   this.apiservice.getUser().subscribe((res:any)=> {
  //     console.log("SUCCESS===",res);
  //     this.users = res;
  //   },(error: any) =>{
  //     console.log("ERROR ===",error);
  //   })
  // }

//   this.sub = this.route.params.subscribe(params => {
//     this.data = params['data']; 
// });


}