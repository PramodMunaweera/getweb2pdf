from setuptools import setup, find_packages

setup(
    name="getweb2pdf",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pdfkit",
        "PyPDF2",
        "beautifulsoup4"
    ],
    entry_points={
        'console_scripts': [
            'getweb2pdf=getweb2pdf.cli:run',
        ],
    },
    author="Pramod Munaweera",
    description="CLI tool to convert a website into a single PDF file",
    keywords="website pdf crawler",
    url="https://github.com/PramodMunaweera/getweb2pdf",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)