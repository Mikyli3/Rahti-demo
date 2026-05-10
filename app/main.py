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

@app.get("/bookings")
def get_bookings():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT b.id, r.room_number, b.datefrom, b.dateto, b.addinfo
        FROM hotel_bookings b
        JOIN hotel_rooms r ON b.room_id = r.id
        ORDER BY b.datefrom;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "room_number": row[1],
            "datefrom": str(row[2]),
            "dateto": str(row[3]),
            "addinfo": row[4]
        }
        for row in rows
    ]


@app.post("/bookings")
async def create_booking(request: Request):
    data = await request.json()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO hotel_bookings (guest_id, room_id, datefrom, dateto, addinfo)
        VALUES (1, %s, %s, %s, %s)
    """, (
        data["room_id"],
        data["date"],
        data["date"],
        data.get("addinfo", "")
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Booking saved"}

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

@app.get("/", response_class=HTMLResponse)
def hotel_frontend():
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Hotel Booking</h1>

        <label>Room:</label>
        <select id="roomSelect"></select>

        <br><br>

        <label>Date:</label>
        <input type="date" id="dateInput">

        <br><br>

        <label>Additional info:</label>
        <input type="text" id="infoInput">

        <br><br>

        <button onclick="saveBooking()">Save booking</button>

        <h2>Bookings</h2>
        <ul id="bookingList"></ul>

        <script>
            async function loadRooms() {
                const response = await fetch('/rooms');
                const rooms = await response.json();
                const select = document.getElementById('roomSelect');

                rooms.forEach(room => {
                    const option = document.createElement('option');
                    option.value = room.id;
                    option.textContent = room.room_number + ' - ' + room.type + ' - ' + room.price + '€';
                    select.appendChild(option);
                });
            }

            async function loadBookings() {
                const response = await fetch('/bookings');
                const bookings = await response.json();
                const list = document.getElementById('bookingList');
                list.innerHTML = '';

                bookings.forEach(booking => {
                    const li = document.createElement('li');
                    li.textContent = 'Room ' + booking.room_number + ' - ' + booking.datefrom + ' - ' + booking.addinfo;
                    list.appendChild(li);
                });
            }

            async function saveBooking() {
                const roomId = document.getElementById('roomSelect').value;
                const date = document.getElementById('dateInput').value;
                const addinfo = document.getElementById('infoInput').value;

                await fetch('/bookings', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        room_id: roomId,
                        date: date,
                        addinfo: addinfo
                    })
                });

                loadBookings();
            }

            loadRooms();
            loadBookings();
        </script>
    </body>
    </html>
    """