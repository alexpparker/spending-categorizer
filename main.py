import json

# Introduction
print("Welcome to our chase csv categorizer!\n"
"For each entry, input the key which corresponds with the correct category for \
that spend. If you want to skip an entry, then type \"skip\" or if you want to \
stop completely, type \"stop\".")

# Categories dictionary
categories = {
    "cof": ["coffee", 0],
    "cow": ["coworking", 0],
    "f": ["flights", 0],
    "g": ["groceries", 0],
    "o": ["other", 0],
    "p": ["phone", 0],
    "ren": ["rent", 0],
    "res": ["restaurants", 0],
    "s": ["subscriptions", 0],
    "t": ["transportation", 0],
    "u": ["utilities", 0]
}

spendings = json.load(open("spendings.json"))


new_csv = input("Enter your csv file name within chase_csv without extension: ")
# Error handling
while True:
    try:
        fh = open("chase_csv/" + new_csv + ".csv")
        next(fh)
        break
    except:
        new_csv = input("Invalid input, try again: ")

for line in fh:
    line = line.strip().split(",")
    date, _, establishment, chase_category, _, charge = line

    spending_category = spendings.get(establishment + "_" + chase_category)
    if spending_category is not None:
        categories[spending_category][1] += float(charge)
        categories[spending_category][1] = round(categories[spending_category][1], 2)
        print("Saved a decision")
        continue

    print("\n", date, establishment, chase_category, charge, "\n")
    # Displaying all the available options
    for key, value in categories.items():
        print("(", key, ") - ", value[0], sep="")

    input_cat = input("Category: ")

    if input_cat == "stop":
        break
    if input_cat == "skip":
        continue
    while True:
        try:
            categories[input_cat][1] += float(charge)
            break
        except:
            input_cat = input("Invalid input, try again: ")

    categories[input_cat][1] = round(categories[input_cat][1],2)
    spendings[establishment + "_" + chase_category] = input_cat

print("\nThis month you spent the following amounts:\n")
total = 0
for category in categories.values():
    total += category[1]
    print("For ", category[0], " you spent $", category[1], sep="")

print("\nYou spent a total of $", round(total, 2), " this month.", sep="")

open("spendings.json", "w").write(json.dumps(spendings, indent = 4))
