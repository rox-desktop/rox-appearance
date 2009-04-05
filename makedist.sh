#!/bin/sh

SCRIPT=`echo "$0" | sed 's|^\./||'`
echo "$SCRIPT" | grep -q '^/' || SCRIPT=`pwd`/"$SCRIPT"
APPDIR=`dirname "$SCRIPT"`
APPNAME=`basename "$APPDIR"`
VERSION=`grep '<Version>' "$APPDIR/AppInfo.xml" | sed 's/.*<Version>\([0-9.]*\).*/\1/'`
cd "$APPDIR/.."
TARNAME=`echo $APPNAME | tr '[:upper:]' '[:lower:]'`
tar cfz "${TARNAME}-${VERSION}.tar.gz" --exclude='*.pyc' --exclude='.svn' \
        --transform="s|^|${TARNAME}-${VERSION}/|" "$APPNAME"
