from search.tfidf_select import select_bp
from flask import Flask

app = Flask(__name__)
# @app.route('/')
# def hello_world():  # put application's code here
#     # return 'Hello World!'
#     return render_template("index.html")
#
#
# @app.route('/search', methods=['POST', "GET"])
# def search():
#
#     search_text = request.form.get("search")
#     search_list = tfidf.select_result(search_text)
#     return render_template("index.html", search_list=search_list)

app.config["JSON_AS_ASCII"] = False
app.register_blueprint(select_bp)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

