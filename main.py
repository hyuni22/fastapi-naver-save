from fastapi import FastAPI, Request
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = FastAPI()

class AddressRequest(BaseModel):
    address: str
    folder: str = "aaaee"  # 기본 저장 리스트 이름

@app.post("/save-address")
async def save_address(data: AddressRequest):
    address = data.address
    folder_name = data.folder

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--lang=ko-KR")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://map.naver.com/v5/search/" + address)
        time.sleep(6)

        driver.switch_to.frame("searchIframe")
        time.sleep(2)

        save_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn_favorite') and .//span[text()='저장']]")
        save_button.click()
        time.sleep(2)

        folder_button = driver.find_element(By.XPATH, f"//button[@class='swt-save-group-info'][.//strong[text()='{folder_name}']]")
        folder_button.click()
        time.sleep(1)

        final_save = driver.find_element(By.XPATH, "//button[@class='swt-save-btn' and text()='저장']")
        final_save.click()
        time.sleep(2)

        driver.quit()
        return {"result": "✅ 저장 성공", "address": address}

    except Exception as e:
        driver.quit()
        return {"result": "❌ 저장 실패", "error": str(e)}
