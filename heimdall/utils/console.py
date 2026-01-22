"""Utilities for console output operations."""

import typing

import click


def verbose_echo(
    verbose: bool,
    message: typing.Any | None = None,
    file: typing.IO[typing.Any] | None = None,
    nl: bool = True,
    err: bool = False,
    color: bool | None = None,
    fg: int | tuple[int, int, int] | str | None = (90, 156, 181),
    bg: int | tuple[int, int, int] | str | None = None,
    bold: bool | None = True,
    dim: bool | None = None,
    underline: bool | None = None,
    overline: bool | None = None,
    italic: bool | None = None,
    blink: bool | None = None,
    reverse: bool | None = None,
    strikethrough: bool | None = None,
    reset: bool = True,
) -> None:
    """
    Print message only when verbose mode is enabled.

    :param verbose: If True, print the message; otherwise do nothing
    :type verbose: bool
    :param message: Text to display when verbose is True
    :type message: typing.Any | None
    :param file: File object to write to (default: stdout)
    :type file: typing.IO[typing.Any] | None
    :param nl: Whether to add newline after message
    :type nl: bool
    :param err: Whether to write to stderr instead of stdout
    :type err: bool
    :param color: Whether to force color output
    :type color: bool | None
    :param fg: Foreground color (default: cyan-like color)
    :type fg: int | tuple[int, int, int] | str | None
    :param bg: Background color
    :type bg: int | tuple[int, int, int] | str | None
    :param bold: Use bold text
    :type bold: bool | None
    :param dim: Use dim text
    :type dim: bool | None
    :param underline: Underline text
    :type underline: bool | None
    :param overline: Overline text
    :type overline: bool | None
    :param italic: Use italic text
    :type italic: bool | None
    :param blink: Blinking text
    :type blink: bool | None
    :param reverse: Reverse foreground and background
    :type reverse: bool | None
    :param strikethrough: Strikethrough text
    :type strikethrough: bool | None
    :param reset: Reset style after message
    :type reset: bool
    """
    if verbose:
        click.echo(
            click.style(
                f"[VERBOSE] {message}",
                fg,
                bg,
                bold,
                dim,
                underline,
                overline,
                italic,
                blink,
                reverse,
                strikethrough,
                reset,
            ),
            file,
            nl,
            err,
            color,
        )


def error_style(text: str) -> str:
    """
    Apply error styling to text.

    :param text: Text to style as an error
    :type text: str
    :return: Text styled with red color and bold formatting
    :rtype: str
    """
    return click.style(text, fg="red", bold=True)
