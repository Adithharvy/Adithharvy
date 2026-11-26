# Satellite Flood Change Explorer

An offline browser demo of water-change detection on a **synthetic** river floodplain. It uses civil Earth-observation methods and generated green and near-infrared reflectances. It contains no real imagery, coordinates or incident measurements.

## Run

With Python 3.11 or later, run `python analyze.py --verify` in this directory. Open the generated `demo.html` in a browser. No packages or server are needed. `python analyze.py --json` prints the full threshold sweep and metrics.

## Results

At the preset NDWI threshold of 0.10, the after-only baseline obtained **0.207 IoU** against the visible synthetic flood reference. Requiring the pixel to cross the water threshold from before to after increased IoU to **0.383**. False positives fell from **631 to 247** and recall stayed at **84.4%**. The before/after change mask estimated **0.378 km²** of candidate water. Of 6,144 total pixels, **416** were masked and excluded from the scores.

## How it works

The seeded generator draws fixed river, standing water, floodplain, vegetation, shadows and cloud masks. It adds noise to green and near-infrared reflectances. The normalized difference water index is `(green − near infrared) / (green + near infrared)`, quantized to 0.001. A new-water candidate crosses the chosen threshold from below. The after-only baseline counts any visible pixel at or above the threshold in the second scene. SQLite computes the confusion counts and metrics for both methods, using a 30 m synthetic pixel size for area. IoU is intersection over union against generated flood labels.

Switch between the change mask, the baseline and the synthetic reference. The threshold sweep measures sensitivity, while the cloud mask measures missing coverage. Neither measures statistical confidence. Shadows and vegetation still cause errors. These numbers describe one generated scene and cannot validate the method on a real flood.

## Interview explanation

The after-only method counts permanent water as flood. Compare the scenes to remove much of that error, then show the remaining false positives and cloud gaps. Explain what real-world validation would require, such as co-registered imagery and an independently mapped flood extent.

This is an AI-assisted portfolio prototype prepared for Adith Harvy. Code is available under the [MIT License](./LICENSE). The source generates every pixel and reference label.
