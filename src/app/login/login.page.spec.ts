import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { AppRoutingModule } from 'src/app/app-routing.module';
import { LoginPage } from './login.page';

describe('LoginPage', () => {
  let component: LoginPage;
  let fixture: ComponentFixture<LoginPage>;
  let router: Router;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ LoginPage ],
      imports: [
        IonicModule.forRoot(), 
        AppRoutingModule
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(LoginPage);
    router = TestBed.get(Router);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  // it('should create', () => {
  //   expect(component).toBeTruthy();
  // });

  it('Home after Login', ()=>{ //simulate something is happening async
    spyOn(router, 'navigate') //test watches navigate function on router object
    component.login();
    expect(router.navigate).toHaveBeenCalledWith('tabs');//asks if function is called with parameter login
  })

  it('Register after Login', ()=>{ //simulate something is happening async
    spyOn(router, 'navigate') //test watches navigate function on router object
    component.register();

    expect(router.navigate).toHaveBeenCalledWith('register');//asks if function is called with parameter login
  })

});
