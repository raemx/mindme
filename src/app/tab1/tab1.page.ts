import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from "@angular/core";
import { Chart } from "chart.js";
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Papa} from "ngx-papaparse";

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
  // private todo : FormGroup;

  // constructor( private formBuilder: FormBuilder ) {
  //   this.todo = this.formBuilder.group({
  //     title: ['', Validators.required],
  //     description: [''],
  // });
  // }
  // logForm(){
  //   console.log(this.todo.value)
  // }
  
  constructor(private papa: Papa) {
    const csvData = "../csv/sleep.csv"
    
    this.papa.parse(csvData,{
        complete: (result) => {
            console.log('Parsed: ', result);
        }
    });
}

  ngOnInit() {

    this.barChart = new Chart(this.barCanvas.nativeElement, {
      type: "bar",
      data: {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
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
    this.doughnutChart = new Chart(this.doughnutCanvas.nativeElement, {
      type: "doughnut",
      data: {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
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
            hoverBackgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#FF6384", "#36A2EB", "#FFCE56"]
          }
        ]
      }
    });
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

  // mood(emot)
  // {
  //     var link  = "../php/tab1.php";
  //     var body = JSON.stringify({emot: emot});
  
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

uploadData(files: FileList){
    console.log(files);
    if(files && files.length > 0) {
       let file : File = files.item(0); 
         console.log(file.name);
         console.log(file.size);
         console.log(file.type);
         let reader: FileReader = new FileReader();
         reader.readAsText(file);
         reader.onload = (e) => {
            let csv: string = reader.result as string;
            console.log(csv);
         }
      }
  }

}