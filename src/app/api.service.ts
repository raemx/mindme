import { Injectable } from '@angular/core';


import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class ApiService {
  headers: HttpHeaders;
  //public key='27fc1238cd6c4c26b36cfb0d3c6ca863'
  
  constructor(public http: HttpClient, private httpclient: HttpClient) { 
  this.headers = new HttpHeaders();
  this.headers.append("Accept", "application/json");
  this.headers.append("Content-Type", "application/json");
  this.headers.append("Access-Control-Allow-Origin", "*");
 
}

  addUser(data){
    return this.http.post('http://localhost/project/api/config/postuser.php', data);
  }

  addMood(data){
    return this.http.post('http://localhost/project/api/config/postmood.php', data);
  }

  addCmt(data){
    return this.http.post('http://localhost/project/api/config/postcmt.php', data);
  }

  getCmt(){
    return this.http.get('http://localhost/project/api/config/getcmt.php');
  }

  getUser(data){
    return this.http.get('http://localhost/project/api/config/retrieveuser.php', data);
  }

  login(){
    return this.http.get('http://localhost/project/api/config/checklogin.php');
  }
}
