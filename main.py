import http.client
import requests
import json


def get_courses(conn, category):
    url = f"/apix/soc/schedule/?category={category}&term=2238"
    # Make request to the API
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read()
    # print raw data --- testing purposes
    # print(data.decode("utf-8"))

    # Parse the JSON data
    parsed_data = json.loads(data)
    total_rows = parsed_data[0]["TOTALROWS"]
    remaining_rows = total_rows

    ''' BASIC LOOP - example demonstration purposes
    for i in range(len(parsed_data[0]["COURSES"])):
        print(parsed_data[0]["COURSES"][i]["name"])
        print([i])
    '''

    # Create an empty container (will be defined to more precise data structure later) to store the courses
    courses = []

    while True:
        for course in parsed_data[0]["COURSES"]:
            instructors_list = []
            # the set below is used to check for duplicate instructors across sections before adding to instructor_list
            instructors_set = set()
            for section in course["sections"]:
                for instructor in section["instructors"]:
                    name = instructor["name"]
                    if name not in instructors_set:
                        instructors_list.append(name)
                        instructors_set.add(name)
            course_data = {
                "name": course["name"],
                "code": course["code"],
                "instructors_list": instructors_list,
                # Add any other attributes to store here
            }
            courses.append(course_data)

        retrieved_rows = parsed_data[0]["RETRIEVEDROWS"]
        remaining_rows -= retrieved_rows
        if remaining_rows <= 0:
            break

        last_control_num = parsed_data[0]["LASTCONTROLNUMBER"]
        url = f"/apix/soc/schedule/?category={category}&term=2238&last-control-number={last_control_num}"

        # Make request to the API with the updated URL
        conn.request("GET", url)
        response = conn.getresponse()
        data = response.read()
        # Parse the JSON data again
        parsed_data = json.loads(data)

    return courses


# Make the HTTP connection
connection = http.client.HTTPSConnection("one.ufl.edu")

# Get the courses for each category --- only humanities being demonstrated
humanities_courses = get_courses(connection, "CWSP&ge-h=true")
# Example looping and printing values for all humanities courses
# Print the courses
'''for course in humanities_courses:
    print(course["name"], course["code"], course["instructors_list"])'''

rate_my_prof_page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=1100")
rmp_data = json.loads(rate_my_prof_page.content)
# print(rmp_data.decode("utf-8"))
