#!/bin/bash
# The purpose of this script is to index all the specified articles
IFS=""

# Check if the template exists
check_template() {
    if [ -z $1 ]; then
        echo "Please specify the index.html template"
        exit 1
    fi

    if [ -z $2 ]; then
        echo "Please specify the article template"
        exit 1
    fi
}


gen() {
    LINKS=""
    for f in ./articles/markdown/*.md; do
        html=$(echo $f | sed "s/\.\(\/.*\)\.md/\1\.html/g")
        html=$(echo $html | sed "s/markdown/html/g")
        pandoc -s --template ./articles/templates/article.html -t html $f -o .$html

        title=$(grep "title: " $(echo $f) | sed "s/^title: \(.*\)$/\1/g")
        date=$(grep "date: " $(echo $f) | sed "s/^date: \(.*\)$/\1/g")

        LINKS="$LINKS<li>$date - <a href=$html>$title</a></li>\\\n"
    done

    # Write the link list to the index file
    LINKS=$(echo -e $LINKS | sort -r -d)
    echo -e $LINKS
    sed -e "s|#LIST|$LINKS|g" $1 > index.html
}


while :; do
    pull=$(git pull origin master 2>/dev/null | grep "Already up to date")

    if [[ -n $pull ]]; then
        check_template $1 $2
        gen $1 $2
    fi

    sleep 1m
done
