import requests

print("Checking course page at https://www.udemy.com/course/automate/")
response = requests.get("https://www.udemy.com/course/automate/")
print("Status code:", response.status_code)