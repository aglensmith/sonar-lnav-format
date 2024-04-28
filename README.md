# sonar-lnav-format

[lnav](https://lnav.org/) log formats for SonarQube, SonarCloud, and SonarScanner logs.

> **From docs.lnav.org:** The Log File Navigator (lnav) is an advanced log file viewer for the console. If you have a bunch of log files that you need to look through to find issues, lnav is the tool for you

## Requirements
* [lnav](https://lnav.org/downloads) installed.

## Installation

```shell
lnav -i git@github.com:aglensmith/sonar-lnav-format.git
```

> See [installing formats](https://docs.lnav.org/en/v0.12.0/formats.html#installing-formats) in lnav docs for more information.

## Usage

Open ce.log in lnav.

```shell
lnav ce.log
```

Get ce tasks ordered by time.

```shell
lnav ce.log -c "; select action, status, time from sqce order by time desc"
```

## Log support
* `es.log` - not yet supported
* `ce.log` - supported
* `web.log` - supported
* `access.log` - supported by lnav by default

## Directory structure


```shell
├── sq_ce_log.json # lnav fromat for SonarQube ce.log 
└──lines.py        # script to create sample line json from log   
```

## Contributing

### Adding and updating RegEx
1. Use [regex101.com](https://regex101.com/) to create RegEx.
1. JSON encode RegEx (replace all `\` with `\\`).
1. Add RegEx object to format file in `./formats/`.

**Example:**

```json
"Delete issue changes": {
    "pattern": "^((?<timestamp>\\d{4}.\\d{2}.\\d{2} \\d{2}:\\d{2}:\\d{2}) (?<level>ERROR|WARN|INFO|DEBUG)( |  )ce\\[(?<pid>[\\w\\-\\.\\$\\+\\]]*)\\]\\[(?<module>[\\w\\-\\.]*)\\])(?<action>[\\w\\ \\=\\.\\-\\:\\']*)((\\|)( changes=(?<changes>[\\d]+)) )(\\|)( status=(?<status>[\\w]*) )(\\|)( time=(?<time>[\\d]*)ms)"
},
```

### Generating sample lines

Use `lines.py` to quickly generate lots of sample lines from a log file.

```shell
# make lines.py executable (*nix)
chmod +x ./lines.py

# create samples for ce.log and output to file
./lines.py ./logs/ce.log > lines.txt

# Example output -->
{"line": "2024.04.25 10:38:07 INFO  ce[][o.s.p.ProcessEntryPoint] Starting Compute Engine"},
{"line": "2024.04.25 10:38:07 INFO  ce[][o.s.ce.app.CeServer] Compute Engine starting up..."},

```

Copy and paste the output to the `sample` array in the format `.json` file.

```json
"sample": [
    {"line": "2024.04.25 10:38:07 INFO  ce[][o.s.p.ProcessEntryPoint] Starting Compute Engine"},
    {"line": "2024.04.25 10:38:07 INFO  ce[][o.s.ce.app.CeServer] Compute Engine starting up..."},
    {"line": "2024.04.25 10:38:07 INFO  ce[][o.sonar.db.Database] Create JDBC data source for jdbc:postgresql://localhost:5432/ee99"}, // <-- Remove trailing comma
]
```

The next time you run `lnav`, the log format regex patterns will be tested against the samples. If one of the samples do not match, lnav will throw and error and log the the sample line that did not match. This is useful for testing that all lines files are parsed. 


## To-do
* Define ce log values in `value` object
* Test more ce logs
* Create [lnav commands](https://docs.lnav.org/en/v0.12.0/commands.html) for useful queries
    * ce tasks by time 