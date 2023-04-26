import http.client
import json

conn = http.client.HTTPSConnection("one.ufl.edu")
url = "/apix/soc/schedule/?category=CWSP&term=2238&ge-h=true"
# Make request to the API
conn.request("GET", url)
response = conn.getresponse()
data = response.read()

# Parse the JSON data
parsed_data = json.loads(data)
total_rows = parsed_data[0]["TOTALROWS"]
remaining_rows = total_rows

while True:
    # Do something with the retrieved data here...
    #print(parsed_data)

    retrieved_rows = parsed_data[0]["RETRIEVEDROWS"]
    remaining_rows -= retrieved_rows
    # Check if there are remaining rows
    if remaining_rows <= 0:
        break

    last_control_num = parsed_data[0]["LASTCONTROLNUMBER"]
    print(last_control_num)
    # Update the URL with the last control number
    url = f"/apix/soc/schedule/?category=CWSP&term=2238&ge-h=true&last-control-number={last_control_num}"
    print(url)

    # Make request to the API with the updated URL
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read()
    # Parse the JSON data again
    parsed_data = json.loads(data)


'''import http.client
import json

conn = http.client.HTTPSConnection("one.ufl.edu")

# conn.request("GET", "/apix/soc/schedule/?category=CWSP&term=2238")
conn.request("GET", "/apix/soc/schedule/?category=CWSP&term=2238&ge-h=true&last-row=10")

res = conn.getresponse()
data = res.read()
# Parse the JSON data
parsed_data = json.loads(data)
# print(parsed_data)

# see raw data contents
# print(data.decode("utf-8"))

last_control_num = parsed_data[0]["LASTCONTROLNUMBER"]
total_rows = parsed_data[0]["TOTALROWS"]
retrieved_rows = parsed_data[0]["RETRIEVEDROWS"]
remaining_rows = total_rows - retrieved_rows
'''


''' FUNCTIONAL
# Create a dictionary of dictionaries, this collects genEd courses if there are any
gen_ed_courses = {}
for course in parsed_data[0]['COURSES']:
    if 'genEd' in course:
        for tag in course['genEd']:
            if tag not in gen_ed_courses:
                gen_ed_courses[tag] = {}
            gen_ed_courses[tag][course['code']] = course

# Print the dictionary of dictionaries
print(gen_ed_courses)
'''

''' printing data --- testing
print(data.decode("utf-8"))

for i in range(len(parsed_data[0]["COURSES"])):
    print(parsed_data[0]["COURSES"][i]["name"])
    print([i])
'''