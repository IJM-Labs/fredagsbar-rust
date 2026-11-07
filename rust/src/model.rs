use serde::Serialize;

//Serialize gør det muligt at omdanne et event til eksempelvis JSON.
//Clone gør det muligt at lave en kopi af et event. Det bruger vi, når vores første handler skal returnere listen.

#[derive(Serialize, Clone)]
pub struct Event {
    pub id: i32,
    pub title: String,
    pub date: String,
    pub capacity: usize,
    pub participants: Vec<String>,
}