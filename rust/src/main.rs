mod model;
mod state;
mod handlers;

use model::Event;
use state::AppState;
use std::sync::Arc;
use axum:: {routing::get,Router};

#[tokio::main]
async fn main() {
    let app_state = AppState {
        events: vec![
            Event {
                id: 1,
                title: String::from("Quizaften"),
                date: String::from("2026-11-15"),
                capacity: 3,
                participants: vec![
                    String::from("Osman"),
                    String::from("Jeppe"),
                ],
            },
        ],
    };



let app = Router::new()
.route("/events", get(handlers::get_events))
.with_state(Arc::new(app_state));

let listener = tokio::net::TcpListener::bind("127.0.0.1:5001")
.await
.expect("Kunne ikke starte serveren på port 5001");

println!("Serveren kører på http://127.0.0.1:5001/events");

axum::serve(listener, app)
.await
.expect("Serveren stoppede med en fejl");

}

//Axum: Håndterer HTTP og endpoints.
//Tokio: Kører serverens asynkrone arbejde.
//Serde: Gør det muligt at omdanne dine Event-data til JSON.