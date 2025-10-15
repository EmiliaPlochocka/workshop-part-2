# import library responsible for writing/reading csv files in Python
import csv
# import function from functions.py
from functions import swedishNumberStringsToFloat
# open network_incidents.csv, read as a list of dictionary items to variable 'networkIncidents'
with open('network_incidents.csv', encoding='utf-8') as f:
    networkIncidents = list(csv.DictReader(f))
conversion = [{
    'affectedUsers': swedishNumberStringsToFloat(number['affected_users']),
    'costSek': swedishNumberStringsToFloat(number['cost_sek']),
    'impactScore': swedishNumberStringsToFloat(number['impact_score'])
} for number in networkIncidents]


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

# displey results with capitalization
print("\n Number of incident per severity level:")
for severity, count in counterSeverity.items():
    print(f"- {severity.capitalize()}:{count}")

#___LIST INCIDENTS AFFECTING >100 USERS___
# using list comprehension to filter incidents that affected more than 100 users
impactfulIncidents = [site for site in conversion
                     if (site['affectedUsers']) > 100]
# include site, device hostname, description and number of affected users for every site
#namesImpInc = [{
#    site[''] + ' '
#    + site['device_hostname'] + ' '
#    + site['description']
#} for site in impactfulIncidents]

#+ ' ' + site'affectedUsers'
#print (namesImpInc)


#___MOST EXPENSIVE INCIDENTS___
# using list comprehension to filter most expensive incidents
# !!!add conditions
expensiveIncidents = [number for number in conversion
                      if (number['costSek'])]

#___TOTAL COST___
# create dictionary containing integer costSekInt for each site
#costSekInt = (int(site['cost_sek']) for number in networkIncidents)
# 
#incidentSum = (sum(costSekInt) for number in networkIncidents)
# for future reference:
# for person in salaries:
# print(person['Förnamn'], person['Efternamn'], person['Månadslön'])
# salarySum += int(person['Månadslön'])
# avgSalary = round(salarySum / len(salaries))
