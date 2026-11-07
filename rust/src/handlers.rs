use std::sync::Arc;

use axum::{extract::State,Json};

use crate::model::Event;
use crate::state::AppState;


pub async fn get_events(State(state): State<Arc<AppState>>, 
)-> Json<Vec<Event>>{
    Json(state.events.clone())
}

//async fn: En funktion, der kan indgå i serverens asynkrone arbejde.
//State(state): Axum giver funktionen adgang til applikationens data via variablen state.
//Arc<AppState>: Flere forespørgsler kan dele den samme AppState. Det giver ikke i sig selv mulighed for at ændre data.
//Json<Vec<Event>>: Funktionen returnerer en liste af events som JSON.
//.clone(): Kopierer listen til svaret.