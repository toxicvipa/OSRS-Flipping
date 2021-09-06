import requests
from requests.exceptions import HTTPError

MIN_PROFIT = 1000

sets = [
    ("Rune armour set (lg)", ["Rune platelegs", "Rune kiteshield", "Rune platebody", "Rune full helm"]),
    ("Rune armour set (sk)", ["Rune plateskirt", "Rune kiteshield", "Rune platebody", "Rune full helm"]),
    ("Adamant set (lg)", ["Adamant platelegs", "Adamant kiteshield", "Adamant platebody", "Adamant full helm"]),
    ("Adamant set (sk)", ["Adamant plateskirt", "Adamant kiteshield", "Adamant platebody", "Adamant full helm"])
]

def find_item_with_id(jsonMap, identifier):
    ind = 0
    for val in jsonMap:
        ind += 1
        if val["id"] == int(identifier):
            return val

def find_item_id(jsonMap, name):
    for val in jsonMap:
        if(val["name"] == name):
            return val["id"]

def print_touple(touple):
    print("\n"*2)
    print("+"*40)
    itemTotal = 0
    for item in setTouple[1]:
        itemData = find_item_with_id(mappingJson, item)
        itemPrice = jsonResponse["data"][str(item)]["low"] + 1
        itemTotal += itemPrice
        print(itemData["name"], ": ", itemPrice)
    print("="*40)
    print(setData["name"], ": ", setPrice)
    print("="*40)
    print("Profit: ", setPrice - itemTotal)
    print("+"*40)

try:
    headers = {
        'User-Agent': 'Set calculator - @Toxicvipa#9789'
    }

    response = requests.get("https://prices.runescape.wiki/api/v1/osrs/latest")
    response.raise_for_status()
    jsonResponse = response.json()

    mappingResponse = requests.get("https://prices.runescape.wiki/api/v1/osrs/mapping", headers=headers)
    mappingJson = mappingResponse.json()

    setIds = []

    for setName in sets:
        data = (find_item_id(mappingJson, setName[0]), [])
        for setItem in setName[1]:
            data[1].append(find_item_id(mappingJson, setItem))
        setIds.append(data)

    for setTouple in setIds:
        setPrice = jsonResponse["data"][str(setTouple[0])]["high"] - 1
        itemTotal = 0
        setData = find_item_with_id(mappingJson, setTouple[0])
        for item in setTouple[1]:
            itemData = find_item_with_id(mappingJson, item)
            itemPrice = jsonResponse["data"][str(item)]["low"] + 1
            itemTotal += itemPrice
        if setPrice - itemTotal >= MIN_PROFIT:
            print_touple(setTouple)


except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
