# Five Shu Points 五輸穴

Rotatable 3D models of the right arm and right leg showing the five shu points (Jing-Well, Ying-Spring, Shu-Stream, Jing-River, He-Sea) of all twelve primary channels, coloured by their five-element assignment.

| Page | Channels | Points |
|---|---|---|
| `index.html` | Landing page | |
| `arm.html` | LU, LI, HT, PC, SI, TB | 30 |
| `leg.html` | ST, SP, BL, KI, GB, LR | 30 |
| `channels.html` | Full courses on a human figure of all twelve channels and the Conception (CV) and Governor (GV) Vessels, grouped by element. Open one directly with its code, for example `#LU`, `#ST`, `#BL` or `#GV` | 361 |
| `li-channel.html` | Redirects to `channels.html#LI` | |

Each page is a single self-contained HTML file. Open it in a browser, or serve the folder (`python3 -m http.server`) so the Arm/Leg switch moves between pages. The only network requests are three.js r128 from cdnjs and the fonts from Google Fonts.

## Using the models

- Drag to rotate, scroll or pinch to zoom.
- Click a point on the model, or in the lists, to fly to it and read its name, shu type, element, channel and location.
- The buttons above the model turn it to a side (palm, back, thumb, little finger; or front, back, inner, outer, sole). The circular-arrow button spins it slowly.
- Each channel and its line can be shown or hidden.

## How the models are built

The limbs are signed distance fields (tapered capsules blended together, plus elliptical cross-sections along the limb) turned into a mesh with surface nets in the browser. Points are placed by walking out from inside the limb to the skin from each textbook location, and channel lines are drawn along the skin between the points.

The arm's width profile, from mid upper arm to wrist, was measured from a vector trace of the arm outline in "Points of lung channel" by Dimitrius. The leg's proportions are modelled by hand.

The channel course page uses the [MakeHuman](https://github.com/makehumancommunity/makehuman) base mesh (CC0). Points are placed by casting rays from the skeleton joints to the skin, measured in cun from the joints, and the course is traced over the skin between them. Solid lines are the channel on the surface, dashed lines are connecting branches on the skin (for example LI16 to GV14 to ST12), and dotted lines are the internal course, drawn as simple lines seen through the body. The scripts are in `tools/body-course/`.

## Data

Point names, element assignments and location text come from the Shu Atlas point list (`data/points.json` in `arm-pz/acupuncture-element-points`). Yin channels run Wood → Fire → Earth → Metal → Water from the well point; yang channels run Metal → Water → Wood → Fire → Earth.

## Credits and licence

The figure in `channels.html` is the MakeHuman base mesh, released under CC0 by its copyright holders.

`arm.html` contains an arm outline derived from ["Points of lung channel"](https://commons.wikimedia.org/wiki/File:Points_of_lung_channel.svg) by Dimitrius, Wikimedia Commons, licensed [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). The arm model is shared under the same licence.

These are schematic study models, not clinical references.
