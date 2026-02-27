"""
抓取博客文章（stackoverflow.com）
"""

from playwright.async_api import async_playwright


class BlogSpider(object):
    """
    url: https://stackoverflow.com/questions?tab=newest&page=2
    """
    def __init__(self):
        self.url = "https://stackoverflow.com/questions?tab=newest&page=1"


    async def get_detail_url(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=True)
            page = await browser.new_page()
            await page.goto(self.url)

            pass