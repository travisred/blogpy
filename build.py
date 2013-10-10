import os, markdown, codecs, string, re
from settings import Settings

index_posts = []
recent_posts = []
archive_links = []

posts = os.listdir(os.getcwd()+"/md")
index_file = codecs.open("site/index.html", mode="w", encoding="utf8")

archive_file = codecs.open("site/archive/index.html", mode="w", encoding="utf8")

header_file = codecs.open("static/header", mode="r", encoding="utf8")
header = header_file.read()
header_file.close()
header = string.replace(header, "site_root", Settings.site_root)
header = string.replace(header, "site_description", Settings.site_description)

footer_file = codecs.open("static/footer", mode="r", encoding="utf8")
footer = footer_file.read()
footer_file.close()
footer = string.replace(footer, "site_root", Settings.site_root)

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

  index_posts.append("<hr><div class="+date+"><a href='"+Settings.site_root+post+"/index.html'><h1>" + string.replace(title, '#', '') + "</h1></a>"+html[html_post_start.start():]+"</div>")
  archive_links.append("<span>"+date+"</span><a href='"+Settings.site_root+post+"/index.html'>" + string.replace(title, '#', '') + "</a><br />")
  recent_posts.append("<li class="+date+"><a href='"+Settings.site_root+post+"/index.html'>"+string.replace(title, '#', '') +"</a></li>")

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
  if (index_post_count<5):
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
