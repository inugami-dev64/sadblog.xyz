#!/bin/python3
import os
import time
import subprocess

# Constant globals defining paths and templates to use
MARKDOWN_PATH = "articles/markdown/"
HTML_PATH = "articles/html/"
INDEX_TEMPLATE = "templates/index.html"
ARTICLE_TEMPLATE = "templates/article.html"
BLOG_TEMPLATE = "templates/blog.html"
RSS_TEMPLATE = "templates/rss.xml"

# How many blog posts would be shown on index.html
INDEX_HTML_BLOG_POST_COUNT = 5
SLEEP_INTERVAL = 60
GIT_PULL_UP_TO_DATE_MSG = "Already up to date.\n"


# Check if directory is created for article html
def check_dst():
    if not os.is_dir(HTML_PATH):
        print("Creating a directory for static html files")
        os.mkdir(HTML_PATH)


# Read the contents of markdown file and return a pair containing the title and date of the blog post
def extract_post_date_and_title(contents):
    title_index = contents.find("title: ")
    date_index = contents.find("date: ")

    title = contents[title_index + len("title: "): contents.find("\n", title_index)]
    date = contents[date_index + len("date: ") : contents.find("\n", date_index)]
    return (title, date)


# Generate html divs for blog.html
def create_blog_html_divs(articles, dates):
    year = dates[0][0:dates[0].find('-')]
    html = "<h2>" + year + "</h2><div class=\"list\"><ul>"

    # Add articles to html
    for i in range(0, len(articles)):
        cur_year = dates[i][0:dates[i].find('-')]

        # Current year does not match the active year
        if cur_year != year:
            year = cur_year
            html += "</ul></div><h2>" + year + "</h2><div class=\"list\"><ul>"

        html += articles[i]

    # Close the divisor
    html += "</ul></div>"
    return html

# Generate list items for index.html
def create_index_html_list(links):
    html = ""
    for i in range(0, min(INDEX_HTML_BLOG_POST_COUNT, len(links))):
        html += links[i]

    return html


# Update blog.html and index.html files
# Returns markdown files sorted by date
def update_html():
    links = []
    dates = []
    md_files = []
    for f in os.listdir(MARKDOWN_PATH):
        md_file = MARKDOWN_PATH + f
        html_file = "/blog/" + f.replace(".md", ".html")

        title_and_date = extract_post_date_and_title(open(md_file, 'r').read());
        dates.append(title_and_date[1])
        links.append("<li>" + title_and_date[1] + " - <a href=\"" + html_file + "\">" + title_and_date[0] + "</a></li>")

    dates.sort(reverse=True)
    links.sort(reverse=True)

    # For each link in links
    for l in links:
        href_pos = l.find("href=\"") + len("href=\"")
        path = l[href_pos: l.find("\"", href_pos)]
        path = path.replace("/blog", "articles/markdown")
        path = path.replace(".html", ".md")

        # Append to md_files
        md_files.append(path)
    
    # Read blog.html template and write output file
    blog_divs = create_blog_html_divs(links, dates)
    blog_html = open(BLOG_TEMPLATE, 'r').read()
    blog_html = blog_html.replace("#LIST", blog_divs)
    open("blog.html", 'w').write(blog_html)

    # Read index.html template and write output file
    index_list = create_index_html_list(links);
    index_html = open(INDEX_TEMPLATE, 'r').read()
    index_html = index_html.replace("#LIST", index_list)
    open("index.html", 'w').write(index_html)

    return md_files



# Generate all pages from changes that happened during the commit
def generate_pages(files):
    # For each markdown file in path generate an html file
    for in_file in files:
        out_file = in_file.replace(".md", ".html")
        out_file = out_file.replace("markdown", "html")
        os.system("pandoc -s --template " + ARTICLE_TEMPLATE + " -t html " + in_file + " -o " + out_file)


# Generate rss feed from provided markdown files
def generate_rss(files):
    rss = ""
    for f in files:
        f_rss = subprocess.check_output("pandoc-rss " + f, shell=True)
        rss += f_rss.decode("utf-8")

    rss_template = open(RSS_TEMPLATE, 'r').read()
    out_rss = rss_template.replace("#RSS", rss)
    open("rss.xml", 'w').write(out_rss)


# Find all modified markdown files from previous commit
def find_md_diffs():
    result = subprocess.check_output("git diff --name-only HEAD HEAD~1", shell=True)
    files = result.decode("utf-8").split(sep="\n")

    output = []
    for i in range(0, len(files) - 1):
        if files[i].find(".md") != -1 and files[i].find("articles/markdown") != -1:
            output.append(files[i])

    return output


# Main server process loop
while True:
    # Attempt to perform git pull
    pull = subprocess.check_output("git pull origin master", shell=True)

    if pull.decode("utf-8") == GIT_PULL_UP_TO_DATE_MSG:
        print("Generating new html files")
        generate_pages(find_md_diffs())
        md_files = update_html()
        generate_rss(md_files)
        print("Done generating html files and rss feed")

    time.sleep(SLEEP_INTERVAL)
