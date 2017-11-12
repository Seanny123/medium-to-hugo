from regexes import title_re, date_re, orig_re
from utils import web_get
from config import export_dir

import bs4
from bs4 import BeautifulSoup

import os

from typing import List, Tuple


def preprocess_file(fi_path: str):
    fil_title, out_lines, out_path, write_dir, body, orig_header = process_header(fi_path)

    content_args = (body, fil_title)

    return out_path, out_lines, content_args, orig_header


def process_header(fi_path: str):
    write_dir = ""
    out_lines = []

    fi_nm = os.path.split(fi_path)[-1]
    fil_title = title_re.search(fi_nm).group(0).replace("--", "-")
    pub_date = date_re.search(fi_nm)

    if pub_date is None:
        new_nm = "%s.md" % fil_title
        write_dir = "_drafts"
    else:
        pub_date = pub_date.group(0)
        new_nm = "%s-%s.md" % (pub_date, fil_title)

    with open(fi_path, "r") as in_fi:
        in_fi_text = in_fi.read()

    fi_header = ""

    if write_dir == "":
        write_dir, fi_header = get_write_dir(fil_title, in_fi_text)

    soup = BeautifulSoup(in_fi_text, "html.parser")

    title = soup.html.title.text

    if write_dir != "replies":
        tags = get_tags(soup)

        out_lines.append("\n".join(('+++',
                                    'title = "%s"' % title,
                                    'date = "%s"' % pub_date,
                                    'categories = ["%s"]' % '", "'.join(tags),
                                    '+++')))
        out_lines.append("\n\n")

    pre_body = soup.findAll("section", {"data-field": "body"})
    assert len(pre_body) == 1
    body = pre_body[0]

    out_path = os.path.join(write_dir, new_nm)

    return fil_title, out_lines, out_path, write_dir, body, fi_header


def get_write_dir(fil_title: str, in_fi_text: str, download=True) -> Tuple[str, bs4.element.Tag]:
    orig_url = orig_re.search(in_fi_text).group(0)
    orig_fi = os.path.join(export_dir, "tmp-download", "%s.html" % fil_title)
    if download:
        web_get(orig_url, orig_fi)

    with open(orig_fi, "r") as o_fi:
        o_soup = BeautifulSoup(o_fi.read(), "html.parser")

    tmp_head = o_soup.find_all("header")
    assert len(tmp_head) == 1
    hd_c = list(tmp_head[0].children)

    if len(hd_c) == 1:
        write_dir = "_posts"
        ret_head = ""
    else:
        write_dir = "replies"
        ret_head = hd_c[1]

    return write_dir, ret_head


def get_tags(soup: bs4.BeautifulSoup) -> List[str]:
    footer = soup.html.body.article.footer
    tags = []

    for tagtag in footer.findAll("a", {"class": "p-tag"}):
        tags.append(tagtag.text)

    return tags
