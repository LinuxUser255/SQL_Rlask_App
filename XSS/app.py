#!/usr/bin/env python3

# bad XSS

from flask import Flask

app = Flask(__name__)



@app.route('/insecure/no_template_engine_replace', methods =['GET'])
def no_template_engine_replace():  # put application's code here
    param = request.args.get('param', 'not set')

    html = open('templates/xss_shared.html').read()
    response = make_response(html.replace('{{ name }}', param)) # Noncompliant: param is not sanitized
    return response


if __name__ == '__main__':
    app.run()
