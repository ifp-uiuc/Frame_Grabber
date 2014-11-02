import web

from post_to_json import post_to_json


urls = (
    '/', 'index'
)

class index:
    def GET(self):
        f = open('index.html', 'r')
        html = f.read()
        f.close()
        return html

    def POST(self):
        data = web.data()
        entries = data.split('&')
        values = [entry.split('=')[1] for entry in entries]
        post_to_json(values)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()