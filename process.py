from regexes import post_url_re, year_re
from utils import web_get
from config import export_dir, new_blog_url

import pypandoc

import re
import os

from typing import List


pandoc_args = {"to": "markdown_github-raw_html", "format": "html"}


def process_content(content, fil_title: str, all_posts: List[str]) -> List[str]:
    img_count = 0
    skipped_title = False
    out_lines = []

    for section in content:
        # classify the content as title, text or image

        if section.name == "h3":
            if not skipped_title:
                skipped_title = True
                continue
            else:
                out_lines.append("## %s" % section.text)

        elif section.name == "figure":
            embed = section.find("iframe")
            if embed is None:
                out_lines.append(process_img(section, img_count, fil_title, all_posts))
                img_count += 1

            else:
                out_lines.append(str(embed))
                out_lines.append("\n")

        else:
            out_lines.append(process_text(str(section), all_posts))

        out_lines.append("\n")

    return out_lines


def process_img(c_val, count: int, fil_title: str, all_posts: List[str], download=False) -> str:
    """Acquire image from Medium server and insert link,
    as well as processing the caption."""

    src = c_val.find("img")["src"]
    ext = os.path.splitext(src)[1]
    img_dir = os.path.join(os.sep, "img", "%s_%s%s" % (fil_title, count, ext))
    img_path = os.path.join(export_dir, img_dir)
    if download:
        web_get(src, img_path)

    caption_tag = c_val.find("figcaption")
    if caption_tag is None:
        caption = ""
    else:
        cap_out = process_text(caption_tag, all_posts)
        caption = "".join(cap_out).rstrip()

    return """{{< figure
  src="%s"
  class=""
  title=""
  caption="%s"
  label=""
  attr=""
  attrlink=""
  alt=""
  link=""
 >}}
{{< section "end" >}}\n""" % (img_path, caption)


def process_text(text: str, all_posts: List[str]):
    """Convert Medium text to Markdown with Pandoc while also redirecting links."""
    conv_text = pypandoc.convert_text(text, **pandoc_args)
    return re_link(conv_text, all_posts)


def re_link(orig_t: str, all_posts: List[str]) -> str:
    """Replace all links from the medium blog with new Jekyll blog links"""

    # for each blog link
    for post_url in post_url_re.finditer(orig_t):
        orig_url = re.compile(post_url.group(0), flags=re.IGNORECASE)

        for post in all_posts:
            search_res = orig_url.search(post)

            if search_res:
                year = year_re.search(post).group(0)
                new_url = "%s%s/%s" % (new_blog_url, year, search_res.group(0))
                orig_url.sub(orig_t, new_url)
                break

    return orig_t
