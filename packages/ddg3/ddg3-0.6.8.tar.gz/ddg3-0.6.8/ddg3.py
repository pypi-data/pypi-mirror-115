#!/usr/bin/env python3
"""
duck duck go module for python 3
"""
import urllib.parse
import requests
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from typing import Optional


__version__ = "0.6.8"
__useragent__ = "ddg3 {__version__}"


class Results:
    """ddg results object"""

    def __init__(self, xml: Element) -> None:
        """constructor"""
        self.type = {
            "A": "answer",
            "D": "disambiguation",
            "C": "category",
            "N": "name",
            "E": "exclusive",
            "": "nothing",
        }[xml.findtext("Type", "")]

        self.api_version = xml.attrib.get("version", None)
        self.heading = xml.findtext("Heading", "")
        self.answer: Optional[Answer] = None
        self.image: Optional[Image] = None

        try:
            self.results = [Result(elem) for elem in xml.getiterator("Result")]  # type: ignore
            self.related = [
                Result(elem) for elem in xml.getiterator("RelatedTopic")  # type: ignore
            ]
        except AttributeError:
            self.results = [Result(elem) for elem in xml.iter("Result")]
            self.related = [Result(elem) for elem in xml.iter("RelatedTopic")]

        self.abstract = Abstract(xml)

        answer_xml = xml.find("Answer")
        if answer_xml is not None:
            self.answer = Answer(answer_xml)
            if not self.answer.text:
                self.answer = None
        else:
            self.answer = None

        image_xml = xml.find("Image")
        if image_xml is not None and image_xml.text:
            self.image = Image(image_xml)
        else:
            self.image = None


class Abstract:
    """ddg abstract object"""

    def __init__(self, xml: Element) -> None:
        """constructor"""
        self.html = xml.findtext("Abstract", "")
        self.text = xml.findtext("AbstractText", "")
        self.url = xml.findtext("AbstractURL", "")
        self.source = xml.findtext("AbstractSource")


class Result:
    """ddg result object"""

    def __init__(self, xml: Element) -> None:
        """constructor"""
        self.html = xml.text
        self.text = xml.findtext("Text")
        self.url = xml.findtext("FirstURL")
        self.icon: Optional[Image] = None

        icon_xml = xml.find("Icon")
        if icon_xml is not None:
            self.icon = Image(icon_xml)
        else:
            self.icon = None


class Image:
    """ddg image object"""

    def __init__(self, xml: Element) -> None:
        """constructor"""
        self.url = xml.text
        self.height = xml.attrib.get("height", None)
        self.width = xml.attrib.get("width", None)


class Answer:
    """ddg answer object"""

    def __init__(self, xml: Element) -> None:
        """constructor"""
        self.text = xml.text
        self.type = xml.attrib.get("type", "")


def query(query_text: str, useragent: str = __useragent__) -> Results:
    """
    Query Duck Duck Go, returning a Results object.

    Here's a query that's unlikely to change:

    >>> result = query('1 + 1')
    >>> result.type
    'nothing'
    >>> result.answer.text
    '1 + 1 = 2'
    >>> result.answer.type
    'calc'
    """
    params = urllib.parse.urlencode({"q": query_text, "o": "x"})
    url = f"http://api.duckduckgo.com/?{params}"

    request = requests.get(url, headers={"User-Agent": useragent})
    response = request.text
    xml = ElementTree.fromstring(response)
    return Results(xml)


def main() -> None:
    """main function for when run as a cli tool"""
    import sys
    from optparse import OptionParser

    parser = OptionParser(
        usage="usage: %prog [options] query", version=f"ddg3 {__version__}"
    )
    parser.add_option(
        "-o",
        "--open",
        dest="open",
        action="store_true",
        help="open results in a browser",
    )
    parser.add_option(
        "-n", dest="n", type="int", default=3, help="number of results to show"
    )
    parser.add_option(
        "-d", dest="d", type="int", default=None, help="disambiguation choice"
    )
    (options, args) = parser.parse_args()
    q = " ".join(args)

    if options.open:
        import webbrowser

        query_url = urllib.parse.urlencode(dict(q=q))
        webbrowser.open(f"http://duckduckgo.com/?{query_url}", new=2)

        sys.exit(0)

    results = query(q)

    if options.d and results.type == "disambiguation":
        try:
            related = results.related[options.d - 1]
        except IndexError:
            print("Invalid disambiguation number.")
            sys.exit(1)
        results = query(related.url.split("/")[-1].replace("_", " "))

    if results.answer and results.answer.text:
        print(f"Answer: {results.answer.text}\n")
    elif results.abstract and results.abstract.text:
        print(f"{results.abstract.text}\n")

    if results.type == "disambiguation":
        print(
            f"""
            '{q}' can mean multiple things. You can re-run your query
            and add '-d #' where '#' is the topic number you're
            interested in.
            """.replace(
                "\n", ""
            ).replace(
                "\t", " "
            )
        )

        for i, related in enumerate(results.related[0 : options.n]):
            name = related.url.split("/")[-1].replace("_", " ")
            summary = related.text
            if len(summary) < len(related.text):
                summary += "..."
            print(f"{i+1}. {name}: {summary}\n")
    else:
        for i, result in enumerate(results.results[0 : options.n]):
            if result.text:
                summary = result.text[0:70].replace("&nbsp;", " ")
                if len(summary) < len(result.text):
                    summary += "..."
                print(f"{i + 1}. {summary}")
                print(f"  <{result.url}>\n")


if __name__ == "__main__":
    main()
