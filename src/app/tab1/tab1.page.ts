import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from "@angular/core";
import { Chart } from "chart.js";
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Papa} from "ngx-papaparse";
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { NavController } from '@ionic/angular';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss'],

  // template: `
  //   <form [formGroup]="todo" (ngSubmit)="logForm()">
  //     <ion-item>
  //       <ion-label>Todo</ion-label>
  //       <ion-input type="text" formControlName="title"></ion-input>
  //     </ion-item>
  //     <ion-item>
  //       <ion-label>Description</ion-label>
  //       <ion-textarea formControlName="description"></ion-textarea>
  //     </ion-item>
  //     <button ion-button type="submit" [disabled]="!todo.valid">Submit</button>
  //   </form>`
})

export class Tab1Page implements OnInit {

  //data = '...csv';

  @ViewChild("barCanvas", {static: true}) barCanvas: ElementRef;
  @ViewChild("doughnutCanvas",  {static: true}) doughnutCanvas: ElementRef;
  @ViewChild("lineCanvas", {static: true}) lineCanvas: ElementRef;

  private barChart: Chart;
  private doughnutChart: Chart;
  private lineChart: Chart;

   /**
    * @name items
    * @type {Array} 
    * @public
    * @description     Used to store returned PHP data
    */
    public items : Array<any> = [];



    constructor(public navCtrl: NavController, 
                public http   : HttpClient) 
    {
 
    }
  
 
    /**
     * Triggered when template view is about to be entered
     * Returns and parses the PHP data through the mood() method
     *
     * @public
     * @method ionViewWillEnter 
     * @return {None}
     */
    ionViewWillEnter() : void
    {
       this.mood();
    }
 
 
 
 
    /**
     * Retrieve the JSON encoded data from the remote server
     * Using Angular's Http class and an Observable - then
     * assign this to the items array for rendering to the HTML template
     *
     * @public
     * @method mood 
     * @return {None}
     */
    mood() : void
    {
       this.http
       .get('http://localhost:8100/tabs/mood.php')
       .subscribe((data : any) => 
       {
          console.dir(data);
          this.items = data;			
       },
       (error : any) =>
       {
          console.dir(error);
       });
    }
 
 
 
 
    /**
     * Allow navigation to the Tab1Page for creating a new entry
     *
     * @public
     * @method addEntry 
     * @return {None}
     */
    addEntry() : void
    {
       this.navCtrl.navigateForward('Tab1Page');
    }
 
 
 
    
    /**
     * Allow navigation to the AddTechnologyPage for amending an existing entry
     * (We supply the actual record to be amended, as this method's parameter, 
     * to the AddTechnologyPage
     *
     * @public
     * @method viewEntry
     * @param param 		{any} 			Navigation data to send to the next page 
     * @return {None}
     */
    viewEntry(param : any) : void
    {
       this.navCtrl.navigateForward('Tab1Page', param);
    }
 

  ngOnInit() {

    this.barChart = new Chart(this.barCanvas.nativeElement, {
      type: "bar",
      data: {
        labels:  ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        datasets: [
          {
            label: "# of Votes",
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)"
            ],
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)"
            ],
            borderWidth: 1
          }
        ]
      },
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              }
            }
          ]
        }
      }
    });
    // this.doughnutChart = new Chart(this.doughnutCanvas.nativeElement, {
    //   type: "doughnut",
    //   data: {
    //     labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    //     datasets: [
    //       {
    //         label: "# of Votes",
    //         data: [12, 19, 3, 5, 2, 3],
    //         backgroundColor: [
    //           "rgba(255, 99, 132, 0.2)",
    //           "rgba(54, 162, 235, 0.2)",
    //           "rgba(255, 206, 86, 0.2)",
    //           "rgba(75, 192, 192, 0.2)",
    //           "rgba(153, 102, 255, 0.2)",
    //           "rgba(255, 159, 64, 0.2)"
    //         ],
    //         hoverBackgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#FF6384", "#36A2EB", "#FFCE56"]
    //       }
    //     ]
    //   }
    // });
    this.lineChart = new Chart(this.lineCanvas.nativeElement, {
      type: "line",
      data: {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [
          {
            label: "My First dataset",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: "butt",
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: "miter",
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: [65, 59, 80, 81, 56, 55, 40],
            spanGaps: false
          }
        ]
      }
    });

  }
}