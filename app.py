# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    #baseurl = "https://query.yahooapis.com/v1/public/yql?"
    #yql_query = makeYqlQuery(req)
    #if yql_query is None:
     #   return {}
    definition = define(req) 

    #yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    #result = urlopen(yql_url).read()
    #data = json.loads(result)
    res = makeWebhookResult(definition)
    return res

'''
def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
'''

def define(req):
    result = req.get("result")
    parameters = result.get("parameters")
    n = parameters.get("define")
    if n is None:
        return None

    if n == "SEO":
        return "definition of SEO"
    elif n == "ABPCO":
        return "ABPCO is the Association of British Professional Conference Organisers"
    elif n == "ABTA":
        return "ABTA is the Association of British Travel Agents"
    elif n == "ADR":
        return "ADR (or ARR) is the Average Daily Rate, or Average Room Rate (calculated by dividing revenue generated from income from hotel rooms sold by the total number of rooms sold)"
    elif n == "ADS":
        return "ADS is an Alternative Distribution System.  The Internet and other non-GDS electronic channels of hotel distribution. Also known as IDS (Internet Distribution System"
    elif n == "Advance Rates":
        return "Advance Rates are generally discounted rates to encourage guests to book in advance."
    elif n == "AGOP":
        return "AGOP stands for Adjusted Gross Operating Profit (equal to the gross operating profit minus the hotel management base fee and any additional expenses)"
    elif n == "AI":
        return "AI stands for Artificial Intelligence - like me! 🤖"
    elif n == "Allocation":
        return "Allocation usually refers to an ‘allocation of rooms’ (e.g a conference or group may have an allocation of rooms at an agreed rate)"
    elif n == "Alternative availability":
        return "Alternative availability generally refers to alternative properties showing when the requested property is unavailable for sale (perhaps it's occupancy is 100% - i.e it's full)"
    elif n == "Amadeus":
        return "Amadeus is a common GDS (Global Distribution System)"
    elif n == "ARI":
        return "ARI stands for either Average Rate Index or Availability, Rates and Inventory, depending on the context"
    elif n == "ATL":
        return "ATL stands for Above The Line and generally refers to mass marketing campaigns that are used to drive awareness, rather than drive direct sales. BTL (Below The Line) campaigns are more focused on ROI (Return on Investment)."
    elif n == "ARR":
        return "ARR stands for Average Room Rate. It's the total room revenue divided by the number of rooms occupied, excluding any rooms offered complimentary."
    elif n == "B2B":
        return "B2B stands for Business to Business. In the context of hotels it could refer to corporate business, e.g. a hotel agreeing a rate to sell rooms to a company for their employees."
    elif n == "B2C":
        return "B2C stands for Business to Consumer. In the context of hotels this could refer to most leisure transactions where a hotel is selling available rooms to the general public."
    elif n == "B&B":
        return "B&B stands for Bed and Breakfast. It refers to rates or offers that include accommodation and breakfast."
    elif n == "Back of House":
        return "Back of House refers to an area of the hotel that is generally off limits to guests (e.g kitchens, offices, storage etc.)"
    elif n == "BAR":
        return "BAR in the context of rates and offers refers to the Best Available Rate (s). Typically these are rates that are the ‘best available’ at the time of booking and are often higher than advance purchase rates/offers. Of course, 'bar' could also refer to the hotel bar! 🍸"
    elif n == "Base Fee":
        return "Base Fee is an agreed upon hotel management fee earned by the hotel operator."
    elif n == "BDE":
        return "BDE stands for Business Day End. i.e. Get me that report for BDE please!"
    elif n == "Benchmarking":
        return "Benchmarking refers to activity to compare your hotel against competitors. This could include benchmarking by product/service, room rate, quality etc."
    elif n == "BEO":
        return "BEO refers to a Banquet Event Order"
    elif n == "BHA":
        return "BHA stands for British Hospitality Association"
    elif n == "Boutique Hotels":
        return "Boutique Hotels tend to be smaller (around 10-100 rooms) luxury hotels that differentiate themselves by their service and product offering. For example, a boutique hotel may have a specific theme or style - ultra modern, chic etc."
    elif n == "BSC":
        return "BSC stands for Balanced Scorecard - a performance management tool for managers."
    elif n == "BTL":
        return "BTL stands for Below The Line and generally refers to a marketing campaign that is focused on return on investment. The opposite is an ATL (Above The Line) campaign which focuses on driving awareness."
    elif n == "Business Guest":
        return "Business Guest/Traveller simply refers to those travelling for business as opposed to leisure."
    elif n == "BOB":
        return "BOB stands for Business On (The) Books and refers to revenue that's confirmed."
    elif n == "Cache":
        return "Cache (or caching) refers to a method to temporarily store information. Types of information cached often includes HTML pages, images, rates and inventory. Can reduce the volume of direct system queries by allowing requests to be satisfied by extracting information from the cache (speeding up processes for guests)"
    elif n == "C&B":
        return "C&B (or C and B) refers to Conference and Banqueting."
    elif n == "C&E":
        return "C&E (or C and E) refers to Conference and Events."
    elif n == "C&I":
        return "C&I (or C and I) refers to Conference and Incentive bookings."
    elif n == "CDP":
        return "CDP can refer to either of the following (dependent on context); 1. Chef de Partie (in charge of a particular area of production within the kitchen) 2. Current Day Processing"
    elif n == "Chain Code":
        return "A Chain Code is a two letter code used in distribution systems to identify a hotel chain. A property needs to be associated with a chain code to be listed in a GDS (Global Distribution System). HEDNA (Hotel Electronic Distribution Networking Association) administers the list of available chain codes."
    elif n == "Channel Management":
        return "Channel Management refers to the process a hotel uses to update ARI (Availability, Rates and Inventory) in various distribution channels."
    elif n == "Chatbot":
        return "A Chatbot, also known as a chatterbot, talkbot, artificial conversational entity is a service that simulates the behaviour of a human within a conversational environment. I think they're amazing. But then I may be a little biased. 🤖"
    elif n == "Check In":
        return "Check In is the process by which a guests registers their arrival at a hotel and receives their key/keycards."
    elif n == "Check Out":
        return "Check Out is the process by which a guest leaves the hotel, settles their bill and hands back any key/keycards."
    elif n == "CMP":
        return "CMP can stand for either of the following, dependent on context; - 1. Certified Meeting Professional – an internationally recognised credential conferred upon an individual by the Convention Industry Council. - 2. Complete Meeting Package – a per person charge, usually with a conference center, that includes the individual’s room, food and beverage, and proportional share of all other charges (room rental, technology, etc.)"
    elif n == "CMS":
        return "CMS stands for Content Management System. This is a system used to update a website, digital platform or Contract Management System (keeps track of contracts and agreements)"
    elif n == "Commis Chef":
        return "Commis Chef  refers to a basic chef in larger kitchens. May have just completed training or part of a training process."
    elif n == "Comp":
        return "Comp usually refers to complimentary - i.e. given for free. It could also be an abbreviation of competition, dependent on the context."
    elif n == "Competitor":
        return "Competitor refers to a rival hotel group or individual property. A Competitor Set would be a list of hotels / hotel chains that are direct competitors."
    elif n == "Corkage":
        return "Corkage is a charge place on beer, liquor, and wine brought into the facility but purchased elsewhere."
    elif n == "Corporate Rates":
        return "Corporate Rates are rates negotiated by corporates/companies with a hotel or sales team. Typically these are lower than standard consumer rates as corporates/companies can offer a high volume of annual bookings."
    elif n == "COS":
        return "COS stands for Cost of Sale."
    elif n == "Covers":
        return "Cover refers to diners within a restaurant. E.g) A hotel restaurant achieved 30 covers (30 people dined)"
    elif n == "CRM":
        return "CRM stands for Customer Relationship Management - i.e. how a hotel communicates with its guests. Commonly automated to include pre and post stay elements, along with loyalty programmes etc."
    elif n == "CRO":
        return "CRO can stand for either of the following, dependent on context; 1. Central Reservations Office – the central ‘hub’ that handles bookings of behalf of a hotel (or chain). 2. Conversion Rate Optimisation - the process of improving the ratio of those who visit a website to those who book. e.g. If you have a conversion rate of 1.5% from 1,000 visitors, that would equate to 15 bookings."
    elif n == "CRS":
        return "CRS stands for Central/Computerised Reservations System. This is the system that facilitates the booking of rooms, conference etc. This might be via telephone, website, email etc."
    elif n == "CVB":
        return "CVB stands for Convention and Visitors Bureau."
    elif n == "Day Guests":
        return "Day Guests are those that arrive and depart on the same day."
    elif n == "DBB":
        return "DBB refers to rates that include Dinner, Bed and Breakfast."
    elif n == "DDR":
        return "DDR stands for Day/Daily Delegate Rate - aper person rate for conference room hire, refreshments, catering etc."
    elif n == "Direct Connect":
        return "Direct Connect is a connection or interface that links a hotels system and a distribution system without relying on a third party switch provider."
    elif n == "DMO":
        return "DMO stands for Destination Marketing Organisation - a company/group responsible for the promotion of an area (this could be regionally, nationally or town/city specific)."
    elif n == "DMP":
        return "DMP refers to a Data Management Platform - used to better understand your hospitality/travel business data, often to achieve a single customer view."
    elif n == "DND":
        return "DND stands for Do Not Disturb ⛔"
    elif n == "Domestic Travellers":
        return "Domestic Travellers/Tourism refers to residents of a country that travel within their own country."
    elif n == "DOSM":
        return "DOSM stands for Director of Sales and Marketing."
    elif n == "EcoTourism":
        return "EcoTourism refers to socially responsible travel. Guests may opt for ‘green hotels’ who operate with sustainable practices."
    elif n == "EPO":
        return "EPO / IPO stands for Each Pays Own, Individual Pays Own."
    elif n == "ETA":
        return "ETA stands for Estimated Time of Arrival."
    elif n == "ExtranetE":
        return "An Extranet is a secured connection between two or more intranets between two companies. Commonly used by OTAs (online travel agencies) to allow hotels to maintain their rates and availability and to receive delivery of reservations."
    elif n == "F&B":
        return "F&B stands for Food and Beverage, referring to restaurant and bar business within a hotel."
    elif n == "Fam Trips":
        return "Fam (or Familiarisation) Tours/Trips generally refer to complimentary stays for corporate guests who may be considering using the hotel for their organisation (accommodation, conferences etc.)"
    elif n == "FF&E":
        return "FF&E stands for Furniture, Furnishings and Equipment."
    elif n == "FIT":
        return "FIT generally stands for Free and Independent Traveller, but could also refer to Foreign Independent Traveller or Fully Independent Traveller. Ultimately, they all define the same thing - those who travel independently. FIT's tend to design their own itineraries and arrange their own ​travel plans, looking for unique and individual experiences."
    elif n == "FOH":
        return "FOH (or Front of House) generally refers to guest facing staff or areas within the reception or public facing parts of the hotel. These may include receptionists, concierge and room porters."
    elif n == "Full Board":
        return "Full Board refers to accommodation rates and offers that includes bed, breakfast, lunch and dinner."
    elif n == "GDS":
        return "GDS stands for Global Distribution System, a network of electronic reservation systems used globally by travel agents booking hotel rooms (and airlines). Common GDS include Sabre, Galileo and Amadeus."
    elif n == "Geo-Coding":
        return "Geo-Coding is the process of identifying a hotels location using geographic coordinates expressed in degrees of longitude and latitude."
    elif n == "GM":
        return "GM stands for General Manager, the person responsible for the general running of the hotel day-to-day."
    elif n == "GOP":
        return "GOP is the Gross Operating Profit (Total revenue less expenses)"
    elif n == "GOPPAR":
        return "GOPPAR  is the Gross Operation Profit Per Available Room."
    elif n == "GOR":
        return "GOR stands for Gross Operating Revenue."
    elif n == "Group Rates":
        return "Group Rates are generally negotiated rates (discounted against standard rates) for group travel. This can include guests attending conferences, meetings, tours, large families etc."
    elif n == "GS":
        return "GS stands for Guest Services."
    elif n == "GSM":
        return "GSM stands for Guest Services Manager."
    elif n == "Half Board":
        return "Half Board is a rate that includes bed, breakfast and either lunch or dinner."
    elif n == "Head Chef":
        return "The Head Chef is in charge of the kitchen, including Sous Chef(s), Chef de Partie(s) and Commis Chef(s)."
    elif n == "HCD":
        return "HCD usually refers to a Hotel Content Database. This is a Content Management System (CMS) used to distribute static information about hotels to 3rd parties including GDS (Global Distribution Systems), OTA (Online Travel Agents), IDS (Internet Distribution Systems) and others."
    elif n == "HEDNA":
        return "HEDNA stands for the Hotel Electronic Distribution Networking Association.  This is an industry organisation formed in 1991 to advance communication training, standards, procedures and technology for the sale of hotel accommodation through electronic systems."
    elif n == "HOD":
        return "HOD stands for Head of Department."
    elif n == "Holdover":
        return "Holdovers are when a hotel may hold your room for a night, or more, should you require a broken night stay (e.g. Stay Monday, Tuesday, Thursday, Friday and room held on Wednesday)."
    elif n == "House Count":
        return "House Count refers to the total occupancy of the hotel at any given moment."
    elif n == "HSMAI":
        return "HSMAI stands for Hospitality Sales & Marketing Association International, a membership organisation founded in the USA in 1927."
    elif n == "IBE":
        return "IBE stands for Internet Booking Engine. Also known as WBE (Web Booking Engine)."
    elif n == "IDS":
        return "IDS refers to an Internet Distribution System; the Internet and other non-GDS channels of hotel electronic distribution like Intranets, Extranets and online services. Also known as ‘ADS’ (Alternate Distribution System)."
    elif n == "Independent Hotel":
        return "An Independent Hotel/Property usually refers to an individual hotel that isn’t part of a larger chain or group."
    elif n == "KPI":
        return "KPI refers to Key Performance Indicator. KPIs are targets against which success can be measured. For example, an occupancy rate of 90%, an ADR of £/$ 200 etc."
    elif n == "L2B":
        return "The L2B or L2B Ratio stands for 'Look to book'. This is the ratio of people who visit your website or CRS (Central Reservations System) divided by the number of reservations received. It's also referred to as the Conversion Rate of your website or CRS."
    elif n == "Late Arrivals":
        return "Late Arrivals are guests that advise they will be later than the agreed time of arrival. Can also be referred to as a Late Show."
    elif n == "Late Charge":
        return "A Late Charge refers to charges that may be passed on to a guest after their departure from a hotel. For example, telephone calls or mini bar charges that weren’t determined before the guest left."
    elif n == "Late Check Outs":
        return "Late Check Outs are when a guest leaves the hotel later than the agreed time of departure. This may be at an agreed ‘Late Check Out’ fee."
    elif n == "LBA":
        return "LBA stands for Local Business Agreement."
    elif n == "Lead Time":
        return "Lead Time is the length of time between when a booking is made and the actual stay date. Typically hotels prefer long lead times as it allows them to plan room inventories/rates. Depending on demand and occupancy levels, short lead times can either drive high rated business (last minute availability for a busy weeknight) or cheap last minute deals (lots of room inventory left, better to sell discounted than have an empty room!)"
    elif n == "Leisure Guest":
        return "Leisure Guests are those travelling for pleasure, rather than business."
    elif n == "Limited Service":
        return "Limited Service usually refers to a hotel that may not offer the full range of services typically expected of it. E.g no restaurant service is available."
    elif n == "L/O":
        return "L/O or LO stands for Land Only - the hotels term for not having any resort fee’s included, e.g. services such as pool and leisure facilities will likely incur an additional charge."
    elif n == "LOS":
        return "LOS (or Length of Stay) refers to the duration of a guests visit. E.g 3 nights. Sometimes special offers have a MLOS (Minimum Length of Stay)."
    elif n == "Loyalty Programme":
        return "Loyalty Programmes are rewards programme for those that stay at a hotel regularly. Rewards can vary, but typically include free stays, dining vouchers, upgrades etc."
    else:
        return "Couldn't find it."

    return{}

def makeWebhookResult(data):
    '''
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))
    '''

    speech = data

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
