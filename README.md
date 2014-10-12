# TerraMotusServer :: 15-112 Term Project (Add-On)

## Overview
_TerraMotusServer_ is an extension to
[TerraMotus](https://github.com/Alex4913/TerraMotus). This enables the base
program to interact with a server to upload and download maps. 

The server is run on top of [Apache 2.x](http://httpd.apache.org/) and uses
[FastCGI](http://www.fastcgi.com/) for direct Python interaction with the
generation of the requested page. Built into this server are a few methods
to generate images from the stored files.
