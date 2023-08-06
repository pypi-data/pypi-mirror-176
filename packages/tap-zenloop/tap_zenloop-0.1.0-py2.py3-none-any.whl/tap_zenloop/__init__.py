#!/usr/bin/env python3
import os
import json
from pprint import pprint

import pendulum
import requests
import singer
from singer import utils, metadata, write_bookmark, get_bookmark
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema


REQUIRED_CONFIG_KEYS = ["start_date", "api_key", "surveys"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """ Load schemas from schemas folder """
    schemas = {}
    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path) as file:
            schemas[file_raw] = Schema.from_dict(json.load(file))
    return schemas


def discover():
    raw_schemas = load_schemas()
    streams = []
    for stream_id, schema in raw_schemas.items():
        stream_metadata = []
        key_properties = []
        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=None,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)


def _fetch_data(config, survey_id, date_from, date_to, page=1):
    url = f"https://api.zenloop.com/v1/surveys/{survey_id}/answers?date_shortcut=custom&order_by=inserted_at&order_type=asc&page={page}&date_from={date_from}&date_to={date_to}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=config.get('http_timeout_in_seconds', 15))

    return response.json()


def _process_answers(config, state, stream):
    survey_data = []
    date_to = pendulum.now().to_iso8601_string()

    for survey_id in config['surveys']:
        date_from = get_bookmark(state, stream.tap_stream_id, survey_id, default=config['start_date'])
        data = _fetch_data(config, survey_id, date_from, date_to)
        survey_data.append(data)
        total_pages = data['meta']['total_pages']
        if total_pages > 1:
            for page in range(2, total_pages + 1):
                survey_data.append(_fetch_data(config, survey_id, date_from, date_to, page=page))
        write_bookmark(state, stream.tap_stream_id, survey_id, date_to)

    for resultset in survey_data:
        rows = []
        for answer in resultset['answers']:
            rows.append({
                'title': resultset['survey']['title'],
                'public_hash_id': resultset['survey']['public_hash_id'],
                'id': answer['id'],
                'score_type': answer['score_type'],
                'score': answer['score'],
                'sentiment': answer['sentiment'],
                'recipient_id': answer['recipient_id'],
                'name': answer['name'],
                'inserted_at': answer['inserted_at'],
                'email': answer['email'],
                'identity': answer['identity'],
                'identity_type': answer['identity_type'],
                'comment': answer['comment'],
            })
        singer.write_records(stream.tap_stream_id, rows)
    singer.write_state(state)


def sync(config, state, catalog):
    """ Sync data from tap source """
    # Loop over selected streams in catalog
    for stream in catalog.get_selected_streams(state):
        LOGGER.info("Syncing stream: " + stream.tap_stream_id)

        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties,
        )

        if stream.tap_stream_id == 'answers':
            _process_answers(config, state, stream)
            pass
        else:
            LOGGER.error(f'Stream {stream.tap_stream_id} does not have a processor assigned, skipping')
            continue


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()
        sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
