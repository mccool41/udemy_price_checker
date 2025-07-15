import requests
import subprocess
import time

def runNotification(title, message):
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

def check_udemy_price():
    # Checking course page at https://www.udemy.com/course/automate/
    response = requests.get("https://www.udemy.com/api-2.0/courses/automate/?fields[course]=price,discount_price,is_paid")

    if response.status_code == 200:
        data = response.json()

        if data["discount_price"] is not None:
            originalPrice = float(data["price"].replace("£", ""))
            discountPrice = float(data["discount_price"]["amount"])
            discountPercentage = round((originalPrice - discountPrice) / originalPrice * 100, 2)
            discountPriceStr = data["discount_price"]["price_string"]
            title = "Udemy Python Automation on Sale Now!"
            message = "The course is " + discountPriceStr + " that's " + str(discountPercentage) + "% off!"
            runNotification(title, message)
            return True

        else:
            return False # not on sale, continue checking

    else:
        title = "Udemy Python Automation is Having an Issue :'("
        message = "Failed to fetch course info: " + response.status_code
        runNotification(title, message)
        return True

while True:
    if check_udemy_price():
        break  # exit early if on sale or URL issue
    time.sleep(900)  # 15 minutes