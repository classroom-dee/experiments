# This is a PoC for manifest registry manager
import sqlite3
import pathlib
import aiofiles


def get_conn(db_path: str):
    with sqlite3.connect(db_path) as conn:
        yield conn.cursor()
        conn.commit()
        conn.close()


# Enable WAL -> better concurrency for RW
def create_table(cursor: sqlite3.Cursor):
    cursor.execute("PRAGMA journal_mode=WAL;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manifest_registry (
        hash TEXT PRIMARY KEY,
        size INTEGER,
        url TEXT,
        filename TEXT,
        filedate DATETIME,
        processed_at DATETIME
    )
    """)
    cursor.execute("""
    CREATE INDEX idx_manifest_registry_processed_at ON manifest_registry(processed_at)
    """)


# On system init or restart, always download full manifest as starting point,
# compare with sqlite registry, and update it accordingly,
# then periodically download latest manifest which is lighter, and append to the manifest registry.
# This should guarantee contiguous dates ALL THE TIME. That is the SLO for this task.
def parse_line(line: str) -> tuple[str, str, str] | None:
    parts = line.split()
    if len(parts) == 3:
        url = parts[2].strip()
        filename = url.split("/")[-1]
        return (
            parts[0].strip(),  # size
            parts[1].strip(),  # hash
            url,
            filename,
            filename.split(".")[0],  # filedate, format: 20150218230000
        )


async def read_meta(path: pathlib.Path):
    async with aiofiles.open(path, "r") as f:
        while line := await f.readline():
            yield line


def insert_record(cursor: sqlite3.Cursor, hash, size, url, filename, filedate):
    cursor.execute(
        """
        INSERT OR IGNORE INTO manifest_registry (hash, size, url, filename, filedate)
        VALUES (?, ?, ?, ?, ?)
    """,
        (hash, size, url, filename, filedate),
    )


# This one is used by other module. Move it
def get_todos(cursor: sqlite3.Cursor):
    cursor.execute("SELECT 1 FROM manifest_registry WHERE processed_at IS NOT NONE")
    result = cursor.fetchall()
    # use the result concurrently, with semaphore (during init it can produce a lot of coroutines)
    return result
