#!/bin/bash

ART_DIR=articles


# The purpose of this script is to index all the specified articles
LINKS=""
for f in `find ./articles -name *.md`; do
    # sed is annoying
    html=$(echo $f | sed "s/\.\(\/.*\)\.md/\.\1\.html/g")
    html=$(echo $html | sed "s/markdown/html/g")
    pandoc -s --template ./articles/templates/article.html -t html $f -o $html

    html=$(echo $html | sed "s/\//\\\ \//g")
    html=$(echo $html | sed "s/ //g")

    title=$(grep "title: " $(echo $f) | sed "s/^title: \(.*\)$/\1/g")
    date=$(grep "date: " $(echo $f) | sed "s/^date: \(.*\)$/\1/g")
    LINKS="$LINKS<li>$date - <a href=\"$html\">$title<\/a><\/li>\n"
done

# Write the link list to the index file
sed -e "s/#LIST/$LINKS/g" $1 > index.html
