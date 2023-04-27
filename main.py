import http.client
import json
from lxml import etree
import time

# Simple class for storing professor data
class Instructor:
    def __init__(self, name, rating, sortRating, courseName):
        self.name = name
        self.rating = rating # Display rating (uses N/A for professors with no data)
        self.sortRating = sortRating # Number rating (used 0.0 for professors with no data, used in sorts)
        self.courseName = courseName

# Method to pull course and scheduling information, takes as input a connection URL, gen-ed category, and required number of credits
def get_courses(conn, category, numOfCredits):
    url = f"/apix/soc/schedule/?category={category}&term=2238" # Term is 2238 - refers to Fall 2023 because no future terms have API data yet
    # Make request to the API
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read()

    # Parse the JSON data
    parsed_data = json.loads(data)
    total_rows = parsed_data[0]["TOTALROWS"] # Used to determine loop (singular GET request can only pull a maximum of 50 rows of data)
    remaining_rows = total_rows

    # Create an empty container to store the courses
    courses = []

    # Loop to get all the rows from the data, not just the first 50
    while True:
        for course in parsed_data[0]["COURSES"]:
            if course["sections"][0]["credits"] == numOfCredits:
                instructors_list = []
                # The set below is used to check for duplicate instructors across sections before adding to instructor_list
                instructors_set = set()
                for section in course["sections"]:
                    for instructor in section["instructors"]:
                        name = instructor["name"]
                        if name not in instructors_set:
                            instructors_list.append(name)
                            instructors_set.add(name)
                # Course data stored in a map-like structure, dictionary in Python
                course_data = {
                    "name": course["name"],
                    "code": course["code"],
                    "instructors_list": instructors_list,
                }
                courses.append(course_data)

        retrieved_rows = parsed_data[0]["RETRIEVEDROWS"]
        remaining_rows -= retrieved_rows
        if remaining_rows <= 0:
            break

        # Another variable used to loop through data
        last_control_num = parsed_data[0]["LASTCONTROLNUMBER"]
        url = f"/apix/soc/schedule/?category={category}&term=2238&last-control-number={last_control_num}"

        # Make request to the API with the updated URL
        conn.request("GET", url)
        response = conn.getresponse()
        data = response.read()
        # Parse the JSON data again
        parsed_data = json.loads(data)

    return courses

# Method to get RateMyProfessor data direct from website
def get_avgRating(profName):

    profName = profName.replace(' ', '%20') # Replaces white spaces with %20 for proper URL functionality

    connection = http.client.HTTPSConnection("www.ratemyprofessors.com")
    url = f"/search/teachers?query={profName}&sid=1100"

    # Request weppage information from ratemyprofessors
    connection.request("GET", url)
    response = connection.getresponse()
    data = str(response.read())

    # Turn raw webpage data into an ElementTree
    root = etree.HTML(data)[0]

    rating = 0.0
# Iterates through the scripts in the XML of the returned webpage to find the data of the professor on RateMyProfessor
    for child in root:
        if child.tag == 'script':
            if(child.text == None): #script tags with no text data, not the right script for our purposes
                continue
            else:
                index = child.text.find("avgRating")
                ratingsIndex = child.text.find("numRatings")
                didFallbackIndex = child.text.find("didFallback") # Variable used to deterine if the professor was listed on UF page or not, if not it falls back to all college query
                if index != -1:
                    index += 11
                    if child.text[index+1:index+2] == ',':
                        rating = float(child.text[index:index+1])
                    else:
                        rating = float(child.text[index:index+3])
                if ratingsIndex != -1:
                    # If there are 0 ratings for a professor, return N/A
                    ratingsIndex += 12
                    if int(child.text[ratingsIndex:ratingsIndex+1]) == 0:
                        return 'N/A'
                if didFallbackIndex != -1:
                    # If there are no results for UF RateMyProfessor page, return N/A
                    didFallbackIndex += 13
                    if child.text[didFallbackIndex:didFallbackIndex+4] == 'true':
                        return 'N/A'

    return rating

# Prompts user for gen-ed requirement input
genEdType = int(input(
    "What gen-ed requirement would you like to fulfill?\n" +
    "1. Biological Sciences\n" +
    "2. Composition\n" +
    "3. Diversity\n" +
    "4. Humanities\n" +
    "5. International\n" +
    "6. Mathematics\n" +
    "7. Physical Sciences\n" +
    "8. Social and Behavioral Sciences\n" +
    "Enter a number 1-8 corresponding to the above gen-ed category: "
))

# Prompts user for credit requirement input
numOfCredits = int(input("How many credits would you like your gen-ed class to be? "))

# Make the HTTP connection
connection = http.client.HTTPSConnection("one.ufl.edu")

# Maps integer user input to correct gen-ed category for url purposes
optionToCategory = {
    1:'b',
    2:'c',
    3:'d',
    4:'h',
    5:'n',
    6:'m',
    7:'p',
    8:'s'
}

# Get the courses for each category
urlString = f"CWSP&ge-{optionToCategory[genEdType]}=true"
courses = get_courses(connection, urlString, numOfCredits)

instructors = []
# Create objects for each instructor
for course in courses:
    for prof in course["instructors_list"]:
        rating = get_avgRating(prof)
        if rating == 'N/A':
            instructor = Instructor(prof, rating, 0.0, course["name"])
        else:
            instructor = Instructor(prof, rating, rating, course["name"])
        instructors.append(instructor)
        #print(instructor.name + " " + str(instructor.rating))


def quickSort(instructorList):
    if len(instructorList) <= 1:
        return instructorList
    else:
        pivotInstructor = instructorList[0]

        belowPivot = [comparisonInstructor for comparisonInstructor in instructorList[1:] if comparisonInstructor.sortRating >= pivotInstructor.sortRating]

        abovePivot = [comparisonInstructor for comparisonInstructor in instructorList[1:] if  comparisonInstructor.sortRating < pivotInstructor.sortRating]

        return quickSort(belowPivot)+[pivotInstructor]+quickSort(abovePivot)

def mergeSort(instructorList):

    if len(instructorList) <= 1:
        return instructorList

    middle = len(instructorList) // 2
    leftSide = mergeSort(instructorList[:middle])
    rightSide = mergeSort(instructorList[middle:])
    
    a = 0
    b = 0

    merged = []

    while a < len(leftSide) and b < len(rightSide):
        if leftSide[a].sortRating >= rightSide[b].sortRating:
            merged.append(leftSide[a])
            a += 1
        else:
            merged.append(rightSide[b])
            b += 1
    
    merged += leftSide[a:]

    merged += rightSide[b:]
    
    return merged
    
pastTimeMergeSort = time.perf_counter()
sortedInstructors = mergeSort(instructors)
currentTimeMergeSort = time.perf_counter()

pastTimeQuickSort = time.perf_counter()
testQuickSort = quickSort(instructors)
currentTimeQuickSort = time.perf_counter()

print("\nBelow is a list of courses that fulfill your chosen gen-ed requirement within your given credits, ranked by rating on RateMyProfessor.\n")

for i in sortedInstructors:
    rate = f' RMP Rating: {i.rating}'
    print(i.courseName + " --- " + " " + i.name + " --- " + rate)

print("\nTime elapsed for Merge Sort of instructor list: " + str((currentTimeMergeSort - pastTimeMergeSort)*1000) + "ms")
print("\nTime elapsed for Quick Sort of instructor list: " + str((currentTimeQuickSort - pastTimeQuickSort)*1000) + "ms")