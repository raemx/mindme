import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';


export enum Type {
  all = '',
  rec  = 'rec',
  type = 'type'
}

@Injectable({
  providedIn: 'root'
})
export class Tab1Service {
  url = 'https://api.nhs.uk/mental-health/self-help/';
  apiKey = '27fc1238cd6c4c26b36cfb0d3c6ca863';

  constructor(private http: HttpClient) { }

  searchData(){

  }

  getRecom(){
    
  }
}
