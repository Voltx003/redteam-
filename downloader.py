import asyncio
import os
import requests
import argparse
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

class WebDownloader:
    def __init__(self, target_url, output_dir):
        self.target_url = target_url
        self.output_dir = output_dir
        self.downloaded_assets = set()
        os.makedirs(self.output_dir, exist_ok=True)

    def download_asset(self, url):
        if url in self.downloaded_assets or not url.startswith("http"):
            return

        parsed_url = urlparse(url)
        path = parsed_url.path
        if not path or path == "/":
            path = "/index.html"

        # Xây dựng đường dẫn file cục bộ
        local_path = os.path.join(self.output_dir, path.lstrip("/"))

        # Đảm bảo đường dẫn file không vượt quá giới hạn hệ thống và không lùi ra ngoài output_dir
        if not os.path.abspath(local_path).startswith(os.path.abspath(self.output_dir)):
             logger.warning(f"Skipping potentially unsafe path: {url}")
             return

        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        try:
            # Sử dụng session để giữ cookies nếu cần
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(response.content)
                self.downloaded_assets.add(url)
                logger.info(f"Downloaded: {url}")
            else:
                logger.error(f"Failed ({response.status_code}): {url}")
        except Exception as e:
            logger.error(f"Error {url}: {e}")

    async def run(self):
        async with async_playwright() as p:
            logger.info(f"Launching browser for {self.target_url}...")
            browser = await p.chromium.launch(headless=True)
            # Giả lập thiết bị để tránh một số WAF cơ bản
            context = await browser.new_context(
                user_agent=HEADERS["User-Agent"],
                viewport={"width": 1280, "height": 720}
            )
            page = await context.new_page()

            # Ẩn navigator.webdriver
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            try:
                # Điều hướng đến trang mục tiêu
                response = await page.goto(self.target_url, wait_until="networkidle", timeout=60000)

                # Chờ cho các nội dung động load
                await asyncio.sleep(5)

                # Lấy nội dung HTML sau khi đã render
                content = await page.content()

                # Lưu file index chính
                index_path = os.path.join(self.output_dir, "index.html")
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info(f"Main page saved to {index_path}")

                # Phân tích tài sản
                soup = BeautifulSoup(content, "html.parser")
                assets = []

                # Tìm scripts, links (css), và images
                for tag in soup.find_all(["script", "link", "img"]):
                    src = tag.get("src") or tag.get("href")
                    if src:
                        full_url = urljoin(self.target_url, src)
                        assets.append(full_url)

                # Lọc và tải tài sản (chỉ tải từ domain liên quan để tránh quá tải)
                domain = urlparse(self.target_url).netloc
                for asset_url in set(assets):
                    asset_domain = urlparse(asset_url).netloc
                    # Chấp nhận domain chính và các CDN phổ biến của mục tiêu
                    if asset_domain == domain or "viator" in asset_domain:
                        self.download_asset(asset_url)
                    else:
                        logger.debug(f"Skipping external: {asset_url}")

            except Exception as e:
                logger.error(f"Execution error: {e}")
                await page.screenshot(path="error_debug.png")

            await browser.close()
            logger.info("Browser closed. Download process finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Client Assets Downloader")
    parser.add_argument("url", help="Target URL to clone")
    parser.add_argument("--output", default="cloned_site", help="Output directory")

    args = parser.parse_args()

    downloader = WebDownloader(args.url, args.output)
    asyncio.run(downloader.run())
