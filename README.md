# myanimelist #

MyAnimeList plugin for FlexGet

This plugin was inspired fuzzylights' plugin on
https://bitbucket.org/fuzzylights/plugins-for-flexget/wiki/Home
<br />
Although now this plugin doesn't contain any code from it.

Some series have stupidly long names on MyAnimeList, so these will most likely not match download inputs.
<br />
E.g. `Magi` is `Magi: The Labyrinth of Magic`

At the moment only animelist is supported, I might think about mangalist if anyone shows interest.

*NOTE*
This flexget myanimelist plugin is whitelisted by MAL’s security systems.
If you’re planning to use this plugin to work with more than a couple of dozen MAL users' accounts at once,
you should register your application at https://atomiconline.wufoo.com/forms/mal-api-usage-notification/
to ensure that MAL’s security systems don’t automatically block you and all other flexget-myanimelist users.

You can override what user-agent to use by putting the string in the options, like so:
```YAML
myanimelist:
    username: username
    user-agent: api-team-12345 # or what ever
```

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
  - `mal_status` the show's airing status like `finished airing`, `currently airing` or `not yet aired`

Exclusive to `myanimelist`:
  - `mal_my_score` your score on the list
  - `mal_my_status` your show's status on the list

Exclusive to `search_myanimelist`:
  - `description` the show's synopsis, usually a few lines long.

# Requirements #
- Python 2.5+
- Flexget
- This plugin
- An internet connection!

# Search Plugin #
Enter a search term and it will create entries from all the results found.
As I haven't implemented any narrowing options every entry found will be added.

*NOTE*: As the official MyAnimeList API requires authentication I made an account for this plugin, please don't change
anything on that account. It will screw up everything.
Also the same white listing thing applies, but there is no easy overriding the user-agent yet.

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
If I have any ideas I will try my best to implement them in, but I lack imagination so I probably won't come up with anything.
Options to be improved in the future
- ~~Search: Enter query terms, return entries.~~ Made `search_myanimelist` plugin
- Add narrowing options to `seach_myanimelist` and `myanimelist`.
  - By `mal_type` this is the only term that I can think of.

# Other Information #
I made this in my spare time, but feel free to make an issue if anything breaks. __I'm a student, I forget things, give me a nudge if I don't answer._
If anyone has any ideas to add or anything to improve; Create an issue, I'll be happy to give it a go.
I should say I'm an not a very experienced programmer, so apologies in advance for anything that's horribly implemented.
