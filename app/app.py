from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    template =  '''
        <h1>This page doesn't exist</h1>
        <h3>%s</h3>
    '''  %(request.url)
    return  render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True)

        

