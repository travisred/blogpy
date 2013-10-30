blogpy v2.0
======

![blogpy](http://git.xtimer.org/img/screenshot.png)

A static blog generator written in python. You can see it in action at [blogpy.reddino.org](http://blogpy.reddino.org).

**Requirements:**
* Python 2.7
* Python-Markdown package

**How to use:**
<ol>
<li>git clone https://github.com/travisred/blogpy.git</li>
<li>edit settings.py to fit your site</li>
<li>edit static/comment to add your disqus code</li>
<li>add a markdown-formatted post to md -- you can see an example at md/hello</li>
<li>python build.py</li>
<li>upload the "site" directory to host</li>
</ol>

Note: as of v2.0, links for posts changed from /md-file-title.html to /md-file-title/.

Licensed under GPL v3.0.