#!/usr/bin/python



from Octavia import app, webMethod

@app.route('/?discovery')
@webMethod
def discovery():
    return 'service schema goes here'
