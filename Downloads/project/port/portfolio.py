from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Chrome Options ---
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ✅ Automatically use correct ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # --- ALWAYS START FROM LOGIN PAGE ---
    driver.delete_all_cookies()
    driver.get("http://localhost/portfolio/login.html")
    wait = WebDriverWait(driver, 10)

    # --- LOGIN ---
    print("🔐 Logging in...")
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("cgmpraveenkumar@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("praveen882005")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()

    # --- Handle alert popup if appears ---
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"⚠️ Alert detected: {alert.text}")
        alert.accept()
    except TimeoutException:
        pass

    # --- RESUME FORM PAGE ---
    print("📝 Filling resume form...")
    wait.until(EC.presence_of_element_located((By.NAME, "name")))

    def ultra_fast_type(element, text, delay=0.005):
        """Type ultra fast into input fields."""
        for ch in text:
            element.send_keys(ch)
            time.sleep(delay)

    # Fill fields very fast
    ultra_fast_type(driver.find_element(By.NAME, "name"), "Praveen Kumar I")
    ultra_fast_type(driver.find_element(By.NAME, "contact"), "cgmpraveenkunmar@gmail.com")

    ultra_fast_type(driver.find_element(By.NAME, "skills"),
        "Python, HTML, CSS — proficient in Python, Java, and C++, strong in OOP and DSA. "
        "Experienced in web dev with HTML, CSS, JS, React, Django. Skilled in MySQL, MongoDB."
    )

    ultra_fast_type(driver.find_element(By.NAME, "experience"),
        "Developed multiple projects using Python, Java, C++. Worked with Django and React, "
        "managed MySQL databases, integrated APIs, and debugged efficiently."
    )

    ultra_fast_type(driver.find_element(By.NAME, "education"),
        "Pursuing Computer Science degree focusing on programming, algorithms, and databases."
    )

    ultra_fast_type(driver.find_element(By.NAME, "additional"),
        "Certified in Python, Java, Web Development, and Database Management."
    )

    # --- PREVIEW & DOWNLOAD ---
    wait.until(EC.element_to_be_clickable((By.ID, "previewBtn"))).click()
    print("👀 Preview button clicked")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Download PDF']"))).click()
    print("📄 Download PDF button clicked")

    time.sleep(2)

except UnexpectedAlertPresentException:
    alert = driver.switch_to.alert
    print(f"⚠️ Unexpected alert: {alert.text}")
    alert.accept()

except Exception as e:
    print("❌ Error:", e)

finally:
    driver.quit()
    print("✅ Automation Completed Successfully!")
