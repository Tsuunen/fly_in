from pydantic import ValidationError, BaseModel, Field
from pathlib import Path
import os
from typing import Iterator, Tuple, List, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class ParseContext:
    file: Optional[str] = None
    line_no: Optional[int] = None
    line: Optional[str] = None
    col: Optional[int] = None
    length: int = 1
    hint: Optional[str] = None


class ParsingError(Exception):
    def __init__(self, message: str, ctx: Optional[ParseContext] = None):
        super().__init__(self._format(message, ctx))
        self.message = message
        self.ctx = ctx

    @staticmethod
    def _format(message: str, ctx: Optional[ParseContext]) -> str:
        def c(text: str, code: str) -> str:
            return f"\x1b[{code}m{text}\x1b[0m"

        BOLD_RED = "31;1"
        GREY = "90"
        BOLD_YELLOW = "33;1"

        if ctx is None:
            return f"{c('ParsingError: ', BOLD_RED)}{message}"

        message = f"{c('ParsingError: ', BOLD_RED)}{message}"

        # Location
        if ctx.file is not None or ctx.line_no is not None:
            message += "\n"
            if ctx.file is not None:
                message += c("at " + ctx.file, GREY)
            if ctx.line_no is not None:
                message += c(f":line {ctx.line_no}", GREY)

        if ctx.line is not None:
            message += "\n"
            src = ctx.line.rstrip("\n")
            prefix = ""
            if ctx.line_no is not None:
                prefix = f"{ctx.line_no} | "
            message += prefix + src

            if ctx.col is not None:
                message += "\n" + " " * \
                    (len(prefix) + ctx.col) + "^" * ctx.length

        if ctx.hint:
            message += c(f"\nHint: {ctx.hint}", BOLD_YELLOW)

        return (message)


class Connection(BaseModel):
    to: str = Field(min_length=1)
    max_link_capacity: int = Field(ge=1, default=1)


class Hub(BaseModel):
    name: str = Field(min_length=1)
    coord: Tuple[int, int] = Field(max_length=2, min_length=2)
    zone_type: str = Field(default="normal")
    color: str = Field(default="white")
    max_drone: int = Field(ge=1, default=1)
    neighboors: List[Connection] = Field(default_factory=list)


class Map(BaseModel):
    start: Hub = Field()
    end: Hub = Field()
    nb_drones: int = Field(ge=1)
    hubs: List[Hub] = Field(default_factory=list)


class MapParser:
    def __init__(self, file_path: str) -> None:
        if Path(file_path).is_file() and os.access(file_path, os.R_OK):
            self.file_path = file_path
        else:
            raise FileNotFoundError(
                f"{file_path} does not exist or is not readable")
        self.no_line = 1

    def iter_lines(self) -> Iterator[str]:
        """"Yield file line one by one"""
        with open(self.file_path, "r") as file:
            for line in file:
                line = line.strip()
                if (len(line) and line[0] != "#"):
                    yield line.rstrip("\n")
                self.no_line += 1

    def format_validation_error(self, e: ValidationError) -> str:
        """Format ValidationError for them to be more clear

        e -- The ValidationError to format
        """
        lines = []
        for err in e.errors():
            field = ".".join(str(p) for p in err["loc"])
            msg = err["msg"]
            lines.append(f"- {field}: {msg}")
        return ("Invalid configuration:\n" + "\n".join(lines))

    @staticmethod
    def find_nth_occurence(c: str, s: str, n: int) -> int:
        index = -1
        for i in range(n):
            index = s.find(c, index + 1)
        return (index)

    def extract(self):
        nb_drones: int | None = None
        for line in self.iter_lines():
            try:
                field, value = line.split(":")
            except ValueError:
                raise ParsingError(
                    "Syntax Error", ParseContext(
                        file=self.file_path,
                        line_no=self.no_line,
                        line=line,
                        col=self.find_nth_occurence(":", line, 2),
                    ))
            if (not nb_drones):
                if (field != "nb_drones"):
                    raise ParsingError(
                        "The first line must be the number of drone")
                nb_drones = int(value)

        # return (Map())
