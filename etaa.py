from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# === مسیر دانلود ===
download_path = "/Users/reihane/Downloads/eitaa_pdfs"
os.makedirs(download_path, exist_ok=True)

# === تنظیمات مرورگر ===
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", prefs)

print("🚀 راه‌اندازی مرورگر...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
actions = ActionChains(driver)

# === ورود به ایتا ===
print("🔐 ورود به Eitaa...")
driver.get("https://web.eitaa.com")
print("⏳ لطفاً وارد حساب شو - 30 ثانیه صبر می‌کنیم...")
time.sleep(30)

# === رفتن به کانال تست ===
print("📡 رفتن به کانال تست...")
driver.get("https://web.eitaa.com/#@testbarname")
time.sleep(10)

# === اسکرول برای بارگذاری پیام‌ها ===
for i in range(6):
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

# === جستجو برای فایل‌های PDF ===
print("🔍 جستجو برای فایل‌های PDF...")
pdf_blocks = driver.find_elements(By.CLASS_NAME, "document-name")
print(f"📄 تعداد فایل PDF پیدا شده: {len(pdf_blocks)}")

successes = []
failures = []

for idx, pdf_block in enumerate(pdf_blocks):
    try:
        file_name = pdf_block.text.strip() or f"فایل شماره {idx+1}"
        parent = pdf_block.find_element(By.XPATH, "..")
        driver.execute_script("arguments[0].scrollIntoView(true);", parent)
        time.sleep(1)

        if parent.is_displayed() and parent.is_enabled():
            actions.move_to_element(parent).click().perform()
            print(f"✅ دانلود موفق: {file_name}")
            successes.append(file_name)
            time.sleep(3)
        else:
            print(f"❌ دانلود نشد (قابل کلیک نیست): {file_name}")
            failures.append(file_name)
    except Exception as e:
        print(f"❌ دانلود نشد: {file_name} | دلیل: {e}")
        failures.append(file_name)

# === گزارش نهایی ===
print("\n📋 گزارش نهایی:")
print(f"🟢 دانلود موفق: {len(successes)} فایل")
for name in successes:
    print(f"  ✅ {name}")
print(f"🔴 دانلود ناموفق: {len(failures)} فایل")
for name in failures:
    print(f"  ❌ {name}")

print(f"\n📁 فایل‌ها در مسیر: {download_path}")
driver.quit()
