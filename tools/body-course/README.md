# Channel course on a full body

Builds `li-channel.html`: the Large Intestine channel (LI1 to LI20) on the MakeHuman base mesh.

1. Get the MakeHuman data (the base mesh and rig are CC0):
   ```
   git clone --depth 1 --filter=blob:none --sparse https://github.com/makehumancommunity/makehuman
   git -C makehuman sparse-checkout set makehuman/data/3dobjs makehuman/data/rigs
   export MAKEHUMAN_DATA=$PWD/makehuman/makehuman/data
   ```
2. From this folder, with numpy installed:
   ```
   mkdir -p build && python3 points.py && python3 paths.py && python3 gen_li.py
   ```

- `mhbody.py` loads the body group of the base mesh and the skeleton joints, and casts rays against the mesh.
- `points.py` places each point by casting a ray from a joint (or from outside the face) to the skin, using cun measured from the joints: 12 cun from elbow to wrist, 9 cun from the armpit fold to the elbow.
- `paths.py` traces the course between points over the skin. Solid segments are on the surface; `connect` and `cheek` are drawn dashed as the connecting course.
- `gen_li.py` writes the page from `li_template.html`, reusing the stylesheet of `arm.html`.

The figure's right side is at negative x, it faces +z, and units are decimetres (scaled to centimetres in the page).
