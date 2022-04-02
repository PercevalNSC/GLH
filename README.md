# GLHデータの可視化と集約化OTICSによるクラスタリングアプリケーション

## 環境
- Python
    - Flask（フロント，バックエンド兼任）
    - pymongo
    - sci-kit.learn.OPTICS
    - matplotlib
- Javascript
    - D3.js
    - mapbox GL JS
    - Dat GUI
    - Node.js
    - express.js

## 使い方
- 事前にMongoDBを起動しておく．
### GLHデータの格納
1. jsondata/ 下にそれぞれの年のディレクトリを作り，月ごとのGLHデータを入れる．

    - jsondata/
        - 2017/
        - 2018/
        - ...


1. コマンドの実行

    storeコマンドはデータの格納のみ．loadは初期クラスタリングまで行う．

        python manage.py store
        or
        python manage.py load
    




### 初期クラスタリング
1. コマンドの実行

    init_clusteringコマンドはデータの格納のみ．loadは初期クラスタリングまで行う．

        python manage.py init_clsutering
        or
        python manage.py load

### サーバーの起動
1. コマンドの実行

        python manage.py server

### オフラインプロット
1. コマンドの実行

        python manage.py plot

## ルーティング
### フロント用
- /

    ルーティングページ

- /visualizer

    GLHデータの可視化ページ

- /aggreagation

    集約化OPTICSのページ

- /map

    Mapboxのgeocoderサンプル


### バック用
あとで記述

- /api/json/point/\<GLH type>
- /api/geojson/point/\<GLH type>
- /api/geojson/line/route

## Issue
- フロントエンド
    - localStorageを使って，集約前データの保持をメモリから移す．
    - generatorによる集約化時のメモリ削減
- バックエンド
    - データベースへのデータ格納時に，ストリーミング処理を行う
        - generatorを使うか，ストリーミング処理のライブラリを使う
    - ルーティングの見直し


