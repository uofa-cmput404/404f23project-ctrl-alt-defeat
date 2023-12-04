def parse_author_id(url):
    parsed_url = url.split("/")

    author_index = parsed_url.index('authors')
    
    author_id = parse_author_id[author_index + 1]
    
    return author_id
    