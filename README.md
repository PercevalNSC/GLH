# Google Location History Visualization

## environment
- flask
- MongoDB, pymongo

## Use
- All script can run in carrent directory only.
### Store GLH data
    python storeGLH.py

- Warning: In default, the script includes all GLH data. If you want to include the file, change include path. 

### Plot
    python dataTrend.py

### start Server
    python flaskServer.py

### API requests
- root/api/json/\<Segmentation>

    Json形式でSegmentationで指定したデータを返す
- root/api/geojson/points/\<Segmentation>

    GeoJson形式のPointの集合としてSegmentationで指定したデータを返す    
- root/api/geojson/line

    GeoJson形式のPolylineとして、GLHデータを線にして返す
- Segmentation 
    - activitySegment.simplifiedRawPath
    - activitySegment.waypointPath
    - placeVisit.simplifiedRawPath
    - placeVisit.location


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