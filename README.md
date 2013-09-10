myanimelist
===========

MyAnimeList plugin for FlexGet

This plugin is the fruit of rewriting fuzzylights outdated plugin on
https://bitbucket.org/fuzzylights/plugins-for-flexget/wiki/Home

Mostly new code; this will search for the text in the anime title instead of
parsing the link with regex

Some series have stupidly long names on MAL, so these will most likely not find a match
Ex. Magi, Magi: The Labyrinth of Magic
Syntax
======
The current version only allows to specify the username and the list to pull.
``` YAML
# Uses watching as a source list
myanimelist: username

# to specify a list
myanimelist:
    username: username
    list: watching | plan to watch | completed | on-hold | dropped
```
Usage Example
============
``` YAML
tasks:
  test:
    import_series:
      from:
        myanimelist:
      	  username: edhaker13
      	  list: plan to watch
    accept_all: yes # this is just to skip filtering on the test
```
Requirements
=============
- Python 2.5+
- Flexget
- An internet connection!

Future Features
==============
If I have any ideas I will try to code them in, but I lack imagination.

Options to be improved in the future
- Search: Enter query terms, return entries.
    - Implemented in search_myanimelist plugin, it might return too many entries.
```YAML
import_series:
     from:
        search_myanimelist: Free!
```

Other Information
==============
I made this in my spare time, but feel free to make an issue if anything breaks.
If anyone has any ideas on what to add or anything to improve, I'll be happy to give it a try.
Also I'm an experienced programmer, so apologies in advance for anything that's horribly coded.
