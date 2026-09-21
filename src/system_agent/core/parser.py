import logging
from collections import Counter
from csv import reader
from io import StringIO
from json import JSONDecodeError, loads
from typing import NamedTuple

logger = logging.getLogger(__name__)


class ParsedResult(NamedTuple):
    type: str
    raw: str
    parsed: dict


class NotTabularError(RuntimeError):
    pass


def parse_text(input: str) -> ParsedResult:
    """
    Parse the input as plain text.
    """
    return ParsedResult(
        type="text", raw=input, parsed={"lines": input.strip().splitlines()}
    )


def parse_json(input: str) -> ParsedResult:
    """
    Parse the input as JSON.
    """
    try:
        parsed_json = loads(input.strip())
        return ParsedResult(type="json", raw=input, parsed={"json": parsed_json})
    except JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        raise JSONDecodeError(e.msg, e.doc, e.pos)


def parse_table(input: str) -> ParsedResult:
    """
    Parse the input as a table.
    """
    lines = input.strip().splitlines()
    col_count = [len(line.strip().split()) for line in lines]

    if len(col_count) < 3 or max(Counter(col_count).values()) / len(col_count) < 0.75:
        logger.error("Input is not a tabular format")
        raise NotTabularError("Input is not a tabular format")

    rows = list(reader(StringIO(input.strip()), delimiter=" ", skipinitialspace=True))
    return ParsedResult(type="table", raw=input, parsed={"rows": rows})


def parse(input: str) -> ParsedResult:
    """
    Attempt to parse the input using available parsers.
    """
    parsers = [parse_json, parse_table, parse_text]
    for parser in parsers:
        try:
            logger.debug(f"Trying with parser: {parser.__name__}")
            return parser(input)
        except (JSONDecodeError, NotTabularError) as e:
            logger.debug(f"Failed with parser: {parser.__name__}. Error: {e}")
    logger.error("Failed to parse input with all available parsers")
    raise RuntimeError("Failed to parse input with all available parsers")
