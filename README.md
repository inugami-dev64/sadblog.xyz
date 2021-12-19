# Source code and original markdown articles for https://sadblog.xyz

Python script is used to generate static html sites for markdown blog posts that are retrieved with each `git pull` request. The script will then 
check after every 60 seconds for any changes in the remote repository and if needed regenerate rss feed and html sites. 


## Prerequisites

You will need to make sure following prerequisites are installed:  
* [pandoc-rss](https://github.com/chambln/pandoc-rss)
* pandoc
* git (obviously)
* some kind of webserver (Nginx or Apache)


## Getting started

Generate initial sites with following command `python3 /scripts/server.py all`. Now you should have generated all static html sites and you can serve them 
directly if you wish so. But for continuous updates create this systemd unit file to `/etc/systemd/system/sadblog.service` with following contents:  

```
[Unit]
Description=Sadblog server static content generation service

[Service]
Type=simple
WorkingDirectory=/var/www/sadblog
ExecStart=/var/www/sadblog/scripts/server.py

[Install]
WantedBy=multi-user.target
```
After that just enable and start the service with following commands:  
`# systemctl enable sadblog`  
`# systemctl start sadblog`

Now you should have your server backend successfully set up. In your webserver configuration make sure that `/blog` path serves `/blog.html` and `/blog/.*\.html` 
serves all html files from `/articles/html/` directory.
