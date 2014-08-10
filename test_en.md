Laser
=====
<h3>Scripts to generate wav-data for laser projector controlled by garvano mirror.</h3>
All data including python script of this repository is under a creative commons License (CC BY 3.0)<br>
By penkich, a member of fablab kitakagaya<br>

Procedure
1) prepare svg files using Bézier tool of Inkscape.<br>
2) convert svg data to x,y data by a script(mkframe.py)<br>
3) add z(on/off) data by a script(addz.py)<br>
4) generate wav file from x,y,z data by a script (mk6wav.py)<br>

<h3>Usage</h3>

$ python mkframe.py file1.svg file2.svg ... | python addz.py | python mk6wav.py out.wav parameter<br>
 Give 2 or more than 2 svg files to the command, then the difference of between svg paths can be calculated and x,y position datta 
is generated as far as the type and the number of the svg elements are same. Otherwise, separate slashes(/) between files then the difference is not calculated.<br>　もし、制御点数が変わる場合は、ファイル間を/(スラッシュ)で区切ることができるが、ファイル間の補間はされない。<br>
 If you change stroke of a path color to red, you can be able not to display it.<br> 
 You may adjust parameter value 3 to 5.<br>

<h3>sample1(http://youtu.be/myfJ6V5ekQA)</h3>

$ python mkframe.py fabnight.svg fabnight.svg fabnight.svg fabnight.svg| python addz.py | python mk6wav.py out.wav 4

 As the same files, a static drawing of fabnight.svg can be appeared. 


<h3>sample2(http://youtu.be/9l8JLKCcH1s)</h3>
  
$ python mkframe.py F.svg F.svg A.svg A.svg B.svg B.svg N.svg N.svg I.svg I.svg G.svg G.svg H.svg H.svg T.svg T.svg F.svg A.svg B.svg N.svg I.svg G.svg H.svg T.svg 88.svg 88.svg| python addz.py | python mk6wav.py out.wav 5

 As the files 要素の並びと制御点数が同一。各ファイルのデータ間は補間されるので、モーフィングのような効果が得られている。
　


<h3>サンプル３(http://youtu.be/eNeM1d6433c)</h3>

$ python mkframe.py 2-0.svg 2-2.svg / 20-1.svg 20-2.svg / 201-1.svg 201-2.svg / 2014-1.svg 2014-2.svg 2014-2.svg 2014-3.svg 2014-4.svg | python addz.py | python mk6wav.py out.wav 4

　数字の移動（要素の並びと制御点数が変化しない）をいくつか組み合わせ、最後に拡大縮小（これも要素の並びと制御点数が変化しない）した例。
