#
# Renato Lacerda, 2016
#
# This is a simple way to make notes
# from the prompt command
# using Evernote API

"""
HUGE TODO LIST:

note = makes a new note
    -tag = add tags to the file
    -quick = title is "Quicknote"
    -book = sets the notebook

list = lists of all notes

books = list of all books

settings = opens up settings options
    change default notebook
    change quick title

login = logins

read = read the last X notes (Needs API permission from Evernote)
search = search the notes

When making a new note, should say what is the default notebook
and how to change it

Add a option to "undo"? (Need permission)

finding a way to set a "quick search" for tags

integrations that allow a quick add
"""
from __future__ import print_function
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import dev_keys
import click


from evernote.api.client import EvernoteClient

@click.group()
def cli():
    pass


@cli.command()
def version():
    """Checks if the lastest version is intalled, if so returns True"""
    version_ok = user_store.checkVersion(
         "Evernote EDAMTest (Python)",
         UserStoreConstants.EDAM_VERSION_MAJOR,
         UserStoreConstants.EDAM_VERSION_MINOR
    )
    print("Is my Evernote API version up to date? ", str(version_ok))
    print("")
    if not version_ok:
        exit(1)

@cli.command()
def list():
    """prints a list with all books in the account"""
    notebooks = note_store.listNotebooks()
    print("Found ", len(notebooks), " notebooks:")
    for notebook in notebooks:
        print("  * ", notebook.name)

@cli.command()
@click.argument("title")
@click.argument("body")
def note(title, body):
    """creates a note"""

    print("Creating a new note in the default notebook")

    # To create a new note, simply create a new Note object and fill in
    # attributes such as the note's title.
    note = Types.Note()
    note.title = title

    # The content of an Evernote note is represented using Evernote Markup Language
    note.content = "<?xml version='1.0' encoding='UTF-8'?>"
    note.content += "<!DOCTYPE en-note SYSTEM " \
        "'http://xml.evernote.com/pub/enml2.dtd'>"
    note.content += "<en-note>" + body + "<br/>"
    note.content += "</en-note>"

    # Finally, send the new note to Evernote using the createNote method
    # The new Note object that is returned will contain server-generated
    # attributes such as the new note's unique GUID.
    created_note = note_store.createNote(note)

    print("Successfully created a new note with GUID: ", created_note.guid)



# Real applications authenticate with Evernote using OAuth, but for the
# purpose of exploring the API, you can get a developer token that allows
# you to access your own Evernote account. To get a developer token, visit
# https://sandbox.evernote.com/api/DeveloperToken.action
auth_token = dev_keys.EVERNOTE_DEV_KEY

# Initial development is performed on our sandbox server. To use the production
# service, change sandbox=False and replace your
# developer token above with a token from
# https://www.evernote.com/api/DeveloperToken.action
client = EvernoteClient(token=auth_token, sandbox=True)

user_store = client.get_user_store()

note_store = client.get_note_store()

if __name__ == "__main__":
    cli()