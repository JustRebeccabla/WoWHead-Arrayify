# WoWHead-Arrayify

WoWHead-Arrayify is a Python script that fetches spell information from the WoWHead website. It uses multiprocessing to fetch data in parallel, making it faster and more efficient.

## Features

- Fetches spell information from WoWHead using spell IDs.
- Uses multiprocessing for parallel data fetching.
- Prints a banner at the start of the script using pyfiglet.

## Dependencies

- requests
- BeautifulSoup
- multiprocessing
- tqdm
- pyfiglet

You can install these dependencies using pip:

pip install requests beautifulsoup4 tqdm pyfiglet

## Usage

1. Clone the repository.
2. Open the `WoWHead-Arrayify.py` file.
3. Insert a list of spell IDs in the `spell_ids` dictionary in the `main` function.
4. Run the script.

