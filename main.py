import requests

print("Checking course page at https://www.udemy.com/course/automate/")
response = requests.get("https://www.udemy.com/api-2.0/courses/automate/?fields[course]=price,discount_price,is_paid")

if response.status_code == 200:
    data = response.json()
    print("Price:", data["price"])
    print("Discounted price:", data["discount_price"])
else:
    print("Failed to fetch course info:", response.status_code)