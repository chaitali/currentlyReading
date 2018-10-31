import oauth2 as oauth
import urllib.parse as urlparse
import webbrowser

url = 'http://www.goodreads.com'
request_token_url = '%s/oauth/request_token' % url
authorize_url = '%s/oauth/authorize' % url
access_token_url = '%s/oauth/access_token/' % url

consumer = oauth.Consumer(key='b7K6UfvGOCmKg3ZeBO5jHg',
                          secret='pHDuNht299YPtmuL79sBLxDMrXIWL4TuOPpu9Dw7RA')

client = oauth.Client(consumer)

response, content = client.request(request_token_url, 'GET')
if response['status'] != '200':
    raise Exception('Invalid response: %s' % response['status'])
print(content)
request_token = dict(urlparse.parse_qsl(content))
print(request_token)

oauth_token = request_token[b'oauth_token'].decode("utf-8")
oauth_secret = request_token[b'oauth_token_secret'].decode("utf-8")

authorize_link = '%s?oauth_token=%s' % (authorize_url, oauth_token)

webbrowser.open(authorize_link)

token = oauth.Token(oauth_token, oauth_secret)

client = oauth.Client(consumer, token)

response, content = client.request(access_token_url, 'POST')
print(response, content)
if response['status'] != '200':
    raise Exception('Invalid response: %s' % response['status'])

access_token = dict(urlparse.parse_qsl(content))

# this is the token you should save for future uses
token = oauth.Token(access_token['oauth_token'],
                    access_token['oauth_token_secret'])

#
# As an example, let's add a book to one of the user's shelves
# #

# import urllib

# client = oauth.Client(consumer, token)
# # the book is: "Generation A" by Douglas Coupland
# body = urllib.urlencode({'name': 'to-read', 'book_id': 6801825})
# headers = {'content-type': 'application/x-www-form-urlencoded'}
# response, content = client.request('%s/shelf/add_to_shelf.xml' % url,
#                                 'POST', body, headers)
# # check that the new resource has been created
# if response['status'] != '201':
#     raise Exception('Cannot create resource: %s' % response['status'])
# else:
#     print 'Book added!'