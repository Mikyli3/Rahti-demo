from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from db import get_db_connection
from init_db import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/rooms")
def get_rooms():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, room_number, type, price
        FROM hotel_rooms
        ORDER BY room_number;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "room_number": row[1],
            "type": row[2],
            "price": float(row[3])
        }
        for row in rows
    ]


@app.get("/api/ip")
def get_ip(request: Request):
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host
    return {"ip": ip}


@app.get("/ip", response_class=HTMLResponse)
def get_ip_html(request: Request):
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host
    return f"<h1>Din publika IP-adress är {ip}</h1>"