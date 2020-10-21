'''THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

# contact :- github@jamessawyer.co.uk



# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
# NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
# DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
# WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy
import pandas
from scipy import stats
from statsmodels import robust
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
import requests
import json
import time
from time import localtime, strftime
import datetime
import calendar
import pytz
#####################################
# Error Handling
import traceback
import sys

set(pytz.all_timezones_set)
YEAR_var = 2018

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

# define empty list
main_epic_ids = []

# open file and read the content in a list
# Sanity Read back
# ALL EPICS
with open('epic_ids.txt', 'r') as filehandle:
    filecontents = filehandle.readlines()

    for line in filecontents:
        # remove linebreak which is the last character of the string
        current_epic_id = line[:-1]

        # add item to the list
        main_epic_ids.append(current_epic_id)

print(main_epic_ids)
# ALL EPICS

b_REAL = False
b_Contrarian = False  # DO NOT SET

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

def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)


def debug_info(err_str):
    # Standard debugging function, pass it a string
    print("-----------------DEBUG-----------------")
    print("#################DEBUG#################")
    print(str(time.strftime("%H:%M:%S")) + ":!!!DEBUG!!!:" + str(err_str))
    print("#################DEBUG#################")
    print("-----------------DEBUG-----------------")


if __name__ == '__main__':

    debug_info("Program Starting...")

    while True:

        for epic_id in main_epic_ids:

            try:

                print(epic_id)

                base_url = REAL_OR_NO_REAL + "/prices/" + epic_id + "/WEEK/18"
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

                high_prices = []
                low_prices = []

                remaining_allowance = d['allowance']['remainingAllowance']
                reset_time = humanize_time(
                    int(d['allowance']['allowanceExpiry']))
                print("-----------------INFO-----------------")
                print("#################INFO#################")
                print("Remaining API Calls left: " + str(remaining_allowance))
                print("Time to API Key reset: " + str(reset_time))
                print("-----------------INFO-----------------")
                print("#################INFO#################")

                for i in d['prices']:

                    if i['highPrice']['bid'] is not None:
                        highPrice = i['highPrice']['bid']
                        high_prices.append(highPrice)
                    ########################################
                    if i['lowPrice']['bid'] is not None:
                        lowPrice = i['lowPrice']['bid']
                        low_prices.append(lowPrice)

                low_prices = numpy.ma.asarray(low_prices)
                high_prices = numpy.ma.asarray(high_prices)

                xi = numpy.arange(0, len(low_prices))

                low_prices_slope, low_prices_intercept, low_prices_lo_slope, low_prices_hi_slope = stats.mstats.theilslopes(
                    low_prices, xi, 0.99)
                high_prices_slope, high_prices_intercept, high_prices_lo_slope, high_prices_hi_slope = stats.mstats.theilslopes(
                    high_prices, xi, 0.99)

                base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
                auth_r = requests.get(
                    base_url, headers=authenticated_headers)
                d = json.loads(auth_r.text)

                print("-----------------DEBUG-----------------")
                print("#################DEBUG#################")
                print(auth_r.status_code)
                print(auth_r.reason)
                print(auth_r.text)
                print("-----------------DEBUG-----------------")
                print("#################DEBUG#################")

                current_bid = d['snapshot']['bid']
                title = d['instrument']['name']
                
                ##################################################################
                ##################################################################
                ##################################################################
                ##################################################################

                # HIGH
                iqr_upper = float(
                    high_prices_intercept + (abs(stats.iqr(high_prices, nan_policy='omit') * 2)))
                # LOW
                iqr_lower = float(low_prices_intercept -
                                  (abs(stats.iqr(low_prices, nan_policy='omit') * 2)))

                high_val = numpy.empty(len(low_prices))
                high_val.fill(iqr_upper)

                low_val = numpy.empty(len(low_prices))
                low_val.fill(iqr_lower)
                
                ##################################################################
                ##################################################################
                ##################################################################
                ##################################################################

                # HIGH
                iqr_upper_MAD = float(
                    high_prices_intercept + (abs(robust.mad(high_prices) * 2)))
                # LOW
                iqr_lower_MAD = float(low_prices_intercept -
                                      (abs(robust.mad(low_prices) * 2)))
                                      
                ##################################################################
                ##################################################################
                ##################################################################
                ##################################################################
                
                high_val_MAD = numpy.empty(len(low_prices))
                high_val_MAD.fill(iqr_upper_MAD)

                low_val_MAD = numpy.empty(len(low_prices))
                low_val_MAD.fill(iqr_lower_MAD)

                intercept_high = numpy.empty(len(low_prices))
                intercept_high.fill(high_prices_intercept)

                intercept_low = numpy.empty(len(low_prices))
                intercept_low.fill(low_prices_intercept)

                plt.plot(high_prices, 'g--')
                plt.plot(low_prices, 'g--')
                plt.plot(high_val, 'h')
                plt.plot(low_val, 'H')
                plt.plot(high_val_MAD, '+')
                plt.plot(low_val_MAD, '+')
                
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

                current_bid = float(d['snapshot']['bid'])
                current_bid_a = numpy.empty(len(low_prices))
                current_bid_a.fill(current_bid)
                
                
                # plt.plot(xi, linreg_close_prices_line,
                # label='linreg_close_prices_line')
                # plt.plot(
                # xi,
                # linreg_low_prices_line,
                # label='linreg_low_prices_line')
                # plt.plot(xi, linreg_high_prices_line,
                # label='linreg_high_prices_line')
                # plt.plot(
                # xi,
                # linreg_mid_prices_line,
                # label='linreg_mid_prices_line')
                # plt.plot(xi, theilsen_close_prices_line,
                # label='theilsen_close_prices_line')
                # plt.plot(xi, theilsen_low_prices_line,
                # label='theilsen_low_prices_line')
                # plt.plot(xi, theilsen_high_prices_line,
                # label='theilsen_high_prices_line')
                plt.plot(xi, intercept_low,
                         label='theilsen_low_prices_line')
                plt.plot(xi, intercept_high,
                         label='theilsen_high_prices_line')
                plt.plot(xi, current_bid_a,
                         label='current_bid')
                plt.legend(loc='upper left')
                plt.fill_between(
                xi,
                intercept_low,
                intercept_high,
                facecolor='green',
                alpha=0.5)
                plt.xlabel('Weeks')
                plt.ylabel('Price')
                plt.title(str(title))
                plt.show()
                plt.clf()

            except Exception as e:
                print(e)
                print("!!INFO!!...Try again!!")
                time.sleep(2)
                continue
