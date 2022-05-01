import { createAction } from "@ngrx/store";

export const show = createAction("[Loading] show");
export const hide = createAction("[Loading] hide");

//buttons click calls action
//action goes throgh reducer
//reducer handles action
//reducer returns state