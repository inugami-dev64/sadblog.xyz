#!/bin/bash

gen() {
    LINKS=""
    for f in ./articles/markdown/*.md; do
        html=$(echo $f | sed "s/\.\(\/.*\)\.md/\1\.html/g")
        html=$(echo $html | sed "s/markdown/html/g")
        pandoc -s --template ./articles/templates/article.html -t html $f -o .$html
 
        title=$(grep "title: " $(echo $f) | sed "s/^title: \(.*\)$/\1/g")
        date=$(grep "date: " $(echo $f) | sed "s/^date: \(.*\)$/\1/g")
 
        html=$(echo $html | sed "s/articles\/html/blog/g")
        LINKS="$LINKS<li>$date - <a href=$html>$title</a></li>\\\n"
    done
 
    # Write the link list to the index file
    LINKS=$(echo -e $LINKS | sort -r -d)
    echo -e $LINKS
    sed -e "s|#LIST|$LINKS|g" $1 > index.html
}

# $1 is index.html template
# $2 is article.html template
gen $1 $2
