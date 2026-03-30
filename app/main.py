from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms = [
    {
        "room_number": 55,
        "type": "single",
        "price": 50,
        "available": True
    },
    {
        "room_number": 997,
        "type": "double",
        "price": 130,
        "available": True
    },
    {
        "room_number": 501,
        "type": "suite",
        "price": 450,
        "available": False
    }
]

@app.get("/rooms")
def get_rooms():
    return rooms



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