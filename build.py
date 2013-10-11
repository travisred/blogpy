__author__ = "Travis Reddell"
__copyright__ = "Copyright 2013, Travis Reddell"
__credits__ = ["Travis Reddell"]
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Travis Reddell"
__email__ = "t@reddino.org"
__status__ = "Production"

import os, markdown, codecs, string, re
from settings import Settings

index_posts = []
recent_posts = []
archive_links = []

posts = os.listdir(os.getcwd()+"/md")
index_file = codecs.open("site/index.html", mode="w", encoding="utf8")
rss_file = codecs.open("site/rss.xml", mode="w", encoding="utf8")
archive_file = codecs.open("site/archive/index.html", mode="w", encoding="utf8")

header_file = codecs.open("static/header", mode="r", encoding="utf8")
header = header_file.read()
header_file.close()
header = string.replace(header, "site_root", Settings.site_root)
header = string.replace(header, "site_name", Settings.site_name)
header = string.replace(header, "site_description", Settings.site_description)

footer_file = codecs.open("static/footer", mode="r", encoding="utf8")
footer = footer_file.read()
footer_file.close()
footer = string.replace(footer, "site_root", Settings.site_root)

# The ugliest RSS feed generator. Should clean it up someday.
def rss(posts, rss_file):
  rss_body = """<rss version="2.0">
  <channel>
  \t<title>""" + Settings.site_name + """</title>
  \t<link>""" + Settings.site_root + """</link>
  \t<description>""" + Settings.site_description + """</description>"""
  posts_dates = []
  for post in posts:
    input_file = codecs.open("md/"+post, mode="r", encoding="utf8")
    file_content = input_file.read()
    file_content_lines = string.split(file_content, '\n')
    title = string.replace(file_content_lines[0], '# ', '')
    title = string.replace(title, ' #', '')
    date = file_content_lines[2]
    input_file.close()
    posts_dates.append(date + "**" + title + "**" + post) #ermygawd, custom delimiter!
    posts_dates.sort()
    posts_dates.reverse()

  for p in posts_dates:
    post_pieces = string.split(p, "**")
    rss_body += """\n\t\t<item>
    \t<title>""" + post_pieces[1] + """</title>
    \t<pubDate>""" + post_pieces[0] + """</pubDate>
    \t<link>""" + Settings.site_root + post_pieces[2] + """/</link>
    </item>"""

  rss_body += "\n\t</channel>\n</rss>"
  rss_file.write(rss_body)
  rss_file.close()


for post in posts:
  input_file = codecs.open("md/"+post, mode="r", encoding="utf8")

  file_content = input_file.read()
  file_content_lines = string.split(file_content, '\n')
  title = file_content_lines[0]
  date = file_content_lines[2]
  input_file.close()

  md = markdown.Markdown()
  html = md.convert(file_content)

  html_post_start = re.search('<div class="articleline2"></div>', html)

  index_posts.append("<hr><div class="+date+"><a href='"+Settings.site_root+post+"/'><h1>" + string.replace(title, '#', '') + "</h1></a>"+html[html_post_start.start():]+"</div>")
  archive_links.append("<span>"+date+"</span><a href='"+Settings.site_root+post+"/'>" + string.replace(title, '#', '') + "</a><br>")
  recent_posts.append("<li class="+date+"><a href='"+Settings.site_root+post+"/'>"+string.replace(title, '#', '') +"</a></li>")

#sort posts by publication date
recent_posts.sort()
recent_posts.reverse()

#sort archive links by publication date
archive_links.sort()
archive_links.reverse()

#sort index posts by publication date
index_posts.sort()
index_posts.reverse()

postgroup = ""
postgroup_count=0
for post in recent_posts:
  if(postgroup_count<12):
    postgroup = postgroup + post
  postgroup_count+=1

index_body = ""
index_post_count = 0
for link in index_posts:
  if (index_post_count < Settings.number_of_posts_on_front_page):
   index_body = index_body + link
  index_post_count += 1

index_header = string.replace(header, "page_title", Settings.site_name)
index_file.write(index_header + index_body + string.replace(footer, "<!-- recent posts -->", postgroup))
index_file.close()

post_count = 0
for post in posts:

  post_count+=1

  input_file = codecs.open("md/"+post, mode="r", encoding="utf8")
  file_content = input_file.read()
  input_file.close()

  title = string.split(file_content, '\n')[0]
  
  md = markdown.Markdown()
  html = md.convert(file_content)
  if not os.path.exists("site/" + post):
    os.makedirs("site/" + post)
  post_file = codecs.open("site/"+post+"/index.html", "w", encoding="utf8")

  title = string.replace(title, '#', '')
  title = string.replace(title, '\n', '')
  curr_header = string.replace(header, "page_title", title)
  curr_header = string.replace(curr_header, "css/style.css", "../css/style.css")

  post_file.write(curr_header + html + string.replace(footer, "<!-- recent posts -->", postgroup))
  post_file.close()

archive_links_count = len(archive_links)
archive_header = index_header
archive_header = string.replace(archive_header, "page_title", "Archive - " + Settings.site_name)
archive_header = string.replace(archive_header, "css/style.css", "../css/style.css")

archive_body = ""
for link in archive_links:
  archive_body = archive_body + "#" + str(archive_links_count) + " - " + link
  archive_links_count -= 1

archive_file.write(archive_header + archive_body + string.replace(footer,"<!-- recent posts -->",postgroup))
archive_file.close()

rss(posts, rss_file)
