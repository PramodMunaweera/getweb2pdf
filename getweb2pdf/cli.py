import os
import argparse
import requests
import pdfkit
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PyPDF2 import PdfMerger

class GetWebToPDF:
    def __init__(self, start_url, output_filename="website.pdf", max_depth=None, 
                 save_intermediate=False, no_merge=False, verbose=False, exclude=None):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited = set()
        self.pdf_files = []
        self.output_filename = output_filename
        self.folder = "website_download"
        self.max_depth = max_depth
        self.save_intermediate = save_intermediate
        self.no_merge = no_merge
        self.verbose = verbose
        self.exclude = exclude or []

        os.makedirs(self.folder, exist_ok=True)

    def should_exclude(self, url):
        return any(pattern.lower() in url.lower() for pattern in self.exclude)

    def download_page_as_pdf(self, url, filename):
        if self.verbose:
            print(f"[+] Saving {url} -> {filename}")
        try:
            pdfkit.from_url(url, filename)
            self.pdf_files.append(filename)
        except Exception as e:
            print(f"[!] Failed to save {url} - {e}")

    def crawl(self, url, depth=0):
        if url in self.visited:
            return
        if self.max_depth is not None and depth > self.max_depth:
            if self.verbose:
                print(f"[!] Max depth reached at {url}")
            return
        if self.should_exclude(url):
            if self.verbose:
                print(f"[!] Skipping excluded URL: {url}")
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
                self.crawl(next_url, depth=depth+1)

    def merge_pdfs(self):
        if not self.pdf_files:
            print("[!] No PDFs to merge.")
            return

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

        if self.no_merge:
            if self.verbose:
                print(f"[INFO] Skipping merge. {len(self.pdf_files)} individual PDFs saved in '{self.folder}'")
            print("[✔] Done!")
        else:
            self.merge_pdfs()
            if not self.save_intermediate:
                # Clean up intermediate PDFs if user didn't ask to save them
                for pdf_file in self.pdf_files:
                    try:
                        os.remove(pdf_file)
                    except Exception as e:
                        print(f"[!] Failed to remove {pdf_file}: {e}")
                os.rmdir(self.folder)
            print("[✔] Done!")

def main():
    parser = argparse.ArgumentParser(
        description="📝 Tool to download a website starting from a URL and save it as a PDF."
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
        help="Output merged PDF filename (default: website.pdf)"
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Maximum depth to crawl (default: no limit)"
    )
    parser.add_argument(
        "--no-merge",
        action="store_true",
        help="Do not merge PDFs, keep individual pages as separate PDFs"
    )
    parser.add_argument(
        "--save-intermediate",
        action="store_true",
        help="Save intermediate PDFs even after merging"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed logging"
    )
    parser.add_argument(
        "--exclude",
        type=str,
        nargs="+",
        help="Skip URLs containing these patterns (ex:--exclude archive login contact)"
    )

    args = parser.parse_args()

    converter = GetWebToPDF(
        start_url=args.url,
        output_filename=args.output,
        max_depth=args.max_depth,
        save_intermediate=args.save_intermediate,
        no_merge=args.no_merge,
        verbose=args.verbose,
        exclude=args.exclude
    )
    converter.run()

def run():
    main()