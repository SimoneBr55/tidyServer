# tidyServer
Scripts to screen new files and create daily photo clips.


# Introduction #

I setup the automatic photo upload from my devices to my server. The net result is that I do not lose any photo, however I end up with lots of photos with weird names (due to Android traditions) without any clear reference to the date of shoot and the context. I also have lots of duplicates, due to - again - peculiar Android traditions.

# Solution #

I thought about it and came up with the following solution. I wrote a series of scripts in python that take care of the problem. 

_hash_start.py_ scans through the photos and calculates a digest of them and stores the hashes and the names in two 'synced' files. The photos that have the same hashes are chosen and discarded (temporarily in a photo bin, though).

_hash_checker.py_ check the newly added photos against the existing hashes and determines if the photos in question are new or duplicates. 

_sort_misc.py_ runs through a selected folder and try and determine the date of the images. Then, it sorts them in a ordered directory structure.

_dailyPhoto.py_ is a bonus script that finds photos and videos in your library that were shoot in the current d/m of the previous years and collates them in two nice videos. (The video compilation is a bit shaky and fails often)

Then, I wrote some bash scripts that (together with some good cronjobs) will keep automagically updated everything.

# Order of Execution #

The scripts are run in the following sequence.

Monthly (manually the first time): _monthly_update.sh_ -> _hash_start.py_

Daily: _dailyPhoto.sh_ -> _dailyPhoto.py_ -> _ffmpeg_creator.sh_

Weekly: _weekly_update.sh -> hash_checker.py -> sort_misc.py -> sort_noname.py (experimental, disabled)_

# Configuration #

You will see that in all scripts there are no variables (i.e. paths) getting set directly. Bash scripts source .set_env_vars to get the variables; Pyhton scripts source .env via the _decouple_ module. In the root directory of this git you will find .set_env_vars.conf and .env.conf files which list all the variables you have to set. I wrote a simple description in those files. (If after cloning you do not find these files: remember, those are hidden files and should be regarded as such). Be nice and copy them to '.set_env_vars' and '.env' in your local machine, edit them and then they will be sourced.
