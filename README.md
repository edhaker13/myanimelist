myanimelist
===========

MyAnimeList plugin for FlexGet

This plugin is the fruit of rewriting fuzzylighs outdated plugin on
https://bitbucket.org/fuzzylights/plugins-for-flexget/wiki/Home

Mostly new code; this will search for the text in the anime title instead of
parsing the link with regex

Some series have stupidly long names on MAL, so these will most likely not find a match
Ex. Magi, Magi: The Labyrinth of Magic
Syntax
======
The current version only allows to specify the username and the list to pull
``` YAML
myanimelist:
    username: username
    list: plan to watch|watching
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
    accept_all: yes
```
Requirements
=============
- Python 2.5+
- Flexget

Future Features
==============
If I have time I will try to code more functionality

Options to be researched in the near future
- Search: Enter query terms, return entries.

Other Information
==============
I made this in my spare time, but feel free to make an issue if anything breaks.
If anyone has any ideas on what to add or anything to improve, I'll be happy to give it a try.
Also I'm not a proper programmer, so apologies in advance for anything that's horribly wrong.
