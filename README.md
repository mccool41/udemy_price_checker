# Udemy Price Checker 🛒

A Python script that checks if [this Udemy course](https://www.udemy.com/course/automate/) is on sale and sends a Windows notification when it is.

---

## 💡 What it does

- Checks Udemy every 15 minutes to see if the course is on sale
- Sends a Windows notification if:
  - The course is on sale
  - There’s a problem fetching the course
- The notification includes the discounted price, percentage off, and stays visible in your Windows Action Center until dismissed
- Stops running after a notification comes through so you don't get spammed

---

## ⚙️ How to Use

1. Clone this repo:
   ```bash
   git clone https://github.com/mccool41/udemy_price_checker.git
2. Install Requirements:
   ```bash
   pip install requests
3. (Optional) Add to Windows Task Scheduler
    - Open Windows Task Scheduler (Press Win + R → type taskschd.msc → Enter)
    - Create a new task:
    - General tab:
        - Name: Udemy Price Checker
    - Triggers tab:
        - New → Begin the task: "At log on"
        - (Optional) Check specific user and choose your own
    - Actions tab:
        - New → Action: "Start a program"
        - Program/script: browse to where you saved "launch_silent.vbs"
    - Save the task.

---

## 🔐 Notes
🔇 Selecting "launch_silent.vbs" instead of the "run_price_checker.bat" in the Windows Task Scheduler suppresses the Command Prompt popup why the Python script is running.

Notifications use PowerShell to call Windows native toast system.

---

## ✅ Example Notification
Title:
Udemy Python Automation on Sale Now!

Message:
The course is £20 — that's 78.95% off!