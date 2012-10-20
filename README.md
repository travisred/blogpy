blogpy
======

![blogpy](https://raw.github.com/travisred/blogpy/master/screenshot.png)

A simple static blog generator in python. You can see it in action at [magnatecha.com](http://magnatecha.com).

**Requirements:**
* Python 2.7
* Python-Markdown package

**How to use:**
<ol>
<li>git clone https://github.com/travisred/blogpy.git</li>
<li>edit /settings.py to add your site title and description</li>
<li>add a markdown-formatted post to /md -- you can see an example at /md/hello</li>
<li>python build.py</li>
<li>upload /site /css /js to host</li>
</ol>

**TODO:**
* Re-enable Disqus comments option

*Note: blogpy was built and tested using Ubuntu 12.04. A system varying from that might produce unexpected results. However, I'm open to any fixes or pull requests :)*


