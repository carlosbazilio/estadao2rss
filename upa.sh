#!/bin/sh
PATH=/usr/local/bin:/usr/local/sbin:~/bin:/usr/bin:/bin:/usr/sbin:/sbin:/anaconda3/bin/python
. env/bin/activate
python estadao2rss.py
git add *.xml
dia=$(date '+%d/%m/%Y')
git commit -m "Atualização Automática - ${dia}"
git push
