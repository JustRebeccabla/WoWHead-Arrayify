import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing import cpu_count
from tqdm import tqdm
import pyfiglet


def fetch_spell_info(spell_id):
    url = f"https://www.wowhead.com/spell={spell_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    spell_name = soup.find("h1", {"class": "heading-size-1"}).text

    if spell_name == "Spells":
        return None

    url = url.replace(" ", "%20")
    return f"[{spell_id}] = true, -- {spell_name} {url}"

def main():
    ##Insert list of spell ids here 
    spell_ids = {}
    banner = pyfiglet.figlet_format("Becca Arrayify")
    print(banner)

    with Pool(processes=min(cpu_count(), len(spell_ids))) as pool:
        results = list(tqdm(pool.imap(fetch_spell_info, spell_ids), total=len(spell_ids)))

    for result in filter(None, results):
        print(result)

if __name__ == "__main__":
    main()