import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PostProvider } from 'src/providers/post-provider';
import { ToastController } from '@ionic/angular';

import { ApiService } from '../api.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {
  name: any;
  name2: any;
  email: any;
  password: any;
  no: any;
  line1: any;
  line2: any;
  city: any;
  town: any;
  postcode: any;


  
  constructor(
    private router: Router, 
    private postPvdr: PostProvider, 
    public toastCtrl: ToastController, 
    public apiservice: ApiService) { }

  ngOnInit() {
  }

  addUser(){
    
    let data = {
    name: this.name, 
    name2: this.name2,
    email: this.email,
    password: this.password,
    line1: this.line1,
    line2: this.line2,
    no: this.no,
    city: this.city,
    town: this.town, 
    postcode: this.postcode
    }
    
    this.apiservice.addUser(data).subscribe((res:any)=> {
      this.name = "";
      this.name2 = "";
      this.email = "";
      this.password = "";
      this.line1 = "";
      this.line2 = "";
      this.no = "";
      this.city = "";
      this.town = "";
      this.postcode = "";
      console.log("SUCCESS===",res);
    },(error: any) =>{
      console.log("ERROR ===",error);
    })
  }
}
  // async register(){
  //   if(this.email=""){
  //     const toast = await this.toastCtrl.create({
  //       message: 'Email required',
  //       duration: 2000
  //     });
  //     toast.present();
  //   }else if (this.password=""){
  //     const toast = await this.toastCtrl.create({
  //       message: 'Password required',
  //       duration: 2000
  //     });
  //     toast.present();
  //   }else {
  //     let body = {
  //     name: this.name,
  //     name2: this.name2,
  //     email: this.email,
  //     password: this.password,
  //     no: this.no,
  //     line1: this.line1,
  //     line2: this.line2,
  //     city: this.city,
  //     town: this.town,
  //     postcode: this.postcode,
  //     aski: 'register'
  //   };
  //     this.postPvdr.postData(body, 'process_api.php').subscribe(async data =>{
  //       var alertmsg = data.msg;
  //       if(data.success){
  //         this.router.navigate(['/login']);
  //         const toast = await this.toastCtrl.create({
  //           message: 'Register Successful',
  //           duration: 2000
  //         });
  //         toast.present();
  //       }else{
  //         const toast = await this.toastCtrl.create({
  //           message: alertmsg,
  //           duration: 2000
  //         });
  //       }
  //     });
  //   }
  //   }
  // }

//   register(name, name2, email, password, no, line1, line2, city, town, postcode)
// {
//     var link  = "../php/register.php";
//     var body = JSON.stringify({name: name, name2: name2, email: email, password: password, no: no, line1: line1, line2: line2, city: city, town: town, postcode: postcode});

//     alert("DATA: "+body);

//     this.http.post(link, body)
//     .subscribe(data => {
//          console.log("DATA:", data);
//     },
//          err => {
//          console.log("ERROR!: ", err);
//          alert(err);
//     });
// }
