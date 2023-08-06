from fake_headers import Headers
import urllib
import requests
import json
import regex
import pandas as pd


def bookssearch(
    search,
    onestring=True,
    onlyfree=True,
    add_to_search_query="",
    language="de",
    timeout=15,
):
    r"""
    from a_pandas_ex_google_book_search_to_df import pd_add_google_books_search
    import pandas as pd
    pd_add_google_books_search()
    df=pd.Q_search_for_books(search='Programming',
                          onestring=True,
                          onlyfree=True,
                          add_to_search_query="",
                          language="en",
                          timeout=15, )


    """

    def get_fake_header():
        header = Headers(headers=False).generate()
        agent = header["User-Agent"]

        headers = {
            "User-Agent": f"{agent}",
        }
        return headers

    addi = add_to_search_query
    language = language.lower()
    addtourl = urllib.parse.quote(search)
    if onestring:
        addtourl = f'"{addtourl}"'
    addtourl = addtourl + addi
    fakeheader = get_fake_header()
    site = f"https://www.googleapis.com/books/v1/volumes?q={addtourl}&maxResults=40&orderBy=newest&printType=books&langRestrict={language}"
    if onlyfree:
        site = site + "&filter=full"
    response = requests.get(site, headers=fakeheader, timeout=timeout)
    result = json.loads(response.content)
    allbooks = []

    for res in result["items"]:
        (
            titel,
            subtitle,
            authors,
            date,
            text,
            idi,
            selfLink,
            publishedDate,
            previewLink,
        ) = (pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA)
        idi = res["id"]
        selfLink = res["selfLink"]
        titel = res["volumeInfo"]["title"]
        try:
            authors = "|".join(res["volumeInfo"]["authors"])
        except KeyError:
            authors = pd.NA
        try:
            date = res["volumeInfo"]["publishedDate"]
        except KeyError:
            date = pd.NA
        try:
            subtitle = res["volumeInfo"]["subtitle"]
        except KeyError:
            subtitle = pd.NA
        try:
            publishedDate = res["volumeInfo"]["publishedDate"]
        except Exception:
            publishedDate = pd.NA
        try:
            previewLink = res["volumeInfo"]["previewLink"]

        except Exception:

            previewLink = pd.NA
        try:
            text = res["searchInfo"]["textSnippet"]
        except KeyError:
            text = pd.NA
        try:
            text = regex.sub(r"\s+", " ", text.strip())
        except Exception:
            pass
        try:
            allbooks.append(
                (
                    titel,
                    subtitle,
                    authors,
                    date,
                    text,
                    idi,
                    selfLink,
                    publishedDate,
                    previewLink,
                )
            )
        except Exception:
            pass
    allbooks.reverse()
    df = pd.DataFrame.from_records(allbooks)
    df.columns = [
        "titel",
        "subtitle",
        "authors",
        "date",
        "text",
        "idi",
        "selfLink",
        "publishedDate",
        "previewLink",
    ]
    return df


def pd_add_google_books_search():
    pd.Q_search_for_books = bookssearch
