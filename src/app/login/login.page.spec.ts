import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { IonicModule, ToastController } from '@ionic/angular';
import { Store, StoreModule } from '@ngrx/store';
import { AppRoutingModule } from 'src/app/app-routing.module';
import { loginReducer } from 'src/store/login/login.reducers';
import { loadingReducer } from 'src/store/loading/loading.reducers';
import { LoginPage } from './login.page';
import { AppState } from 'src/store/AppState';
import { AuthService } from '../services/auth/auth.service';
import { User } from '../model/user/User';
import { toastController } from '@ionic/core';
import { throwError } from 'rxjs/internal/observable/throwError';
import { LoadingState } from "src/store/loading/LoadingState";
import { LoginState } from "src/store/login/LoginState";
import { of } from 'rxjs/internal/observable/of';
import { recoverPassword, recoverPasswordFail, recoverPasswordSuccess } from 'src/store/login/login.actions';

describe('LoginPage', () => {
  let component: LoginPage;
  let fixture: ComponentFixture<LoginPage>;
  let router: Router;
  let page: any;
  let store: Store<AppState>;
  let toastController: ToastController;
  let authService: AuthService;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ LoginPage ],
      imports: [
        IonicModule.forRoot(), 
        AppRoutingModule,
        //ReactiveFormsModule,
        //StoreModule.forRoot([]),
        //StoreModule.forFeature("loading", loadingReducer),
        //StoreModule.forFeature("login", loginReducer)
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(LoginPage);
    router = TestBed.inject(Router);
    // store = TestBed.inject(Store);
    // toastController = TestBed.inject(ToastController);
    component = fixture.componentInstance;
    // page = fixture.debugElement.nativeElement;
    // authService = TestBed.inject(AuthService);
    fixture.detectChanges();
  }));

  // it('should create', () => {
  //   expect(component).toBeTruthy();
  // });

  // it('Create Form on Init', ()=>{ //simulate something is happening async
  //   component.ngOnInit();
  //   expect(component.form).not.toBeUndefined();
  // })

  // it('Home after Login', ()=>{ //simulate something is happening async
  //   spyOn(router, 'navigate') //test watches navigate function on router object
  //   component.login();
  //   expect(router.navigate).toHaveBeenCalledWith('tabs');//asks if function is called with parameter login
  // })

  // it('Register after Login', ()=>{ //simulate something is happening async
  //   spyOn(router, 'navigate') //test watches navigate function on router object
  //   component.register();

  //   expect(router.navigate).toHaveBeenCalledWith('register');//asks if function is called with parameter login
  // })

  // it('Recover Email on Forgot button', ()=>{ //simulate something is happening async
  //  fixture.detectChanges();
  //  component.form.get('email').setValue("valid@email.com");
  //  page.querySelector("#recoverPasswordButton").click();
  //  store.select('login').subscribe(loginState => {
  //    expect(loginState.isRecoveringPassword).toBeTruthy();
  //  })
  // })

  // it('show loading when recovering password', () => {
  //   fixture.detectChanges();
  //   store.dispatch(recoverPassword());
  //   store.select('loading').subscribe(loadingState => {
  //     expect(loadingState.show).toBeTruthy();
  //   })
  // })

  // it('Hide Load Show Success when Recovered', () => {
  //   spyOn(toastController, 'create');
  //   fixture.detectChanges();
  //   store.dispatch(recoverPassword());
  //   store.dispatch(recoverPasswordSuccess());
  //   store.select('loading').subscribe(loadingState => {
  //     expect(loadingState.show).toBeFalsy();
  //   })
  //   expect(toastController.create).toHaveBeenCalledTimes(1);
  // })

  // it('Hide Load Show Error Msg when trying Recover', () => {
  //   spyOn(toastController, 'create');
  //   fixture.detectChanges();
  //   store.dispatch(recoverPassword());
  //   store.dispatch(recoverPasswordFail({error: "message"}));
  //   store.select('loading').subscribe(loadingState => {
  //     expect(loadingState.show).toBeFalsy();
  //   })
  //   expect(toastController.create).toHaveBeenCalledTimes(1);
  // })

  // it('Hide Load then Start Login once Logging in', () => {
  //   spyOn(router, 'navigate');
  //   spyOn(authService, 'login').and.returnValue(of(new User()));
    
  //   fixture.detectChanges();
  //   component.form.get('email').setValue('valid@gmail.com');
  //   component.form.get('password').setValue('anyPassword');
  //   page.querySelector('#loginButton').click();
  //   store.select('loading').subscribe(loadingState => {
  //       expect(loadingState.show).toBeFalsy();
  //   })
  //   store.select('login').subscribe(loginState =>{
  //       expect(loginState.isLoggedIn).toBeTruthy();
  //   })
  //   expect(router.navigate).toHaveBeenCalledWith(['tab1'])
  // })

  // it('Hide Load then Show Error as User cannot Login', () => {
  //   spyOn(authService, 'login').and.returnValue(throwError({message: 'error'}));
  //   spyOn(toastController, 'create').and.returnValue(<any> Promise.resolve({present: () => {}}));
  //   fixture.detectChanges();
  //   component.form.get('email').setValue('error@gmail.com');
  //   component.form.get('password').setValue('anyPassword');
  //   page.querySelector('#loginButton').click();
  //   store.select('loading').subscribe(loadingState => {
  //       expect(loadingState.show).toBeFalsy();
  //   })
  //   expect(toastController.create).toHaveBeenCalledTimes(1);
  // })

});
