from setuptools import setup, find_namespace_packages

setup(
    name="NadeOCR",
    version="1.0.1.3",
    author="Natsume",
    author_email="jonathan.197ariza@gmail.com",
    license="GPLv3",
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=[
        "google-cloud-vision",
        "manga_ocr",
        "pynput",
        "pyperclip",
        "PyQt5",
        "PySide6",
        "screeninfo"
    ],
    entry_points={
        "console_scripts": [
            "nadeocr = nadeocr.__main__:run",
        ]
    },
)
