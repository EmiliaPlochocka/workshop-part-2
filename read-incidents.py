import csv

from functions import swedishNumberStringsToFloat

with open('network_incidents.csv', encoding='utf-8') as f:
    networkIncidents = list(csv.DictReader(f))

conversion = [{
    'affectedUsers': swedishNumberStringsToFloat(number['affected_users']),
    'costSek': swedishNumberStringsToFloat(number['cost_sek']),
    'impactScore': swedishNumberStringsToFloat(number['impact_score'])
} for number in networkIncidents]


# Site ID and analysis period
#for site in networkIncidents:
#    print(site['site'], site['week_number'])

# Sum incidents per severity
countersSeverity = {}
for severityTypes in networkIncidents['severity']:
    severity = 
    if severity not in countersSeverity:
        countersSeverity[severity] = 0
    countersSeverity[severity] +=1

# Affected over 100 people
affectedIncidents = [number for number in conversion
                     if (number['affectedUsers']) > 100]

# Most expensive
expensiveIncidents = [number for number in conversion
                      if (number['costSek'])]
# Total cost of incidents
costSekInt = (int(number['cost_sek']) for number in networkIncidents)
incidentSum = (sum(costSekInt) for number in networkIncidents)
print (costSekInt)