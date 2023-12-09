import requests

def get_post(url, author_id, post_id, username, password):            
    
    print('requesting', url + "authors/" + author_id + "/posts/" + post_id)
    data = requests.get(url + "authors/" + author_id + "/posts/" + post_id, auth=(username, password))
    # print('response:', data)
    data = data.json()
    print('api data:', data)
    
    new_item = dict()                
    new_item['author_id'] = author_id
    new_item['username'] = data['author']['displayName']
    new_item['post_id'] = post_id
    new_item['date_posted'] = data['published']

    new_item['title'] = data['title']
    new_item['content_type'] = data['contentType']
    new_item['image_id'] = None # Deprecated at this point
    new_item['visibility'] = data["visibility"].lower()

    return new_item