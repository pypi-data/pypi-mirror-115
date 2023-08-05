# pylint: disable=no-value-for-parameter
"""
Main module for txt2ebook console app.
"""

import logging
import re
from pathlib import Path

import click
import markdown
from ebooklib import epub

from txt2ebook import __version__

logger = logging.getLogger(__name__)


@click.command(no_args_is_help=True)
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--title", "-t", default=None, show_default=True, help="Set the title of the ebook."
)
@click.option(
    "--language",
    "-l",
    default="en",
    show_default=True,
    help="Set the language of the ebook.",
)
@click.option(
    "--author",
    "-a",
    default=None,
    show_default=True,
    help="Set the author of the ebook.",
)
@click.option(
    "--remove_wrapping",
    "-rw",
    is_flag=True,
    show_default=True,
    help="Remove word wrapping.",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    flag_value=logging.DEBUG,
    show_default=True,
    help="Enable debugging log.",
)
@click.version_option(prog_name="txt2ebook", version=__version__)
@click.pass_context
def main(ctx, **kwargs):
    """
    Console tool to convert txt file to different ebook format.
    """

    logging.basicConfig(level=kwargs["debug"], format="[%(levelname)s] %(message)s")

    ctx.obj = kwargs

    try:
        filename = kwargs["filename"]
        title = kwargs["title"]

        logger.debug("Processing txt file: '%s'.", filename)

        with open(filename, "r") as file:
            content = file.read()

            if not content:
                raise RuntimeError(f"Empty file content in '{filename}'.")

            chapters = split_chapters(content)

            if title:
                output_filename = title + ".epub"
            else:
                match = re.search(r"《(.*)》", content)
                if match:
                    title = match.group(1)
                    output_filename = title + ".epub"
                else:
                    output_filename = Path(filename).stem + ".epub"

        build_epub(output_filename, chapters)

    except RuntimeError as error:
        click.echo(f"Error: {str(error)}!", err=True)


@click.pass_obj
def split_chapters(ctx, content):
    """
    Split the content of txt file into chapters by chapter header.
    """

    regex = r"^[ \t]*第.*[章卷].*$|^[ \t]*序章.*$|^[ \t]*内容简介.*$"
    pattern = re.compile(regex, re.MULTILINE)
    headers = re.findall(pattern, content)

    if not headers:
        filename = ctx["filename"]
        raise RuntimeError(f"No chapter headers found in '{filename}'.")

    bodies = re.split(pattern, content)
    chapters = list(zip(headers, bodies[1:]))

    return chapters


@click.pass_obj
def build_epub(ctx, output_filename, chapters):
    """
    Generate epub from the parsed chapters from txt file.
    """

    book = epub.EpubBook()

    if ctx["title"]:
        book.set_title(ctx["title"])

    if ctx["language"]:
        book.set_language(ctx["language"])

    if ctx["author"]:
        book.add_author(ctx["author"])

    toc = []
    for chapter_title, body in chapters:
        chapter_title = chapter_title.strip()
        chapter_title = re.sub(r"\s+", " ", chapter_title)
        body = body.strip()

        regex = r"第.*[章卷]|序章|内容简介"
        match = re.search(regex, chapter_title)
        if match:
            filename = match.group()
        else:
            filename = chapter_title

        logger.debug(chapter_title)

        html = markdown.markdown(to_markdown(chapter_title, body))

        html_chapter = epub.EpubHtml(title=chapter_title, file_name=filename + ".xhtml")
        html_chapter.content = html
        book.add_item(html_chapter)
        toc.append(html_chapter)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.toc = toc
    book.spine = ["nav"] + toc

    logger.debug("Generating epub file: '%s'.", output_filename)
    epub.write_epub(output_filename, book, {})


@click.pass_obj
def to_markdown(ctx, chapter_title, body):
    """
    Generate whole chapter in Markdown.
    """

    paragraphs = body.split("\n")
    double_newlines_body = "\n\n".join([p.strip() for p in paragraphs if p])

    if ctx["remove_wrapping"]:
        chapter_body = ""
        for line in double_newlines_body.split("\n\n"):
            if re.search(r"[…。？！]$", line) and "「" in line and "」" not in line:
                chapter_body = chapter_body + line.strip()
            elif re.search(r"[…。？！]{1}」?$", line) or re.match(
                r"^[ \t]*……[ \t]*$", line
            ):
                chapter_body = chapter_body + line.strip() + "\n\n"
            else:
                chapter_body = chapter_body + line.strip()
    else:
        chapter_body = double_newlines_body

    return "# " + chapter_title + "\n\n" + chapter_body


if __name__ == "__main__":
    main()
