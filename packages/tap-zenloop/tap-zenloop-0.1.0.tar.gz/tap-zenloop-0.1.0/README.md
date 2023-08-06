# tap-zenloop

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from the [Zenloop API](https://docs.zenloop.com/reference/introduction)
- Currently it only extracts answers to surveys, but this should be easy to extend for your own needs.
  - [Answers](https://docs.zenloop.com/reference/get-answers)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## Usage

* Create a copy of the `sample_config.json`
* Fill in your API key and add the surveys you want to sync
* Run `tap-zenloop -c config.json --discover > catalog.json`
* Set `"selected": true` on the schema of the `answers` stream
* Run the first sync: `tap-zenloop -c config.json --catalog catalog.json`
* Process the STATE messages of the output stream to create a state file.
* In subsequent runs include the state to only load new answers: `tap-zenloop -c config.json --catalog catalog.json --state state.json`
