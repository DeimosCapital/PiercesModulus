import requests
import bs4
import urllib
import urllib3
from bs4 import BeautifulSoup
import time
from termcolor import colored
import colorama
from colorama import init
import datetime
from datetime import datetime

links = []
PRICE_link = 'https://api.glassnode.com/v1/metrics/market/price_usd_ohlc?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
MCTCR_link = 'https://api.glassnode.com/v1/metrics/mining/marketcap_thermocap_ratio?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
MVRVZ_link = 'https://api.glassnode.com/v1/metrics/market/mvrv_z_score?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
Puell_link = 'https://api.glassnode.com/v1/metrics/indicators/puell_multiple?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
STH_NUPL_link = 'https://api.glassnode.com/v1/metrics/indicators/nupl_less_155?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
LTH_NUPL_link = 'https://api.glassnode.com/v1/metrics/indicators/nupl_more_155?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
MFRP_link = 'https://api.glassnode.com/v1/metrics/mining/revenue_from_fees?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
PSIP_link  = 'https://api.glassnode.com/v1/metrics/supply/profit_relative?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
TSLA30to90_link = 'https://api.glassnode.com/v1/metrics/supply/active_1m_3m?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
RP_link = 'https://api.glassnode.com/v1/metrics/indicators/realized_profit?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
NVT_link = 'https://api.glassnode.com/v1/metrics/indicators/nvts?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
CVDD_link = 'https://api.glassnode.com/v1/metrics/indicators/cvdd?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
RC_link = 'https://api.glassnode.com/v1/metrics/market/marketcap_realized_usd?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='

links = [(PRICE_link,"price"),(RC_link,"rc"), (CVDD_link,"cvdd"), (Puell_link,"puell"),(STH_NUPL_link,"sthnupl"),(LTH_NUPL_link,"lthnupl"),(MVRVZ_link,"mvrvz"),(MCTCR_link,"mctcr"), (NVT_link,"nvt"),(RP_link,"rp"),(MFRP_link,"mfrp"),(PSIP_link,"psip"), (TSLA30to90_link, "tsla")]

api_appended_links = []
api_key = '6293830e-a13c-42c5-853e-8e316e17731f'
print("Calculating...")
for link in links:
    newlink = link[0] + api_key
    api_appended_links.append((newlink, link[1]))

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def acquire_datasets(links):
    datasets = []
    for link in links:
        html = urllib.request.urlopen(link[0])
        time.sleep(1)
        soup = BeautifulSoup(html, "html.parser")
        split_soup = str(soup).split("\n")
        datapoints = []
        ss = split_soup[1:(len(split_soup)-1)]
        for line in ss:
            split_line = line.split(",")
            datapoints.append(split_line[1])
        datasets.append((link[1],datapoints))
    return datasets

def GetMCTCR_data(data):
    values = data[1]
    if float(values[-1]) < 0.0000038:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        print("Final MCTCR datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red"))
        return (float(values[-1])/0.0000038)
    else:
        print("Final MCTCR datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/0.0000038)

def GetMVRVZ_data(data):
    values = data[1]
    if float(values[-1]) < 7:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        print("Final MVRVZ datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red"))
        return (float(values[-1])/7)
    else:
        print("Final MVRVZ datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/7)
    
def GetPuell_data(data):
    values = data[1]
    if float(values[-1]) < 4.2:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        print("Final Puell datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red"))
        return (float(values[-1])/4.2)
    else:
        print("Final Puell datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/4.2)

def GetSTHNUPL_data(data):
    values = data[1]
    if float(values[-1]) < .48:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        print("Final STHNUPL datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red"))
        return (float(values[-1])/.48)
    else:
        print("Final STHNUPL datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/.48)

def GetLTHNUPL_data(data):
    values = data[1]
    if float(values[-1]) < .85:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        print("Final LTHNUPL datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red"))
        return (float(values[-1])/.85)
    else:
        print("Final LTHNUPL datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/.85)

def GetMFRP_data(data):
    values = data[1]
    if float(values[-1]) < .35:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        print("Final MFRP datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red"))
        return (float(values[-1])/.35)
    else:
        print("Final MFRP datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/.35)

def GetPSIP_data(data):
    values = data[1]

    if float(values[-1]) < .9:
        not_in_high_zone = True
    else:
        not_in_high_zone = False
    
    last10sum = 0
    for value in values[-11:-1]:
        if float(value) > .90:
            last10sum = last10sum+1
        else:
            last10sum = last10sum+0
    
    if last10sum > 8:
        been_in_high_zone = True
    
    if not_in_high_zone == True:
        if been_in_high_zone == True:
            dangerzone = True
        else:
            dangerzone = False
    else:
        dangerzone = False

    if dangerzone == True:
        print("Final PSIP datapoint: "  + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red"))
        return 1
    else:
        print("Final PSIP datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return 0

def GetTSLA_data(data):
    values = data[1]
    slopes = []
    counter = 1
    while counter < len(values):
        if values[counter] == "":
            if values[counter-1] == "":
                slope = 0
            else:
                slope = 0 - float(values[counter-1])
        elif values[counter-1] == "":
            slope = float(values[counter]) - 0
        else:
            slope = float(values[counter]) - float(values[counter-1])
        slopes.append(slope)
        counter = counter +1
    
    positive_slope_sum = 0
    for slope in slopes[-11:-2]:
        if float(slope) > 0:
            positive_slope_sum = positive_slope_sum + 1
        else:
            positive_slope_sum = positive_slope_sum + 1
    
    if slopes[-1] > 0:
        dangerzone = False
    else:
        if positive_slope_sum > 9:
            dangerzone = True
        else:
            dangerzone = False

    if dangerzone == True:
        print("Final TLSA30to90 verdict-- last ten slopes postive, current slope negative, indicating that we are in the " + colored("DANGER ZONE", "red"))
        return 1
    else:
        print("Final TLSA30to90 verdict-- we are in the " + colored("SAFE ZONE", "green"))
        return 0

def GetRP_data(data):

    values = data[1]
    slopes = []
    counter = 1
    while counter < len(values):
        if values[counter] == "":
            if values[counter-1] == "":
                slope = 0
            else:
                slope = 0 - float(values[counter-1])
        elif values[counter-1] == "":
            slope = float(values[counter]) - 0
        else:
            slope = float(values[counter]) - float(values[counter-1])
        slopes.append(slope)
        counter = counter +1
    
    positive_slope_sum = 0
    for slope in slopes[-11:-2]:
        if float(slope) > 0:
            positive_slope_sum = positive_slope_sum + 1
        else:
            positive_slope_sum = positive_slope_sum + 1
    
    if slopes[-1] > 0:
        dangerzone = False
    else:
        if positive_slope_sum > 9:
            dangerzone = True
        else:
            dangerzone = False

    if dangerzone == True:
        print("Final RP verdict-- last ten slopes postive, current slope negative, indicating that we are in the " + colored("DANGER ZONE", "red"))
        return 1
    else:
        print("Final RP verdict-- we are in the " + colored("SAFE ZONE", "green"))
        return 0

def GetCVDD_data(data):
    values = data[1]
    slopes = []
    counter = 1
    while counter < len(values):
        if values[counter] == "":
            if values[counter-1] == "":
                slope = 0
            else:
                slope = 0 - float(values[counter-1])
        elif values[counter-1] == "":
            slope = float(values[counter]) - 0
        else:
            slope = float(values[counter]) - float(values[counter-1])
        slopes.append(slope)
        counter = counter +1
    
    if slopes[-1] > 60:
        dangerzone = True
    else:
        dangerzone = False

    if dangerzone == True:
        print("Final CVDD verdict-- we are in the " + colored("DANGER ZONE", "red"))
        return 1
    else:
        print("Final CVDD verdict-- we are in the " + colored("SAFE ZONE", "green"))
        return 0
    
def GetNVT_data(data):

    values = data[1]
    slopes = []
    counter = 1
    while counter < len(values):
        if values[counter] == "":
            if values[counter-1] == "":
                slope = 0
            else:
                slope = 0 - float(values[counter-1])
        elif values[counter-1] == "":
            slope = float(values[counter]) - 0
        else:
            slope = float(values[counter]) - float(values[counter-1])
        slopes.append(slope)
        counter = counter +1
    
    positive_slope_sum = 0
    for slope in slopes[-11:-2]:
        if float(slope) > 0:
            positive_slope_sum = positive_slope_sum + 1
        else:
            positive_slope_sum = positive_slope_sum + 1
    
    if slopes[-1] > 0:
        dangerzone = False
    else:
        if positive_slope_sum > 9:
            dangerzone = True
        else:
            dangerzone = False

    if dangerzone == True:
        print("Final NVT verdict-- last ten slopes postive, current slope negative, indicating that we are in the " + colored("DANGER ZONE", "red") + " (Note: this is a sell indicator only valid during INSANE bull runs for finding absolute price peaks)")
    else:
        print("Final NVT verdict-- we are in the " + colored("SAFE ZONE", "green"))
    
    if dangerzone == True:
        return 1
    else:
        return 0

def GetRC_data(data):
    values = data[1]
    slopes = []
    counter = 1
    while counter < len(values):
        if values[counter] == "":
            if values[counter-1] == "":
                slope = 0
            else:
                slope = 0 - float(values[counter-1])
        elif values[counter-1] == "":
            slope = float(values[counter]) - 0
        else:
            slope = float(values[counter]) - float(values[counter-1])
        slopes.append(slope)
        counter = counter +1

    counter = 1
    jerks = []
    for slope_point in slopes:
        if counter < (len(slopes)):
            jerk = abs((float(slopes[counter]) - float(slopes[counter-1]))/100000)
            jerks.append(jerk)
        counter = counter +1

    if jerks[-1] > 25000:
        dangerzone = True
    else:
        dangerzone = False

    if dangerzone == True:
        print("Final RCJ datapoint: " + str(jerks[-1]) + ", indicating we are in the " + colored("DANGER ZONE", "red"))
    else:
        print("Final RCJ datapoint: " + str(jerks[-1]) + ", indicating we are in the " + colored("SAFE ZONE", "green"))
    return (jerks[-1]/25000)

def GetPrice_data(data):
    values = data[1]
    return values[-2]

def GetCurrentDate(data):
    datasets = []
    for link in data:
        if link[1] == "price":
            html = urllib.request.urlopen(link[0])
            time.sleep(1)
            soup = BeautifulSoup(html, "html.parser")
            split_soup = str(soup).split("\n")
            datapoints = []
            ss = split_soup[1:(len(split_soup)-1)]
            line_of_interest = ss[-2]
            split_line_of_interest = line_of_interest.split(",")
            current_date = split_line_of_interest[0]
    return current_date

acquired_data = acquire_datasets(api_appended_links)

for dataset in acquired_data:
    if dataset[0] == "mctcr":
        MCTCR = GetMCTCR_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "mvrvz":
        MVRVZ = GetMVRVZ_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "puell":
        PUELL = GetPuell_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "sthnupl":
        STHNUPL = GetSTHNUPL_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "lthnupl":
        LTHNUPL = GetLTHNUPL_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "mfrp":
        MFRP = GetMFRP_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "psip":
        PSIP = GetPSIP_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "tsla":
        TSLA = GetTSLA_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "rp":
        RP = GetRP_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "cvdd":
        CVDD = GetCVDD_data(dataset)


for dataset in acquired_data:
    if dataset[0] == "nvt":
        NVT = GetNVT_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "rc":
        RC = GetRC_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "price":
        PRICE = GetPrice_data(dataset)

date_time = GetCurrentDate(api_appended_links)

BinaryIndicators = (CVDD + NVT + RP + TSLA + PSIP)/5
Non_BinaryIndicators = (RC + MCTCR + MVRVZ + PUELL + STHNUPL + LTHNUPL + MFRP)/7
IndicatorMetric = (BinaryIndicators + Non_BinaryIndicators)/2
if (IndicatorMetric * 100) > 85:
    tcolor = "red"
elif (IndicatorMetric *100) >70:
    tcolor = "orange"
elif (IndicatorMetric*100) > 50:
    tcolor = "yellow"
else:
    tcolor = "green"
indicator_metric_string = str((round(IndicatorMetric*100,2))) + "%"
print("Pierce's Modulus for " +  date_time + " is " + colored(indicator_metric_string, tcolor) + ". Greater than 70% indicates highly probable sell.")
if tcolor == "red":
    print("You should fucking sell right now")
elif tcolor == "orange":
    print("probably hold, but be careful")
elif tcolor == "yellow":
    print("hodl")
elif tcolor == "green":
    print("hodlllll")
print("\nIf one or more of these indicators is red, there is cause for alarm")

output_string = ""
for dataset in acquired_data:
    values = dataset[1]
    if dataset[0] == "price":
        value_of_interest = values[-2]
    else:
        value_of_interest = values[-1]
    output_string = output_string+ value_of_interest+ ","

print(output_string)


finish = input("Press enter to close the window...")
