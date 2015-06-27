blogpy v2.0
======

![blogpy](https://raw.github.com/travisred/blogpy/master/screenshot.png)

A static blog generator written in python. You can see it in action at [blogpy.magnatecha.com](http://blogpy.magnatecha.com).

**Requirements:**
* Python 2.7
* Python-Markdown package

**How to use:**
<ol>
<li>git clone https://github.com/travisred/blogpy.git</li>
<li>edit settings.py to fit your site</li>
<li>add a markdown-formatted post to md -- you can see an example at md/hello</li>
<li>python build.py</li>
<li>upload the "site" directory to host</li>
</ol>

Note: as of v2.0, links for posts changed from /md-file-title.html to /md-file-title/.

Licensed under GPL v3.0.

If you need somewhere to host your site, check out [Digital Ocean](https://www.digitalocean.com/?refcode=314851abcefa)
