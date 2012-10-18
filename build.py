import os, markdown, codecs, string, re

site_root = ""
index_posts = []
recent_posts = []
archive_links = []

posts = os.listdir(os.getcwd()+"/md")
index_file = codecs.open("site/index.html", mode="w", encoding="utf8")

archive_file = codecs.open("site/archive.html", mode="w", encoding="utf8")

header_file = codecs.open("static/header", mode="r", encoding="utf8")
header = header_file.read()
header_file.close()

footer_index = codecs.open("static/footer", mode="r", encoding="utf8")
footer_i = footer_index.read()
footer_index.close()

footer_post = codecs.open("static/footer_post", mode="r", encoding="utf8")
footer_p = footer_post.read()
footer_post.close()

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

  index_posts.append("<hr><div class="+date+"><a href='"+post+".html'><h1>" + string.replace(title, '#', '') + "</h1></a>"+html[html_post_start.start():]+"</div>")
  archive_links.append("<span>"+date+"</span><a href='"+post+".html'>" + string.replace(title, '#', '') + "</a><span><br />")
  recent_posts.append("<li class="+date+"><a href='"+site_root+post+".html'>"+string.replace(title, '#', '') +"</a><li>")

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

index_header = string.replace(header, "titlefixed", "blogpy")
index_file.write(index_header + index_body + string.replace(footer_i, "<!-- recent posts -->", postgroup))
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
  post_file = codecs.open("site/"+post+".html", "w", encoding="utf8")

  titlefixed = string.replace(title, '#', '')
  titlefixed = string.replace(titlefixed, '\n', '')
  curr_header = string.replace(header, "titlefixed", titlefixed)

  post_file.write(curr_header + html + string.replace(footer_p, "<!-- recent posts -->", postgroup))
  post_file.close()

archive_links_count = len(archive_links)
archive_body = ""
for link in archive_links:
  archive_body = archive_body + "#" + str(archive_links_count) + " - " + link
  archive_links_count -= 1

archive_file.write(index_header + archive_body + string.replace(footer_i,"<!-- recent posts -->",postgroup))
archive_file.close()
