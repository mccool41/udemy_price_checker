import requests
import subprocess

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

# Checking course page at https://www.udemy.com/course/automate/
response = requests.get("https://www.udemy.com/api-2.0/courses/automate/?fields[course]=price,discount_price,is_paid")

if response.status_code == 200:
    data = response.json()

    if data["discount_price"] is not None:
        discountPercentage = round((data["price"] - data["discount_price"]) / data["price"] * 100, 2)
        title = "Udemy Python Automation on Sale Now!"
        message = "The course is " + data["price"] + " that's " + discountPercentage + "% off!"

    else:
        title = "Udemy Python Automation isn't on Sale :("
        message = "The course is " + data["price"] + " with no discount available."

else:
    # Printing the error code to console if needed
    print("Failed to fetch course info:", response.status_code)
    title = "Udemy Python Automation is Having an Issue :'("
    message = "Failed to fetch course info: " + response.status_code

runNotification(title, message)