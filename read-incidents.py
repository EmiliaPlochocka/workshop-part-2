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


#___LIST SITE AND PERIOD OF ANALYSIS___
#for site in networkIncidents:
#    print(site['site'], site['week_number'])

#___LIST NO. INCIDENTS FER SEVERITY SCORE___
# create empty counter
countersSeverity = {}
# 
# for severityTypes in networkIncidents['severity']:
#    severity = 
#    if severity not in countersSeverity:
#        countersSeverity[severity] = 0
#    countersSeverity[severity] +=1

#___LIST INCIDENTS AFFECTING >100 USERS___
# using list comprehension to filter incidents that affected more than 100 users
impactfulIncidents = [site for site in conversion
                     if (site['affectedUsers']) > 100]
# include site, device hostname, description and number of affected users for every site
namesImpInc = [{
    site[''] + ' '
    + site['device_hostname'] + ' '
    + site['description']
} for site in impactfulIncidents]

#+ ' ' + site'affectedUsers'
print (namesImpInc)


#___MOST EXPENSIVE INCIDENTS___
# using list comprehension to filter most expensive incidents
# !!!add conditions
expensiveIncidents = [number for number in conversion
                      if (number['costSek'])]

#___TOTAL COST___
# create dictionary containing integer costSekInt for each site
costSekInt = (int(site['cost_sek']) for number in networkIncidents)
# 
incidentSum = (sum(costSekInt) for number in networkIncidents)
# for future reference:
# for person in salaries:
# print(person['Förnamn'], person['Efternamn'], person['Månadslön'])
# salarySum += int(person['Månadslön'])
# avgSalary = round(salarySum / len(salaries))
