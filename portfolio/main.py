import datetime
import json
import os
import re
import urllib.request
import configparser
import xml.etree.ElementTree
from html import escape
from json import JSONDecodeError
from typing import Optional
from urllib.parse import urlparse
from xml.dom import minidom

config = configparser.ConfigParser()
config.read("config.ini")

auth_token = os.environ.get("NOTION_TOKEN")
notion_api_version = config["parser"]["notion_api_version"]
base_url = config["parser"]["base_url"]
force_rebuild = config["parser"]["force_rebuild"]
main_page_id = config["parser"]["main_page"]
page_url_to_id = config["urls"]

page_id_to_url = {page_id: url for url, page_id in config["urls"].items()}

def get_html_file_name(page_id: str) -> str:
    page_id = page_id.replace("-", "")
    if page_id == main_page_id:
        return "index"
    return page_id_to_url.get(page_id, page_id)


def get_url(page_id: str) -> str:
    page_id = page_id.replace("-", "")
    if page_id == main_page_id:
        return ""
    return base_url + "/" + page_id_to_url.get(page_id, page_id)


def download_image(url: str, image_id: str) -> str:
    extention = os.path.splitext(urlparse(url).path)[1]
    print(f"Downloading image {url}, extention {extention}")
    image_name = f"{image_id}{extention}"
    urllib.request.urlretrieve(url, f"img/{image_name}")
    return image_name


def fetch(url: str):
    print(f"GET {url}")
    request = urllib.request.Request(url, method="GET", headers={
        "Authorization": f"Bearer {auth_token}",
        "Notion-Version": notion_api_version,
    })
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())


def get_page(page_id: str):
    return fetch(f"https://api.notion.com/v1/pages/{page_id}")


def get_block(block_id: str):
    return fetch(f"https://api.notion.com/v1/blocks/{block_id}")


def fetch_all(url):
    "Iterates through all pages and returns them all (non lazily)"
    results = []
    start_cursor = None
    while True:
        if start_cursor:
            iterator = fetch(f"{url}?page_size=100&start_cursor={start_cursor}")
        else:
            iterator = fetch(f"{url}?page_size=100")
        results.extend(iterator["results"])
        start_cursor = iterator["next_cursor"]
        if not iterator["has_more"]:
            break
    return results


def get_block_children(block_id) -> list:
    return fetch_all(f"https://api.notion.com/v1/blocks/{block_id}/children")


def read_built_pages():
    try:
        with open("built_pages.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except JSONDecodeError:
        return {}


def write_built_pages(built):
    with open("built_pages.json", "w+") as f:
        return json.dump(built, f)


def write_html(page_id: str, html: str):
    with open(f"{get_html_file_name(page_id)}.html", "w+") as f:
        return f.write(html)


def wrap(content: str, tag: str) -> str:
    return f"<{tag}>{content}</{tag}>"


def wrap_link(content: str, link: str) -> str:
    return f'<a href="{link}"">{content}</a>'


def get_page_link(page_id):
    page = get_page(page_id)
    return get_link(get_url(page_id), get_page_title(page), (page.get("icon") or {}).get("emoji"))


def build_text(text_items):
    html = ""
    for item in text_items:
        if item["type"] == "mention" and item["mention"]["type"] == "page":
            mention_id = item["mention"]["page"]["id"]
            html += get_page_link(mention_id)
            continue
        assert item["type"] == "text"
        content = escape(item["text"]["content"])
        link = item["text"]["link"]
        annotations = item["annotations"]
        if annotations["bold"]:
            content = wrap(content, "b")
        if annotations["italic"]:
            content = wrap(content, "i")
        if annotations["strikethrough"]:
            content = wrap(content, "s")
        if annotations["underline"]:
            content = wrap(content, "u")
        if annotations["code"]:
            content = wrap(content, "code")
        if link:
            content = wrap_link(content, link["url"])
        html += content
    return html


def get_page_title(page: dict) -> str:
    title = build_text(page["properties"]["title"]["title"])
    return title


def get_link(url: str, title: str, icon: Optional[str]) -> str:
    link = wrap_link(title, url)
    if icon:
        emoji = f'<span style="font-size: 1.2em; margin-right: 5px;">{icon}</span>'
        link = emoji + link
    return f'<div class="page-link">{link}</div>'


def build_children(root_block_id: str) -> str:
    html = ""

    is_opened = {"bulleted_list_item": False, "numbered_list_item": False}
    open_list = {"bulleted_list_item": "<ul>", "numbered_list_item": "<ol>"}
    close_list = {"bulleted_list_item": "</ul>", "numbered_list_item": "</ol>"}

    blocks = [*get_block_children(root_block_id), {"type": "[empty]"}]  # fake child to close lists
    for block in blocks:
        def text(tag: str, items) -> str:
            content = build_text(items)
            if block.get('has_children') and block_type != "child_page":
                content += build_children(block["id"])
            return wrap(content, tag)

        block_type = block["type"]

        for list_type in is_opened.keys():
            if is_opened[list_type] and block_type != list_type:
                html += close_list[list_type]
                is_opened[list_type] = False

        if block_type in is_opened.keys():
            if not is_opened[block_type]:
                html += open_list[block_type]
                is_opened[block_type] = True

        print(block)

        if block_type == "paragraph":
            content = text("p", block[block_type]["text"])
        elif block_type == "bulleted_list_item":
            content = text("li", block[block_type]["text"])
        elif block_type == "numbered_list_item":
            content = text("li", block[block_type]["text"])
        elif block_type == "code":
            content = wrap(text("code", block[block_type]["text"]), "pre")
        elif block_type == "quote":
            content = text("q", block[block_type]["text"])
        elif block_type == "heading_1":
            content = text("h1", block[block_type]["text"])
        elif block_type == "heading_2":
            content = text("h2", block[block_type]["text"])
        elif block_type == "heading_3":
            content = text("h3", block[block_type]["text"])
        elif block_type == "image":
            caption = build_text(block["image"]["caption"])
            image_type = block["image"]["type"]
            image_url = block["image"][image_type]["url"]
            image_name = download_image(image_url, block["id"])
            content = f'<img src="{base_url}/img/{image_name}" style="display: block; margin-left: auto; margin-right: auto"></img>'
            if content:
                content += f"<div>{caption}</div>"
        elif block_type == "child_page":
            content = get_page_link(block["id"])
        elif block_type == "column_list":
            content = f'<div class="flex-container">{build_children(block["id"])}</div>'
        elif block_type == "column":
            content = f'<div class="flex-child">{build_children(block["id"])}</div>'
        elif block_type == "[empty]":
            content = ""
        elif block_type == "embed" and "github" in block["embed"]["url"]:
            content = f'<script src="{block["embed"]["url"]}.js"></script>'
        elif block_type == "video" and "youtube" in block["video"]["external"]["url"]:
            regex_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", block["video"]["external"]["url"])
            video_id = regex_match.group(1)
            video_url = f"https://www.youtube.com/embed/{video_id}?feature=oembed&rel=0&controls=0"
            content = f'<div class="video"><iframe src="{video_url}" frameborder="0" ' \
                      f'sandbox="allow-scripts allow-popups allow-top-navigation-by-user-activation ' \
                      f'allow-forms allow-same-origin" allowfullscreen></iframe></div>'
        else:
            raise RuntimeError(f"Unknown block type {block['type']}")

        html += content
    return html


def build_html(page, page_id: str) -> str:
    title = get_page_title(page)
    icon = (page.get("icon") or {}).get("emoji")
    print(f"Page id: {page_id}, title: {title}")

    if page_id != main_page_id:
        home_link = f'<div class="home-link">{get_link("../", "Back", "")}</div>'
    else:
        home_link = ""

    # Pretty CSS inspired by https://sreeram-venkitesh.github.io/notion.css/
    html = (
        '<html>' +
        '<head>' +
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0,user-scalable=0"></meta>' +
        '<meta name="title" content="Ksenia"></meta>' +
        '<meta name="description" content="Product Designer"></meta>'
        f'<title>{title}</title>' +
        '<link rel="shortcut icon" href="../public/favicon.ico"></link>' +
        '<link rel="apple-touch-icon" href="favicon.ico"></link>' +
        '<link rel="stylesheet" href="style.css"></link>' +
        '</head>' +
        '<body>' +
        "<div class='main'>" +
        home_link
    )
    html += f"<h1 class='page_title' style='margin-top: 0.5em;'>{title}</h1>"
    html += build_children(page_id)
    html += home_link
    html += "</div></body></html>"
    return html


def substitute(template: str, vars: dict):
    for name, value in vars.items():
        template = template.replace("{{" + name + "}}", value)
    return template

built = {}
for page_id in [main_page_id, *page_id_to_url.keys()]:
    page = get_page(page_id)
    last_edited = page["last_edited_time"]
    built_pages = read_built_pages()
    last_built = built_pages.get(page_id)
    built[page_id] = last_edited
    if last_built == last_edited and force_rebuild != "1":
        print(f"Skip build page {page_id}, already built")
        continue
    html = build_html(page, page_id)
    write_html(page_id, html)

write_built_pages(built)
