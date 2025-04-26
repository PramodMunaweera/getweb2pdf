# 📚 GetWeb2PDF

**getweb2pdf** is a simple command-line tool to **crawl a website starting from a given URL** and **save the content into a single PDF**.  
It is perfect for collecting documentation, technical articles, or educational resources into one offline file.


## 🚀 Features

- Crawl all internal HTML pages from a starting URL
- Download each page as a PDF
- Merge all PDFs into one single document
- Easy to use, works from the command line
- Lightweight, no heavy browser automation needed


## 📦 Installation

Make sure you have **Python 3.7+** installed.

1. Clone this repository:

```bash
git clone https://github.com/yourname/getweb2pdf.git
cd getweb2pdf
```

2. Install required Python libraries:

```bash
pip install -r requirements.txt
```

3. Install `wkhtmltopdf` (required by `pdfkit`):

- **Ubuntu/Debian:**

  ```bash
  sudo apt update
  sudo apt install wkhtmltopdf
  ```

- **Windows / macOS:**  
  Download from [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html) and install.

4. Install `getweb2pdf` locally:

```bash
pip install .
```

✅ Now you can use the `getweb2pdf` command from anywhere!


## 🛠 Usage

Basic command:

```bash
getweb2pdf <starting_url> -o <output_file.pdf>
```

### Example:

```bash
getweb2pdf https://example.com/docs.html -o example_docs.pdf
```

Arguments:

| Argument | Description |
|:---|:---|
| `starting_url` | The URL to start crawling from (must be the same domain). |
| `-o, --output` | Name of the output PDF file (default: `website_docs.pdf`). |

For help:

```bash
getweb2pdf --help
```


## ⚠️ Disclaimer

This tool is intended for **personal** and **educational purposes** only.  
It is **not intended for commercial use**, mass website scraping, or redistribution of copyrighted materials.

**Do not use getweb2pdf** to generate PDFs for **money-making purposes** without the permission of the original content owners.  
Always respect the terms of service and robots.txt of websites you crawl.


## 📃 License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.


## ✨ Contributing

Pull requests are welcome! Feel free to open an issue if you want to add new features or report bugs.