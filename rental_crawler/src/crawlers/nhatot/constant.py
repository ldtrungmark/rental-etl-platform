class NhaTotEndpoint:
    WEB_URL = 'https://www.nhatot.com/'
    API_POSTS = "https://gateway.chotot.com/v1/public/ad-listing"


class SearchFilter:
    NEWEST = 0
    LOWEST_PRICE = 1
    HIGHEST_PRICE = 6


class SelectorPathBS4:
    SEARCH_PAGE_POSTS = dict(name="script", attrs={"id": "__NEXT_DATA__"})


class DictPath:
    SEARCH_PAGE_POST = 'props.initialState.adlisting.data.ads'
