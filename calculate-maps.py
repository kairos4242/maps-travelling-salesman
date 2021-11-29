#! python3
# mapIt.py - Launches a map in the browser using an address from the
# command line or clipboard.
import webbrowser, sys, pyperclip, itertools
from selenium import webdriver
if len(sys.argv) > 1:
    # Get address from command line.
    address = ' '.join(sys.argv[1:])
else:
    # Get address from clipboard.
    address = pyperclip.paste()

print("Selected address: " + address)

# Alright now let's grab the list of place names from the URL

full_addresses = []
raw_list = address.split("/")
for i in raw_list:
    print(i)
chopped_list = raw_list[5:-2]
print("CHOP CHOP")
for i in chopped_list:
    print(i)
start = chopped_list[0]
end = chopped_list[-1]
mobile_list = chopped_list[1:-1]
print("Start: " + start, "End: " + end, "Mobile List: " + str(mobile_list))

possible_perms_no_bookend = list(itertools.permutations(mobile_list))

print(possible_perms_no_bookend)
possible_perms = []
for perm in possible_perms_no_bookend:
    possible_perms.append((start, *perm , end))
print(possible_perms)

#webbrowser.open(address)