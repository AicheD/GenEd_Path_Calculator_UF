import http.client

conn = http.client.HTTPSConnection("one.ufl.edu")

conn.request("GET", "/apix/soc/schedule/?category=CWSP&term=2238&course-code=mac2311")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))