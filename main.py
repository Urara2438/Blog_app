from flask import Flask, render_template, redirect, request
# 最初にflaskというライブラリからFlaskクラスをimport
# FlaskクラスのインスタンスはWSGIアプリケーションになる
# WSGI：Pythonで標準化されているWebアプリとWebサーバ間のインタフェース

from flask_sqlalchemy import SQLAlchemy
# SQLAlchemyの利点:データベースの種類に関係なく同じコードで操作できる, SQLを書かなくてもPythonのコードでデータベースを操作できる
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_user, login_required,logout_user
from werkzeug.security import generate_password_hash, check_password_hash


from datetime import datetime
import pytz
import os
# Timezoneの設定に必要なモジュール

#アプリの作成------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
# Flaskをインスタンス化したもの
# 最初の引数はアプリケーションのモジュールまたはパッケージの名前
# __name__はモジュールまたはパッケージの名前用に殆どの場合で適切な便利なショートカット。これはテンプレート、静的ファイルなどのリソースを探す場所をFlaskが知るために必要。


#ログイン機能------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
app.config["SECRET_KEY"] = os.urandom(24)

#ログイン管理システム
login_manager = LoginManager()
login_manager.init_app(app)

#現在のユーザーを識別する関数
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



#データベースの接続設定(覚えなくてOK)------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
db = SQLAlchemy() # データベースの初期化
DB_INFO = {
    "user": "postgres",
    "password": "yoneken812",
    "host": "localhost",
    "name": "postgres"
}
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://{user}:{password}@{host}/{name}".format(**DB_INFO) # データベースへの接続情報
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI # アプリ内部の設定にデータベースの設定を保存
db.init_app(app) 
migrate = Migrate(app,db) #マイグレートのためのインスタンス


#データベースのテーブルの作成-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Article(db.Model): 
    #このような決まりとして受け入れる、クラス名からテーブル名が自動生成される。
    #ここで作成したテーブルの操作には、今後このクラスを用いて操作する
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(5000), nullable=False)
    tokyo_timezone = pytz.timezone("Asia/Tokyo")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(tokyo_timezone))
    # テーブルの作成には、ターミナルでpythonと入力してpythonのシェルを開いたあと、"from main import app, db" -> "with app.app_context():" -> " db.create_all()"を順番に実行し、Enterを2回押す。
    img_name = db.Column(db.String(100), nullable=True)
    #データベースに変更(カラムの追加や削除)を加えるには「マイグレーション」が必要
    #データベースの変更には、ターミナルでflask --app main db init -> flask --app main db migrate -m "コメント" -> flask --app main db upgrade
    
class Users(UserMixin, db.Model): #ログイン機能に関するテーブル作成では、UserMixinというクラスも追加で継承する
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    

#記事の閲覧(Read)------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/") # routeメソッドを呼び出してルーティング処理
# urlが叩かれると、GETメソッドがpython上でルーティングされた関数に送られる。
def index():
    articles =Article.query.all() #query = ~をくださいという命令、articlesはテーブルの各レコードが要素になったリスト
    return render_template("index.html", articles=articles) #()内は、html上での変数名 = python上での変数名


#記事の詳細の閲覧(ReadMore)------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/<int:article_id>/readmore") # routeメソッドを呼び出してルーティング処理
def readmore(article_id):
    article = Article.query.get(article_id)
    return render_template("readmore.html", article = article)
    

#ブログの新規作成(Create)------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/create", methods = ["POST", "GET"]) 
@login_required
def create():
    # リクエストのメソッドの判定　 = if文でGETとPOSTで分岐させる
    if request.method == "POST":
        # リクエストで来た情報の取得 = htmlで<form>タグで入力された情報)の取得-------------------------------------------------
        title = request.form.get("title") #htmlでname属性で指定した入力情報が得られる。
        body = request.form.get("body")
        file = request.files["img"] #htmlから画像情報の取得
        filename = file.filename #画像ファイル名の抽出
        # 情報の保存------------------------------------------------------------------------------------------------
        article = Article(title = title, body = body, img_name = filename) 
        #ここでは、データベース上でのカラム名 = 保存する情報が入った変数名
        #idはpirmary_keyで自動生成、created_atはデフォルトを指定しているので書かなくてもOK
        #articleというインスタンスがテーブルの各レコードに対応し、データとして保存される
        #データベースのimg_nameのカラムに画像名(ここではfilename)が保存される
        save_path = os.path.join(app.static_folder, "img", filename) #保存先のパスの作成
        file.save(save_path) #画像ファイルのパスを指定してファイルを保存
        # 追加と実行------------------------------------------------------------------------------------------------
        db.session.add(article) #データの追加
        db.session.commit() #実行
        return redirect("/admin") #redirectの中身はurlの文字列、ルーティングの中身と一緒
        
    elif request.method == "GET":
        return render_template("create.html") #render_templateの中身はhtmlのファイル名


#記事の編集および更新(Edit)------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/edit_option")
@login_required
def edit_option():
    articles = Article.query.all()
    return render_template("edit_option.html", articles=articles)


@app.route("/<int:article_id>/edit", methods = ["POST", "GET"]) 
@login_required
def edit(article_id):
    article = Article.query.get(article_id) #primary_keyを指定して、編集対象のレコードを取得する
    if request.method == "POST":
        article.title = request.form.get("title") #article.titleが、今回html上で入力された情報で上書きされる。
        article.body = request.form.get("body")
        db.session.commit() 
        return redirect("/admin")
        
    elif request.method == "GET":        
        return render_template("edit.html", article=article) #htmlで最初に編集前のデータを表示するために、articleを渡さないといけない。

  
#記事の削除(Delete)------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/delete_option")
@login_required
def delete_option():
    articles = Article.query.all()
    return render_template("delete_option.html", articles = articles)

@app.route("/<int:article_id>/delete")
@login_required
#methodはGETのみでOK
def delete(article_id):
    article = Article.query.get(article_id) 
    db.session.delete(article)
    db.session.commit()
    return redirect("/delete_option")


#-管理者画面-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/admin")
@login_required #ログインが必要な画面に書き足すことで、ログインしていないと見れないようにできる
def admin():
    return render_template("admin.html")

#サインアップ-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)
        user = Users(user_name = user_name, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    
    elif request.method == "GET":
        return render_template("signup.html")
    
#ログイン-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #ユーザー名とパスワードの受け取り
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        #ユーザー名をもとにデータベースから情報を取得
        user = Users.query.filter_by(user_name=user_name).first()
        #入力されたパスワードとデータベースのパスワードが一致しているか確認
        #一致していればログインし、管理者ページにリダイレクト
        if check_password_hash(user.password, password=password):
            login_user(user)
            return redirect("/admin")
        #一致していなければログイン画面に戻して、エラーメッセージを表示
        else: 
            return render_template("login.html", msg="ユーザー名またはパスワードが違います！🙀")
    elif request.method == "GET":
        return render_template("login.html", msg="")
    
#ログアウト-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
        
    
    
    
        
        
    




    