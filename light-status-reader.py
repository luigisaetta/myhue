#
# Author: L. Saetta
# 25 march 2018
#
# pylint: disable=invalid-name
#
# History:
# 25/03/2018: first version
#

import json
import time
import sys
import requests
import json
import configparser

#
# Configurations
#
# time between msg send
config = configparser.ConfigParser()
config.read('./light-reader.ini')

sleepTime = 60
# read from ini file
HUE_ENDPOINT = config['DEFAULT']['hue_url']

# list of lights ID (defined by HUE bridge)
ids = ['1', '2', '3', '4', '5', '6']

counters = [0, 0, 0, 0, 0, 0]

#
# Main
#
print("*******************")
print("Starting simulation....")

count = 0

# initialize counters
for id in ids:
    counters[int(id) - 1] = 0

while True:
    count = count + 1
    
    print('*** Iteration n.', count)

    try:
        r = requests.get(url = HUE_ENDPOINT)

        resp = json.loads(r.content.decode("utf-8"))

        for id in ids:
            # rule to establish if the light is on
            is_on = resp[id]['state']['on'] and resp[id]['state']['reachable']
            
            print('Light ', id , is_on)

            if is_on:
                counters[int(id) - 1] = counters[int(id) - 1] + 1
    except:
        print('*** Error in GET !')
        print('\n')
        print('*** Error info: ', sys.exc_info()[0], sys.exc_info()[1])
    
    if count % 10 == 0:
        print('*** Counters: ')
        print(counters)

    time.sleep(sleepTime)
