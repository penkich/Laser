Laser
=====
<h3>ガルバノミラーでレーザー描画するためのデータ作成プログラム。</h3>
All data including python script of this repository is under a creative commons License (CC BY 3.0)<br>
By penkich, a member of fablab kitakagaya<br>

１）Inkscapeで描画したいデータを作成(svg形式)<br>
２）svgをxy座標データに変換(mkframe.py)<br>
３）on/offデータを追加(addz.py)<br>
４）wavファイルに変換(mk6wav.py)<br>
５）aplayコマンドなどでwavファイルを再生<br>

<h3>使用方法</h3>

$ python mkframe.py svgファイル1 svgファイル2 ・・・ | python addz.py | python mk6wav.py 出力ＷＡＶファイル パラメータ
 
　svgファイルは、２以上指定することにより、ファイル間が補間され、なめらかな（パラパラ）動画となる。<br>
　ただし、svgデータは要素の並びおよび制御点の数が同一である必要がある。<br>
　もし、制御点数が変わる場合は、ファイル間を/(スラッシュ)で区切ることができるが、ファイル間の補間はされない。<br>

　線を赤に指定すると（svg要素の並びおよび制御点の数を同一に維持しつつ）発光を止めることができる。<br>
　パラメータは、３〜５くらいで調整する。<br>


<h3>サンプル１(http://youtu.be/myfJ6V5ekQA)</h3>

$ python mkframe.py fabnight.svg fabnight.svg fabnight.svg fabnight.svg| python addz.py | python mk6wav.py out.wav 4

　同じファイルを指定しているので、fabnight.svgが静止画で描画される。



<h3>サンプル２(http://youtu.be/9l8JLKCcH1s)</h3>
  
$ python mkframe.py F.svg F.svg A.svg A.svg B.svg B.svg N.svg N.svg I.svg I.svg G.svg G.svg H.svg H.svg T.svg T.svg F.svg A.svg B.svg N.svg I.svg G.svg H.svg T.svg 88.svg 88.svg| python addz.py | python mk6wav.py out.wav 5

　指定したsvgファイルは、要素の並びと制御点数が同一。各ファイルのデータ間は補間されるので、モーフィングのような効果が得られている。
　


<h3>サンプル３(http://youtu.be/eNeM1d6433c)</h3>

$ python mkframe.py 2-0.svg 2-2.svg / 20-1.svg 20-2.svg / 201-1.svg 201-2.svg / 2014-1.svg 2014-2.svg 2014-2.svg 2014-3.svg 2014-4.svg | python addz.py | python mk6wav.py out.wav 4

　数字の移動（要素の並びと制御点数が変化しない）をいくつか組み合わせ、最後に拡大縮小（これも要素の並びと制御点数が変化しない）した例。



<h3>サンプル４（https://www.youtube.com/watch?v=lbtdb77kan0)</h3>

$ python mkframe.py tanabata1.svg tanabata2.svg / tanabata3.svg tanabata4.svg tanabata4.svg tanabata5.svg tanabata5.svg / tanabata2.svg tanabata2.svg | python addz.py | python mk6wav.py out.wav 3

