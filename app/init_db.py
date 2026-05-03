from db import get_db_connection

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS hotel_rooms (
        id SERIAL PRIMARY KEY,
        room_number INT NOT NULL UNIQUE,
        type VARCHAR(50) NOT NULL,
        price NUMERIC(10,2) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS hotel_guests (
        id SERIAL PRIMARY KEY,
        firstname VARCHAR(100) NOT NULL,
        lastname VARCHAR(100) NOT NULL,
        address VARCHAR(255) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS hotel_bookings (
        id SERIAL PRIMARY KEY,
        guest_id INT NOT NULL,
        room_id INT NOT NULL,
        datefrom DATE NOT NULL,
        dateto DATE NOT NULL,
        addinfo VARCHAR(255) DEFAULT '',
        FOREIGN KEY (guest_id) REFERENCES hotel_guests(id),
        FOREIGN KEY (room_id) REFERENCES hotel_rooms(id)
    );
    """)

    # sample data
    cur.execute("""
    INSERT INTO hotel_rooms (room_number, type, price)
    VALUES (101, 'Single', 89.00)
    ON CONFLICT DO NOTHING;

    INSERT INTO hotel_rooms (room_number, type, price)
    VALUES (102, 'Double', 129.00)
    ON CONFLICT DO NOTHING;

    INSERT INTO hotel_guests (firstname, lastname, address)
    VALUES ('Mikael', 'Ylirotu', 'Helsinki')
    ON CONFLICT DO NOTHING;
    """)

    conn.commit()
    cur.close()
    conn.close()