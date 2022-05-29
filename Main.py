import os
from pathlib import Path
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

blackList = ['[document]',   'noscript', 'header',
             'html', 'meta', 'head', 'input', 'script', "style"]


def epubToHtml(epubPath):
    book = epub.read_epub(epubPath)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters


def chapterToText(chapter):
    output = []
    soup = BeautifulSoup(chapter, from_encoding="utf-8")
    text = soup.findAll(text=True)
    for t in text:
        if t.parent.name not in blackList:
            output.append(t)
    return ''.join(output)


def epubToText(epubPath):
    chapters = epubToHtml(epubPath)
    parts = []
    for chapter in chapters:
        parts.append(chapterToText(chapter))
    writeToTxt(epubPath, '\n'.join(parts))


def writeToTxt(epubPath, text):
    outputFile = Path(str(epubPath)[:-4]+"txt")
    with open(outputFile, "w", encoding="utf-8") as f:
        f.write(text.strip())


if __name__ == "__main__":
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".epub"):
                epubToText(Path(os.getcwd(), os.path.join(root, file)))
