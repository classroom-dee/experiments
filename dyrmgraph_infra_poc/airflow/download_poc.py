"""
example manifest
150383 297a16b493de7cf6ca809a7cc31d0b93 http://data.gdeltproject.org/gdeltv2/20150218230000.export.CSV.zip
318084 bb27f78ba45f69a17ea6ed7755e9f8ff http://data.gdeltproject.org/gdeltv2/20150218230000.mentions.CSV.zip
10768507 ea8dde0beb0ba98810a92db068c0ce99 http://data.gdeltproject.org/gdeltv2/20150218230000.gkg.csv.zip
149211 2a91041d7e72b0fc6a629e2ff867b240 http://data.gdeltproject.org/gdeltv2/20150218231500.export.CSV.zip
339037 dec3f427076b716a8112b9086c342523 http://data.gdeltproject.org/gdeltv2/20150218231500.mentions.CSV.zip
10269336 2f1a504a3c4558694ade0442e9a5ae6f http://data.gdeltproject.org/gdeltv2/20150218231500.gkg.csv.zip
149723 12268e821823aae2da90882621feda18 http://data.gdeltproject.org/gdeltv2/20150218233000.export.CSV.zip
357229 744acad14559f2781a8db67715d63872 http://data.gdeltproject.org/gdeltv2/20150218233000.mentions.CSV.zip
11279827 66b03e2efd7d51dabf916b1666910053 http://data.gdeltproject.org/gdeltv2/20150218233000.gkg.csv.zip
158842 a5298ce3c6df1a8a759c61b5c0b6f8bb http://data.gdeltproject.org/gdeltv2/20150218234500.export.CSV.zip
374528 dd322c888f28311aca2c735468405551 http://data.gdeltproject.org/gdeltv2/20150218234500.mentions.CSV.zip
11212939 cd20f295649b214dd16666ca451b9994 http://data.gdeltproject.org/gdeltv2/20150218234500.gkg.csv.zip

gdelt manifest url: http://data.gdeltproject.org/gdeltv2/masterfilelist.txt
"""

# import threading
import aiohttp
from aiohttp import TCPConnector, ThreadedResolver
import asyncio


async def custom_check(response):
    # Just an example
    if response.status not in {200, 201, 202, 301}:
        raise RuntimeError(f"Unexpected status code: {response.status}")


async def main():
    resolver = ThreadedResolver()
    async with aiohttp.ClientSession(
        raise_for_status=custom_check, connector=TCPConnector(resolver=resolver)
    ) as session:
        links = [
            "http://www.example.com",
            "http://www.python.org",
            "http://www.google.com",
        ]

        async def _job(link: str):
            async with session.get(
                link,
            ) as response:
                print("URL:", response.url)
                print("Status:", response.status)
                print("Content-type:", response.headers["content-type"])

                html = await response.text()
                print("Body:", html[:15], "...")
                print("-------------------------------")

                # print("History:", response.history) # redirect history

        await asyncio.gather(*[_job(link) for link in links])


asyncio.run(
    main()
)  # For a distributed setup, you can use something like Celery to distribute the tasks across workers.


# But don't use threading with asyncio. It's more natural to share session pool across tasks
# def worker(link: str):
#     asyncio.run(job(link=link))


# links = ["http://www.example.com", "http://www.python.org", "http://www.google.com"]

# threads = []

# for link in links:
#     thread = threading.Thread(
#         target=worker, args=(link,)
#     )  # otherwise, the loop variable will be shared across threads and cause issues
#     threads.append(thread)
#     thread.start()

# # Wait for all threads to complete
# for thread in threads:
#     thread.join()
