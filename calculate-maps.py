#! python3
# Launches a map in the browser using an address from the
# command line or clipboard.
import webbrowser, sys, pyperclip, itertools, re
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

possible_perms_no_bookend = list(itertools.permutations(mobile_list, len(mobile_list)))
print("Possible perms with no bookend")
print(possible_perms_no_bookend)
possible_perms = []
for perm in possible_perms_no_bookend:
    possible_perms.append((start, *perm , end))
print(possible_perms)

#Now we have our possible permutations, let's get selenium to open them all and read the transit time for each
browser = webdriver.Chrome()
regex = re.compile(r'\d+(?:\.\d+)?')
time_list = []
for perm in possible_perms:
    url_params = "/".join(perm)
    print("URL params: " + url_params)
    browser.get(url='https://www.google.com/maps/dir/' + url_params)
    element = browser.find_element_by_class_name("xB1mrd-T3iPGc-iSfDt-n5AaSd")
    text = element.text
    print("Element text:" + text)
    if "hr" in text:
        #we have an hour marker so let's ensure we're properly converting into minutes
        numbers = [int(s) for s in text.split() if s.isdigit()]
        time = numbers[0] * 60 + numbers[1]
    else:
        time = regex.findall(text)[0]
    print("Stripped text: " + str(time))
    time_list.append(int(time))

#Now that we have data from selenium, let's find the best path and return it to the user

best_time_index = time_list.index(min(time_list))
best_perm = possible_perms[best_time_index]
best_address = 'https://www.google.com/maps/dir/' + "/".join(best_perm)

webbrowser.open(best_address)