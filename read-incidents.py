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

# loop though each incident entry from CSV file
for incident in networkIncidents:
    # get site name from CSV file
    site = incident['site']
    # get week number and convert to integer
    try:
        week = int(incident['week_number'])
    # if conversion fails (ex. empty data), skip
    except:
        continue
    # if given site name is not in dictionary yet, add
    if site not in analysisPeriod:
        analysisPeriod[site] = {'min': week, 'max': week}
    # if site name is present in dictionary, compare and update week range
    else:
        if week < analysisPeriod[site]['min']:
            analysisPeriod[site]['min'] = week
        if week > analysisPeriod[site]['max']:
            analysisPeriod[site]['max'] = week

# after looping through incidents, display week ranges
print("Analysis periods per site:")
for site, weeks in analysisPeriod.items():
    print(f"- {site}: {weeks['min']}-{weeks['max']}")


#___COUNT OF INCIDENTS PER SEVERITY LEVEL___
# create empty counter
counterSeverity = {}

for incident in networkIncidents:
    # normalize text to lowercase
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
# list comprehension to filter out incidents that affected fewer than 100 users
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

print("\n Incidents affecting more than 100 users:")
for inc in incidentSummaries:
    print(f"- {inc['site']} | {inc['device']} | {inc['description']} ({inc['affectedUsers']} users)")


#___MOST EXPENSIVE INCIDENTS___
# create a field where the value of cost is converted to float
for incident in networkIncidents:
    incident['costFloat'] = swedishNumberStringsToFloat(incident['cost_sek'])

# sort descending by costFloat
# can use lambda or def function
sortedByCost = sorted(networkIncidents, key=lambda x: x['costFloat'], reverse=True)
# choose 5 most expensive incidents
topExpensive = sortedByCost[:5]

print("\n 5 most expensive incidents:")
for inc in topExpensive:
    print(f"- {inc['site']} | {inc['device_hostname']} | {inc['description']} | Cost: {inc['cost_sek']}")


#___TOTAL COST___
totalCost = 0.0
# loop through data and add up cost_sek in float format to totalCost
for incident in networkIncidents:
    try:
        cost = swedishNumberStringsToFloat(incident['cost_sek'])
        totalCost += cost
    except:
        continue

# .2f - display up to two decimal spaces
# , - add comma as 000s separator
print(f"\n Total incident cost: {totalCost:,.2f} SEK")


#___AVERAGE RESOLUTION TIME PER SEVERITY LEVEL___
# create dictionary where key = severity, value = list of resolution times
resolutionTime = {}
for incident in networkIncidents:
    severity = incident['severity']
    try:
        minutes = float(incident['resolution_minutes'])
    except:
        continue
    if severity not in resolutionTime:
        resolutionTime[severity] = []
    resolutionTime[severity].append(minutes)

print("\n Average resolution time per severity:")
for severity, times in resolutionTime.items():
    avgTime = round(sum(times) / len(times), 1) if times else 0
    print(f" {severity}: {avgTime} minutes")


#___OVERVIEV PER SITE___
# summarize incidents by location
siteSummary = {}
for incident in networkIncidents:
    site = incident['site'].strip()
    cost = swedishNumberStringsToFloat(incident['cost_sek'])
    resolution = 0
    try:
        resolution = int(incident['resolution_minutes'])
    except:
        resolution = 0

    # if new site, create entry
    if site not in siteSummary:
        siteSummary[site] = {
            'incidents': 0,
            'totalCost': 0,
            'totalResolution': 0
        }
    # update counters
    siteSummary[site]['incidents'] += 1
    siteSummary[site]['totalCost'] += cost
    siteSummary[site]['totalResolution'] += resolution

print("\n Overview per site:")
for site, data in siteSummary.items():
    avgResolution = data['totalResolution'] / data['incidents'] if data['incidents'] > 0 else 0
    print(f"{site}: {data['incidents']} incidents, "
    f"totalCost {data['totalCost']:.2f} SEK, "
    f"averageResolution {avgResolution:.1f} min")


#___AVERAGE IMPACT SCORE PER CATEGORY___
categoryImpact = {}
for incident in networkIncidents:
    category = incident['category'].strip()
    impact = swedishNumberStringsToFloat(incident['impact_score'])
    
    # create entry if category missing
    if category not in categoryImpact:
        categoryImpact[category] = {
            'totalImpact': 0,
            'count': 0
        }
    # sum impact and count
    categoryImpact[category]['totalImpact'] += impact
    categoryImpact[category]['count'] += 1

print("\n Average impact score per category:")
for category, data in categoryImpact.items():
    avgImpact = data['totalImpact'] / data['count'] if data['count'] > 0 else 0
    print(f" {category}: {avgImpact:.2f}")


#___WRITE SUMMARY IN CSV___
with open('network_incidents_overview.csv', 'w', encoding='utf-8') as f:
    fieldnames = ['site', 'incidents', 'total_cost', 'avg_resolution_minutes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
  
    # write column headers
    writer.writeheader()
    #write summarized data row by row
    for site, data in siteSummary.items():
        avgResolution = data['totalResolution'] / data['incidents'] if data['incidents'] > 0 else 0
        writer.writerow({
            'site': site,
            'incidents': data['incidents'],
            'total_cost': round(data['totalCost'], 2),
            'avg_resolution_minutes': round(avgResolution, 1)
        })