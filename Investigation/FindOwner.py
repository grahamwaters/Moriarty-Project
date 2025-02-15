import asyncio
from playwright.async_api import async_playwright
from pyvirtualdisplay import Display
import time

async def google_mail(page, email, password):
    try:
        await page.locator("#identifierId").fill(email)
        await page.click("#identifierNext > div > button > span")
        await page.locator("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input").fill(password)
        await page.locator("#passwordNext > div > button > span").click()
        try:
            await page.click("#submit_approve_access > div > button > div.VfPpkd-RLmnJb")
        except:
            await page.click("#submit_approve_access > div:nth-child(1) > button:nth-child(1) > div:nth-child(1)")
    except:
        pass

async def get_name(page):
    try:
        name = await page.text_content("#app > main > div > div > div > div.rounded-xl.overflow-hidden.shadow > header > div:nth-child(1) > div.font-montserrat.text-lg.sm\:text-2xl.flex-none", timeout=10000)
    except:
        name = await page.text_content("#app > main > div > div > div > div.flex.items-center.gap-4.mb-4 > div > h3")
        if "Oops! Search limit exceeded." in name:
            name = "exceeded"
    return name

async def get_additional_info(page):
    try:
        additional_info = await page.text_content("#app > main > div > div > div > div.rounded-xl.overflow-hidden.shadow > header > div:nth-child(2) > div.font-montserrat.text-lg.sm\:text-2xl.flex-none", timeout=10000)
    except:
        additional_info = ""
    return additional_info

async def run(playwright, phone_number, email, password):
    display = Display(visible=0, size=(1600, 1200))
    display.start()
    firefox = playwright.firefox
    browser = await firefox.launch(headless=True)
    page = await browser.new_page()
    await page.goto("https://truecaller.com")
    await page.locator("#app > main > header > div > form > input").fill(phone_number)
    await page.locator("#app > main > header > div > form > button").click()
    await page.locator("#app > main > div > div > a:nth-child(2)").click()
    await google_mail(page, email, password)
    name = await get_name(page)
    additional_info = await get_additional_info(page)
    await browser.close()
    display.stop()
    return name, additional_info

async def main(phone_number, email, password):
    async with async_playwright() as playwright:
        name, additional_info = await run(playwright, phone_number, email, password)
        print(f"Name: {name}")
        if additional_info:
            print(f"Additional Info: {additional_info}")
