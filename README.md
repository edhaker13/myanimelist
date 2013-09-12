# myanimelist #

MyAnimeList plugin for FlexGet

This plugin was based fuzzylights' plugin on
https://bitbucket.org/fuzzylights/plugins-for-flexget/wiki/Home
<br />
Although now this plugin doesn't contain any code from it.

Some series have stupidly long names on MyAnimeList, so these will most likely not match download inputs.
<br />
E.g. `Magi` is `Magi: The Labyrinth of Magic`

At the moment only animelist is supported, I might think about mangalist if anyone shows interest.

## Syntax ##

Allows to specify the username and from section of the list to pull.
```YAML
# Uses the default list: watching as a source list
myanimelist: username

# to specify a list
myanimelist:
  username: username
  list: watching | plan to watch | completed | on-hold | dropped
```

## Usage Example ##
```YAML
tasks:
  test:
    import_series:
      from:
        myanimelist:
      	  username: edhaker13
      	  list: plan to watch
```

# Added by plugins #
In this new version I also fetch some info from MyAnimeList and add it to the Entry,
you should be able to use it in other places like templates but I haven't tried it yet.

New fields available on both `myanimelist` and `search_myanimelist`:
  - `mal_id` the unique id for the anime in MyAnimeList
  - `mal_type` the type of show that it is like `Movie`, `OVA` or `TV`
  - `mal_image_url` the anime's poster image
  - `mal_episodes` the number of episodes in the anime
  - `mal_url` the link to the information page on [MyAnimeList.net](http://myanimelist.net)

Exclusive to `myanimelist`:
  - `mal_status` the show's airing status like `finished airing`, `currently airing` or `not yet aired`
  - `mal_user_score` the user's score on the list
  - `mal_watched_status` the show's status on the list

Exclusive to `seach_myanimelist`:
  - `description` the show's synopsis, usally a few lines long.

# Requirements #
- Python 2.5+
- Flexget
- This plugin
- An internet connection!

# Search Plugin #
Enter a search term and it will create entries from all the results found.
As I haven't implemented any narrowing options every entry will be added.

## Syntax ##
```YAML
# simple use
seach_myanimelist: query term

# advanced usage
search_myanimelist:
  - term
  - another term
```

## Usage Example ##
```YAML
# using a single query term
import_series:
  from:
    search_myanimelist: Free!

# using a list of queries
import_series:
  from:
    search_myanimelist:
      - Free! Specials
      - Clannad Movie
```

# Future Features #
If I have any ideas I will try to code them in, but I lack imagination.
Options to be improved in the future
- ~~Search: Enter query terms, return entries.~~ Made `search_myanimelist` plugin
- Add narrowing options to `seach_myanimelist` and `myanimelist`.
  - By `mal_type` this is the only term to use, that I can think of.

# Other Information #
I made this in my spare time, but feel free to make an issue if anything breaks.
If anyone has any ideas on what to add or anything to improve, I'll be happy to give it a try.
Also I'm an experienced programmer, so apologies in advance for anything that's horribly coded.
