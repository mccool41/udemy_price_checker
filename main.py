import requests
from plyer import notification

# Checking course page at https://www.udemy.com/course/automate/
response = requests.get("https://www.udemy.com/api-2.0/courses/automate/?fields[course]=price,discount_price,is_paid")

if response.status_code == 200:
    data = response.json()

    if data["discount_price"] is not None:
        discountPercentage = round((data["price"] - data["discount_price"]) / data["price"] * 100, 2)
        notification.notify(
            title = "Udemy Python Automation Discount Alert",
            message = "Discounted to " + data["discount_price"] + " that's " + discountPercentage + "% off!",
            timeout = 10
        )
    else:
        notification.notify(
            title = "Udemy Python Automation Discount Alert",
            message = "No discount available :( the price is: " + data["price"],
            timeout = 10
        )

else:
    # Printing the error code to console if needed
    print("Failed to fetch course info:", response.status_code)
    notification.notify(
            title = "Udemy Python Automation Discount Alert",
            message = "Failed to fetch course info:" + response.status_code,
            timeout = 10
        )