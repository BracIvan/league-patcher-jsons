import requests
import os
import json
from multiprocessing.pool import ThreadPool

# regions = ['br', 'cn', 'eun', 'eune', 'euw', 'garena2', 'garena3', 'id', 'jp', 'kr', 'la', 'la1', 'la2', 'lan',
#            'las', 'na', 'oc', 'oc1', 'oce', 'pbe', 'ph', 'ru', 'sg', 'tencent', 'th', 'tr', 'tw', 'vn'] # Uncomment for testing
regions = ["br", "eune", "euw", "jp", "kr", "la1", "la2", "na", "oc1", "ru", "tr"] # All currently available regions

urls = [(f"./live-{r}-win", f"https://lol.dyn.riotcdn.net/channels/public/live-{r}-win.json") for r in regions]
urls += [(f"./maclive-{r}-mac", f"https://lol.dyn.riotcdn.net/channels/public/maclive-{r}-mac.json") for r in regions]
urls.extend([("./pbe-pbe-win", "https://lol.dyn.riotcdn.net/channels/public/pbe-pbe-win.json"),
             ("./pbe-pbe_test-win", "https://lol.dyn.riotcdn.net/channels/public/pbe-pbe_test-win.json"),
             ("./macpbe-pbe-mac", "https://lol.dyn.riotcdn.net/channels/public/macpbe-pbe-mac.json"),
             ("./macpbe-pbe_test-mac", "https://lol.dyn.riotcdn.net/channels/public/macpbe-pbe_test-mac.json")])

def download_jsons(entry):
    path, url = entry
    # print(path) # Uncomment for testing
    json_file = requests.get(url)
    if json_file.status_code == 200:
        # print(path) # Uncomment for testing
        version = json.loads(json_file.content)["version"]
        os.makedirs(path, exist_ok=True)
        try:
            with open(f"{path}/{version}.json", "x") as out_file:
                out_file.write(json_file.content.decode("utf-8"))
        except FileExistsError:
            pass

any(ThreadPool(25).imap_unordered(download_jsons, urls))
