Laser
=====
ガルバノミラーでレーザー光を描画するためのデータ作成プログラム。

１）Inkscapeで描画したいデータを作成(svg形式)
２）svgをxy座標データに変換(mkflame.py)
３）on/offデータを追加(addz.py)
４）wavファイルに変換(mk6wav.py)

使用方法
　python mkframe.py svgファイル1 svgファイル2 ・・・ | python addz.py | python mk6wav.py 出力ＷＡＶファイル パラメータ
 
　svgファイルは、多数指定することにより、ファイル間が補間され、なめらかなパラパラ動画なる。
　ただし、svgデータは要素の並びおよび制御点の数が同一である必要がある。
　もし、制御点数が変わる場合は、ファイル間を/(スラッシュ)で区切ることができるが、ファイル間の補間はされない。

　パラメータは、３〜５くらいで調整する。

サンプル１(http://youtu.be/myfJ6V5ekQA)

 python mkframe.py fabnight.svg fabnight.svg fabnight.svg fabnight.svg| python addz.py | python mk6wav.py out.wav 4

　同じファイルを指定しているので、fabnight.svgが静止画で描画される。

サンプル２(http://youtu.be/9l8JLKCcH1s)
  
python mkflame.py F.svg F.svg A.svg A.svg B.svg B.svg N.svg N.svg I.svg I.svg G.svg G.svg H.svg H.svg T.svg T.svg F.svg A.svg B.svg N.svg I.svg G.svg H.svg T.svg 88.svg 88.svg| python addz.py | python mk6wav.py out.wav 5

　指定したsvgファイルは、要素の並びと制御点数が同一。各ファイルのデータ間は補間されるので、モーフィングのような効果が得られている。
　
