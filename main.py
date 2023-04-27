import http.client
import json


def get_courses(conn, category):
    url = f"/apix/soc/schedule/?category={category}&term=2238"
    # Make request to the API
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read()

    # Parse the JSON data
    parsed_data = json.loads(data)
    total_rows = parsed_data[0]["TOTALROWS"]
    remaining_rows = total_rows

    ''' printing data --- testing
    print(data.decode("utf-8"))

    for i in range(len(parsed_data[0]["COURSES"])):
        print(parsed_data[0]["COURSES"][i]["name"])
        print([i])
    '''

    # Create an empty container (will be defined to more precise data structure later) to store the courses
    courses = []

    while True:
        for course in parsed_data[0]["COURSES"]:
            course_data = {
                "name": course["name"],
                "code": course["code"],
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

# Get the courses for each category --- only humanities being demostrated
humanities_courses = get_courses(connection, "CWSP&ge-b=true")
# example looping and printing values for all humanities courses
# Print the courses
for course in humanities_courses:
    print(course["name"], course["code"])
