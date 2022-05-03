import { Injectable} from "@angular/core";
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { map } from 'rxjs/operators';

@Injectable()
export class PostProvider {
    server: string = "http://localhost/mindme/api";

    constructor(public http: HttpClient) {

    }

    postData(body, file){
        let type = "application/json; charset-UTF-8";
        let headers = new HttpHeaders({'Content-Type': type});
        let options = {headers: headers}

        return this.http.post(this.server + file, JSON.stringify(body), options).pipe(map((res: any) => res.json()));
    // }
    }
}