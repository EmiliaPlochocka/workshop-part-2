# import library responsible for writing/reading csv files in Python
import csv
# import functions from functions.py
from functions import safe_int
from functions import swedishNumberStringsToFloat
# open network_incidents.csv, read as a list of dictionary items to variable 'networkIncidents'
with open('network_incidents.csv', encoding='utf-8') as f:
    networkIncidents = list(csv.DictReader(f))


#___SITES AND PERIOD OF ANALYSIS___
# create empty dictionary to store analysis period per site
analysisPeriod = {}

# loop though each line from csv file
for incident in networkIncidents:
    # get site name from csv file
    site = incident['site']
    # get week number and convert to int
    try:
        week = int(incident['week_number'])
    # if not possible (ex. empty row), skip
    except:
        continue
    # if given site name is not in dictionary, add
    if site not in analysisPeriod:
        analysisPeriod[site] = {'min': week, 'max': week}
    # if site name is present in dictionary, check if week number
    # happens to be lesser or higher than current 'week value'
    else:
        if week < analysisPeriod[site]['min']:
            analysisPeriod[site]['min'] = week
        if week > analysisPeriod[site]['max']:
            analysisPeriod[site]['max'] = week

# after looping through data and filling the dictionary, print output
print("Analysis periods per site:")
for site, weeks in analysisPeriod.items():
    print(f"- {site}: {weeks['min']}-{weeks['max']}")


#___COUNT OF INCIDENTS PER SEVERITY SCORE___
# create empty counter
counterSeverity = {}
for incident in networkIncidents:
    # convert upper to lower case
    severity = incident['severity'].strip().lower()
    # if a severity level not present in dictionary, add with starting value of 0
    if severity not in counterSeverity:
        counterSeverity[severity] = 0
    # if severity level present, add 1 to counter
    counterSeverity[severity] +=1

# display results with capitalization
print("\n Number of incident per severity level:")
for severity, count in counterSeverity.items():
    print(f"- {severity.capitalize()}:{count}")


#___INCIDENTS AFFECTING >100 USERS___
# create list comprehension to filter out incidents that affected fewer than 100 users
impactfulIncidents = [
    incident for incident in networkIncidents
    # use function safe_int to ignore empty variables
    if safe_int(incident['affected_users']) > 100
]
# create a list with dictionaries containing basic info about incidents
# and containing safe_int to ignore empty variables
incidentSummaries = [
    {
        'site': inc['site'],
        'device': inc['device_hostname'],
        'description': inc['description'],
        'affectedUsers': safe_int(inc['affected_users'])
    } for inc in impactfulIncidents
]
print("\nIncidents affecting more than 100 users:")
for inc in incidentSummaries:
    print(f"- {inc['site']} | {inc['device']} | {inc['description']} ({inc['affectedUsers']} users)")


#___MOST EXPENSIVE INCIDENTS___
# create a list where the value of cost is converted to float
for incident in networkIncidents:
    incident['costFloat'] = swedishNumberStringsToFloat(incident['cost_sek'])

# sort through the list as the value of cost is falling
# can use lambda or def function
sortedByCost = sorted(networkIncidents, key=lambda x: x['costFloat'], reverse=True)
# choose 5 most expensive incidents
topExpensive = sortedByCost[:5]

print("\n 5 most expensive incidents:")
for inc in topExpensive:
    print(f"- {inc['site']} | {inc['device_hostname']} | {inc['description']} | Cost: {inc['cost_sek']}")


#___TOTAL COST___
totalCost = 0.0
for incident in networkIncidents:
    try:
        cost = swedishNumberStringsToFloat(incident['cost_sek'])
        totalCost += cost
    except KeyError:
        continue
# .2f - display up to two decimal spaces
# , - add comma as 000s separator
print(f"\n Total incident cost: {totalCost:,.2f} SEK")