## Adding and removing triggers in game

You can add triggers in game by typing

` #add_trigger [word or phrase] `


Similarly, you can remove triggers by typing

` #remove_trigger [word or phrase] `


Note: to remove a trigger, you must match the syntax of the existing trigger exactly. That includes capitalization and spaces (but does not include leading and trailing whitespace).

## Adding and removing ignore words in game

Ignore words are words that will prevent a trigger from firing if the ignore word is in the same line as a trigger. For example, if one of your triggers is "tells you", you would get a notification every time you visit Dogle Pitt. If you don't want to get a notification for visiting Dogle Pitt, but still want a notification for tells, you can add Dogle to your ignore words.

You can add ignore words in game by typing

` #add_ignore [word or phrase] `


Similarly, you can remove ignore words by typing

` #remove_ignore [word or phrase] `


## Setting Timers

This was the top requested feature for the update. The parser currently supports manually setting an infinite number of concurrent timers, and will alert you with a custom word 5 seconds before that timer is up.

You can start a timer by typing:

` #start_timer [word or phrase], [number of seconds] `


Note: Syntax is very important here. If you forget a comma between your word and the number of seconds, the timer will not set.

The above commands are configurable in the eqparse_config.json file. 
