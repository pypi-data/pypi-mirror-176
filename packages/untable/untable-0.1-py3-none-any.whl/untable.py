from bs4 import BeautifulSoup
from difflib import SequenceMatcher


def single(
    html: str = None,
    soup: BeautifulSoup = None,
    skip=0,
    threshold: float = 0.8,
    deep_signature=False,
) -> dict:
    """Scrape data from a single entity HTML table.

    A single entity table is one that contains data from only one entity, for example:

    |               |              |
    | ------------- | ------------ |
    | *Name:*       | Ada Lovelace |
    | *DOB:*        | 12-10-1815   |
    | *Profession:* | Programmer   |

    The first final `<td>` of the table (i.e. a `<td>` without any nested `<td>`s) is
    considered to contain a label. The next final `<td>`s will be compared to the
    previous one. If it is similar (according to a signature composed by its tag name
    and attributes), it is considered to contain a new label. If not, it is considered
    to contain the value corresponding to the previous found label. Multiple values for
    the same label are grouped into a list. Empty `<td>`s are ignored. `<th>`s are
    treated the same way as `<td>`s.

    Args:
        html (str): HTML code containing a table. If there is more than one table, the
            first one is taken. This parameter is mandatory if `soup` is `None` and
            ignored if `soup` is not `None`.
        soup (BeautifulSoup, optional): An HTML soupcontaining a table.
        skip (int, optional): Number of final `<td>`s to be skipped before starting the
            scanning of elements. Default is 0.
        threshold (float, optional): A number from 0 to 1 indicating the minimum
            similarity a `<td>` has to have when compared to the first `<td>` to be
            considered to contain a label. Use higher values the more the `<td>`s
            containing values are similar to the ones containing labels. Default is 0.8.
        deep_signature (bool, optional): If `True`, a `<td>` signature will also be
            composed of the tag names and attributes of its descendents. Useful when it
            is not possible to differentiate a `<td>` containing a label from one
            containing a value by looking at the original signature only, but it is
            possible by looking the elements' children. Default is `False`.

    Returns:
        A `dict` containing table data.
    """
    if not soup:
        soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table") if soup.name != "table" else soup
    item = {}
    label_signature = None
    curr_label = None

    for td in find_all_final(table, ["th", "td"])[skip:]:
        cleared_text = clear_text(td.text)

        if not cleared_text:  # Empty cell, skipping
            continue

        if not label_signature:
            label_signature = _get_signature(td, deep=deep_signature)

        curr_signature = _get_signature(td, deep=deep_signature)
        similarity = compare_texts(label_signature, curr_signature)

        if similarity > threshold:  # Text looks like a new label
            curr_label = cleared_text
        else:  # Text doesn't look like a new label, assuming it's a value
            if not curr_label:
                continue  # No label for this value, skipping

            curr_value = cleared_text

            if (
                curr_label in item
            ):  # Make a list for multiple values under the same label
                try:
                    item[curr_label].append(curr_value)
                except AttributeError:
                    item[curr_label] = [item[curr_label]] + [curr_value]
            else:
                item[curr_label] = curr_value

    return item


def multi(
    html: str = None,
    soup: BeautifulSoup = None,
    skip=0,
) -> list:
    """Scrape data from a multi-entity HTML table.

    A multi-entity table is one that contains data from more than one entity, for
    example:

    |  *Name*               | *Profession*  |
    | --------------------- | ------------- |
    | Leonhard Euler        | Mathematician |
    | Alberto Santos-Dumont | Aviator       |
    | Stephen King          | Writer        |

    The table's first row (represented by a `<tr>` element) is considered to contain the
    labels. Other rows are considered to contain values.

    Args:
        html (str): HTML code containing a table. If there is more than one table, the
            first one is taken. This parameter is mandatory if `soup` is `None` and
            ignored if `soup` is not `None`.
        soup (BeautifulSoup, optional): An HTML soupcontaining a table.
        skip (int, optional): Number of rows to be skipped before starting the scanning
            of elements. Default is 0.
    Returns:
        A `list` of `dict`s, each one containing table data.
    """
    if not soup:
        soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table") if soup.name != "table" else soup
    items = []
    labels = []

    # Extracting labels
    trs = find_all_final(table, "tr")
    tr_labels = trs[skip]

    if tr_labels.find("th"):
        labels = [clear_text(th.text) for th in tr_labels.find_all("th")]
    else:
        labels = [clear_text(td.text) for td in tr_labels.find_all("td")]

    # Extracting values
    for tr in trs[skip + 1 :]:
        valores = [clear_text(td.text) for td in tr.find_all("td")]
        assert len(valores) == len(labels)
        item = {nome: valor for nome, valor in zip(labels, valores)}
        item.pop("", None)
        items.append(item)

    return items


def find_all_final(soup: BeautifulSoup, tag) -> list:
    """List all final elements of a given tag or list of tags in a soup.

    A final element is one that does not have another element of the same tag as a
    descendent. If a list of tags is passed, a final element cannot have any element of
    the list as descendent.

    Args:
        soup (BeautifulSoup): An HTML soup.
        tag (str or list): Element tag name or a list of tag names.

    Returns:
        A list of all final elements of the given tag. It can be an empty list.
    """
    return [e for e in soup.find_all(tag) if not e.find(tag)]


def clear_text(text: str) -> str:
    """Remove non-printable characters from a text (spaces are kept).

    Args:
        text (str): text to be cleaned

    Returns:
        Cleaned text.
    """
    return " ".join(text.split())


def compare_texts(text1: str, text2: str) -> float:
    """Compare and assign a similarity value between two given texts.

    Args:
        text1 (str): First text to be compared.
        text2 (str): Second text to be compared.

    Returns:
        Comparison result as a float from 0 to 1. The closest to 1 is the result, the
        more similar the texts are.
    """
    return SequenceMatcher(None, text1, text2).ratio()


def _get_signature(tag, deep=False):
    tag_str = (
        tag.name
        + " "
        + " ".join(
            attr + " " + str(val)
            for attr, val in tag.attrs.items()
            if attr not in ["id", "name"]
        )
    )

    if deep:
        children_str = " ".join(
            t.name
            + " "
            + " ".join(
                attr + " " + str(val)
                for attr, val in t.attrs.items()
                if attr not in ["id", "name"]
            )
            for t in tag()
        )

        tag_str += " " + children_str

    return tag_str
