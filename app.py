import os
from urllib.parse import quote

import httpx
import streamlit as st


# KONFIGURATION
st.set_page_config(
    page_title="Fredagsbarens events",)

# Lokalt bruger API'en port 5001.
# I Docker ændres API_URL med en miljøvariabel.
API_URL = os.environ.get(
    "API_URL",
    "http://127.0.0.1:5001",
)


# HJÆLPEFUNKTION TIL API-KALD
def api_request(method, path, **kwargs):
    """Sender et HTTP-kald til Flask-API'en."""

    try:
        response = httpx.request(
            method=method,
            url=f"{API_URL}{path}",
            timeout=2.0,
            **kwargs,
        )

        # Opretter en HTTPStatusError ved fx 400, 404 og 409.
        response.raise_for_status()

        return response

    except httpx.ConnectError:
        st.error(
            "API'en kører ikke. Start Flask-serveren "
            "og prøv igen."
        )

    except httpx.TimeoutException:
        st.error(
            "API'en svarer for langsomt. Prøv igen senere."
        )

    except httpx.HTTPStatusError as error:
        try:
            error_data = error.response.json()
            error_message = error_data.get(
                "error",
                "Ukendt API-fejl",
            )
        except (ValueError, AttributeError):
            error_message = "API'en returnerede et ugyldigt svar."

        st.error(
            f"API-fejl {error.response.status_code}: "
            f"{error_message}"
        )

    except httpx.RequestError:
        st.error(
            "Der opstod en netværksfejl under forbindelsen "
            "til API'en."
        )

    return None



# SIDEHOVED OG SESSION STATE
st.title("Fredagsbarens events")

# Gemmer brugerens navn mellem Streamlit-reruns.
if "name" not in st.session_state:
    st.session_state.name = ""

# Vis en gemt succesbesked efter st.rerun().
if "success_message" in st.session_state:
    st.success(
        st.session_state.pop("success_message")
    )

st.sidebar.header("Bruger")

st.sidebar.text_input(
    "Indtast dit navn",
    key="name",
    placeholder="Indtast dit navn",
)

current_name = st.session_state.name.strip()



# HENT EVENTS FRA API'EN
events_response = api_request(
    method="GET",
    path="/events",
)

if events_response is None:
    st.stop()

try:
    events = events_response.json()
except ValueError:
    st.error("API'en returnerede ikke gyldig JSON.")
    st.stop()

if not isinstance(events, list):
    st.error("API'en returnerede ikke en liste af events.")
    st.stop()



# OVERSIGT OVER EVENTS
st.header("Oversigt over events")

event_overview = []

for event in events:
    number_of_participants = len(
        event.get("participants", [])
    )

    available_spots = (
        event.get("capacity", 0)
        - number_of_participants
    )

    event_overview.append(
        {
            "Titel": event.get("title"),
            "Dato": event.get("date"),
            "Tilmeldte": number_of_participants,
            "Pladser tilbage": available_spots,
        }
    )

# Dette skal stå efter for-løkken.
if event_overview:
    st.dataframe(
        event_overview,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Der er ingen events at vise endnu.")



# TILMELDING OG AFMELDING
st.header("Tilmelding og afmelding")

if events:
    selected_event = st.selectbox(
        "Vælg et event",
        options=events,
        format_func=lambda event: (
            f"{event.get('title')} - "
            f"{event.get('date')}"
        ),
    )

    participants = selected_event.get(
        "participants",
        [],
    )

    capacity = selected_event.get("capacity", 0)
    event_id = selected_event.get("id")

    number_of_participants = len(participants)
    available_spots = capacity - number_of_participants
    event_is_full = number_of_participants >= capacity

    st.write(
        f"**Pladser:** {number_of_participants} "
        f"ud af {capacity}"
    )

    st.write(
        f"**Ledige pladser:** {available_spots}"
    )

    if participants:
        st.write("**Deltagere:**")

        for participant in participants:
            st.write(f"- {participant}")
    else:
        st.info("Ingen er tilmeldt endnu.")

    signup_column, cancel_column = st.columns(2)

    # Tilmeldingsknap
    with signup_column:
        signup_clicked = st.button(
            "Tilmeld",
            disabled=event_is_full,
            use_container_width=True,
        )

        if signup_clicked:
            if not current_name:
                st.error(
                    "Skriv dit navn i sidebaren først."
                )
            else:
                signup_response = api_request(
                    method="POST",
                    path=f"/events/{event_id}/signups",
                    json={
                        "name": current_name,
                    },
                )

                if signup_response is not None:
                    st.session_state.success_message = (
                        f"{current_name} er nu tilmeldt "
                        f"{selected_event.get('title')}."
                    )

                    st.rerun()

    # Afmeldingsknap
    with cancel_column:
        cancel_clicked = st.button(
            "Afmeld",
            use_container_width=True,
        )

        if cancel_clicked:
            if not current_name:
                st.error(
                    "Skriv dit navn i sidebaren først."
                )
            else:
                # Sikrer, at navnet kan bruges i en URL.
                encoded_name = quote(
                    current_name,
                    safe="",
                )

                cancel_response = api_request(
                    method="DELETE",
                    path=(
                        f"/events/{event_id}/signups/"
                        f"{encoded_name}"
                    ),
                )

                if cancel_response is not None:
                    st.session_state.success_message = (
                        f"{current_name} er blevet afmeldt "
                        f"{selected_event.get('title')}."
                    )

                    st.rerun()

else:
    st.info(
        "Opret et event, før du tilmelder deltagere."
    )



# OPRET EVENT
st.header("Opret et nyt event")

with st.form(
    "create_event_form",
    clear_on_submit=True,
):
    new_title = st.text_input("Titel")

    new_date = st.date_input("Dato")

    new_capacity = st.number_input(
        "Antal pladser",
        min_value=1,
        value=10,
        step=1,
    )

    create_clicked = st.form_submit_button(
        "Opret event"
    )

if create_clicked:
    if not new_title.strip():
        st.error("Du skal skrive en titel.")
    else:
        create_response = api_request(
            method="POST",
            path="/events",
            json={
                "title": new_title.strip(),
                "date": new_date.isoformat(),
                "capacity": int(new_capacity),
            },
        )

        if create_response is not None:
            st.session_state.success_message = (
                f"Eventet {new_title.strip()} blev oprettet."
            )

            st.rerun()