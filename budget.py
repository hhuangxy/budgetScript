import csv
import os.path
from sys import argv, exit

FOOD = [
  "A & W",
  "A&W",
  "BAKERY",
  "BAR",
  "BBQ",
  "BISTRO",
  "BREW",
  "CACTUS CLUB",
  "CHURCH'S CHICKEN",
  "COCKNEY KINGS",
  "DENNY'S",
  "EAST IS EAST",
  "FATBURGER",
  "GRILL",
  "ICE CREAM",
  "INSADONG",
  "KFC",
  "KISHIMOTO",
  "LIQUOR",
  "MCDONALD",
  "MENCHIE",
  "MEXICAN",
  "PANAGO",
  "PIZZA",
  "PMC SIERRA",
  "PUB",
  "RED ROBIN",
  "RESTAURAN",
  "STARBUCKS",
  "SUBWAY",
  "SUN SUI WAH",
  "SUPERSTORE",
  "SUSHI",
  "T&T",
  "THAI",
  "THE LAST CRUMB",
  "TOMOKAZU",
  "WHITE SPOT",
  "ZIPANG PROVISIONS"
]

GAS = ['CHEVRON', 'ESSO', 'PETROCAN']

UTILITIES = ['7 ELEVEN CANADA', 'TELUS', 'SHAW']

ELECTRONICS = ['ELECTRONIC', 'FARNEL', 'NCIX']

TRANSPORTATION = ['HONDA', 'PARKING']

ENTERTAINMENT = ['CINEPLEX', 'FAMOUS PLAYER', 'STEAMGAMES']

CLOTHING = ["MARK'S WORK WEARHOUSE", 'NEW BALANCE']

INSURANCE = ['ICBC']

MEDICAL = ['DR A.C.K. CHEUNG', 'FALSE CREEK EYE CARE', 'KINTEC FOOTLABS', 'PHARMASAVE']

HOUSEHOLD = ['BED BATH & BEYOND', 'CDN TIRE STORE', 'HOME DEPOT', 'IKEA', 'PIER 1 IMPORTS']

PERSONAL = []

GIFTS = []

MISC = []

catTable = [FOOD, GAS, UTILITIES, ELECTRONICS, TRANSPORTATION, ENTERTAINMENT,
            CLOTHING, INSURANCE, MEDICAL, HOUSEHOLD, PERSONAL, GIFTS, MISC]

outHdr = ['Date', 'Description', 'Food', 'Gas', 'Utilities', 'Electronics', 'Transportation',
          'Entertainment', 'Clothing', 'Insurance', 'Medical', 'Household', 'Personal', 'Gifts', 'Misc', 'Adjustments', 'Uncat']

outMonth = [['Jan'], ['Feb'], ['Mar'], ['Apr'], ['May'], ['Jun'], ['Jul'], ['Aug'], ['Sep'], ['Oct'], ['Nov'], ['Dec']]


##########################################################
# Searches through list of categories and returns the ID #
##########################################################
def catSearch(catTable, desc):
  for cat in catTable:
    for type in cat:
      if type in desc:
        return catTable.index(cat)
  return -1


###########################
# Main budget categorizer #
###########################
def budget(inFile):
  with open(inFile, 'rU') as fh:
    fcsv = csv.reader(fh, delimiter=',')
    for row in fcsv:
      [date, desc, monOut, monIn] = row[0:4]
      if 'PAYMENT - THANK YOU' in desc:
        # Payment, ignore
        print 'Ignored: %r' % row
        continue
      if 'ANNUAL CASH REBATE' in desc:
        # Rebate, ignore
        print 'Ignored: %r' % row
        continue
      # Set up output
      outRow = ['']*len(outHdr)
      outRow[0] = date
      outRow[1] = desc
      if monIn != '':
        # Catch money coming in, put in Uncat
        outRow[-1] = -float(monIn)
      else:
        # Search through categories
        catID = catSearch(catTable, desc)
        if catID == -1:
          # Uncat
          outRow[-1] = monOut
        else:
          outRow[2+catID] = monOut
      # Prepare output
      month = int(date.split('/')[0])-1
      outMonth[month].append(outRow)


#########################
# Write outMonth to CSV #
#########################
def toCSV(outFdr):
  for month in outMonth:
    if len(month) > 1:
      # Something for this month
      outFName = outFdr + '/' + month[0] + '.csv'
      outFName = os.path.normpath(outFName)
      if os.path.isfile(outFName):
        outMode = 'ab'
      else:
        outMode = 'wb'
      # Append/Write to file
      with open(outFName, outMode) as fh:
        fcsv = csv.writer(fh, delimiter=',')
        # Write a header
        if outMode == 'wb':
          fcsv.writerow(outHdr)
        fcsv.writerows(month[1:])
      print month[0] + ' Success!'

if __name__ == "__main__":
  if len(argv) == 2:
    argv.append('.')
  elif len(argv) == 3:
    # OK
    pass
  else:
    print 'Invalid Arguments'
    print 'python budget.py <input file> <output folder>'
    exit()

  budget(argv[1])
  toCSV(argv[2])
