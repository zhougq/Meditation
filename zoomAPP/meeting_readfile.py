
item_list = []

file_name = "meeting_registrant.csv"

with open(file_name, "r") as f:
    for line in f:
        item_list = line.split(',')
        item_email = item_list[0]
        item_first_name = item_list[1]
        item_last_name = item_list[2]