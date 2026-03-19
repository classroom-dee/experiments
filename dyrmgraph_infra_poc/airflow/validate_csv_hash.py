# TODO: Should emit retry based on date of the file
# TODO: Lacking a function to load up "already-processed-registry"

import hashlib
import pathlib
import aiofiles
import aiohttp
from aiohttp import TCPConnector, ThreadedResolver


# 1. download meta (this is just for test! Reuse the download_file function in the repo)
async def download_file(url: str, path: pathlib.Path):
    resolver = ThreadedResolver()
    connector = TCPConnector(resolver=resolver)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.read()
            async with aiofiles.open(path, "wb") as f:
                await f.write(content)


# 2. read meta
# 3. parse meta
# 4. download csv (reuse the download_file function)
# 5. compare hash
# 6. if not match, emit retry


def parse_line(line: str) -> tuple[str, str, str] | None:
    parts = line.split()
    if len(parts) == 3:
        return (
            parts[0].strip(),  # size
            parts[1].strip(),  # hash
            parts[2].strip(),  # url
            parts[2].strip().split("/")[-1],  # filename
        )


async def read_meta(path: pathlib.Path):
    async with aiofiles.open(path, "r") as f:
        while line := await f.readline():
            yield line


async def check_hash_and_size(
    path: pathlib.Path, expected: str, expected_size: str
) -> bool:
    h = hashlib.md5()
    size = 0
    async with aiofiles.open(path, "rb") as f:
        while chunk := await f.read(8192):
            h.update(chunk)
            size += len(chunk)

    return h.hexdigest() == expected and str(size) == expected_size


async def main():
    meta_path = pathlib.Path("example_manifest.txt")
    csv_dir = pathlib.Path("./")

    async for line in read_meta(meta_path):
        parsed = parse_line(line)
        if parsed is None:
            print("Invalid meta format")
            return
        expected_size, expected_hash, url, filename = parsed

        await download_file(url, csv_dir / filename)

        if await check_hash_and_size(csv_dir / filename, expected_hash, expected_size):
            print("Hash and size match, file is valid.")
        else:
            print(
                f"File {filename} expected size {expected_size} and hash {expected_hash}"
            )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
