import { StoreModule } from "@ngrx/store";
import { loginReducer } from "./login/login.reducers";
import { loadingReducer } from "./loading/loading.reducers";


export const AppStoreModule = [
    StoreModule.forRoot([]),
    StoreModule.forFeature("loading", loadingReducer),
    StoreModule.forFeature("login", loginReducer)
]