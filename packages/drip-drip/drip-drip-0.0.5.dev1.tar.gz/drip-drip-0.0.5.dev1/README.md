[drip_feed](https://gitlab.com/nest.lbl.gov/drip_feed) contains the python package that provides a utility to control automatic copying of files from one directory to another such that:

* the rate of copying can be throttled; and

* the number of files in the destination directory can be limited, so that it does not become overly large.

This utility also allows for a python class to be executed just before a file is placed in the destination directory in order to prepare for the appearance of the files to be copied.
