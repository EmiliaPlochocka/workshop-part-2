# declare function that coverts numbers with space as separators
# and commas as decimal separators to float
def swedishNumberStringsToFloat(string):
    try:
        return float (string.replace(' ','').replace(',','.'))
    except:
        return 0

# declare function that ignores empty variables 
def safe_int(value, default=0):
    try:
        return int(value) if value else default
    except ValueError:
        return default