# scripts/data_download.py
import os
import requests

os.makedirs("../data", exist_ok=True)
DATA_DIR = "../data"

# replace these with the actual DfT download links for a year (example placeholders)
URL_COLLISIONS = "https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2023.csv"
URL_CASUALTIES = "https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-casualty-2023.csv"
URL_VEHICLES = "https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-vehicle-2023.csv"

def download(url, outpath):
    print("Downloading", url)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(outpath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Saved to", outpath)

if __name__ == "__main__":
    download(URL_COLLISIONS, os.path.join(DATA_DIR, "collisions_2023.csv"))
    download(URL_CASUALTIES, os.path.join(DATA_DIR, "casualties_2023.csv"))
    download(URL_VEHICLES, os.path.join(DATA_DIR, "vehicles_2023.csv"))
