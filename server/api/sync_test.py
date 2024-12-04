import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_get_title():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto('http://localhost:8000/api/templates/sports?page=1&size=15')

        title = await page.title()
        assert title == 'Список видов спорта'

        await browser.close()
        
@pytest.mark.asyncio
async def testbad_create_sport_modal():
    async with async_playwright() as p:
        # headless=True - запуск в фоновом режиме
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("http://localhost:8000/api/templates/sports")

        await page.click('button#createExampleSportButton')

        modal_title = await page.inner_text('h5.modal-title#sportModalLabel')

        assert modal_title == "Создание вида спорта", f"Expected 'Создание вида спорта', but got {modal_title}"

        await browser.close()
        
@pytest.mark.asyncio
async def test_create_sport_modal():
    async with async_playwright() as p:
        # headless=True - запуск в фоновом режиме
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("http://localhost:8000/api/templates/sports")

        await page.click('button#createSportButton')

        modal_title = await page.inner_text('h5.modal-title#sportModalLabel')

        assert modal_title == "Создание вида спорта", f"Expected 'Создание вида спорта', but got {modal_title}"

        await browser.close()