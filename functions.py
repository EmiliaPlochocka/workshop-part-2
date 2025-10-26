# declare function that coverts numbers with space as separators
# and commas as decimal separators to float
def swedishNumberStringsToFloat(string):
    # remove spaces and replace comma with dot
    try:
        return float (string.replace(' ','').replace(',','.'))
    except:
        # if conversion fails, return 0
        return 0

# declare function that safely converts str to int and ignores invalid values 
def safe_int(value, default=0):
    try:
        # return int if valid, otherwise default (0)
        return int(value) if value else default
    except ValueError:
        return default