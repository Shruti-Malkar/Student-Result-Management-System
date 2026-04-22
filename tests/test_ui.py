from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
pytest.skip("Skipping Selenium in CI", allow_module_level=True)

def test_homepage():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://localhost:5000")

    assert "Student" in driver.title

    driver.quit()