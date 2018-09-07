from japronto import Application

def hello(request):
    return request.Response(text='hello world')

app = Application()
app.router.add_route('/', hello)
app.run(debug=True)
