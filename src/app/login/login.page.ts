import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  constructor(private router: Router) { }

  ngOnInit() {
  }

  // login(){
  //   this.router.navigate(['tabs']);
  // }

  async login(){
    //you can use either of below
    this.router.navigateByUrl('tabs/tab1');
    //this.navCtrl.navigateRoot('/app/tabs/(home:home)')
  }

  register(){
    this.router.navigate(['register']);
  }

}
