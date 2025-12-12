import time
import httpx


async def retry_request(callable_func, retries=3, backoff_factor=1):
    for attempt in range(retries):
        try:
            return await callable_func()
        except (httpx.RequestError, httpx.TimeoutException) as e:
            if attempt == retries - 1:
                raise e
            sleep_time = backoff_factor * (2 ** attempt)
            time.sleep(sleep_time)
