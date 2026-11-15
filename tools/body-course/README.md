# Channel courses on a full body

Builds `channels.html`: the courses of the Lung, Large Intestine, Heart, Small Intestine, Pericardium and Triple Burner channels on the MakeHuman base mesh. Each channel opens at `channels.html#LU`, `#LI`, `#HT`, `#SI`, `#PC` or `#TB`.

1. Get the MakeHuman data (the base mesh and rig are CC0):
   ```
   git clone --depth 1 --filter=blob:none --sparse https://github.com/makehumancommunity/makehuman
   git -C makehuman sparse-checkout set makehuman/data/3dobjs makehuman/data/rigs
   export MAKEHUMAN_DATA=$PWD/makehuman/makehuman/data
   ```
2. From this folder, with numpy installed:
   ```
   python3 channels.py && python3 gen_channels.py
   ```

| File | What it does |
|---|---|
| `mhbody.py` | Loads the body of the base mesh and its skeleton joints; casts rays against the mesh. |
| `channels.py` | Places every point and traces every course. Writes `build/data.json`. |
| `meta.py` | Point names, categories and locations. |
| `courses.json` | The course description for each channel. |
| `li_points.json`, `shu_points.json` | LI point text, and five-shu point text from the Shu Atlas data. |
| `gen_channels.py` | Writes `channels.html` from `channels_template.html`, using the stylesheet of `arm.html`. |

How points are placed: each point starts inside the limb, at a skeleton joint or along a bone, and a ray finds the skin in a set direction (thumb side, back of the hand, crease side of the elbow, and so on). Face, ear and chest points are found by casting from outside the skin inward. Distances use cun measured on the figure: 12 cun from elbow to wrist, 9 cun from the armpit fold to the elbow, and 4 cun from the midline to the nipple.

Each course is a list of segments:
- `surface`: the channel on the skin. It is traced between points by casting back onto the skin.
- `connect`: a connecting branch on the skin, drawn dashed.
- `internal`: the internal course, drawn dotted through the body.

The figure's right side is at negative x, it faces +z, and units are decimetres (scaled to centimetres in the page).
