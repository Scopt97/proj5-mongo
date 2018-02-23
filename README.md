# acp brevet calculator using Flask, Ajax, and Mongo

## What?

A calculator for ACP brevet control times based on the calculator: https://rusa.org/octime_acp.html and rules: https://rusa.org/octime_alg.html , https://rusa.org/pages/rulesForRiders . This is a webserver that runs in docker-compose and uses flask, ajax, and mongodb (pymongo).


## Use

Clone the repo, cd to DockerMongo, and run `sudo docker-compose up`

The "Submit" button sends the control data to the mongo database. The "Display" button displays all controls in the database.

requires: docker, docker-compose, python3 (and pip). Other requirements are installed into the container upon running.


## Changes from proj4

### Additions:

"Submit" and "Display" buttons, with error messages for no times, negative control distance, and too long control distance.

### Fixes:

proj4 displayed the wrong times due to timezone adjustments made by moment.js. The correct dates/times are now displayed (both in the table and the display button page).




### Author: Kyle Nielsen   Contact: kylen@uoregon.edu
