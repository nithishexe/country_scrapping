from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
import json

def fetch_data(capital):
    if "<ul>" in capital:
        capital = capital.split("<ul>")[1].split("</ul>")[0]
    return BeautifulSoup("<ul>" + capital + "</ul>", 'html5lib')

def join_list(data):
    if len(data) == 1:
        return data[0]
    return data

def country_data(request, country_name):
    URL = "https://en.wikipedia.org/wiki/" + str(country_name)
    r = requests.get(URL)
    html = r.text.replace("&#160;", "")
    soup = BeautifulSoup(r.content, 'html5lib')
    country_details = {}
    country_details["flag_link"] = soup.find(
        'meta', property="og:image")["content"]
    country_details["capital"] = []
    try:
        capital = html.split(">Capital<")[1].split("Largest city")[0]
        capital = fetch_data(capital)
        for capi in capital.ul.find_all("a"):
            try:
                country_details["capital"].append(
                    str(capi["title"].encode("ascii", "ignore")))
            except:
                continue
        country_details["capital"] = join_list(country_details["capital"])
    except:
        country_details["capital"] = ""

    country_details["largest_cities"] = []
    try:
        capital = html.split(">Largest city<")[1].split("Officiallanguages")[0]
        capital = fetch_data(capital)
        for city in capital.find_all("a"):
            try:
                country_details["largest_cities"].append(
                    str(city["title"].encode("ascii", "ignore")))
            except:
                continue
        country_details["largest_cities"] = join_list(
            country_details["largest_cities"])
    except:
        country_details["largest_cities"] = ""

    try:
        capital = html.split("Officiallanguages")[1].split("</div>")[0]
        capital = fetch_data(capital)
        country_details["offiacial_languages"] = []
        for city in capital.find_all("a"):
            try:
                country_details["offiacial_languages"].append(
                    str(city["title"].encode("ascii", "ignore")))
            except:
                continue
        country_details["offiacial_languages"] = join_list(
            country_details["offiacial_languages"])
    except:
        country_details["offiacial_languages"] = ""

    try:
        country_details["total_area"] = str(html.split(
            ">Area <")[1].split('infobox-data">')[1].split("<")[0])
    except:
        country_details["total_area"] = ""

    try:
        country_details["population"] = str(html.split(
            ">Population<")[1].split('infobox-data">')[1].split("<")[0])
    except:
        country_details["population"] = ""

    try:
        country_details["gdp_nominal"] = "$" + \
            str(html.split("(nominal)")[1].split("$")[1].split("<")[0])
    except:
        country_details["gdp_nominal"] = ""

    print(country_details)
    context = {"status_code": 200, "country_details": country_details}
    return HttpResponse(json.dumps(context))
