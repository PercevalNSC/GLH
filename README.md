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
    - Node.js(フロントサーバーの代替予定)

## 使い方
- MongoDBが起動している前提．
### GLHデータの格納
1. storeGLH/jsondata/ 下にそれぞれの年のディレクトリを作り，月ごとのGLHデータを入れる．

1. storeGLH/ 下でstoreGLH.pyを実行する

        python storeGLH.py

### 初期結果の格納
1. clustering.pyの実行

        python clustering.py

### サーバーの起動
1. serverGLH.pyの実行

        python serverGLH.py

### オフラインプロット
1. clustering_figure.pyの実行

        python clustering_figure.py

## ルーティング
### フロント用
- /

    集約化OPTICSのデモ

- /geocoder

    Mapboxのgeocoderサンプル

- /get-center

    地図の中心座標を取得するページ

- /reachability

    集約化到達性プロットのみ

- /map

    mapboxマップのみ

### バック用
あとで記述

- /api/json/point/\<GLH type>
- /api/geojson/point/\<GLH type>
- /api/geojson/line/route

## Issue
- フロントエンド
    - フロントサーバーをFlaskから切り離し，Node.jsにして，フロントエンドをJSで完結させる．
    - localStorageを使って，集約前データの保持をメモリから移す．
    - generatorによる集約化時のメモリ削減
    - GLHデータの表示ページを作る．
- バックエンド
    - データベースへのデータ格納時に，ストリーミング処理を行う
        - generatorを使うか，ストリーミング処理のライブラリを使う
    - データ格納と初期クラスタリングを連続で行う．
    - ルーティングの見直し
    - 起動スクリプトを見直し，単体のスクリプトに引数を渡すことで，複数機能実行できるようにする．


