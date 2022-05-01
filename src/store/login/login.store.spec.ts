
import { loginReducer } from "./login.reducers"
import { recoverPassword, recoverPasswordSuccess, recoverPasswordFail } from "./login.actions"
import { LoginState } from "./LoginState"
import {AppInitialState} from "../AppInitialState";

describe("Login store", () => {

    it("recoverPassword", () => {
        const initialState: LoginState = AppInitialState.login;

        const newState = loginReducer(initialState, recoverPassword());
        expect(newState).toEqual({
            ...initialState,
            error: null, 
            isRecoveringPassword: true
        })
    })

    it("recoverPasswordSuccess", () => {
        const initialState: LoginState = AppInitialState.login;

        const newState = loginReducer(initialState, recoverPasswordSuccess());
        expect(newState).toEqual({
            ...initialState,
            error: null, 
            isRecoveredPassword: true,
            isRecoveringPassword: false,
        })
    })

    it("recoverPasswordFail", () => {
        const initialState: LoginState = AppInitialState.login;
        const error = {error: 'error'};
        const newState = loginReducer(initialState, recoverPasswordFail({error}));
        expect(newState).toEqual({
            ...initialState,
            error, 
            isRecoveredPassword: false,
            isRecoveringPassword: false,
        })
    })

})