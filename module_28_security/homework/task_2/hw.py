from flask import Flask, request, make_response

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
  {user_input}
</body>
</html>
"""

@app.route('/')
def index():
    user_input = "<h1>Hello, CSP!</h1><script>alert('This script won`t run!');</script>"

    rendered = HTML.format(user_input=user_input)
    response = make_response(rendered)

    csp_value = "default-src 'self'; script-src 'self';"
    response.headers['Content-Security-Policy'] = csp_value

    return response


if __name__ == '__main__':
    app.run(debug=True)
