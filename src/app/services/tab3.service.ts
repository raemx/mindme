
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {map } from 'rxjs/operators';

import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';


export enum SearchType {
  all = '',
  topicId = ''
}
 
@Injectable({
  providedIn: 'root'
})
export class Tab3Service {
  headers: HttpHeaders;
  url = 'http://health.gov/myhealthfinder/api/v3/';
  apiKey = '8baec6d685fb4d3aa803c6de9194a057';
 
    constructor(public http: HttpClient, private httpclient: HttpClient) { 
  // this.headers = new HttpHeaders();
  // this.headers.append("Accept", "application/json");
  // this.headers.append("Content-Type", "application/json");
  // this.headers.append("Access-Control-Allow-Origin", "*");
  }
  /**
   *
   * Constructor of the Service with Dependency Injection
   * @param http The standard Angular HttpClient to make requests
   */

 
  /**
  * Get data from the OmdbApi 
  * map the result to return only the results that we need
  * 
  * @param {string} title Search Term
  * @param {SearchType} type
  * @returns Observable with the search results
  * https://health.gov/myhealthfinder/api/v3/topicsearch.json?TopicId=527
  * https://health.gov/myhealthfinder/api/v3/myhealthfinder.json?age=35&sex=female&pregnant=no&sexuallyActive=yes&tobaccoUse=no
  */
  

  searchData(title: string, type: SearchType): Observable<any> {
        return this.http.get(`${this.url}topicsearch.json?${type}=${encodeURI(title)}`).pipe(
      map(results => results['Search'])
    );
  }
 
  /**
  * Get the detailed information for an ID using the "i" parameter
  * 
  * @param {string} TopicId imdbID to retrieve information
  * @returns Observable with detailed information
  */
  getDetails(TopicId) {
    return this.http.get(`${this.url}?i=${TopicId}`);
  }
}


