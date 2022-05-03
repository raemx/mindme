
import { Tab3Service, SearchType } from './../services/tab3.service';
import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
 

@Component({
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss']
})
export class Tab3Page implements OnInit {

  results: Observable<any>;
  searchTerm: string = '';
  type: SearchType = SearchType.all;

  constructor(private tab3service: Tab3Service) { }
 
  ngOnInit() { }
 
  searchChanged() {
    // Call our service function which returns an Observable
    this.results = this.tab3service.searchData(this.searchTerm, this.type);
  }

  
}
