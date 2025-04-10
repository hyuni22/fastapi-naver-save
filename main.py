from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import logging

app = FastAPI()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AddressRequest(BaseModel):
    address: str
    folder: str = "aaaee"

@app.post("/save-address")
async def save_address(data: AddressRequest):
    address = data.address
    folder_name = data.folder

    logger.info(f"📍 요청 받은 주소: {address} / 저장리스트: {folder_name}")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--lang=ko-KR")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        logger.info("🚀 크롬 드라이버 실행 완료")

        driver.get(f"https://map.naver.com/v5/search/{address}")
        logger.info("🌐 네이버 지도 페이지 접속 완료")
        time.sleep(6)

        # iframe 자동 감지 후 전환
        try:
            iframe = driver.find_element(By.ID, "searchIframe")
            driver.switch_to.frame(iframe)
            logger.info("🖼️ iframe 전환 완료")
        except Exception:
            logger.warning("⚠️ iframe 없음 → 현재 페이지에서 바로 진행 시도")

        try:
            save_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn_favorite') and .//span[text()='저장']]")
            save_button.click()
            logger.info("⭐ 저장 버튼 클릭 완료")
            time.sleep(2)
        except Exception as e:
            logger.error(f"❌ 저장 버튼 클릭 실패: {e}")
            driver.quit()
            return {"result": "❌ 저장 버튼 클릭 실패", "error": str(e)}

        try:
            folder_button = driver.find_element(By.XPATH, f"//button[@class='swt-save-group-info'][.//strong[text()='{folder_name}']]")
            folder_button.click()
            logger.info("📁 저장 리스트 클릭 완료")
            time.sleep(1)
        except Exception as e:
            logger.error(f"❌ 저장 리스트 클릭 실패: {e}")
            driver.quit()
            return {"result": "❌ 저장 리스트 클릭 실패", "error": str(e)}

        try:
            final_save = driver.find_element(By.XPATH, "//button[@class='swt-save-btn' and text()='저장']")
            final_save.click()
            logger.info("💾 최종 저장 클릭 완료")
            time.sleep(2)
        except Exception as e:
            logger.error(f"❌ 최종 저장 실패: {e}")
            driver.quit()
            return {"result": "❌ 최종 저장 실패", "error": str(e)}

        driver.quit()
        logger.info("✅ 저장 성공")
        return {"result": "✅ 저장 성공", "address": address}

    except Exception as e:
        logger.exception("❌ 전체 예외 발생")
        return {"result": "❌ 저장 실패", "error": str(e)}
