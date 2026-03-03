"""
    通过 playwright 实现 stackoverflow 文章自动化采集
"""
import asyncio
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'blogs.settings')
django.setup()
from playwright.async_api import async_playwright


class BlogSpider:
    def __init__(self):
        self.url = "https://stackoverflow.com/questions?tab=newest&page=1"

    async def get_detail_url(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(channel="chrome", headless=False)
            page = await browser.new_page()
            await page.goto(self.url)
            # 等待问题列表加载
            await page.wait_for_selector("h3.s-post-summary--content-title a.s-link")
            # 获取所有问题链接
            links = await page.locator("h3.s-post-summary--content-title a.s-link").all()
            # 标签
            tags = await page.locator("ul.js-post-tag-list-wrapper > li > a").all_inner_texts()
            url_list = []
            for i, link in enumerate(links):
                href = await link.get_attribute("href")
                title = await link.inner_text()
                if href:
                    url_list.append((title, "https://stackoverflow.com" + href))
            # 调用函数获取博客链接详情
            for url in url_list:
                text = await self.get_url_text(page, url[1])
                print(f"{url[0]}的正文内容: \n{text}")
                print("=" * 100)
            await browser.close()

    @staticmethod
    async def get_url_text(page, url):
        await page.goto(url)
        await page.wait_for_selector("div.js-post-body", timeout=15000)
        return await page.locator("div.js-post-body").first.inner_text()


if __name__ == '__main__':
    blog = BlogSpider()
    asyncio.run(blog.get_detail_url())