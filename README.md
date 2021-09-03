# Google Location History Visualization

## environment
- flask
- MongoDB, pymongo


## storeGLH
JSONとMongoDBのやり取りの管理
- storeGLH.py

    GLHのjsonファイルからデータを読み取りMongoDBへ格納する。
- GLHload.py

    GLHjsonデータをの処理を記述したpythonファイル
- dataTrend.py

    MongoDBを検索してデータをプロットする

## serverGLH
Flaskサーバーを起動し、MongoDBのデータを取り出し、Webページに表示
- flaskServer.py

    サーバー起動スクリプト。APIのルーティングを行い、MongoDBへのアクセスを行う。
- CreateList.py

    APIリクエストを受けて、データ処理をするクラス
- CreateGeoJSON.py

    GeoJSON形式のクラスの定義
- static
    - js
        - GLH.js

            mapbox APIを使って、MongoDBへデータをリクエストして、データ点を表示する
        - geocoder.js

            mapbox APIのgeocoderサンプル
- templates
    - GLH.html

        GLH表示用HTML。mapbox APIを宣言しているのと、表を表示する
    - geocoder.html

        geocoderサンプル用のHTML