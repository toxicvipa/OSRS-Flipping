import requests, sys, csv
from requests.exceptions import HTTPError

PROFIT_PERCENTAGE = 5
MEMBERS_ENABLED = False
MIN_VOLUME = 0

if len(sys.argv) < 3:
    print("Call with arguments: <min margin percentage> <members_enabled> [min volume]")
    exit(1)

PROFIT_PERCENTAGE = int(sys.argv[1])
MEMBERS_ENABLED = sys.argv[2].lower() == 'true'
if len(sys.argv) > 3:
    MIN_VOLUME = int(sys.argv[3])

print(f"Running with parameters Profit: {PROFIT_PERCENTAGE}, Members: {MEMBERS_ENABLED}")

def find_item_with_id(jsonMap, identifier):
    ind = 0
    for val in jsonMap:
        ind += 1
        if val["id"] == int(identifier):
            return val

file = open("Data.csv", "w", newline="")

writer = csv.writer(file, delimiter=";")
writer.writerow(["name", "limit", "buy", "sell", "profit percentage", "volume (6h)"])

try:
    headers = {
        'User-Agent': 'Flipping calculator - @Toxicvipa#9789'
    }
    mappingResponse = requests.get("https://prices.runescape.wiki/api/v1/osrs/mapping", headers=headers)
    mappingJson = mappingResponse.json()

    response = requests.get("https://prices.runescape.wiki/api/v1/osrs/latest")
    response.raise_for_status()

    volumeRequest = requests.get("https://prices.runescape.wiki/api/v1/osrs/6h", headers=headers)
    volumeJson = volumeRequest.json()

    jsonResponse = response.json()
    for key, value in jsonResponse["data"].items():
        instaBuy = value["high"]
        instaSell = value["low"]
        if instaBuy == None or instaSell == None:
            continue
        margin = instaBuy - instaSell
        percentage = instaSell / 100 * PROFIT_PERCENTAGE
        if margin > percentage:
            itemData = find_item_with_id(mappingJson, key)
            if not MEMBERS_ENABLED and itemData["members"]:
                continue
            if "limit" not in itemData:
                continue
            if key in volumeJson["data"]:
                volumeData = volumeJson["data"][key]
                totalVolume = int(volumeData["highPriceVolume"] + volumeData["lowPriceVolume"])
            else:
                totalVolume = 0
            if totalVolume < MIN_VOLUME:
                continue
            row = [itemData["name"], itemData["limit"], instaSell, instaBuy, int(margin / instaSell * 100), totalVolume]
            writer.writerow(row)
            print('[%36s] {limit: %5s} buy: %8s, sell: %8s, profit percentage: %6s, vol: %6s' % (itemData['name'], itemData["limit"], instaSell, instaBuy, int(margin / instaSell * 100), totalVolume))


except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')

file.close()
