#!/usr/bin/env python

"""
make a note (card) for anki.
if anki is not running (sqlite3db not locked), will use anki py lib to add to db
otherwise use anki-connect http server plugin to add
"""



# https://www.juliensobczak.com/tell/2016/12/26/anki-scripting.html
# https://github.com/FooSoft/anki-connect

import sys, os

# Load Anki library
sys.path.append("anki") 
from anki.storage import Collection

# Define the path to the Anki SQLite collection
PROFILE_HOME = os.path.expanduser("~/Documents/Anki/User 1/") 
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

#front='front abcd'
#back='back abcd'
if len(sys.argv) < 3:
 print("USAGE:\n %s 'front' 'back'"%sys.argv[0])
 sys.exit(1)

front=sys.argv[1]
back=sys.argv[1]

# try using sql -- if anki is not running
try:
 # Load the Collection
 col = Collection(cpath, log=True) # Entry point to the API
 # get the deck we add all cards to
 deck = col.decks.byName("Default")
 
 # make a new note
 note = col.newNote()
 note.model()['did'] = deck['id']
 
 # add values to the note
 note.fields[0] = front
 note.fields[1] = back
 
 # import anki.models
 # [ x['name'] for x in note.model()['flds'] ]
 # 'Front', 'Back'
 
 # save the note
 res=col.addNote(note)
 #print(res)
 col.save() # maybe autosave?

# anki is running, use the anki-connect plugin
# https://github.com/FooSoft/anki-connect
# curl http://127.0.0.1:8765 -H "Content-Type: application/json" -X POST -d '{"action":"addNote","modelName":"Basic","params": {"deckName": "Default", "fields": {"Front":"FM","Back": "BM"} }}'
except:
 import requests
 import json
 import pprint
 address='http://127.0.0.1:8765'
 headers = {"Content-type": "application/json"}
 note={
    'action': 'addNote',
    'params': {
        'note':{
            'deckName': 'Default',
            'modelName': 'Basic',
            'fields': {
                'Front': front, 
                'Back': back,
            },
            'tags': []
        }
    }
 }
 print(json.dumps(note))
 r=requests.post(address,\
                data=json.dumps(note),\
                headers=headers)
 pprint.pprint(r)


# # Use the available methods to list the notes
# for cid in col.findNotes(""): 
#     note = col.getNote(cid)
#     front =  note.fields[0] # "Front" is the first field of these cards
#     print(front)
