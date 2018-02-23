# acp brevet calculator using Flask, Ajax, and Mongo

## What?

A calculator for ACP brevet control times based on the calculator: https://rusa.org/octime_acp.html and rules: https://rusa.org/octime_alg.html , https://rusa.org/pages/rulesForRiders . This is a webserver that runs in docker-compose and uses flask, ajax, and mongodb (pymongo).

### Rules

Times follow the table linked in .../octime_alg.html above. Based on the min and max speeds, and the distance from the start to the control, the open and close times for each control are calculated. Only the part of the distance within a threshold follows that min/max speed (e.g. a control at 300km has the first 200km treated as 0-200 and the last 100km treated as 200-400). The time for the final control is based on the given brevet distance, and the final control can be no more that 20% longer than the given brevet distance.


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
