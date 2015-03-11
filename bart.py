import os
import urllib2
import urllib
import random
from cert import KEY
from lxml import etree


def pack(url, params):
    if not params:
	return url
    return url + '?' + urllib.urlencode(params)

PATH = "http://api.bart.gov/api/etd.aspx"

default_params = {
    'cmd':'etd',
    'orig':'ASHB',
    'key':KEY,
    'dir':'s'
}

fun_strings = [
	"YOU! BETTER RUN TO BART. TRAIN LEAVES IN %s minutes",
	"OH DIGGITY IGGITY! LOOK AT THE TIME! DEPARTURE IN %s",
	"Tee minus %s minutes until BART TRAIN",
	"HEY YOU! STOP READING REDDIT AND GO TO FUCKING WORK! %s minutes",
	"WHOOP WHOOP ALL HANDS WHOOP WHOOP ALL HANDS. CODE RED. BART INBOUND. LAUNCH ALL ZIGS. %s till impact. LAUNCH ALL ZIGS  WHOOP WHOOP CODE RED WHOOP WHOOP",
	"GOOD NEWS EVERYONE! IF YOU BRUSH YOUR TEETH AND SPRINT OUT THE DOOR YOU CAN STILL MAKE THE TRAIN. %s mins until it leaves!",
	"GONNA GO FOR A WALK NOW THE SUMMER SUN CALLIN MY NAME, BE HAPPY NOW.  GO GET THAT WORLD! %s till BART!"
]
def departure_times():
    res = urllib.urlopen(pack(PATH, default_params))
    xml_res = res.read()
    root = etree.fromstring(xml_res)
    minutes=root.findall('.//minutes')
    if minutes is None:
	print "BAD RESPONSE: %s" % etree.tostring(root, pretty_print=True) 
	return []

    int_mins = []
    for m in minutes:
        if m.text == "Leaving":
		int_mins.append(0)
        else:
            int_mins.append(int(m.text))

    return int_mins


def main():
    departs = departure_times()
    print departs   
    relevent_departs = [depart  for depart in departs if depart in [9]]

    if any(relevent_departs):
	saystr = random.choice(fun_strings) % min(relevent_departs)
        print saystr
	os.system("""espeak '%s'""" % saystr)


main()
