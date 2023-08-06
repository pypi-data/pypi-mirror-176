# this file defines all the configuration values passable to the pytest plugin, and any that can be provided
# to the cli via a configuration file. the contents will be scrapped and pytest args generated for each line

# the format of the following table is ['--flag', 'type', 'some help text'] OR
# ['--flag', 'type', 'some help text', {'extra': 'argparse args'}]


CONFIG_OPTIONS = [
    # core pytest flags
    [
        "--contract-path",
        str,
        "List of paths to look up contract files from",
        {"action": "append"},
    ],
    ["--proptests", bool, "run hypothesis property tests"],
    ["--benchmarks", bool, "run performance benchmark tests"],
    [
        "--baseline",
        bool,
        "run baseline parameterizations (for --benchmarks && --proptests",
    ],
    ["--tracing", bool, "enable tracing"],
    [
        "--timeout",
        int,
        "timeout",
    ],
    # network client configuration
    ["--connection-file", str, "network connection file with configuration details"],
    ["--network-config", str, "network connection file with configuration details"],
    [
        "--skip-consistency-check",
        bool,
        "skip the consistency check on the network fixture teardown",
    ],
    [
        "--skip-requires-network",
        bool,
        "skip the tests without multi node network",
        {"default": False},
    ],
    # Honeycomb
    ["--output-dir", str, "output location for any saved data"],
    [
        "--sdk-log-level",
        str,
        "what level to log at, error, warn, info, debug",
        {"default": "info"},
    ],
]
