
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



@Component({
  selector: 'app-tab4',
  templateUrl: './tab4.page.html',
  styleUrls: ['./tab4.page.scss'],
  providers: [NavParams, LocalNotifications, Push]
})
export class Tab4Page implements OnInit {
  discussionid: any;
  comment: any;
  discussions: any = [];
  users: any = [];
  data: any;
  email:any;
  id: any;
  
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
    private push: Push) { }

  async ngOnInit() {
    

    this.email = this.navParams.get('email');
    this.id = 1
    
    var headers = new Headers();
    headers.append("Accept", 'application/json');
    headers.append('Content-Type', 'application/json' );
    let options = ({ headers: headers });

    let data = {
     //email: this.email
     id: this.id
  };

  // let loader = this.loadingCtrl.create({
  //   message: 'Processing please wait...',
  //   });    

  // (await loader).present().then(() => {
  // this.http.post('http://localhost/project/api/config/retrievedis.php',data)
  // .subscribe(async res => {
  //   console.log(res);
  // (await loader).dismiss()
     
  //   this.discussions=res
    
  //   console.log(this.discussions);
  //   });
  //   });

   }
  addComment(){
    
    let data = {
    id: this.id, 
    discussionid: this.discussionid,
    comment: this.comment,

    }
    
    this.apiservice.addCmt(data).subscribe((res:any)=> {
      this.discussionid = "";
      this.comment = "";
      this.id = "";
      console.log("SUCCESS===",res);
    },(error: any) =>{
      console.log("ERROR ===",error);
    })
  }

  

}
