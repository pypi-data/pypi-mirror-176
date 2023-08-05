
# HTTP/Common Log Format log parser

Installs `log_parser` for parsing apache common log format and report unique ip address, top n uri requested, and top n most active ip addresses.

## Installation

Install using pip3.

#### Requirements

`python v3.2`

`pip3`

```bash
  pip install common-log-parser
```

## Usage/Examples

```bash
usage: log_parser [-h] [-t top] [-v] filename

Parse log file

positional arguments:
  filename

optional arguments:
  -h, --help         show this help message and exit
  -t top, --top top  get top n ips and urls
  -v                 verbose mode
```

## Assumptions

## Author

- [@adeelahmad](https://www.github.com/adeelahmad)

## License

[MIT](https://choosealicense.com/licenses/mit/)
