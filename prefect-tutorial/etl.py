import json
from datetime import datetime, timedelta

import aircraftlib as aclib
import prefect
from prefect import Flow, Parameter, task
from prefect.executors import DaskExecutor
from prefect.schedules import IntervalSchedule
from prefect.engine.results import LocalResult



def raw_ert():
    dulles_airport_position = aclib.Position(lat=38.9519444444, long=-77.4480555556)
    area_surrounding_dulles = aclib.bounding_box(dulles_airport_position, radius_km=200)

    # Extract: fetch data from multiple data sources
    ref_data = aclib.fetch_reference_data()
    raw_aircraft_data = aclib.fetch_live_aircraft_data(area=area_surrounding_dulles)

    # Transform: clean the fetched data and add derivative data to aid in the analysis
    live_aircraft_data = []
    for raw_vector in raw_aircraft_data:
        vector = aclib.clean_vector(raw_vector)
        if vector:
            aclib.add_airline_info(vector, ref_data.airlines)
            live_aircraft_data.append(vector)

    # Load: save the data for future analysis
    db = aclib.Database()
    db.add_live_aircraft_data(live_aircraft_data)
    db.update_reference_data(ref_data)





@task(max_retries=3, retry_delay=timedelta(seconds=10))
def extract_reference_data():
    logger = prefect.context.get("logger")
    logger.info("Extracting reference")

    reference_data = list( range(3) ) # aclib.fetch_reference_data()
    return reference_data


@task(max_retries=3, retry_delay=timedelta(seconds=10))
def extract_live_data(airport, radius, ref_data):
    logger = prefect.context.get("logger")
    logger.info("Fetching live data")
    return [1,2,3]

    area = None
    if airport:
        airport_data = ref_data.airports[airport]
        airport_position = aclib.Position(
            lat=float(airport_data["latitude"]), long=float(airport_data["longitude"])
        )
        area = aclib.bounding_box(airport_position, radius)

    raw_aircraft_data = aclib.fetch_live_aircraft_data(area=area)
    live_data = raw_aircraft_data
    return live_data


@task
def transform(live_data, reference_data):
    # clean the live data
    transformed_data = live_data
    return transformed_data


@task
def load_reference_data(reference_data):
    # save reference data to the database
    print(reference_data)


@task
def load_live_data(transformed_data):
    # save transformed live data to the database
    print(transformed_data)


# enables users to persist Results returned from each Task to a storage of choice: S3, Google Cloud Storage, Azure Storage, and more
# any results generated by individual Tasks are written out to the ./my-results directory, relative to where the Flow was executed from
results = LocalResult(dir="./my-results")

schedule = IntervalSchedule(
    start_date=datetime.utcnow() + timedelta(seconds=1),
    interval=timedelta(minutes=1),
)

#with Flow("Aircraft-ETL", schedule=schedule, result=results) as flow:
with Flow("Aircraft-ETL", result=results) as flow:
    airport = Parameter("airport", default="IAD")
    radius = Parameter("radius", default=200)

    reference_data = extract_reference_data()
    live_data = extract_live_data(airport, radius, reference_data)

    transformed_live_data = transform(live_data, reference_data)

    load_reference_data(reference_data)
    load_live_data(transformed_live_data)


flow.visualize(filename="etl-flow", format="svg")
with open("etl-flow.json", "wt") as f:
    json.dump(flow.serialize(), f, indent=2)

#flow.run(executor=DaskExecutor())
flow.run()
# the Executor interface (i.e. appropriate submit, map, and wait functions, similar to Python's concurrent.futures.Executor interface).