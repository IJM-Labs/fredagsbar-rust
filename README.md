# Fredagsbarens event-system

Et simpelt event-system udviklet som obligatorisk opgave på Python Elective.

Systemet består af en Flask API og en Streamlit-frontend. Brugere kan se fredagsbarens events, oprette nye events samt tilmelde og afmelde deltagere.

## Funktioner

- Vis alle events og deres dato
- Vis antal tilmeldte og ledige pladser
- Opret nye events
- Tilmeld en person til et event
- Afmeld en person fra et event
- Forhindr dobbelttilmeldinger
- Forhindr tilmeldinger, når et event er fuldt
- Vis tydelige fejl ved forbindelsesfejl, timeout og ugyldige requests

## Teknologier

- Python 3.12
- Flask
- Streamlit
- httpx
- uv
- Docker
- Docker Compose

## Projektstruktur

```text
fredagsbar/
├── api.py
├── app.py
├── swagger.json
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Start systemet med Docker

Docker Desktop skal være installeret og startet.

Kør følgende kommando fra projektets rodmappe:

```bash
docker compose up --build
```

Når begge services er startet, kan de åbnes her:

- Streamlit-frontend: http://localhost:8501
- Flask API: http://localhost:5001
- Alle events: http://localhost:5001/events

Stop systemet med `Ctrl+C`, og fjern containerne med:

```bash
docker compose down
```

## Start systemet lokalt

Installer først projektets dependencies:

```bash
uv sync
```

Start API'en i den første terminal:

```bash
uv run python api.py
```

Start frontenden i en anden terminal:

```bash
uv run streamlit run app.py
```

Åbn derefter frontenden på:

```text
http://localhost:8501
```

API'en kører lokalt på:

```text
http://localhost:5001
```

## API-endpoints

| Metode | Endpoint | Beskrivelse |
|---|---|---|
| `GET` | `/events` | Hent alle events |
| `GET` | `/events/<id>` | Hent ét event |
| `POST` | `/events` | Opret et nyt event |
| `POST` | `/events/<id>/signups` | Tilmeld en person |
| `DELETE` | `/events/<id>/signups/<name>` | Afmeld en person |
| `DELETE` | `/events/<id>` | Slet et event |

### Eksempel på et event

```json
{
  "id": 1,
  "title": "Quizaften",
  "date": "2026-11-15",
  "capacity": 3,
  "participants": ["osman", "jeppe"]
}
```

### Eksempel på en tilmelding

Send en `POST`-request til:

```text
/events/1/signups
```

med følgende JSON:

```json
{
  "name": "Anna"
}
```

## Statuskoder

API'en anvender følgende statuskoder:

| Statuskode | Betydning |
|---|---|
| `200` | Requesten lykkedes |
| `201` | Et event eller en tilmelding blev oprettet |
| `204` | Et event eller en tilmelding blev slettet |
| `400` | Requesten indeholder ugyldige eller manglende oplysninger |
| `404` | Eventet eller tilmeldingen findes ikke |
| `409` | Eventet er fuldt, eller personen er allerede tilmeldt |

## API-dokumentation

Alle endpoints, request bodies og fejlsvar er dokumenteret i:

```text
swagger.json
```

Filen kan åbnes i [Swagger Editor](https://editor.swagger.io/).

## Fejlhåndtering

Streamlit-frontenden viser en tydelig fejlbesked, hvis:

- Flask API'en ikke kører
- API'en svarer for langsomt
- API'en returnerer statuskode `400`, `404` eller `409`

Brugeren får derfor ikke vist en Python-stack trace i browseren.

## Opbevaring af data

Events og deltagere gemmes i en Python-liste i hukommelsen. Data, som oprettes under kørsel, bliver derfor nulstillet, når API'en eller Docker-containeren genstartes.