import json
from datetime import datetime
from flask import Flask, render_template
from flask import request, redirect
from flask import Markup, escape



application = Flask(__name__)

DATA_FILE = "norilog.json"


def save_data(origin, destination, memo, created_at):
    """記録データの保存
    :parma origin: 乗った駅
    :tyoe origin: str
    :param destination:　降りた駅
    :type destination: str
    :param memo: 乗り降りのメモ
    :type memo: str
    :param created_at: 乗り降りの日時
    :type created_at: datetime.datetime
    :return: None
    """
    try:
        # データベースを開く
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))

    except FileNotFoundError:
        database = []

    # 指定したインデックスに値を挿入する,複数の辞書をリストとして格納する
    database.insert(0, {
        "origin": origin,
        "destination": destination,
        "memo": memo,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M")

    })
    # ensure_ascii=False：Unicodeがデフォルトとして設定されているため、日本語の文字化けを回避
    # dump: dictを文字列にエンコードし、ファイルを保存
    json.dump(database, open(DATA_FILE, mode="w", encoding="utf-8"), indent=4, ensure_ascii=False)


# URL(/)で受信した場合デコレーターで関数を呼び出す
@application.route("/")
def index():
    """トップページ
    テンプレートを使用してページを表示します
    """
    rides = load_data()
    return render_template("index.html", rides=rides)  # rides = template変数


def load_data():
    """記録データを返します"""
    try:
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))

    except FileNotFoundError:
        database = []

    return database


@application.route("/save", methods=["POST"])
def save():
    """記録用"""
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    memo = request.form.get("memo")
    created_at = datetime.now()
    save_data(origin, destination, memo, created_at)
    
    return redirect("/")


@application.template_filter("nl2br")
def nl2br_filter(s):
    """改行文字をbrタグに置き換えるテンプレートフィルター"""
    return escape(s).replace("\n", Markup("<br>"))

def main():
    application.run("127.0.0.1", 8000)



if __name__ == "__main__":
    # ipアドレス0.0.0.0の8000番ポートでアプリケーションを実行します
    application.run("127.0.0.1", 8000, debug=True)

