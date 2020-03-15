# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
# NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
# DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
# WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

from __future__ import division
import requests
import json
import time
import datetime
from itertools import permutations
from math import log


#CREDS###################################################################
LIVE_API_KEY = ''
LIVE_USERNAME = ""
LIVE_PASSWORD = ""
LIVE_ACC_ID = ""
##########################################################################
DEMO_API_KEY = ''
DEMO_USERNAME = ""
DEMO_PASSWORD = ""
DEMO_ACC_ID = ""
###########################################################################

b_REAL = False

if b_REAL:
    REAL_OR_NO_REAL = 'https://api.ig.com/gateway/deal'
    API_ENDPOINT = "https://api.ig.com/gateway/deal/session"
    API_KEY = LIVE_API_KEY
    data = {"identifier": LIVE_USERNAME, "password": LIVE_PASSWORD}
else:
    REAL_OR_NO_REAL = 'https://demo-api.ig.com/gateway/deal'
    API_ENDPOINT = "https://demo-api.ig.com/gateway/deal/session"
    API_KEY = DEMO_API_KEY
    data = {"identifier": DEMO_USERNAME, "password": DEMO_PASSWORD}

headers = {'Content-Type': 'application/json; charset=utf-8',
           'Accept': 'application/json; charset=utf-8',
           'X-IG-API-KEY': API_KEY,
           'Version': '2'
           }

r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)

headers_json = dict(r.headers)
CST_token = headers_json["CST"]
print(R"CST : " + CST_token)
x_sec_token = headers_json["X-SECURITY-TOKEN"]
print(R"X-SECURITY-TOKEN : " + x_sec_token)

# GET ACCOUNTS
base_url = REAL_OR_NO_REAL + '/accounts'
authenticated_headers = {'Content-Type': 'application/json; charset=utf-8',
                         'Accept': 'application/json; charset=utf-8',
                         'X-IG-API-KEY': API_KEY,
                         'CST': CST_token,
                         'X-SECURITY-TOKEN': x_sec_token}

auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)

base_url = REAL_OR_NO_REAL + '/session'

if b_REAL:
    data = {
        "accountId": LIVE_ACC_ID,
        "defaultAccount": "True"}  # Main Live acc
else:
    data = {
        "accountId": DEMO_ACC_ID,
        "defaultAccount": "True"}  # Main Demo acc

auth_r = requests.put(
    base_url,
    data=json.dumps(data),
    headers=authenticated_headers)

# print("-----------------DEBUG-----------------")
# print("#################DEBUG#################")
# print(auth_r.status_code)
# print(auth_r.reason)
# print(auth_r.text)
# print("-----------------DEBUG-----------------")
# print("#################DEBUG#################")


epic_ids = [
    'CS.D.AUDUSD.TODAY.IP',
    'CS.D.EURCHF.TODAY.IP',
    'CS.D.EURGBP.TODAY.IP',
    'CS.D.EURJPY.TODAY.IP',
    'CS.D.EURUSD.TODAY.IP',
    'CS.D.GBPEUR.TODAY.IP',
    'CS.D.GBPUSD.TODAY.IP',
    'CS.D.USDCAD.TODAY.IP',
    'CS.D.USDCHF.TODAY.IP',
    'CS.D.USDJPY.TODAY.IP',
    'CS.D.CADCHF.TODAY.IP',
    'CS.D.CADJPY.TODAY.IP',
    'CS.D.CHFJPY.TODAY.IP',
    'CS.D.EURCAD.TODAY.IP',
    'CS.D.EURSGD.TODAY.IP',
    'CS.D.EURZAR.TODAY.IP',
    'CS.D.GBPCAD.TODAY.IP',
    'CS.D.GBPCHF.TODAY.IP',
    'CS.D.GBPHKD.TODAY.IP',
    'CS.D.GBPJPY.TODAY.IP',
    'CS.D.GBPSGD.TODAY.IP',
    'CS.D.GBPZAR.TODAY.IP',
    'CS.D.MXNJPY.TODAY.IP',
    'CS.D.NOKJPY.TODAY.IP',
    'CS.D.PLNJPY.TODAY.IP',
    'CS.D.SEKJPY.TODAY.IP',
    'CS.D.SGDJPY.TODAY.IP',
    'CS.D.USDHKD.TODAY.IP',
    'CS.D.USDSGD.TODAY.IP',
    'CS.D.USDZAR.TODAY.IP',
    'CS.D.ZARJPY.TODAY.IP',
    'CS.D.AUDCAD.TODAY.IP',
    'CS.D.AUDCHF.TODAY.IP',
    'CS.D.AUDEUR.TODAY.IP',
    'CS.D.AUDGBP.TODAY.IP',
    'CS.D.AUDJPY.TODAY.IP',
    'CS.D.AUDNZD.TODAY.IP',
    'CS.D.AUDSGD.TODAY.IP',
    'CS.D.EURAUD.TODAY.IP',
    'CS.D.EURNZD.TODAY.IP',
    'CS.D.GBPAUD.TODAY.IP',
    'CS.D.GBPNZD.TODAY.IP',
    'CS.D.NZDAUD.TODAY.IP',
    'CS.D.NZDCAD.TODAY.IP',
    'CS.D.NZDCHF.TODAY.IP',
    'CS.D.NZDEUR.TODAY.IP',
    'CS.D.NZDGBP.TODAY.IP',
    'CS.D.NZDJPY.TODAY.IP',
    'CS.D.NZDUSD.TODAY.IP',
    'CS.D.CHFHUF.TODAY.IP',
    'CS.D.CHFTRY.TODAY.IP',
    'CS.D.EURCZK.TODAY.IP',
    'CS.D.EURHUF.TODAY.IP',
    'CS.D.EURILS.TODAY.IP',
    'CS.D.EURMXN.TODAY.IP',
    'CS.D.EURPLN.TODAY.IP',
    'CS.D.EURTRY.TODAY.IP',
    'CS.D.GBPCZK.TODAY.IP',
    'CS.D.GBPHUF.TODAY.IP',
    'CS.D.GBPILS.TODAY.IP',
    'CS.D.GBPMXN.TODAY.IP',
    'CS.D.GBPPLN.TODAY.IP',
    'CS.D.GBPTRY.TODAY.IP',
    'CS.D.TRYJPY.TODAY.IP',
    'CS.D.USDCZK.TODAY.IP',
    'CS.D.USDHUF.TODAY.IP',
    'CS.D.USDILS.TODAY.IP',
    'CS.D.USDMXN.TODAY.IP',
    'CS.D.USDPLN.TODAY.IP',
    'CS.D.USDTHB.TODAY.IP',
    'CS.D.USDTRY.TODAY.IP',
    'CS.D.CADNOK.TODAY.IP',
    'CS.D.CHFNOK.TODAY.IP',
    'CS.D.EURDKK.TODAY.IP',
    'CS.D.EURNOK.TODAY.IP',
    'CS.D.EURSEK.TODAY.IP',
    'CS.D.GBPDKK.TODAY.IP',
    'CS.D.GBPNOK.TODAY.IP',
    'CS.D.GBPSEK.TODAY.IP',
    'CS.D.NOKSEK.TODAY.IP',
    'CS.D.USDDKK.TODAY.IP',
    'CS.D.USDNOK.TODAY.IP',
    'CS.D.USDSEK.TODAY.IP',
    'CS.D.AUDCNH.TODAY.IP',
    'CS.D.CADCNH.TODAY.IP',
    'CS.D.CNHJPY.TODAY.IP',
    'CS.D.BRLJPY.TODAY.IP',
    'CS.D.GBPINR.TODAY.IP',
    'CS.D.INRJPY.TODAY.IP',
    'CS.D.USDBRL.TODAY.IP',
    'CS.D.USDIDR.TODAY.IP',
    'CS.D.USDINR.TODAY.IP',
    'CS.D.USDKRW.TODAY.IP',
    'CS.D.USDPHP.TODAY.IP',
    'CS.D.USDTWD.TODAY.IP',
    'CS.D.EURCNH.TODAY.IP',
    'CS.D.GBPCNH.TODAY.IP',
    'CS.D.NZDCNH.TODAY.IP',
    'CS.D.RUBJPY.TODAY.IP',
    'CS.D.USDCNH.TODAY.IP', ]


def midpoint(p1, p2):
    return (p1 + p2) / 2     # or *0.5


def dashinsert(epic_str):
    midPoint = len(epic_str) // 2
    return epic_str[:midPoint] + '_' + epic_str[midPoint:]


prices_epic = {}
epic_count = 0

for epic_id in epic_ids:

    try:
        time.sleep(1) #IG Index Rate Limit
        epic_count += 1
        base_url = REAL_OR_NO_REAL + "/markets/" + str(epic_id)
        auth_r = requests.get(base_url, headers=authenticated_headers)
        d = json.loads(auth_r.text)

        bid = float(d["snapshot"]["bid"])
        offer = float(d["snapshot"]["offer"])

        spread = float(abs(float(bid) - float(offer)))
        epic_id = epic_id[:-9]
        epic_id = epic_id[5:]
        epic_id = dashinsert(epic_id)
        print ("[+]debug..." + str(epic_id))
        print ("[+]debug..." + str(spread))
        print ("(" + str(epic_count) + "/" + str(len(epic_ids)) + ")")
        if float(spread) > 3:
            #prices_epic[epic_id] = midpoint(bid, offer)
            print ("[+]debug...ignore, spread too high!")
            continue
        prices_epic[epic_id] = midpoint(bid, offer)
        print("########")
    except Exception as e:
        print("[-]trying next epic...")
        print(e)
        continue


print(prices_epic)
prices_epic = json.dumps(prices_epic)

##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################


def _bf(V, E, src):

    # init
    dist = dict(zip(V, [float('Inf') for v in V]))
    pred = dict(zip(V, [None for v in V]))
    dist[src] = 0

    # relax
    valid_pairs = [(u, v) for (u, v) in permutations(V, 2) if v in E[u]]
    for i in range(len(V) - 1):
        for (u, v) in valid_pairs:
            if dist[u] + E[u][v] < dist[v]:
                dist[v] = dist[u] + E[u][v]
                pred[v] = u

    # return the unique negative cycles
    negative_cycles = {}
    for (u, v) in valid_pairs:
        if dist[u] + E[u][v] < dist[v]:

            cycle = [v]
            while len(cycle) == len(set(cycle)):
                cycle.append(pred[cycle[-1]])

            if cycle[0] == cycle[-1] and len(cycle) > 1:
                negative_cycles[str(set(cycle))] = cycle

            i = 1
            while cycle[i] != cycle[-1]:
                i += 1
            if len(cycle[i:]) > 1:
                negative_cycles[str(set(cycle[i:]))] = cycle[i:]

    return negative_cycles.values()


def find_arbitrage():

    data = json.loads(prices_epic)

    # build graph
    E = {'_': {}}
    for pair, v in data.items():
        front, back = pair.split("_")
        if front == back:
            continue
        if front not in E:
            E[front] = {}
        E[front][back] = -log(float(data[pair]))
    V = E.keys()
    for v in V:
        E['_'][v] = 0

    arbs = _bf(E.keys(), E, '_')

    arb_string = ""
   # display
    for arb in arbs:
        seq = [(arb[i], arb[i + 1]) for i in range(len(arb) - 1)]
        arb_string += ''.ljust(80, '*') + "\n"
        #print(''.ljust(80, '*'))
        arb_string += "ARBITRAGE OPPORTUNITY:" + str(arb) + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S (UTC)') + "\n"
        # print("ARBITRAGE OPPORTUNITY:" + str(arb),
              # datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S (UTC)'))
        arb_string += ''.ljust(80, '*') + "\n"
        # print(''.ljust(80, '*'))
        x = 1
        for i in range(len(seq)):
            front, back = seq[i]
            y = x * float(data['%s_%s' % (front, back)])
            sell = "SELL %s %s" % (x, front)
            buy = " BUY %s %s" % (y, back)
            arb_string += sell.ljust(25) + buy.ljust(25) + "[Rate %s = %s]" % ('%s_%s' % (front, back), data['%s_%s' % (front, back)]) + "\n"
            # print(sell.ljust(25) +
                  # buy.ljust(25) +
                  # "[Rate %s = %s]" %
                  # ('%s_%s' %
                   # (front, back), data['%s_%s' %
                                       # (front, back)]))
            x = y
            arb_string += "PROFIT = %s %s" % (x - 1, arb[0]) + "\n"
            # print("PROFIT = %s %s" % (x - 1, arb[0]))
            arb_string += ''.ljust(80, '*') + "\n"
            # print(''.ljust(80, '*'))
            print(arb_string)


find_arbitrage()
