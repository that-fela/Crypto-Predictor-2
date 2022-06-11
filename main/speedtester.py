import json
import asyncpg
import asyncio
import datetime as dt

db = {
    "database": "binancedata",
    "user": "postgres",
    "password": "12341234",
    "host": "127.0.0.1",
    "port": "5432"
}


async def get_conn():
    conn = await asyncpg.connect(**db)
    return conn


async def main():
    conn = await get_conn()

    val = [2533.99000000, 2534.63000000]
    query = "SELECT bids FROM bdata WHERE bids @> $1"
    st = dt.datetime.now()
    resp = await conn.fetch(query, val)
    et = dt.datetime.now()
    print(len(resp))

    print(f"asyncpg time: {et-st}")

    


def file_read():
    with open("_binance.txt", mode='r') as infile:
        raw_data = infile.readlines()
    
    json_data = []
    for line in raw_data:
        line = line.replace("\'","\"")
        json_data.append(json.loads(line))

    response = []
    st = dt.datetime.now()
    for record in json_data:
        if record["lastUpdateId"] >= 15316254032 and record["lastUpdateId"] <= 15317233493:
            response.append(record)
    et = dt.datetime.now()

    print(f"file time {et-st}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    file_read()