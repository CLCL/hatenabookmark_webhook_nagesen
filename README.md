#hatenabookmark_webhook_nagesen

hatenabookmark_webhook_nagesenは、はてなブックマークのWebHook機能で、ブックマークしたエントリの作者にはてなポイントを自動で送信する「投げ銭機能」を実現するPerl CGIスクリプトです。

投げ銭機能は、大昔のはてなブックマークに実装されていた機能でしたが、はてなブックマークリニューアルでオミットされてしまったものです。

その後、はてなブックマークにWebHook機能が実装され、ブックマーク操作ごとにHTTPアクセスを発生する仕組みが実装されましたので、このスクリプトを設置することで、投げ銭機能を追加することが出来ます。

ver 0.0.4よりGitHubにて公開。

* 最初作った時のエントリ http://blog.dtpwiki.jp/dtp/2009/06/web-hook-645b.html
* ver 0.0.3まで http://svn.coderepos.org/share/lang/perl/misc/hatenabookmark_webhook_nagesen/
* ver 0.0.4を作った時のエントリ http://cl.hatenablog.com/entry/hatenabookmark_webhook_nagesen_004

##files

設置者が自分で準備し書き換える必要があるファイルは以下の通りです。

* ~apache/.pit/default.yaml : はてなブックマークWebHook APIのキーと、パスワードを記録します。apacheのユーザが変更されている場合は、設置場所が変わります。

内容はこんな感じです。

"hatena.ne.jp": 
  "auth_key": 'はてなブッックマークWeb Hookのキー'
  "id": '自分のはてなのID'
  "password": '自分のはてなのpassword'

パスワードが書かれているので管理は厳重に。

CGIスクリプトは、Webからアクセスできるところに設置してください。詳しくは、はてなブックマークWebHookのページ http://hatena.g.hatena.ne.jp/hatenabookmark/20090603/1244012770 を参照のこと。

##changes

* 2013-02-26 ver 0.0.4 ポイント送信ページ変更に対応
* 2012-01-26 ver 0.0.3 はてなブログ対応
* 2009-10-03 ver 0.0.2 最新のMechでも動くように
* 2009-06-07 ver 0.0.1 ファーストポスト
