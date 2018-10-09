from chalice import Chalice, Response
import datetime
import hashlib
import os
import time

app = Chalice(app_name='test-xss')
app.debug = True


@app.route('/test', methods=['GET'])
def test():
    print('test')
    return {
        'test': '<script>alart("aaa")</script>'
    }


@app.route('/login', methods=['GET'])
def login():
    print('login')
    thisyear = datetime.datetime.now().year
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(os.urandom(800))
    session_id = ripemd160.hexdigest()
    expires = time.strftime("%a, %d-%b-{0:d} %H:%M:%S GMT", time.gmtime()).format(thisyear + 2)
    print(expires)
    headers = {
            'Content-Type': 'text/plain',
            'Content-Length': '0',
            'Set-Cookie': f'session={session_id}; domain=.execute-api.ap-northeast-1.amazonaws.com; path=/; expires={expires}'
    }
    print(headers)
    return Response(
        body='',
        status_code=200,
        headers=headers
    )


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
