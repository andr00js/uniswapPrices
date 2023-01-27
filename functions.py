from datetime import datetime
import requests, json
from contracts import USDC_WETH, WBTC_WETH, LDO_WETH, LINK_WETH


def getCurrentBlock():
    timestamp = str(round(datetime.timestamp(datetime.now())))
    link = "https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=" + timestamp + "&closest=before&apikey=3JGAJUKSIMFXWNJWDB4X9QY5CWYP8P262A"
    dictionary = json.loads(requests.get(link).text)
    return dictionary.get("result")

def getTokenTxns(contract):
    currentBlock = getCurrentBlock()
    link = "https://api.etherscan.io/api?module=account&action=tokentx&address=" + str(contract) + "&startblock=" + str(int(currentBlock)-100) +"&endblock=" + str(currentBlock)+ "&apikey=3JGAJUKSIMFXWNJWDB4X9QY5CWYP8P262A"
    return json.loads(requests.get(link).text)

def getWETHRatio(contract):
    tokentxns = getTokenTxns(contract).get("result")
    swap1 = tokentxns[0]
    decimal1 = int(swap1.get("tokenDecimal"))
    divisor = 10**decimal1
    amount1 = float(swap1.get("value"))/divisor
    swap2 = tokentxns[1]
    decimal2 = int(swap2.get("tokenDecimal"))
    divisor = 10**decimal2
    amount2 = int(swap2.get("value"))/divisor
    if swap2.get("tokenSymbol") == "WETH":
        numeratorAmount = amount1
        denominatorAmount = amount2
    else:
        numeratorAmount = amount2
        denominatorAmount = amount1
    return round((numeratorAmount/denominatorAmount),5)

def getUSDCRatio(contract):
    ratio = float(getWETHRatio(contract))
    wethRatio = float(getWETHRatio(USDC_WETH))
    return round(wethRatio/ratio, 2)

def test():
    output = getTokenTxns(USDC_WETH).get("message")
    return output

def run():
    print(test())