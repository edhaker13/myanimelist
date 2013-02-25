myanimelist
===========

MyAnimeList plugin for FlexGet

This plugin is the fruit of rewriting fuzzylighs outdated plugin on
https://bitbucket.org/fuzzylights/plugins-for-flexget/wiki/Home

Mostly new code; this will search for the text in the anime title instead of
parsing the link with regex

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
preset:
  global:
    import_series:
    	from:
      		myanimelist:
      			username: edhaker13
      			list: plan to watch

tasks:
  test:
    accept_all: yes
```
Future Features
==============
If I have time I will try to code more functionality

Options to be enabled in the near future

- Search queries, return entries.

