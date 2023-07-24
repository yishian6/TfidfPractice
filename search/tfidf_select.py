from flask import Blueprint, request, jsonify, render_template

from tfidf.tfidf_algorithm import TfidfExtract

select_bp = Blueprint("search", __name__)


@select_bp.route("/")
def index():
    return render_template("index.html")


@select_bp.route("/search", methods=["POST"])
def tfidf_select():
    search_text = request.form.get("search")
    search_result = TfidfExtract("data.json").select_result(search_text)
    return jsonify(code=200, msg="查询成功", data=search_result)
    # return render_template("index.html", search_list=search_result, msg="查询成功,结果如下")
