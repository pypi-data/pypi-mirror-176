def append_slash(url):
    if not url.endswith('/'):
        url += '/'
    return url