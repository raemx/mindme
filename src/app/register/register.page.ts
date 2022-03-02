import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {

  constructor() { }

  ngOnInit() {
  }

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

}
