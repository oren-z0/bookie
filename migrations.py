async def m001_initial(db):

    await db.execute(
        """
        CREATE TABLE bookie.competitions (
            id TEXT PRIMARY KEY,
            wallet TEXT NOT NULL,
            name TEXT NOT NULL,
            info TEXT NOT NULL,
            closing_date TEXT NOT NULL,
            amount_tickets INTEGER NOT NULL,
            price_per_ticket INTEGER NOT NULL,
            sold INTEGER NOT NULL,
            time TIMESTAMP NOT NULL DEFAULT """
        + db.timestamp_now
        + """
        );
    """
    )

    await db.execute(
        """
        CREATE TABLE bookie.tickets (
            id TEXT PRIMARY KEY,
            wallet TEXT NOT NULL,
            competition TEXT NOT NULL,
            name TEXT NOT NULL,
            reward_target TEXT NOT NULL,
            registered BOOLEAN NOT NULL,
            time TIMESTAMP NOT NULL DEFAULT """
        + db.timestamp_now
        + """
        );
    """
    )


async def m002_changed(db):

    await db.execute(
        """
        CREATE TABLE bookie.ticket (
            id TEXT PRIMARY KEY,
            wallet TEXT NOT NULL,
            competition TEXT NOT NULL,
            name TEXT NOT NULL,
            reward_target TEXT NOT NULL,
            registered BOOLEAN NOT NULL,
            paid BOOLEAN NOT NULL,
            time TIMESTAMP NOT NULL DEFAULT """
        + db.timestamp_now
        + """
        );
    """
    )

    for row in [list(row) for row in await db.fetchall("SELECT * FROM bookie.tickets")]:
        usescsv = ""

        for i in range(row[5]):
            if row[7]:
                usescsv += "," + str(i + 1)
            else:
                usescsv += "," + str(1)
        usescsv = usescsv[1:]
        await db.execute(
            """
            INSERT INTO bookie.ticket (
                id,
                wallet,
                competition,
                name,
                reward_target,
                registered,
                paid
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (row[0], row[1], row[2], row[3], row[4], row[5], True),
        )
    await db.execute("DROP TABLE bookie.tickets")
