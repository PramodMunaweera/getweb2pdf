import os
import argparse
import requests
import pdfkit
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PyPDF2 import PdfMerger

class GetWebToPDF:
    def __init__(self, start_url, output_filename="website.pdf"):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited = set()
        self.pdf_files = []
        self.output_filename = output_filename
        self.folder = "website_download"
        os.makedirs(self.folder, exist_ok=True)

    def download_page_as_pdf(self, url, filename):
        print(f"[+] Saving {url} -> {filename}")
        try:
            pdfkit.from_url(url, filename)
            self.pdf_files.append(filename)
        except Exception as e:
            print(f"[!] Failed to save {url} - {e}")

    def crawl(self, url):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"[!] Error fetching {url}: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Save this page
        page_name = urlparse(url).path.strip("/").replace("/", "_") or "index"
        page_name = page_name.split(".")[0]  # Remove .html if present
        pdf_path = os.path.join(self.folder, f"{len(self.visited):03d}_{page_name}.pdf")
        self.download_page_as_pdf(url, pdf_path)

        # Find all internal links
        for link_tag in soup.find_all('a', href=True):
            href = link_tag['href']
            parsed_href = urlparse(href)

            if parsed_href.netloc and parsed_href.netloc != self.domain:
                continue  # Skip external links

            next_url = urljoin(url, href)

            if next_url.endswith(".html") or next_url.endswith("/"):
                self.crawl(next_url)

    def merge_pdfs(self):
        print("[*] Merging all PDFs into one...")
        merger = PdfMerger()
        for pdf in self.pdf_files:
            merger.append(pdf)

        merger.write(self.output_filename)
        merger.close()
        print(f"[✔] All pages merged into {self.output_filename}")

    def run(self):
        print(f"[*] Starting crawl at {self.start_url}")
        self.crawl(self.start_url)
        self.merge_pdfs()
        print("[✔] Done!")

def main():
    parser = argparse.ArgumentParser(
        description="📝 Tool to download a website starting from a URL and save it as a single PDF."
    )
    parser.add_argument(
        "url", 
        type=str,
        help="Starting URL of the website (example: https://example.com/docs/)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="website.pdf",
        help="Output PDF filename (default: website.pdf)"
    )

    args = parser.parse_args()

    converter = GetWebToPDF(args.url, args.output)
    converter.run()

def run():
    main()
