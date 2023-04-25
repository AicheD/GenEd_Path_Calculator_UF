import http.client
import json

conn = http.client.HTTPSConnection("one.ufl.edu")

conn.request("GET", "/apix/soc/schedule/?category=CWSP&term=2238")

res = conn.getresponse()
data = res.read()

# Parse the JSON data
parsed_data = json.loads(data)

for i in range(len(parsed_data[0]["COURSES"])):
    print(parsed_data[0]["COURSES"][i]["name"])
    print([i])


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
'''