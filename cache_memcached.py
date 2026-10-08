from pymemcache.client import base
import requests
import time

cache = base.Client(("localhost", 11211))


def get_file(url: str, filename: str) -> None:
    filedump = cache.get(url)

    if not filedump:
        print("Requested file is missing from cache")
        r = requests.get(url)

        if r.status_code == 200:
            print("File downloaded from network")
            filedump = r.content

            cache.set(url, filedump, expire=20)
            print("File saved to cache")

    else:
        print("Requested file retrieved from cache!")

    with open(filename, "wb") as f:
        f.write(filedump)


if __name__ == "__main__":
    URL1 = "https://zakarpattya.net.ua/Blogs/208873-Z-istorii-vzaiemostosunkiv-liudyny-ta-pryrody-na-Zakarpatti"
    URL2 = "https://gumoreska.in.ua/opys-pryrody/"
    
    url = URL2
    tm1 = time.time()
    get_file(url, url.split("/")[-1])
    tm2 = time.time()
    print(f"Execution time: {tm2 - tm1:.4f} seconds")
