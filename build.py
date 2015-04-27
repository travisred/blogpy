import os
import codecs
import re

import markdown

from settings import Settings

class Post:
    title = ""
    date = ""
    url = ""

def rss(posts):
  rss_body = """<rss version="2.0">
  <channel>
  \t<title>""" + Settings.site_name + """</title>
  \t<link>""" + Settings.site_root + """</link>
  \t<description>""" + Settings.site_description + """</description>"""
  
  for post in posts:
    rss_body += """\n\t<item>
    \t\t<title>""" + post.title + """</title>
    \t\t<pubDate>""" + post.date + """</pubDate>
    \t\t<link>""" + post.url + """</link>
    \t</item>"""

  rss_body += "\n\t</channel>\n</rss>"
  rss_file = codecs.open("site/rss.xml", mode="w", encoding="utf8")
  rss_file.write(rss_body)
  rss_file.close()

def parse_posts(posts):
  parsed_posts = []
  for post in posts:
    parsed_post = Post()

    # Read post markdown file
    input_file = codecs.open("md/"+post, mode="r", encoding="utf8")
    file_content = input_file.read()
    input_file.close()

    file_content_lines = file_content.split('\n')
    
    parsed_post.slug = post
    parsed_post.title = file_content_lines[0]
    parsed_post.date = file_content_lines[1]
    parsed_post.url = Settings.site_root + post + '/'
    parsed_post.html = '\n'.join(file_content_lines[2:])
    parsed_post.html = markdown.Markdown().convert(parsed_post.html)
    parsed_posts.append(parsed_post)
      
    parsed_posts.sort(key = lambda x: x.date, reverse=True)
  
  return parsed_posts

posts = os.listdir(os.getcwd()+"/md")

header_file = codecs.open("static/header", mode="r", encoding="utf8")
header = header_file.read()
header_file.close()
header = header.replace("site_root", Settings.site_root)
header = header.replace("site_name", Settings.site_name)
header = header.replace("site_description", Settings.site_description)

footer_file = codecs.open("static/footer", mode="r", encoding="utf8")
footer = footer_file.read()
footer_file.close()
footer = footer.replace("site_root", Settings.site_root)

parsed_posts = parse_posts(posts)

postgroup = ""
for i in range(len(parsed_posts[0:11])):
  postgroup = postgroup + "<li><a href='" + (parsed_posts[i].url + 
    "'>" + parsed_posts[i].title + "</a></li>")

index_body = ""
for i in range(len(parsed_posts[0:Settings.number_of_posts_on_front_page - 1])):
  index_html = parsed_posts[i].html.replace('../img/', 'img/')
  index_body = index_body + "<div><a href='" + (parsed_posts[i].url + 
    "'><h1>" + parsed_posts[i].title) + ("</h1><hr>" + parsed_posts[i].date +
    "</a>" + index_html + "</div>")

index_header = header.replace("page_title", Settings.site_name)
index_file = codecs.open("site/index.html", mode="w", encoding="utf8")
index_file.write(index_header + (index_body +
  footer.replace("<!-- recent posts -->", postgroup)))
index_file.close()

for parsed_post in parsed_posts:
  if not os.path.exists("site/" + parsed_post.slug):
    os.makedirs("site/" + parsed_post.slug)
  post_file = codecs.open("site/" + (parsed_post.slug +
    "/index.html"), "w", encoding="utf8")

  curr_header = header.replace("page_title", parsed_post.title)
  curr_header = curr_header.replace("css/style.css", "../css/style.css")
  title_h1 = "<h1>" + parsed_post.title + "</h1>"
  date_hr = "<hr>" + parsed_post.date + "<hr>"
  post_file.write(curr_header + title_h1 + date_hr + (parsed_post.html +
    footer.replace("<!-- recent posts -->", postgroup)))
  post_file.close()

archive_header = index_header
archive_header = archive_header.replace("page_title", "Archive - " + Settings.site_name)
archive_header = archive_header.replace("css/style.css", "../css/style.css")

archive_body = ""
for i in range(len(parsed_posts)):
  archive_body = archive_body + "#" + str(i) + " - " +"<span>" + parsed_posts[i].date + "</span> <a href='" + parsed_posts[i].url + "'>" + parsed_posts[i].title + "</a><br>"

archive_file = codecs.open("site/archive/index.html", mode="w", encoding="utf8")
archive_file.write(archive_header + archive_body + footer.replace("<!-- recent posts -->",postgroup))
archive_file.close()

rss(parsed_posts)
