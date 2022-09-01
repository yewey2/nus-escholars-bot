import gspread

service_account = gspread.service_account(filename="googleServiceAccount.json")
workbook = service_account.open("e-scholar-bot-users")
sheet = workbook.worksheet("Sheet1")

def get_chat_ids():
    # sheet.update('A6:B6', [['yes', 41929]])
    records = sheet.get_all_records()
    # print(records)
    chat_ids = {d['username']: d['chat_id'] for d in records}
    return chat_ids

def update_chat_ids(username, chat_id):
    chat_ids = get_chat_ids()
    chat_ids[username] = int(chat_id)
    sheet.update("A2", [[key, value] for key,value in sorted(chat_ids.items())])
    return chat_ids
