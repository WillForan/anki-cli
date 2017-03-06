#!/usr/bin/env python
import os,sys

"""
make a note (card) for anki.
if anki is not running (sqlite3db not locked), will use anki py lib to add to db
otherwise use anki-connect http server plugin to add
"""



# https://www.juliensobczak.com/tell/2016/12/26/anki-scripting.html
# https://github.com/FooSoft/anki-connect





"""
add note using anki py libs
will error if db is locked (anki is open)
"""
def viadb(front,back):
  # Define the path to the Anki SQLite collection
  PROFILE_HOME = os.path.expanduser("~/Documents/Anki/User 1/") 
  cpath = os.path.join(PROFILE_HOME, "collection.anki2")
  thispath= os.path.dirname(os.path.abspath(__file__))
  # Load Anki library
  sys.path.append(thispath + "/anki") 
  from anki.storage import Collection
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

"""
use anki-connect plugin to add a card when anki is running
"""
def viaplugin(front,back):
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



def main():
  #front='front abcd'
  #back='back abcd'
  if len(sys.argv) < 3:
    print("USAGE:\n %s 'front' 'back'"%sys.argv[0])
    sys.exit(1)

  front=sys.argv[1]
  back=sys.argv[2]
  
  # try using sql -- if anki is not running
  try:
    viadb(front,back)
  # anki is running, use the anki-connect plugin
  except:
    viaplugin(front,back)


"""
run main if we aren't importing
"""
if __name__ == "__main__":
    main()
