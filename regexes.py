import re

orig_re = re.compile(r"https://medium.com/p/[a-z0-9]+")
year_re = re.compile(r"(?<=[0-9]{2})[0-9]{2}")
date_re = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
title_re = re.compile(r"(?<=_).+(?=-[a-z0-9]+\.html$)")
blog_re = re.compile(r"https://medium.com/@seanaubin/")
post_url_re = re.compile(r"(?<=https://medium.com/@seanaubin/).+(?=-[a-z0-9#.]+\))")
title_from_header_re = re.compile(r"(?<=https://medium.com/@seanaubin/).+(?=-[a-z0-9#.]+)")
title_from_file_re = re.compile(r"(?<=[0-9]{4}-[0-9]{2}-[0-9]{2}-)[a-z0-9-]+(?=\.md)", re.IGNORECASE)
