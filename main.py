import httpx
import random
import concurrent.futures

tokens = open("tokens.txt").readlines()
proxies = open("proxies.txt").readlines()
threads = 20


def get_random_proxy():
    return random.choice(proxies).strip()


def check_token(tkn, proxy):
    try:
        r = httpx.post("https://discord.com/api/v9/outbound-promotions/890374599315980288/claim", headers={"Authorization": tkn.strip()}, proxies="http://" + proxy).json()
    except:
        print("connection failed")
        return 0
    return r['code']


with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    futures = {executor.submit(check_token, token, get_random_proxy()) for token in tokens}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result != 0:
            with open("output.txt", "a") as f:
                f.write(f"{result}\n")