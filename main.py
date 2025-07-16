import requests
import subprocess
import time
import os

def run_notification(title, message):
    powershell_command = f'''
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
    $template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02
    $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template)
    $text = $xml.GetElementsByTagName("text")
    $text.Item(0).AppendChild($xml.CreateTextNode("{title}")) > $null
    $text.Item(1).AppendChild($xml.CreateTextNode("{message}")) > $null
    $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
    $appId = "Udemy Price Checker"
    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId)
    $notifier.Show($toast)
    '''
    subprocess.run(["powershell", "-Command", powershell_command])

def check_udemy_price(udemy_course_name):
    response = requests.get(f"https://www.udemy.com/api-2.0/courses/{udemy_course_name}/?fields[course]=price,discount_price,is_paid")
    udemy_course_title = udemy_course_name.replace("-", " ").title()  # Format course name for notification

    if response.status_code == 200:
        data = response.json()
        if data["discount_price"] is not None:
            original_price = float(data["price"].replace("£", ""))
            discount_price = float(data["discount_price"]["amount"])
            discount_percentage = round((original_price - discount_price) / original_price * 100, 2)
            discount_price_str = data["discount_price"]["price_string"]
            title = f"Udemy {udemy_course_title} Course on Sale Now!"
            message = f"The course is {discount_price_str} that's {str(discount_percentage)} % off!"
            run_notification(title, message)
            return True

        else:
            return False # not on sale, continue checking

    else:
        title = f"Udemy {udemy_course_title} Course is Having an Issue"
        message = f"Failed to fetch course info: {str(response.status_code)}"
        run_notification(title, message)
        return True

def get_udemy_urls_from_file():
    udemy_course_name_array = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "udemy_links.txt")
    with open(file_path, "r") as file:
        course_links = [line.strip() for line in file if line.strip()]
    
    for link in course_links:
        udemy_course_name_array.append(link.split("/course/")[1].split("/")[0].split("?")[0])
    
    return udemy_course_name_array

while True:
    udemy_course_name_array = get_udemy_urls_from_file()
    for udemy_course_name in udemy_course_name_array[:]: # create a shallow copy to iterate over
        udemy_course_on_sale = check_udemy_price(udemy_course_name)
        if udemy_course_on_sale:
            udemy_course_name_array.remove(udemy_course_name)

    if len(udemy_course_name_array) == 0:
        break
    
    time.sleep(900)  # 15 minutes