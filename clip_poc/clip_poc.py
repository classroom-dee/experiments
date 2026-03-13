import threading
import time
from io import BytesIO
import random

import requests
import torch
import clip
from PIL import Image


def search(word: str, api_url: str):
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": word,
        "gsrnamespace": 6,
        "gsrlimit": 5,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
    }
    headers = {"User-Agent": "clip-test-poc/0.1"}

    resp = requests.get(api_url, params=params, headers=headers)
    if resp.status_code != 200:
        print(f"HTTP error: {resp.status_code}")
        return []
    try:
        r = resp.json()
        if "query" not in r:
            return []
    except Exception:
        print(f"Bad response: {resp.text[:200]}")

    images = []
    for page in r["query"]["pages"].values():
        images.append(page["imageinfo"][0]["url"])
    return images


def process_img(
    model,
    preprocess,
    img_url: str,
    word: str,
    avoid_categories: list[str],
    num: int,
    delay=5,
):
    time.sleep(random.uniform(delay, delay * 2))

    headers = {"User-Agent": "clip-test-poc/0.1"}
    resp = requests.get(img_url, headers=headers)  # use aiohttp later
    # Not an image?
    if resp.status_code != 200:
        print(f"bad status: {resp.status_code}")
        return
    if "image" not in resp.headers.get("Content-Type", ""):
        print(f"Not an image: {resp.headers.get('Content-Type')}")
        return
    img = resp.content

    try:
        image = preprocess(Image.open(BytesIO(img))).unsqueeze(0).to(device)
    except Exception as e:
        # weird formatS?
        print(f"Bad image: {e}")
        return

    text = clip.tokenize(avoid_categories + [word]).to(device)

    with torch.inference_mode():
        image_features = model.encode_image(image)  # noqa
        text_features = model.encode_text(text)  # noqa
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()

    print(f"Word {word} scores:", probs)
    if probs.argmax() == len(avoid_categories):
        print(f"This is the image I want: image number {num}")
        with open(f"{word}_{num}.png", "wb") as f:
            f.write(img)


if __name__ == "__main__":
    API_URL = "https://commons.wikimedia.org/w/api.php"

    WORD = "apple"
    torch.set_num_threads(
        1
    )  # avoid oversubscription ... torch already uses threading internally
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    img_urls = search(WORD, API_URL)
    # print(img_urls)

    threads = []
    avoids = ["a logo", "a computer", "a laptop"]

    for i, u in enumerate(img_urls):
        t = threading.Thread(
            target=process_img,
            args=(model, preprocess, u, WORD, avoids, i),
            kwargs={"delay": 1},
        )
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
