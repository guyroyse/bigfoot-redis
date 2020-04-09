# Messing with Sasquatch

Herein are all the details you'll ned to load a bunch of bifoot sightings into a GeoSet with Redis.

## Get Python with Sasquatch

You need a Python environment to make this all work. I used Python 3.8—the latest, greatest, and most updatest at the time of this writing. I also used `venv` to manage my environment.

I'll assume you can download and install Python 3.8 on your own. So lets go ahead and setup the environment:

    $ python3.8 -m venv venv

Once `venv` is installed, you need to activate it:

    $ . venv/bin/activate

Now when you run `python` from the command line, it will always point to Python3.8 and any libraries you install will only be for this specific environment.

If you want to deactivate this environment, you can do so from anywhere with the following command:

    $ deactivate

## Get Some Dependencies

Next, let's install all the dependencies. These are all listed in `requirements.txt` and can be installed with `pip` like this.

    $ pip install -r requirements.txt

Run that command, and you'll have all the dependencies nstalled and will be ready to run the code.

## Data to Redis Commands with Sasquatch

So, the data file we have isn't ready to load into Redis. We need to convert it to Redis commands so we can load it via redis-cli. So, let's generate a file with those commands in it.

This is as easy as running the following.

    $ python prepare.py

This will generate a series of command to load Hashes with each sighting under a key of `bigfoot:sightings:report:<report_id>` and load our GeoSet with the location those sightings under the key `bigfoot:sightings:locations`. Each member of the GeoSet is named `report:<report_id>`. And, all the report IDs will be shoved into a Set at `bigfoot:sightings:ids`.

When it runs, you should see something like this.

    Read 4586 rows and 27 columns from 'bfro_reports_geocoded.csv'.
    Dropped all columns except ['observed', 'county', 'state', 'title', 'latitude', 'longitude', 'date', 'number', 'classification'].
    Dropped 0 rows where 'number' is empty.
    Dropped 927 rows where 'longitude' is empty.
    Dropped 0 rows where 'latitude' is empty.
    Number: 9765 Long: -99.1702 Lat: 35.3011
    Number: 4983 Long: -81.67339 Lat: 39.38745
    .
    .
    .
    Number: 2094 Long: -84.6971 Lat: 34.1088
    Number: 19421 Long: -84.73846 Lat: 34.1318
    Done!

When it's done, you'll have a file named `redis_bigfoot_commands.txt` that's ready to load into Redis. So let's do that:

    $ cat redis_bigfoot_commands.txt | redis-cli

And that's it.
