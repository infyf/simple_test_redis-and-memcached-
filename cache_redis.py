from redis import StrictRedis
import requests
import time

cache = StrictRedis(
    host="localhost",
    port=6379,
    db=0,
    # decode_responses=True,
)


def get_file(url: str, filename: str) -> None:
    filedump = cache.get(url)

    if not filedump:
        print("Requested file is missing from cache")
        r = requests.get(url)

        if r.status_code == 200:
            print("File downloaded from network")
            filedump = r.content

            cache.set(url, filedump, ex=20)
            print("File saved to cache")

    else:
        print("Requested file retrieved from cache!")

    with open(filename, "wb") as f:
        f.write(filedump)


if __name__ == "__main__":
    URL1 = "https://www.ixbt.com/img/n1/news/2023/6/4/IMG_0826_large.JPG"

    url = URL1
    tm1 = time.time()
    get_file(url, url.split("/")[-1])
    tm2 = time.time()
    print(f"Execution time: {tm2 - tm1:.4f} seconds")