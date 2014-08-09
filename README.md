Laser
=====
ガルバノミラーでレーザー描画するためのデータ作成プログラム。

１）Inkscapeで描画したいデータを作成(svg形式)
２）svgをxy座標データに変換(mkflame.py)
３）on/offデータを追加(addz.py)
４）wavファイルに変換(mk6wav.py)
５）wavファイルを再生

使用方法
$ python mkframe.py svgファイル1 svgファイル2 ・・・ | python addz.py | python mk6wav.py 出力ＷＡＶファイル パラメータ
 
　svgファイルは、多数指定することにより、ファイル間が補間され、なめらかなパラパラ動画なる。
　ただし、svgデータは要素の並びおよび制御点の数が同一である必要がある。
　もし、制御点数が変わる場合は、ファイル間を/(スラッシュ)で区切ることができるが、ファイル間の補間はされない。

　線を赤に指定して発光を止めることができる。
　
　パラメータは、３〜５くらいで調整する。


サンプル１(http://youtu.be/myfJ6V5ekQA)

$ python mkframe.py fabnight.svg fabnight.svg fabnight.svg fabnight.svg| python addz.py | python mk6wav.py out.wav 4

　同じファイルを指定しているので、fabnight.svgが静止画で描画される。



サンプル２(http://youtu.be/9l8JLKCcH1s)
  
$ python mkflame.py F.svg F.svg A.svg A.svg B.svg B.svg N.svg N.svg I.svg I.svg G.svg G.svg H.svg H.svg T.svg T.svg F.svg A.svg B.svg N.svg I.svg G.svg H.svg T.svg 88.svg 88.svg| python addz.py | python mk6wav.py out.wav 5

　指定したsvgファイルは、要素の並びと制御点数が同一。各ファイルのデータ間は補間されるので、モーフィングのような効果が得られている。
　


サンプル３(http://youtu.be/eNeM1d6433c)
$ python mkframe.py 2-0.svg 2-2.svg / 20-1.svg 20-2.svg / 201-1.svg 201-2.svg / 2014-1.svg 2014-2.svg 2014-2.svg 2014-3.svg 2014-4.svg | python addz.py | python mk6wav.py z.wav 4

　数字の移動（要素の並びと制御点数が変化しない）をいくつか組み合わせ、最後に拡大縮小（これも要素の並びと制御点数が変化しない）した例。



サンプル４（http://youtu.be/lbtdb77kan0)
$ python mkframe.py tanabata1.svg tanabata2.svg / tanabata3.svg tanabata4.svg tanabata4.svg tanabata5.svg tanabata5.svg / tanabata2.svg tanabata2.svg | python addz.py | python mk6wav.py zz.wav 3

