import os
import re
from flask import Flask, request, Response


# create an app
app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    # get GET parm called name. Set to 'Anonymous` by default
    name = request.args.get('name', 'Anonymous')
    ip = request.remote_addr
    resp_html = f"""
        <center>
            <h1>Hello {name}</h1>
            <p> your IP address is {ip}</p>
        </center>
        """
    # create a response object setting http code and content-type
    resp = Response(resp_html, 200, headers={'Content-type': 'text/html'})
    return resp


if __name__ == '__main__':
    # get $PORT environment variable, set to 8080 by default
    port = int(os.environ.get('PORT', 8080))
    # run the app
    app.run(host='0.0.0.0', port=port)
