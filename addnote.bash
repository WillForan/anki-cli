#!/usr/bin/env bash
set -e
# uses dmenu patched with imlib2
#
# get front and back of a card
# from answers/back can be:
#   screenshot,
#   xclip,
#   stored picture
MEDIAFOLDER="$HOME/Documents/Anki/User 1/collection.media"

# use dmenu for the image menu
# remove any leading apostrophe -- useful to enter text that is a partial match for another selection
# eg ''take  to not match 'take_a_screenshot'
imgmenu() {
  dmenu -is 300 -l 15 | 
  sed "1 s/^''//"
}

clipboard() {
 xclip -o $@|
 sed "
   s/'/\&#39;/g;
   s/\"/\&#34;/g;" |
 sed ':a;N;$!ba;s/\n/<br>/g'
}

front(){
 pick=$(
  (
  clipboard
  clipboard -selection CLIPBOARD
  ) | imgmenu
 )
 [ -z "$pick" ] && return 1
 echo $pick
}


# run dmenu on images to select one (or take a screenshot)
pict_opts(){
  local screenshottext="take_a_screenshot"

  local pick=$(
   (echo ;find "$MEDIAFOLDER"  -regex '.*\(png\|jpg\|jpeg\|gif\)') |
   sed "s:$MEDIAFOLDER/\(.*\)$:&\t\1:;
        s/^/IMG:/;
        1i '$(clipboard )'
        1i '$(clipboard -selection CLIPBOARD)'
        1i $screenshottext
        /^IMG:$/d;
        "|
   imgmenu
  )

  # killed dmenu
  [ -z "$pick" ] && return 1

  # want to take a screenshot
  if [ "$pick" == "$screenshottext" ]; then
    local desc=$(echo $1 | cut -d' ' -f1-5 |tr ' ' _)
    [ -n "$desc" ] && desc=_$desc
    pick=$(date +%F_%H:%M)$desc.png
    scrot -s "$MEDIAFOLDER/$pick"
  fi

  finalimgortext="$pick"
  [  -r "$MEDIAFOLDER/$finalimgortext" ] && finalimgortext="<img src='$pick' >"
  echo $finalimgortext
}

f="$(front)"
b="$(pict_opts $f)"

./addnote_anki.py "$f" "$b"
