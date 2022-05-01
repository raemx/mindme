import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { User } from "../../model/user/User";

@Injectable({
    providedIn: 'root'
})
export class AuthService{

    constructor() {}

    recoverEmailPassword(email: string) : Observable<void> {
        return new Observable<void>(observer => {
            setTimeout(() => {
                if (email == "error@gmail.com"){
                    observer.error({message: "Email not found"});
                }
                observer.next();
                observer.complete();
            }, 3000);
        })
    }
    
    login(email: string, password: string) : Observable<User>{ 
        return new Observable<User>(observer => {
            setTimeout(() => {
                if (email == "error@gmail.com"){
                    observer.error({message: "Email not found"});
                    observer.next();
                } else {
                    const user = new User;
                    user.email = email;
                    user.id = "userId";
                    observer.next(user);
                }
                observer.complete();
            }, 3000);
    })
}
}