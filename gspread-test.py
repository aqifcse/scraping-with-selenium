import gspread

gc = gspread.service_account(filename='creds.json')

sh = gc.open('scrapetosheets').sheet1

sh.append_row(['First', 'Second', 'Third'])

