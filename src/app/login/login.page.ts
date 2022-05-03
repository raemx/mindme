import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AlertController, ToastController, LoadingController, NavController  } from '@ionic/angular';
import { Store } from '@ngrx/store';
import { AppState } from 'src/store/AppState';
import { AuthService } from 'src/app/services/auth/auth.service';
import { ApiService } from '../api.service';
import {HttpClient, HttpHeaders}  from "@angular/common/http";
import { RouterOutlet,  ActivationStart } from '@angular/router';
import { Tab1Page } from '../tab1/tab1.page';
import { RegisterPage } from '../register/register.page';




@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage { // Oninit, OnDestroy

  data:string;
  users:any;    
  @ViewChild("email") email: { value: string; };
  @ViewChild("password") password: { value: string; };
  @ViewChild(RouterOutlet) outlet: RouterOutlet;

  constructor(private router: Router, 

    private store: Store<AppState>,
    private toastCtrl: ToastController, 
    private authService: AuthService,
    private apiService: ApiService,
    private alertCtrl: AlertController,
    private loadingCtrl: LoadingController,
    private http: HttpClient,
    private navCtrl: NavController
    ) { }


  ngOnInit() {
    // this.form = new LoginPageForm(this.formBuilder).createForm();

    // this.loginStateSubscription = this.store.select('login').subscribe(loginState => {
    //   this.onIsRecoverPassword(loginState);
    //   this.onIsRecoveringPassword(loginState);
    //   this.onError(loginState);
    //   this.onIsLoggedIn(loginState);
    //   this.onIsLoggingIn(loginState);
    //   this.toggleLoading(loginState);
    //   })

    
    this.router.events.subscribe(e => {
      if (e instanceof ActivationStart && e.snapshot.outlet === "administration")
        this.outlet.deactivate();
    });
  }

  register(){
    this.router.navigate(['/register']);
  }

  async login(){
     //this.router.navigate(['/tabs']);

     if(this.email.value=="" ){

      let alert = this.alertCtrl.create({
     
      header:"ATTENTION",
      message:"Email required",
      buttons: ['OK']
      });
     
      (await alert).present();
       } else
     
      if(this.password.value==""){
     
      let alert = this.alertCtrl.create({
     
        header: "ATTENTION",
        message:"Password field is empty",
        buttons: ['OK']
      });
     
      (await alert).present();
           
     }
      else
      {
     
       var headers = new Headers();
         headers.append("Accept", 'application/json');
         headers.append('Content-Type', 'application/json' );
         let options = {headers: headers}
     
     
           let data = {
             email: this.email.value,
             password: this.password.value
           };
     
           
     
      let loader = this.loadingCtrl.create({
         message: 'Processing please wait...'
       });
     
      (await loader).present().then(() => {
     
     
       this.http.post('http://localhost/project/api/config/checklogin.php',data)
       .subscribe(async res => {
       console.log(res)
        ;(await loader).dismiss()

       if(res=="Login Success"){
  
           this.navCtrl.navigateRoot(['/tabs/tab1']);
       }else
       {
        let alert = this.alertCtrl.create({
        header:"Unsuccessful",
        message:"Your email or password is invalid",
        buttons: ['OK']
        });
       
        (await alert).present();
         } 
       });
       });
        }
       
       }

  // async onsubmit(){
  //   const loading = await this.loadingCtrl.create({message: 'Logging In ...'})
  //   await loading.present();

  //   this.apiService.login(this.form.value).subscribe(
  //     async token => {
  //       localStorage.setItem('token', token);
  //       loading.dismiss();
  //       this.router.navigateByUrl('/create');
  //     },
  //     async () => {
  //       const alert = await this.alertCtrl.create({message: 'Logging In Failed...', buttons:['OK']});
  //       await alert.present();
  //       loading.dismiss();
  //     }
  //   );
  // }
//   ngOnDestroy(){
//     if (this.loginStateSubscription){
//       this.loginStateSubscription.unsubscribe();
//     }
//   }

  

//   private toggleLoading(loginState: LoginState){
//     if (loginState.isLoggedIn || loginState.isRecoveringPassword){
//       this.store.dispatch(show());
//     }
//     else {
//       this.store.dispatch(hide());
//     }


//   }

//   private onIsLoggedIn(loginState: LoginState){
//     if (loginState.isLoggedIn){
//       this.router.navigate(['tab1']);
//     }
//   }
  
//   private onIsLoggingIn(loginState: LoginState){
//     if (loginState.isLoggingIn){
//       const email = this.form.get('email').value;
//       const password = this.form.get('password').value;
//       this.authService.login(email, password).subscribe(user =>{
//         this.store.dispatch(loginSuccess({user}));
//       }, error =>{
//         this.store.dispatch(loginFail({error}));
//       })
//     }
//   }

  // login(){
  //   this.router.navigate(['/app/tabs/tab1:tab1']);
  // }
//   login(){
//     //you can use either of below
//     //this.router.navigateByUrl('/app/tabs/tab1:tab1')
//     // this.store.dispatch(login()); 
//     this.router.navigate(['tabs']);
//   }

//   register(){
//     this.router.navigate(['register']);
//   }


//   private async onError(loginState: LoginState){
//     if (loginState.error){

//       const toaster = await this.toastController.create({
//         position: "bottom",
//         message: loginState.error.message,
//         color: "danger"
//       });
//       toaster.present();
//     }
//   }

//   private async onIsRecoveringPassword(loginState: LoginState){
//     if (loginState.isRecoveringPassword){

//       this.authService.recoverEmailPassword(this.form.get('email').value).subscribe(() => {
//         this.store.dispatch(recoverPasswordSuccess());
//       }, error=>{
//         this.store.dispatch(recoverPasswordFail({error}))
//       });
//     }
//   }

//   private async onIsRecoverPassword(loginState: LoginState){
//     if (loginState.isRecoveredPassword){
//       const toaster = await this.toastController.create({
//         position: "bottom",
//         message: "Recovery email sent",
//         color: "primary"
//       });
//       toaster.present();
//     }
//   }

//   forgotEmailPassword(){
//     this.store.dispatch(recoverPassword());
//   }

}

