#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script creates fixtures for database seeding with demo samples
based on data dumps from https://openlibrary.org/developers/dumps
prices are generated randomly
"""
import gzip
import json
from os import path
from random import randint
import re
from shutil import which
from subprocess import run, PIPE
from urllib.request import urlretrieve


URI_BOOKS_DUMP = "https://openlibrary.org/data/ol_dump_editions_latest.txt.gz"
URI_AUTHORS_DUMP = "https://openlibrary.org/data/ol_dump_authors_latest.txt.gz"
FILENAME_BOOKS_DUMP = "books.txt.gz"
FILENAME_AUTHORS_DUMP = "authors.txt.gz"
FILENAME_BOOKS = "books.json"
FILENAME_AUTHORS = "authors.json"
PATTERN = re.compile("({.*})")


def main():
    # download authors and editions dumps if we don't have them locally
    if not path.exists(FILENAME_AUTHORS_DUMP):
        download_file(URI_AUTHORS_DUMP, FILENAME_AUTHORS_DUMP)
    if not path.exists(FILENAME_BOOKS_DUMP):
        download_file(URI_BOOKS_DUMP, FILENAME_BOOKS_DUMP)

    # dumps contains millions of editions & authors;
    # we pick up the ones with the following keys, narrowing down data samples
    # to few hundreds and also making our data more consistent
    keywords = ["description", "covers", "/languages/eng", "title",
                "publishers", "publish_date", "authors", "isbn_10", "isbn_13"]
    books = filter_by_keywords(FILENAME_BOOKS_DUMP, keywords)

    # filter out authors of books not in our database
    author_keys_from_books = {author["key"] for book in books
                              for author in book.get("authors", [])
                              if isinstance(author, dict)}
    authors = filter_authors(FILENAME_AUTHORS_DUMP, author_keys_from_books)

    # some books don't have author records in authors dump;
    # we don't want books with unknown authors in our database either
    books = filter_books_by_authors(books, {a["key"] for a in authors})

    # and once again filter out authors of books removed from database
    author_keys_from_books = {a["key"] for b in books for a in b["authors"]}
    authors = [a for a in authors if a["key"] in author_keys_from_books]

    save_to_file(filter_author_fields(authors), FILENAME_AUTHORS)
    save_to_file(filter_book_fields(books), FILENAME_BOOKS)


def download_file(uri, filename):
    if which("aria2c"):
        run(f"aria2c -x 16 -s 16 -k 1M -o {filename} {uri}", shell=True)
    else:
        urlretrieve(uri, filename)


def filter_by_keywords(filename, keywords):
    keywords = [f"\"{keyword}\"" for keyword in keywords]
    if which("zcat"):
        cmd = [f"zcat {filename}"] + [f"grep '{k}'" for k in keywords]
        cmd = " | ".join(cmd)
        books = run(cmd, check=True, stdout=PIPE, shell=True).stdout
        return [decode(book) for book in books.split(b"\n") if book]
    else:
        with gzip.open(filename, "rb") as books_dump:
            keywords = [k.encode("utf-8") for k in keywords]
            return [decode(book) for book in books_dump
                    if all(k in book for k in keywords)]


def decode(bin_str):
    return json.loads(re.search(PATTERN, bin_str.decode("utf-8")).group(1))


def filter_authors(filename, author_keys):
    with gzip.open(filename, "rb") as authors_dump:
        return [a for a in (decode(author) for author in authors_dump)
                if a.get("key") in author_keys and a.get("name")]


def filter_books_by_authors(books, author_keys):
    return [book for book in books
            if all(isinstance(a, dict) and a["key"] in author_keys
                   for a in book["authors"])]


def filter_book_fields(books):
    def plain_description(d):
        return d["value"] if isinstance(d, dict) else d

    def get_full_title(b):
        prefix = b.get("title_prefix", "")
        return f"{prefix} {b['title']}" if prefix else b["title"]

    return [dict(model="store.book",
                 pk=b["key"][7:],
                 fields=dict(title=get_full_title(b),
                             authors=[a["key"][9:] for a in b["authors"]],
                             publisher=b["publishers"][0],
                             publish_date=b["publish_date"],
                             description=plain_description(b["description"]),
                             cover=b["covers"][0],
                             isbn_10=b["isbn_10"][0],
                             isbn_13=b["isbn_13"][0],
                             price=randint(100, 1000)/10))
            for b in books]


def filter_author_fields(authors):
    return [dict(model="store.author",
                 pk=author["key"][9:],
                 fields=dict(name=author["name"]))
            for author in authors]


def save_to_file(seq, filename):
    with open(filename, "w") as out:
        json.dump(seq, out, indent=4)


if __name__ == "__main__":
    main()
