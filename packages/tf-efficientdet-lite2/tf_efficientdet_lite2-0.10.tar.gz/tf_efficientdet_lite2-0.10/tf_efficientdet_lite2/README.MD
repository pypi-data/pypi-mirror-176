# Object detection with tensorflow

<img src="https://github.com/hansalemaos/screenshots/raw/main/tensorflowscreen.png"/>

```python
$pip install tf-efficientdet-lite2
from tf_efficientdet_lite2 import TfEfficientdetLite2
tflo= TfEfficientdetLite2(sevenzip_path = r"C:\Program Files\7-Zip\7z.exe",set_visible_devices_0 = True) #works without 7-zip as well
tflo.detect(r'https://images.pexels.com/photos/14139354/pexels-photo-14139354.jpeg?cs=srgb&dl=pexels-olena-bohovyk-14139354.jpg&fm=jpg&_gl=1*19indnx*_ga*ODM0MDU4MTIyLjE2NjgzMzEwODk.*_ga_8JE65Q40S6*MTY2ODMzMTA4OS4xLjEuMTY2ODMzMTA5My4wLjAuMA..',draw_results=True,draw_result_min_score=.3)
tflo.get_df()

        aa_class  aa_x_start  aa_y_start  aa_x_end  aa_y_end   aa_conf
0         person         449         124       870       611  0.915973
1            cup         916         521      1022       654  0.642683
2            cup         652         360       732       469  0.561634
3   dining table         829          21      1200       793  0.545763
4          chair         926           1      1198       176  0.235585
..           ...         ...         ...       ...       ...       ...
95         chair         988          13      1188       253  0.012212
96           cup         857         491       947       616  0.011954
97         chair        1149         728      1196       793  0.011811
98         spoon         651         371       666       409  0.011780
99         spoon        1013         290      1062       358  0.011758


tflo.get_drawn_results()

```