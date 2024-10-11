from typing import Coroutine, Any, List

import logging
import asyncio
import httpx

logging.basicConfig(
    level=logging.INFO,
    format="\u001b[36;1m[\u001b[0m%(asctime)s\u001b[36;1m]\u001b[0m %(message)s\u001b[0m",
    datefmt="%H:%M:%S"
)

class WebsiteSpammer:
    proxy: str
    email: str

    def __init__(self, proxy: str, website: str) -> None:
        self.proxy: str = proxy
        self.website: str = website

    async def spam(self):
        async with httpx.AsyncClient(
            proxies={"http://": self.proxy},
            verify=False
        ) as client:
            while True:
                response = await client.post(
                    self.website,
                    headers={
                        "accept": "*/*",
                        "accept-language": "en-US,en;q=0.9",
                        "content-type": "application/json",
                        "origin": self.website,
                        "priority": "u=1, i",
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                        "x-client": "web",
                    },
                    json={
                        "test": "WebsiteSpammer"
                    }
                )

                if 200 <= response.status_code < 300:
                    logging.info(
                        f"Successfully sent request! -> {self.website}"
                    )

class FastRoutine:
    """
    A simple class for fast gathering, and execution of coroutines.
    """

    func: Coroutine[Any, Any, Any]
    repetitions: int

    def __init__(self, func: Coroutine[Any, Any, Any], repetitions: int = 24) -> None:
        self.func: Coroutine[Any, Any, Any] = func
        self.repetitions: int = repetitions

    async def gather_coroutines(self) -> None:
        tasks: List[asyncio.Task[Any]] = [
            asyncio.create_task(self.func()) for _ in range(self.repetitions)
        ]
        await asyncio.gather(*tasks)

async def main():
    zoom: FastRoutine = FastRoutine(
        func=WebsiteSpammer(
            proxy=None,
            website="https://httpbin.org/post"
        ).spam,
        repetitions=24
    )
    await zoom.gather_coroutines()

if __name__ == "__main__":
    asyncio.run(main())
