"""Build an offline before/after water-change demo with synthetic imagery and truth."""
import argparse
import base64
import json
import math
import random
import sqlite3
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
WIDTH, HEIGHT, PIXEL_M = 96, 64, 30
THRESHOLDS = [-0.05, 0.00, 0.05, 0.10, 0.15, 0.20, 0.25]
DEFAULT = 0.10


def scene():
    rng = random.Random(917)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            river = 44 + 10*math.sin(y/11)
            distance = abs(x-river)
            permanent = distance < 2.5 or (x-70)**2+(y-45)**2 < 28
            floodplain = 4.3 + 5*max(0, math.sin((y-6)/10))
            flooded = distance < floodplain and 10 < y < 58 and not permanent
            # Shadowed terrain and weakly flooded vegetation deliberately overlap the decision boundary.
            shadow = (x-23)**2/100+(y-37)**2/150 < 1
            weak = math.sin(x*.7+y*.25)>0.5
            base = .36 if permanent else (.03 if shadow else -.23)
            event = (.10 if weak else .30) if flooded else base + (.12 if shadow else 0)
            green0, nir0 = bands(base, rng)
            green1, nir1 = bands(event, rng)
            cloud = (x-53)**2/156+(y-20)**2/48 < 1 or (x-10)**2/55+(y-12)**2/38 < 1
            yield (green0, nir0, green1, nir1, int(cloud), int(flooded))


def bands(water_signal, rng):
    signal = water_signal + rng.gauss(0, .067)
    brightness = rng.uniform(.27, .47)
    return (round(brightness*(1+signal)/2, 5), round(brightness*(1-signal)/2, 5))


def scores(db, prediction):
    # prediction is a constant name selected internally by the caller.
    tp, fp, fn = db.execute(
        f'SELECT sum({prediction} AND truth), sum({prediction} AND NOT truth), '
        f'sum(NOT {prediction} AND truth) FROM pixels WHERE NOT masked'
    ).fetchone()
    return dict(tp=tp, fp=fp, fn=fn, precision=round(tp/max(1, tp+fp), 3),
                recall=round(tp/max(1, tp+fn), 3), iou=round(tp/max(1, tp+fp+fn), 3),
                area=round((tp+fp)*PIXEL_M**2/1_000_000, 3))


def analyze():
    pixels = [(round(1000*(g-n)/(g+n)), round(1000*(a-b)/(a+b)), mask, truth) for g,n,a,b,mask,truth in scene()]
    with sqlite3.connect(':memory:') as db:
        db.execute('CREATE TABLE pixels (before REAL, after REAL, masked INTEGER, truth INTEGER, post INTEGER, change INTEGER)')
        db.executemany('INSERT INTO pixels VALUES (?,?,?,?,0,0)',
                       pixels)
        output = []
        for threshold in THRESHOLDS:
            db.execute('UPDATE pixels SET post=after>=?, change=after>=? AND before<?',
                       (round(1000*threshold),)*3)
            output.append(dict(threshold=threshold, post=scores(db, 'post'), change=scores(db, 'change')))
        masked, hidden_truth = db.execute('SELECT sum(masked), sum(masked AND truth) FROM pixels').fetchone()
    return dict(width=WIDTH, height=HEIGHT, area_per_pixel=PIXEL_M**2/1_000_000, default=DEFAULT,
                masked=masked, hidden_truth=hidden_truth, results=output,
                pixels=pixels)


def check(data):
    assert len(data['pixels']) == WIDTH * HEIGHT
    assert 0 < data['hidden_truth'] < data['masked']
    for row in data['results']:
        t = round(1000*row['threshold'])
        visible = [p for p in data['pixels'] if not p[2]]
        tp = sum(after >= t > before and truth for before, after, _, truth in visible)
        fp = sum(after >= t > before and not truth for before, after, _, truth in visible)
        fn = sum(not (after >= t > before) and truth for before, after, _, truth in visible)
        assert (tp, fp, fn) == tuple(row['change'][k] for k in ('tp','fp','fn'))
    default_row = next(r for r in data['results'] if r['threshold'] == DEFAULT)
    assert default_row['change']['iou'] > default_row['post']['iou']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    data = analyze()
    if args.verify:
        check(data)
    if args.json:
        print(json.dumps({key:val for key,val in data.items() if key!='pixels'}, indent=2))
    else:
        template = (HERE/'template.html').read_text(encoding='utf-8')
        data['packed'] = base64.b64encode(b''.join(
            struct.pack('<hhB', before, after, mask | truth << 1)
            for before, after, mask, truth in data.pop('pixels')
        )).decode('ascii')
        (HERE/'demo.html').write_text(template.replace('__DATA__', json.dumps(data, separators=(',',':'))), encoding='utf-8')
        print('Generated demo.html from the seeded synthetic scene')


if __name__ == '__main__':
    main()
