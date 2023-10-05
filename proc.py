import json
from icecream import ic
from datetime import datetime
import re


with open("sms_phone.json") as f:
    msgs1 = json.load(f)

with open("sms_tablet.json") as f:
    msgs2 = json.load(f)

# msgs = msgs["messages"]
cib_msgs = [msg for msg in msgs1 if msg["number"] == "CIB"]
cib_msgs.extend([msg for msg in msgs2 if msg["number"] == "CIB"])

card1_msgs = sorted(
    [
        msg
        for msg in cib_msgs
        if (
            msg["body"].startswith("Your credit card#**4012 was charged for")
            or msg["body"].startswith("Your credit card#4012 was charged for")
        )
    ],
    key=lambda x: datetime.fromisoformat(x["received"]),
)
card2_msgs = sorted(
    [
        msg
        for msg in cib_msgs
        if (
            msg["body"].startswith("Your credit card#**5018 was charged for")
            or msg["body"].startswith("Your credit card#5018 was charged for")
        )
    ],
    key=lambda x: datetime.fromisoformat(x["received"]),
)
ic(card1_msgs)
ic(card2_msgs)
# card1_balances = []
# card2_transactions = []
currency_pattern = re.compile("(EGP|GBP|USD)[\s]*([0-9]*.[0-9]*)")
number_pattern = re.compile("[0-9]+.[0-9]*")

for msg in card1_msgs:
    date = datetime.fromisoformat(msg["received"])
    body = msg["body"]
    charge_str = body[body.find("charged for"):body.find("at")]
    limit_str = body[body.find("Available limit is"):body.find("For details")]
    ic(body)
    ic(charge_str)
    ic(limit_str)
    charge = currency_pattern.findall(charge_str)
    limit = number_pattern.findall(limit_str)
    # money = [(a[0], float(a[1])) for a in money]
    ic(date, charge, limit)

for msg in card2_msgs:
    date = datetime.fromisoformat(msg["received"])
    body = msg["body"]
    charge_str = body[body.find("charged for"):body.find("at")]
    limit_str = body[body.find("Available limit is"):body.find("For details")]
    ic(body)
    ic(charge_str)
    ic(limit_str)
    charge = currency_pattern.findall(charge_str)
    limit = number_pattern.findall(limit_str)
    # money = [(a[0], float(a[1])) for a in money]
    ic(date, charge, limit)
