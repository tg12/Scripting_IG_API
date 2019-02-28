# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
# NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
# DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
# WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import traceback
import pytz
import calendar
import datetime
import random
import time
import json
import requests
import math
import pandas
import numpy
from time import localtime, strftime
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels import robust
# from matplotlib.pyplot import plot, scatter, show, fill_between
from numpy import NaN, Inf, arange, isscalar, asarray, array
import sys
from scipy import stats

# Time stuff
set(pytz.all_timezones_set)
tz = pytz.timezone('Europe/London')
# https://gist.github.com/mjrulesamrat/0c1f7de951d3c508fb3a20b4b0b33a98
YEAR_var = 2019
market_close_tm = "00:00"
market_open_tm = "00:01"

#CREDS###################################################################
LIVE_API_KEY = '13f5c77f9c9aaa73761b5255d133a17aa7342cf9'
# LIVE_API_KEY = '2ef2256acd086cbbda999bd3c05317aa47f65589' #NOT IN USE
LIVE_USERNAME = "JamesSawyer12"
LIVE_PASSWORD = "W1rew0rm"
LIVE_ACC_ID = "SXWLH"
##########################################################################
DEMO_API_KEY = 'e8cd1f19e8120ad6e94110f14987f0381ea60ab9'
# DEMO_API_KEY = '915d0afe6dc6df32b8a979f042b80ee5fb67cc5e' #NOT IN USE
# DEMO_API_KEY = 'e8ac2586a8bb7ff31d2717665425be5332985eed' #NOT IN USE
DEMO_USERNAME = "py_JamesSawyer"
DEMO_PASSWORD = "abcABC123$$$"
DEMO_ACC_ID = "Z5F0G"
###########################################################################

b_REAL = False
b_Contrarian = False  # DO NOT SET
hacks_enabled = False

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


##########################################################################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################################################################

###########################################################################
###########################################################################
###########################################################################
############################CONFIG VARIABLES###############################
############################CONFIG VARIABLES###############################
############################CONFIG VARIABLES###############################
###########################################################################
###########################################################################
###########################################################################
# PROGRAMMABLE VALUES, IG specific.
# SET INITIAL VARIABLES
orderType_value = "MARKET"
size_value = "1"
expiry_value = "DFB"
guaranteedStop_value = True
currencyCode_value = "GBP"
forceOpen_value = True
###########################################################################
profit_indicator_multiplier = 0.3
ESMA_new_margin = 21                    # (20% for stocks)
too_high_margin = 100                   # No stupidly high pip limit per trade
# Normally would be 3/22 days but dull stocks require a lower multiplier
ce_multiplier = 2
max_trades = int(int(size_value) * 1)   # Max Trades (total per point) Per Epic
spread_check = -2                       # Low spread
acc_used_pct = 85                       # How much of account to use
greed_indicator = 30                 # Dont hang onto profitable trades too long
SUPER_LOW_NEG_MARGIN = 100          # Dont trust IG to take care of ESMA margins
var_high_low_limit_pips = 10  # See notes below
###########################################################################
indices = "93262"  # live

# indices = "xxxxx"  # demo, remember to change this if you change to demo
# epic_ids = []  # not in use, yet!
# market_sentiment = []

net_change = [] #global, for ease...hacky af
percent_change = [] #global, for ease...hacky af

#remember to change these for DEMO!!!
types = {
    # 'Cryptocurrency': ['', 'Europe/London']}
    # 'Options (Australia 200)': '',
    # 'Weekend Indices': '',
    # 'Indices': '',
    # 'Forex': ['', 'Europe/London']}
    # 'Commodities Metals Energies': '',
    # 'Bonds and Moneymarket': '',
    # 'ETFs, ETCs & Trackers': '',
    'Shares - UK': ['180500', 'Europe/London'],
    'Shares - UK International (IOB)': ['97695', 'Europe/London'],
    # 'Shares - US (All Sessions)': '',
    # 'Shares - US': '',
    # 'Shares - Austria': '',
    # 'Shares - Belgium': '',
    'Shares - LSE (UK)': ['172904', 'Europe/London']}
# 'Shares - Finland': '',
# 'Shares - Canada': '',
# 'Shares - France': '',
# 'Shares - Denmark': '',
# 'Shares - Germany': '',
# 'Shares - Greece': '',
# 'Shares - Hong Kong': '',
# 'Shares - Ireland (ISEQ)': '',
# 'Shares - Ireland (LSE)': '',
# 'Shares - Netherlands': '',
# 'Shares - Norway': '',
# 'Shares - Portugal': '',
# 'Shares - Singapore': '',
# 'Shares - South Africa': '',
# 'Shares - Sweden': '',
# 'Shares - Switzerland': '',
# 'Options (Eu Stocks 50)': '',
# 'Options (France 40)': '',
# 'Options (FTSE)': '',
# 'Options (Germany)': '',
# 'Options (Italy 40)': '',
# 'Options (Spain 35)': '',
# 'Options (Sweden 30)': '',
# 'Options (US 500)': '',
# 'Options (Wall St)': '',
# 'Options on FX Majors': '',
# 'Options on Metals, Energies': ''}

###########################################################################
###########################################################################
###########################################################################
############################CONFIG VARIABLES###############################
############################CONFIG VARIABLES###############################
############################CONFIG VARIABLES###############################
###########################################################################
###########################################################################
###########################################################################


def market_index_check(nodeID):
    base_url = REAL_OR_NO_REAL + '/marketnavigation/' + nodeID
    r = requests.get(base_url, headers=authenticated_headers)

    global net_change
    global percent_change

    if isinstance(r.json()['nodes'], list):
        for node in r.json()['nodes']:
            time.sleep(2)
            market_index_check(node['id'])
    if isinstance(r.json()['markets'], list):
        for market in r.json()['markets']:
            # print(market['epic'])

            dfb_today_daily_checks = [
                "DFB" in str(
                    market['epic']), "TODAY" in str(
                    market['epic']), "DAILY" in str(
                    market['epic']), ]

            if any(dfb_today_daily_checks):
                # print(str(market['epic']))
                # print(str(market['instrumentName']))

                major_indices_check = [
                    "FTSE 100" in str(
                        market['instrumentName']), "Germany 30" in str(
                        market['instrumentName']), "Wall Street" in str(
                        market['instrumentName']), "US 500" in str(
                        market['instrumentName']), "US Tech 100" in str(
                        market['instrumentName']), "France 40" in str(
                            market['instrumentName']), "EU Stocks 50" in str(
                                market['instrumentName']), "Italy 40" in str(
                                    market['instrumentName']), "Spain 35" in str(
                                        market['instrumentName']), "Australia 200" in str(
                                            market['instrumentName']), "Japan 225" in str(
                                                market['instrumentName']), "China 300" in str(
                                                    market['instrumentName'])]

                if any(major_indices_check):
                    # print("adding ... " + str(market['instrumentName']))
                    # print("epic id ... " + str(market['epic']))
                    # print("net change ..." + str(market['netChange']))
                    # print("percent change ..." + str(market['percentageChange']))
                    net_change.append(float(market['netChange']))
                    percent_change.append(float(market['percentageChange']))
                    print("checking..." + str(time.strftime("%H:%M:%S")))


def exploreNode(nodeID):
    base_url = REAL_OR_NO_REAL + '/marketnavigation/' + nodeID
    r = requests.get(base_url, headers=authenticated_headers)

    if isinstance(r.json()['nodes'], list):
        for node in r.json()['nodes']:
            time.sleep(2)
            exploreNode(node['id'])
    if isinstance(r.json()['markets'], list):
        for market in r.json()['markets']:
            # print(market['epic'])

            dfb_today_daily_checks = [
                "DFB" in str(
                    market['epic']), "TODAY" in str(
                    market['epic']), "DAILY" in str(
                    market['epic'])]

            if any(dfb_today_daily_checks):
                # if hacks_enabled:
                    # if tradeable_epic(
                        # "KA.D.GKP.DAILY.IP",
                            # market['marketStatus']):  # KA.D.GKP.DAILY.IP or any epic_id you like really
                        # print("trading.... " + str(market['epic']))
                        # no_trade_window()
                        # main_trade_function("KA.D.GKP.DAILY.IP")
                # # else:
                    # # print(
                    # # "!!INFO!!...not DFB,TODAY,DAILY!!...." +
                    # # str(
                    # # market['epic']))

                # else:
                if tradeable_epic(market['epic'], market['marketStatus']):
                    print("trading.... " + str(market['epic']))
                    no_trade_window()
                    main_trade_function(market['epic'])
                # else:
                    # print(
                    # "!!INFO!!...not DFB,TODAY,DAILY!!...." +
                    # str(
                    # market['epic']))


def peakdet(v, delta, x=None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    Returns two arrays

    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

    """
    maxtab = []
    mintab = []

    if x is None:
        x = arange(len(v))

    v = asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)


def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = numpy.average(values, weights=weights)
    variance = numpy.average((values - average)**2, weights=weights)
    return (average, math.sqrt(variance))


def midpoint(p1, p2):
    return (p1 + p2) / 2     # or *0.5


def debug_info(err_str):
    # Standard debugging function, pass it a string
    # print("-----------------DEBUG-----------------")
    print("#################DEBUG##################")
    print(str(time.strftime("%H:%M:%S")) + ":!!!DEBUG!!!:" + str(err_str))
    print("#################DEBUG##################")
    # print("-----------------DEBUG-----------------")


def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]


def percentage(part, whole):
    return 100 * float(part) / float(whole)


def percentage_of(percent, whole):
    # percent should always be 20 for stocks
    # ESMA regulations calculating min stop loss (20% for stocks)
    return (percent * whole) / 100.0


def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)


def idTooMuchPositions(key, positionMap):
    if((key in positionMap) and (int(positionMap[key]) >= int(max_trades))):
        return True
    else:
        return False


def all_same(items):
    return all(x == items[0] for x in items)


def try_market_order(epic_id, trade_direction, limit, stop_pips, positionMap):

    if trade_direction == "NONE":
        return None

    key = epic_id + '-' + trade_direction
    # print(str(key) + " has position of " + str(positionMap[key]))
    if idTooMuchPositions(key, positionMap):
        print(str(key) +
              " has position of " +
              str(positionMap[key]) +
              ", hence should not trade")
        return None

    no_trade_window()  # last chance to bail to avoid neg balance

    limitDistance_value = str(limit)  # Limit
    stopDistance_value = str(stop_pips)  # Stop

    ##########################################################################
    print(
        "Order will be a " +
        str(trade_direction) +
        " Order, With a limit of: " +
        str(limitDistance_value))
    print(
        "stopDistance_value for " +
        str(epic_id) +
        " will bet set at " +
        str(stopDistance_value))
    ##########################################################################

    # MAKE AN ORDER
    base_url = REAL_OR_NO_REAL + '/positions/otc'
    data = {
        "direction": trade_direction,
        "epic": epic_id,
        "limitDistance": limitDistance_value,
        "orderType": orderType_value,
        "size": size_value,
        "expiry": expiry_value,
        "guaranteedStop": guaranteedStop_value,
        "currencyCode": currencyCode_value,
        "forceOpen": forceOpen_value,
        "stopDistance": stopDistance_value}
    r = requests.post(
        base_url,
        data=json.dumps(data),
        headers=authenticated_headers)

    # print("-----------------DEBUG-----------------")
    # print("#################DEBUG#################")
    # print(r.status_code)
    # print(r.reason)
    # print(r.text)
    # print("-----------------DEBUG-----------------")
    # print("#################DEBUG#################")

    d = json.loads(r.text)
    deal_ref = d['dealReference']
    time.sleep(1)
    # CONFIRM MARKET ORDER
    base_url = REAL_OR_NO_REAL + '/confirms/' + deal_ref
    auth_r = requests.get(base_url, headers=authenticated_headers)
    d = json.loads(auth_r.text)
    DEAL_ID = d['dealId']
    print("DEAL ID : " + str(d['dealId']))
    print(d['dealStatus'])
    print(d['reason'])

    if str(d['reason']) != "SUCCESS":
        print("some thing occurred ERROR!!")
        time.sleep(5)
        print("!!!INFO!!!...Order failed, Check IG Status, Resuming...")
    else:
        print("!!INFO!!...Yay, ORDER OPEN")
        time.sleep(3)


def Chandelier_Exit_formula(TRADE_DIR, ATR, Price):
    # Chandelier Exit (long) = 22-day High - ATR(22) x 3
    # Chandelier Exit (short) = 22-day Low + ATR(22) x 3

    if TRADE_DIR == "BUY":

        return float(Price) - float(ATR) * int(ce_multiplier)

    elif TRADE_DIR == "SELL":

        return float(Price) + float(ATR) * int(ce_multiplier)


def calculate_stop_loss(d):

    try:

        price_ranges = []
        closing_prices = []
        first_time_round_loop = True
        TR_prices = []
        price_compare = "bid"

        for i in d['prices']:
            if first_time_round_loop:
                ###########################################
                # First time round loop cannot get previous
                ###########################################
                closePrice = i['closePrice'][price_compare]
                closing_prices.append(closePrice)
                high_price = i['highPrice'][price_compare]
                low_price = i['lowPrice'][price_compare]
                price_range = float(high_price - closePrice)
                price_ranges.append(price_range)
                first_time_round_loop = False
            else:
                prev_close = closing_prices[-1]
                ###########################################
                closePrice = i['closePrice'][price_compare]
                closing_prices.append(closePrice)
                high_price = i['highPrice'][price_compare]
                low_price = i['lowPrice'][price_compare]
                price_range = float(high_price - closePrice)
                price_ranges.append(price_range)
                TR = max(high_price - low_price,
                         abs(high_price - prev_close),
                         abs(low_price - prev_close))
                TR_prices.append(TR)

        return str(int(float(max(TR_prices))))

    except Exception as e:
        # print(e)
        # print(traceback.format_exc())
        # print(sys.exc_info()[0])
        debug_info(
            "Cleaner Error, Cant do much about missing or incomplete data ... IG!!")
        time.sleep(1)
        pass


def main_trade_function(epic_id):

    position_base_url = REAL_OR_NO_REAL + "/positions"
    position_auth_r = requests.get(
        position_base_url, headers=authenticated_headers)
    position_json = json.loads(position_auth_r.text)

    positionMap = {}

    # print("-------------Position Info-------------")
    # print("#################DEBUG#################")
    # print(position_auth_r.status_code)
    # print(position_auth_r.reason)
    # print(position_auth_r.text)
    # print("-----------------DEBUG-----------------")
    # print("#################DEBUG#################")

    for item in position_json['positions']:
        direction = item['position']['direction']
        dealSize = item['position']['dealSize']
        ccypair = item['market']['epic']
        key = ccypair + '-' + direction
        if(key in positionMap):
            positionMap[key] = dealSize + positionMap[key]
        else:
            positionMap[key] = dealSize
    print('current position summary:')
    print(positionMap)

    try:

        # obligatory sleep, gets round IG 60 per min limit
        time.sleep(2)

        base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
        auth_r = requests.get(
            base_url, headers=authenticated_headers)
        d = json.loads(auth_r.text)

        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")
        # print(auth_r.status_code)
        # print(auth_r.reason)
        # print(auth_r.text)
        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")

        current_bid = d['snapshot']['bid']
        current_offer = d['snapshot']['offer']
        ######################################
        current_mid = float(midpoint(current_bid, current_offer))
        ######################################
        instrument_name = str(d['instrument']['name'])

        ###############got current prices and calculated midpoint for accuracy#
        ###############got current prices and calculated midpoint for accuracy#
        ###############got current prices and calculated midpoint for accuracy#

        base_url = REAL_OR_NO_REAL + "/prices/" + epic_id + "/MINUTE_10/24"
        # Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5,
        # MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3,
        # HOUR_4, DAY, WEEK, MONTH)
        auth_r = requests.get(base_url, headers=authenticated_headers)
        d = json.loads(auth_r.text)

        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")
        # print(auth_r.status_code)
        # print(auth_r.reason)
        # print(auth_r.text)
        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")

        remaining_allowance = d['allowance']['remainingAllowance']
        reset_time = humanize_time(
            int(d['allowance']['allowanceExpiry']))
        debug_info("Remaining API Calls left: " + str(remaining_allowance))
        debug_info("Time to API Key reset: " + str(reset_time))

        high_prices = []
        low_prices = []
        close_prices = []
        ltv = []

        for i in d['prices']:

            if i['highPrice']['bid'] is not None:
                highPrice = i['highPrice']['bid']
                # print (highPrice) #debug
                high_prices.append(highPrice)
            ########################################
            if i['lowPrice']['bid'] is not None:
                lowPrice = i['lowPrice']['bid']
                # print (lowPrice) #debug
                low_prices.append(lowPrice)
            ########################################
            if i['closePrice']['bid'] is not None:
                close_price = i['closePrice']['bid']
                # print (close_price) #debug
                close_prices.append(close_price)
            ########################################
            if isinstance(i['lastTradedVolume'], int):
                ltvol = int(i['lastTradedVolume'])
                # print (ltvol) #debug
                ltv.append(ltvol)

        # debug
        # print ("len of high_prices..." + str(len(high_prices)))
        # print ("len of low_prices..." + str(len(low_prices)))
        # print ("len of close_prices..." + str(len(close_prices)))
        # print ("len of ltv..." + str(len(ltv)))

        array_len_check = []
        array_len_check.append(len(high_prices))
        array_len_check.append(len(low_prices))
        array_len_check.append(len(close_prices))
        array_len_check.append(len(ltv))
        # debug
        # print (array_len_check)
        # silently drop out
        if all_same(array_len_check) == False:
            print("Fuck this! Incomplete dataset from IG")
            return None

        ATR = calculate_stop_loss(d)

        ###############################################################
        ###############################################################
        ###############################################################

        low_prices = numpy.ma.asarray(low_prices)
        high_prices = numpy.ma.asarray(high_prices)
        ltv = numpy.ma.asarray(ltv)

        # weighted_avg_and_std(values, weights)
        low_weighted_avg, low_weighted_std_dev = weighted_avg_and_std(
            low_prices, ltv)
        high_weighted_avg, high_weighted_std_dev = weighted_avg_and_std(
            high_prices, ltv)

        # debug_info("instrument_name: " + str(instrument_name))
        # debug_info("high_weighted_avg: " + str(high_weighted_avg))
        # debug_info("low_weighted_avg: " + str(low_weighted_avg))
        # debug_info("current_mid: " + str(current_mid))

        # debug_info("low_weighted_std_dev: " + str(low_weighted_std_dev))
        # debug_info("high_weighted_std_dev: " + str(high_weighted_std_dev))

        # The VWAP can be used similar to moving averages, where prices above
        # the VWAP reflect a bullish sentiment and prices below the VWAP
        # reflect a bearish sentiment. Traders may initiate short positions as
        # a stock price moves below VWAP for a given time period or initiate
        # long position as the price moves above VWAP

        ###############################################################
        ###############################################################
        ###############################################################

        tmp_high_weight_var = float(high_weighted_avg + high_weighted_std_dev)
        tmp_low_weight_var = float(low_weighted_avg + low_weighted_std_dev)
        # e.g
        # series = [0,0,0,2,0,0,0,-2,0,0,0,2,0,0,0,-2,0]

        maxtab_high, _mintab_high = peakdet(high_prices, .3)
        _maxtab_low, mintab_low = peakdet(low_prices, .3)

        # print(array(maxtab_high)[:, 1])
        # print(array(mintab_low)[:, 1])
        # convert to array so can work on min/max

        mintab_low_a = array(mintab_low)[:, 1]
        maxtab_high_a = array(maxtab_high)[:, 1]

        print(mintab_low_a)
        print(maxtab_high_a)

        xb = range(0, len(mintab_low_a))
        xc = range(0, len(maxtab_high_a))

        mintab_low_a_slope, mintab_low_a_intercept, mintab_low_a_lo_slope, mintab_low_a_hi_slope = stats.mstats.theilslopes(
            mintab_low_a, xb, 0.99)
        maxtab_high_a_slope, maxtab_high_a_intercept, maxtab_high_a_lo_slope, maxtab_high_a_hi_slope = stats.mstats.theilslopes(
            maxtab_high_a, xc, 0.99)

        peak_count_high = 0
        peak_count_low = 0
        # how may "peaks" are BELOW the threshold
        for a in mintab_low_a:
            if float(a) < float(tmp_low_weight_var):
                peak_count_low += 1

        # how may "peaks" are ABOVE the threshold
        for a in maxtab_high_a:
            if float(a) > float(tmp_high_weight_var):
                peak_count_high += 1

        print("peak_count_low..." + str(peak_count_low))
        print("peak_count_high..." + str(peak_count_high))

        print("mintab_low_a_slope..." + str(mintab_low_a_slope))
        # print("mintab_low_a_intercept..." + str(mintab_low_a_intercept))
        # print("mintab_low_a_lo_slope..." + str(mintab_low_a_lo_slope))
        # print("mintab_low_a_hi_slope..." + str(mintab_low_a_hi_slope))

        print("maxtab_high_a_slope..." + str(maxtab_high_a_slope))
        # print("maxtab_high_a_intercept..." + str(maxtab_high_a_intercept))
        # print("maxtab_high_a_lo_slope..." + str(maxtab_high_a_lo_slope))
        # print("maxtab_high_a_hi_slope..." + str(maxtab_high_a_hi_slope))

        additional_checks_buy = [
            int(peak_count_low) > int(peak_count_high),
            float(mintab_low_a_slope) < float(maxtab_high_a_slope),
            float(current_mid) >= float(
                numpy.min(mintab_low_a))]
        additional_checks_sell = [
            int(peak_count_high) > int(peak_count_low),
            float(maxtab_high_a_slope) > float(mintab_low_a_slope),
            float(current_mid) <= float(
                numpy.max(maxtab_high_a))]

        if all(additional_checks_sell):
            debug_info("!!SELL SIGNAL!!!")
        elif all(additional_checks_buy):
            debug_info("!!BUY SIGNAL!!!")
        else:
            debug_info("!!!NEUTRAL SIGNAL!!!")

        buy_rules = [
            float(current_mid) > float(
                numpy.max(maxtab_high_a)), all(additional_checks_buy)]
        ###############################################################
        sell_rules = [
            float(current_mid) < float(
                numpy.min(mintab_low_a)), all(additional_checks_sell)]

        # # alt
        # # if there is a change of direction > peak in both directions
        # # change to use any(), as before .... if current is below average price "sell". If it's above then "buy" (there must be interest in that stock??)
        # sell_rules = [
        # float(current_mid) >= float(
        # numpy.max(maxtab_high_a)),
        # float(current_mid) <= float(tmp_low_weight_var)]
        # ###############################################################
        # buy_rules = [
        # float(current_mid) <= float(
        # numpy.min(mintab_low_a)),
        # float(current_mid) >= float(tmp_high_weight_var)]

        # # alt, overbought vs oversold
        # ###############################################################
        # # battle between buyers and sellers so as long as its not over the max
        # # peak, i.e lower than < and above the high weight average, trend is
        # # probably back down
        # ###############################################################
        # sell_rules = [
        #     float(current_mid) <= float(
        #         numpy.max(maxtab_high_a)),
        #     float(current_mid) >= float(tmp_high_weight_var)]
        # ###############################################################
        # # battle between buyers and sellers so as long as its not below the min
        # # peak, i.e lower than < (the sellers are winning) and below the low
        # # weight average trend is probably up, as this is a bargin at this
        # # price
        # ###############################################################
        # buy_rules = [
        #     float(current_mid) >= float(
        #         numpy.min(mintab_low_a)),
        #     float(current_mid) <= float(tmp_low_weight_var)]

        if any(buy_rules):
            debug_info("!!BUY SIGNAL...." + str(instrument_name))
            trade_direction = "BUY"
        elif any(sell_rules):
            debug_info("!!SELL SIGNAL...." + str(instrument_name))
            trade_direction = "SELL"
        else:
            debug_info("!!NEUTRAL SIGNAL...." + str(instrument_name))
            trade_direction = "NONE"
            pip_limit = 9999999  # Junk Data
            stop_pips = "999999"  # Junk Data
            debug_info("Nope")

        ###############################################################
        ###############################################################
        ###############################################################

        if trade_direction == "BUY":
            pip_limit = int(abs(float(max(high_prices)) - \
                            float(current_bid)) * profit_indicator_multiplier)
            ce_stop = Chandelier_Exit_formula(
                trade_direction, ATR, min(low_prices))
            stop_pips = str(int(abs(float(current_bid) - (ce_stop))))
            print("!!INFO!!...BUY!!")
            print(str(epic_id))
            print(
                "!!INFO!!...Take Profit@...." +
                str(pip_limit) +
                " pips")
        elif trade_direction == "SELL":
            pip_limit = int(abs(float(min(low_prices)) - \
                            float(current_bid)) * profit_indicator_multiplier)
            ce_stop = Chandelier_Exit_formula(
                trade_direction, ATR, max(high_prices))
            stop_pips = str(int(abs(float(current_bid) - (ce_stop))))
            print("!!INFO!!...SELL!!")
            print(str(epic_id))
            print(
                "!!INFO!!...Take Profit@...." +
                str(pip_limit) +
                " pips")
        elif trade_direction == "NONE":
            debug_info("Trade direction is NONE")

        # if b_Contrarian:
            # print("!!!WARNING!!! b_Contrarian flag set")
            # print("!!!WARNING!!! b_Contrarian flag set")
            # print("!!!WARNING!!! b_Contrarian flag set")
            # if trade_direction == "SELL":
            # trade_direction == "BUY"
            # elif trade_direction == "BUY":
            # trade_direction == "SELL"
        # else:
            # print("!!!INFO!!! b_Contrarian NOT flag set")
            # print("!!!INFO!!! b_Contrarian NOT flag set")
            # print("!!!INFO!!! b_Contrarian NOT flag set")

        ###############################################################
        ###############################################################
        ########################SANITY CHECKS##########################
        ###############################################################
        ###############################################################

        # reset vars

        global net_change
        global percent_change

        net_change = []
        percent_change = []

        market_index_check(indices)

        print("debug ... " + str(net_change))
        print("debug ... " + str(percent_change))

        #######################################################
        net_positive = all(x > 0 for x in net_change)
        percent_positive = all(y > 0 for y in percent_change)
        #######################################################
        if all([net_positive, percent_positive]):
            market_good = True
        else:
            market_good = False
        #######################################################
        print("debug ... " + str(sum(net_change)))
        print("debug ... " + str(sum(percent_change)))
        if all(
            [float(
                sum(net_change)) > 0, float(
                sum(percent_change)) > 0]):
            market_good = True
        else:
            market_good = False
        #######################################################

        print("is the market good..." + str(market_good) +
              " @ " + str(time.strftime("%H:%M:%S")))

        if all([trade_direction == "BUY", market_good]):
            debug_info("Okay, Buy!....")
        elif all([trade_direction == "SELL", market_good == False]):
            debug_info("Okay, Sell!....")
        else:
            trade_direction = "NONE"
            debug_info("Perhaps not....")

        if trade_direction != "NONE":

            esma_new_margin_req = int(
                percentage_of(
                    ESMA_new_margin,
                    current_bid))

            if int(esma_new_margin_req) > int(stop_pips):
                debug_info("ESMA Readjustment....")
                stop_pips = int(esma_new_margin_req)
            # is there a case for a 20% drop? ... Especially over 18 weeks or
            # so?
            if int(stop_pips) > int(esma_new_margin_req):
                debug_info("ESMA Readjustment....")
                stop_pips = int(esma_new_margin_req)
            if int(pip_limit) == 0:
                debug_info("Pip limit 0!!")  # not worth the trade
                trade_direction = "NONE"
            if int(pip_limit) == 1:
                debug_info("Pip limit 1!!")  # not worth the trade
                trade_direction = "NONE"
            if int(pip_limit) >= int(greed_indicator):
                pip_limit = int(greed_indicator - 1)
            if float(current_mid) > float(numpy.max(maxtab_high_a)):
                # since we have no idea how far this trade can go, Take a guess at
                # the limit, take a reasonable limit.
                pip_limit = int(var_high_low_limit_pips)
                debug_info(
                    "var_high_low_limit_pips adjustment been made (high)!!!")
            if float(current_mid) < float(numpy.min(mintab_low_a)):
                # again, since we have no idea how far this trade can go below the line as
                # its broken past resistance, Take a guess at the limit, take a
                # reasonable limit.
                pip_limit = int(var_high_low_limit_pips)
                debug_info(
                    "var_high_low_limit_pips adjustment been made (low)!!!")
            if int(stop_pips) > int(too_high_margin):
                # Remember this "confusing" error
                # message, It's not always too high
                # margin
                debug_info(
                    "Got to be junk data OR too_high_margin limit hit!!")
                trade_direction = "NONE"

            #################################################################
            #################################################################
            try_market_order(
                epic_id, trade_direction, pip_limit, stop_pips, positionMap)
            #################################################################
            #################################################################
        else:
            debug_info("Literally, NO trade. Exhausted every possibility!!")

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print(sys.exc_info()[0])
        debug_info(
            "Something fucked up with the order, or the pricing or whatever!!, Try again!!")
        time.sleep(2)
        pass


def tradeable_epic(epic_id, status):

    try:

        if hacks_enabled:
            status = "TRADEABLE"  # out of hours hack

        if str(status) == "TRADEABLE":
            base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
            auth_r = requests.get(
                base_url, headers=authenticated_headers)
            d = json.loads(auth_r.text)

            current_bid = d['snapshot']['bid']
            ask_price = d['snapshot']['offer']
            spread = float(current_bid) - float(ask_price)

            if float(spread) >= spread_check:
                print(
                    "!!INFO!!...FOUND GOOD EPIC..., passing to trade function ..." +
                    str(epic_id))
                time.sleep(1)
                return True
            else:
                print(
                    "!!INFO!!...skipping, NO GOOD EPIC....Checking next epic spreads...")
                time.sleep(1)
                pass
        else:
            print(
                "!!INFO!!...skipping, not tradeable):" +
                str(epic_id))
            time.sleep(0.5)

    except Exception as e:
        # print(e)
        # print(traceback.format_exc())
        # print(sys.exc_info()[0])
        debug_info("bid/ask probably returned NoneType!!!")
        pass


def no_trade_window():

    while True:

        try:

            base_url = REAL_OR_NO_REAL + "/accounts"
            auth_r = requests.get(base_url, headers=authenticated_headers)
            d = json.loads(auth_r.text)

            # print("--------------Account Info-------------")
            # print("#################DEBUG#################")
            # print(auth_r.status_code)
            # print(auth_r.reason)
            # print(auth_r.text)
            # print("-----------------DEBUG-----------------")
            # print("#################DEBUG#################")

            for i in d['accounts']:
                if str(i['accountType']) == "SPREADBET":
                    balance = i['balance']['balance']
                    deposit = i['balance']['deposit']

            percent_used = percentage(deposit, balance)
            neg_bal_protect = i['balance']['available']

            debug_info(
                "!!INFO!!...Percent of account used ..." +
                str(percent_used))

            neg_balance_checks = [
                float(percent_used) > float(acc_used_pct),
                float(neg_bal_protect) < SUPER_LOW_NEG_MARGIN]

            if any(neg_balance_checks):
                print("!!INFO!!...Don't trade, Too much margin used up already")
                time.sleep(60)
                continue
            else:
                debug_info("!!INFO!!...OK to trade...")
                # dont check too often, IG Index API limit 60/min
                time.sleep(3)
                return

        except Exception as e:
            # print(e)
            # print(traceback.format_exc())
            # print(sys.exc_info()[0])
            debug_info("!!ERROR!!...No trade window error!!")
            pass


if __name__ == '__main__':

    debug_info("Program Starting...")

    while True:

        try:
            for t in types.keys():
                try:
                    id, time_zone = types[t]
                    tz = pytz.timezone(time_zone)
                    now_time = datetime.datetime.now(tz=tz).strftime("%H:%M")
                    if is_between(
                        str(now_time),
                        (str(market_close_tm),
                         str(market_open_tm))):
                        print("!!INFO!!...Market Closed, waiting....")
                        timeDelay = random.randrange(0, 90)
                        time.sleep(timeDelay)
                    else:
                        print("!!INFO!!...Market Likely Open")
                        # as not to start again from the start
                        exploreNode(id)
                        # check market sentiment here? .... TO DO!
                        no_trade_window()
                except Exception as e:
                    print(e)
                    print(traceback.format_exc())
                    print(sys.exc_info()[0])
                    debug_info("!!ERROR!!...Nothing to see here moving on....")
                    continue

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(sys.exc_info()[0])
            debug_info("!!ERROR!!...Generic Program Error...Moving on!!")
            continue
