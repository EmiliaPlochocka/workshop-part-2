# Declare function that coverts numbers with space as separators
# and commas as decimal separators to float
def swedishNumberStringsToFloat(string):
    try:
        return float (string.replace(' ','').replace(',','.'))
    except:
        return 0
    impact_score = float(string['impact_score']) if string['impact_score'] else 0.0

    
def safe_int(value, default=0):
    try:
        return int(value) if value else default
    except ValueError:
        return default