import pandas as pd

INPUT_FILE = 'bfro_reports_geocoded.csv'
OUTPUT_FILE = 'redis_bigfoot_commands.txt'

IDS_KEY = 'bigfoot:sightings:ids'
LOCATIONS_KEY = 'bigfoot:sightings:locations'
REPORTS_KEY = 'bigfoot:sightings:report'

def main():
  # read in the CSV data
  data = pd.read_csv(INPUT_FILE, encoding='utf-8')
  print(f"Read {data.shape[0]} rows and {data.shape[1]} columns from '{INPUT_FILE}'.")

  # drop unwanted columns
  data = data.filter(items=['observed', 'county', 'state', 'title', 'latitude', 'longitude', 'date', 'number', 'classification'])
  print(f"Dropped all columns except {data.columns.to_list()}.")

  # drop rows that are missing a values
  data = remove_rows_with_null(data, 'number')
  data = remove_rows_with_null(data, 'longitude')
  data = remove_rows_with_null(data, 'latitude')

  # prepare to write the output file
  output_file = open(OUTPUT_FILE, 'w')

  # walk the data
  for index, row in data.iterrows():

    # get the fields
    id = int(row['number'])
    title = str(row['title'])
    date = row['date']
    observed = str(row['observed'])
    county = row['county']
    state = row['state']
    longitude = row['longitude']
    latitude = row['latitude']
    classification = row['classification']

    # print a status
    print(title)

    ## write to the file
    escaped_title = title.replace('\\', '\\\\').replace('"', '\\"')
    escaped_observed = observed.replace('\\', '\\\\').replace('"', '\\"')

    output_file.write(f"SADD {IDS_KEY} report:{id}\n")
    output_file.write(f"HSET {REPORTS_KEY}:{id} id {id} title \"{escaped_title}\" date \"{date}\" observed \"{escaped_observed}\" county \"{county}\" state \"{state}\" classification \"{classification}\"\n")
    output_file.write(f"GEOADD {LOCATIONS_KEY} {longitude} {latitude} report:{id}\n")

  # all done!
  output_file.close()
  print("Done!")
  print()

def remove_rows_with_null(data, column):
  filter = data[column].isnull()
  rows_to_drop = data[filter].index
  data = data.drop(rows_to_drop)
  print(f"Dropped {rows_to_drop.size} rows where '{column}' is empty.")
  return data

main()