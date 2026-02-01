# 🤖 Portfolio Automation with Selenium

This project automates portfolio form submission using **Selenium WebDriver**. It logs in, fills forms, and validates data automatically.

---

## 📋 Table of Contents

1. [What is Selenium Automation?](#what-is-selenium-automation)
2. [10 Easy Steps to Understand Automation](#10-easy-steps-to-understand-automation)
3. [Installation & Setup](#installation--setup)
4. [How to Run](#how-to-run)
5. [Project Structure](#project-structure)

---

## 🎯 What is Selenium Automation?

**Selenium** is a tool that controls your web browser automatically. Think of it as a robot that:

- Opens websites
- Fills forms
- Clicks buttons
- Submits data
- Validates results

Instead of doing these tasks manually, the computer does them for you!

---

## 🚀 10 Easy Steps to Understand Automation

### **Step 1: Install Selenium** ✅

First, install Selenium in your computer:

```bash
pip install selenium
pip install webdriver-manager
```

**Why?** You need Selenium libraries to control the browser.

---

### **Step 2: Import Packages** 📦

At the top of your Python file, import Selenium tools:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
```

**Why?** These tools help you control the browser.

---

### **Step 3: Open Browser** 🌐

Tell Selenium to open Chrome (or Firefox):

```python
driver = webdriver.Chrome()
```

**Why?** This opens a browser window that Selenium will control.

---

### **Step 4: Navigate to Website** 🔗

Go to the website you want to automate:

```python
driver.get("http://localhost/portfolio/login.html")
```

**Why?** This loads the page where you want to perform actions.

---

### **Step 5: Find Elements** 🔍

Search for buttons, input boxes, and text fields:

```python
element = driver.find_element(By.NAME, "email")
```

**Why?** You need to locate what you want to click or fill.

---

### **Step 6: Interact with Elements** 👆

Type text, click buttons, and submit forms:

```python
element.send_keys("your@email.com")      # Type text
element.click()                           # Click button
element.submit()                          # Submit form
```

**Why?** This performs actions just like a human would.

---

### **Step 7: Wait for Elements** ⏳

Wait for page to load before continuing:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)  # Wait max 10 seconds
wait.until(EC.presence_of_element_located((By.NAME, "email")))
```

**Why?** Some elements take time to load. Don't rush!

---

### **Step 8: Handle Popups & Errors** ⚠️

Deal with alert boxes and unexpected issues:

```python
try:
    alert = driver.switch_to.alert
    alert.accept()
except:
    print("No alert found")
```

**Why?** Sometimes websites show popups. Be ready for them.

---

### **Step 9: Verify Your Work** ✔️

Check if automation worked correctly:

```python
success_message = driver.find_element(By.CLASS_NAME, "success")
print(f"Status: {success_message.text}")
```

**Why?** Confirm that data was submitted successfully.

---

### **Step 10: Close Browser** ❌

Always close the browser when done:

```python
driver.quit()
```

**Why?** This prevents memory leaks and closes the browser window.

---

## 💻 Installation & Setup

### **1. Install Python**

Download from [python.org](https://www.python.org)

### **2. Install Required Packages**

```bash
pip install selenium
pip install webdriver-manager
```

### **3. Clone the Repository**

```bash
git clone https://github.com/Praveen882005/Automation-of-portfolio.git
cd Automation-of-portfolio
```

### **4. Configure Credentials**

Edit `portfolio.py` and add your login details:

```python
email = "your@email.com"      # Change this
password = "your_password"    # Change this
```

---

## 🎬 How to Run

Run the automation script:

```bash
python portfolio.py
```

**What happens:**

1. ✅ Browser opens automatically
2. ✅ Login form is filled
3. ✅ Resume form is filled
4. ✅ Data is submitted
5. ✅ Browser closes

---

## 📁 Project Structure

```
portfolio-automation/
├── portfolio.py          # Main automation script
├── steps/                # Step-by-step instructions
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

---

## 🔧 Troubleshooting

| Problem                    | Solution                              |
| -------------------------- | ------------------------------------- |
| **ChromeDriver not found** | Run `pip install webdriver-manager`   |
| **Element not found**      | Increase wait time or check selector  |
| **Connection refused**     | Make sure localhost server is running |
| **Login fails**            | Check if credentials are correct      |

---

## 📚 Learn More

- **Selenium Docs:** https://www.selenium.dev/documentation/
- **By Selectors:** https://www.selenium.dev/documentation/webdriver/locating_elements/
- **WebDriverWait:** https://www.selenium.dev/documentation/webdriver/waits/

---

## 👨‍💻 Author

- **Praveen Kumar**
- Email: cgmpraveenkumar@gmail.com
- GitHub: [@Praveen882005](https://github.com/Praveen882005)

---

## 📝 License

This project is open source and available under the MIT License.

---

**Happy Automating! 🚀**
