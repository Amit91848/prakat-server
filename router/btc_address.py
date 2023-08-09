import requests
import json
import pickle
from fastapi import APIRouter, Query
from pymongo import MongoClient

router = APIRouter()

client = MongoClient(
    'mongodb+srv://yash23malode:9dtb8MGh5aCZ5KHN@cluster.u0gqrzk.mongodb.net/')
db = client['prakat23']
collection = db['ner_tags']

pipeline = [
    {
        "$match": {"ents.label": "BTC Wallet Address"}
    },
    {
        "$unwind": "$ents"
    },
    {
        "$match": {"ents.label": "BTC Wallet Address"}
    },
    {
        "$lookup": {
            "from": "crawled_sites",
            "localField": "url_id",
            "foreignField": "_id",
            "as": "url"
        }
    },
    {
        "$unwind": "$url"
    },
    {
        "$project": {
            "_id": 0,
            "btc_entity": "$ents.entity",
            "url": "$url.url"
        }
    }
]


@router.get('/')
async def getAllBtc():
    print('adwait gandu')
    query = {"ents.label": "BTC Wallet Address"}
    projection = {"ents.entity": 1, "_id": 0, "ents.label": 1}

    # results = list(collection.find(query, projection))

    # print(listresults)
    # print(results[0])
    # for doc in results:
    #     for entity_obj in doc["ents"]:
    #         if entity_obj["label"] == "BTC Wallet Address":
    #             print(doc[])
    #             print(entity_obj["entity"])

    # results = list(collection.aggregate(pipeline))
    # results = list(collection.aggregate(pipeline))
    # unique_results = organize_by_unique_entities(results)

    btc_address_unique_pickle = "btc_address.pickle"

    # # # Open the file in binary write mode and pickle the data
    # with open(btc_address_unique_pickle, 'wb') as file:
    #     pickle.dump(unique_results, file)

    # if unique_results:
    #     print(unique_results[0])
    with open(btc_address_unique_pickle, 'rb') as file:
        unique_results = pickle.load(file)

    # Return the unique results
    return unique_results[0: 100]


def organize_by_unique_entities(results):
    unique_entities = {}  # To store unique btc_entity values and their corresponding URLs
    for result in results:
        btc_entity = result['btc_entity']
        url = result['url']
        if btc_entity not in unique_entities:
            unique_entities[btc_entity] = {
                'btc_entity': btc_entity, 'urls': [url]}
        else:
            unique_entities[btc_entity]['urls'].append(url)

    unique_results = list(unique_entities.values())
    return unique_results


@router.get('/get-data')
async def getData(address: str = Query()):
    return get_info(address)


@router.get('/get_direct_links')
async def getDirectLinks(address: str = Query()):
    return get_direct_links(address)


# def get_outgoing_node(transaction_hash):
#     base_url = "https://api.blockcypher.com/v1/btc/main/txs/"
#     url = base_url + transaction_hash
#     resp = requests.get(url)
#     info = json.loads(resp.text)
#     outgoing_node = info["outputs"][0]["addresses"][0]
#     return outgoing_node


# def convert_value(dec_int):
#     return str(float("0." + str(dec_int))) + " BTC"


# def get_info(address):
#     base_url = "https://api.blockcypher.com/v1/btc/main/addrs/"
#     url = base_url + address
#     resp = requests.get(url)
#     info = json.loads(resp.text)
#     end_dict = {}
#     total_received = convert_value(info["total_received"])
#     total_sent = convert_value(info["total_sent"])
#     balance = convert_value(info["balance"])
#     end_dict["balance"] = balance
#     end_dict["total_received"] = total_received
#     end_dict["total_sent"] = total_sent
#     transactions = info["txrefs"]
#     incoming_transacs = []
#     outgoing_transacs = []
#     for transaction in transactions:
#         transac_id = transaction["tx_hash"]
#         val = convert_value(transaction["value"])
#         timestamp = transaction["confirmed"]
#         transac_keys = transaction.keys()
#         if "spent_by" in transac_keys:
#             linked_node = transaction["spent_by"]
#             incoming_transacs.append({
#                 "hash": transac_id,
#                 "amount": val,
#                 "timestamp": timestamp,
#                 "sender": linked_node
#             })
#         else:
#             linked_node = get_outgoing_node(transac_id)
#             outgoing_transacs.append({
#                 "hash": transac_id,
#                 "amount": val,
#                 "timestamp": timestamp,
#                 "receiver": linked_node
#             })
#     end_dict["incoming_transactions"] = incoming_transacs
#     end_dict["outgoing_transactions"] = outgoing_transacs
#     return end_dict


# def remove_duplicate_entities(results):
#     unique_entities = {}  # To store unique btc_entity values and their corresponding results
#     for result in results:
#         btc_entity = result['btc_entity']
#         if btc_entity not in unique_entities:
#             unique_entities[btc_entity] = result

#     unique_results = list(unique_entities.values())
#     return unique_results

def get_outgoing_node(transaction_hash):
    base_url = "https://api.blockcypher.com/v1/btc/main/txs/"
    url = base_url + transaction_hash
    resp = requests.get(url)
    info = json.loads(resp.text)
    outgoing_node = info["outputs"][0]["addresses"][0]
    return outgoing_node


def convert_value(dec_int):
    return float("0." + str(dec_int))


def get_info(address):
    base_url = "https://api.blockcypher.com/v1/btc/main/addrs/"
    url = base_url + address
    resp = requests.get(url)
    info = json.loads(resp.text)
    end_dict = {}
    total_received = convert_value(info["total_received"])
    total_sent = convert_value(info["total_sent"])
    balance = convert_value(info["balance"])
    end_dict["balance"] = balance
    end_dict["total_received"] = total_received
    end_dict["total_sent"] = total_sent
    transactions = info["txrefs"]
    incoming_transacs = []
    outgoing_transacs = []
    for transaction in transactions:
        transac_id = transaction["tx_hash"]
        val = convert_value(transaction["value"])
        timestamp = transaction["confirmed"]
        transac_keys = transaction.keys()
        if "spent_by" in transac_keys:
            linked_node = transaction["spent_by"]
            incoming_transacs.append({
                "hash": transac_id,
                "amount": val,
                "timestamp": timestamp,
                "sender": linked_node
            })
        else:
            linked_node = get_outgoing_node(transac_id)
            outgoing_transacs.append({
                "hash": transac_id,
                "amount": val,
                "timestamp": timestamp,
                "receiver": linked_node
            })
    end_dict["incoming_transactions"] = incoming_transacs
    end_dict["outgoing_transactions"] = outgoing_transacs
    return end_dict


def get_num_val(btc_string):
    return float(btc_string.split(" ")[0])


def get_direct_links(address):
    data = get_info(address)
    outgoing_transacs = data["outgoing_transactions"]
    if data["balance"] == 0 and data["total_sent"] == 0:
        return []

    balanced_transactions = []
    for transac in outgoing_transacs:
        if transac["amount"] != 0:
            balanced_transactions.append({
                "address": transac["hash"],
                "amount": transac["amount"]
            })

    return balanced_transactions


# print(get_direct_links("1LuhHNxRLn1YXB54FZjoaD8ibHww1aYhey"))
