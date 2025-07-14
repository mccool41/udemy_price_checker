import requests

print("Checking course page at https://www.udemy.com/course/automate/")
response = requests.get("https://www.udemy.com/api-2.0/courses/automate/?fields[course]=price,discount_price,is_paid")

if response.status_code == 200:
    data = response.json()

    if data["discount_price"] is not None:
        discountPercentage = round((data["price"] - data["discount_price"]) / data["price"] * 100, 2)
        print("Original price: ", data["price"])
        print("Discounted price: ", data["discount_price"])
        print("Discount percentage: ", discountPercentage, "%")
    else:
        print("Price: ", data["price"])
        print("No discount available")

else:
    print("Failed to fetch course info:", response.status_code)