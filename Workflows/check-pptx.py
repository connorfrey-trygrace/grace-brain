#!/usr/bin/env python3
"""Check a .pptx for the faults that make PowerPoint ask to repair it.

    python3 Workflows/check-pptx.py <deck.pptx> [--fix]

Checks:
  1. duplicate package parts  - two zip entries with the same name, different content.
     This is the one that has actually bitten us (2026-08-29, the 8/30 lunch deck).
     python-pptx round-trips them silently and resolves to the LAST copy; PowerPoint
     may resolve to the other, which is the repair prompt.
  2. orphan slide/media/notes parts - present in the package, referenced by nothing.
     Left behind when a slide is removed from <p:sldIdLst> without dropping the part.
  3. hand-written <p:timing> animation XML - corrupted this deck once already.

--fix rewrites the file keeping the last copy of each duplicated name and leaves a
.bak beside it. Orphans are reported, not removed (the container's pptx skill has
scripts/clean.py for that).

Run this after every build, before handing a deck to Connor.

Also: python-pptx RENUMBERS slide parts on save, so ppt/slides/slideN.xml matches
presentation order only until the next save by something else. Never target a slide
by filename from an earlier inspection - resolve position -> partname through
<p:sldIdLst> in ppt/presentation.xml and ppt/_rels/presentation.xml.rels. Pass
--map to print that mapping.
"""
import collections, os, shutil, sys, zipfile

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    fix = '--fix' in sys.argv
    if not args:
        print(__doc__); return 2
    f = args[0]
    z = zipfile.ZipFile(f)
    names = z.namelist()
    dupes = {k: v for k, v in collections.Counter(names).items() if v > 1}
    timing = [n for n in names if n.startswith('ppt/slides/slide') and b'<p:timing' in z.read(n)]

    refs = set()
    for n in names:
        if n.endswith('.rels') or n.endswith('.xml'):
            d = z.read(n).decode('utf8', 'replace')
            for tok in ('slides/slide', 'media/image', 'media/media', 'notesSlides/notesSlide'):
                i = 0
                while True:
                    i = d.find(tok, i)
                    if i < 0: break
                    j = i
                    while j < len(d) and d[j] not in '"\'<> ': j += 1
                    refs.add(d[i:j].lstrip('./')); i = j
    orphans = []
    for n in names:
        for pre in ('ppt/slides/slide', 'ppt/media/', 'ppt/notesSlides/notesSlide'):
            if n.startswith(pre) and not n.endswith('.rels') and '_rels' not in n:
                short = n[len('ppt/'):]
                if short not in refs and not any(short in r for r in refs):
                    orphans.append(n)
                break

    if '--map' in sys.argv:
        import re
        pres = z.read('ppt/presentation.xml').decode()
        prels = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="slides/(slide\d+\.xml)"',
                                z.read('ppt/_rels/presentation.xml.rels').decode()))
        for i, (_, rid) in enumerate(re.findall(r'<p:sldId id="(\d+)" r:id="(rId\d+)"/>', pres), 1):
            part = prels[rid]
            titles = re.findall(r'<a:t>(.*?)</a:t>', z.read('ppt/slides/' + part).decode())
            print('%3d  %-14s %s' % (i, part, (titles[0] if titles else '')[:46]))
        print()

    ok = True
    if dupes:
        ok = False
        print('DUPLICATE PARTS (%d) - this is what makes PowerPoint offer to repair:' % len(dupes))
        for k in sorted(dupes): print('   ', k, 'x%d' % dupes[k])
    if orphans:
        print('ORPHAN PARTS (%d) - referenced by nothing, safe to strip:' % len(orphans))
        for n in sorted(orphans)[:40]: print('   ', n)
    if timing:
        ok = False
        print('ANIMATION XML on:', ', '.join(timing), '- remove it, add animations in PowerPoint by hand')
    try:
        from pptx import Presentation
        print('slides:', len(Presentation(f).slides._sldIdLst))
    except Exception as e:
        ok = False
        print('python-pptx could not open it:', e)
    if ok and not dupes and not timing:
        print('OK - no duplicate parts, no animation XML')

    if fix and dupes:
        shutil.copy2(f, f + '.bak')
        infos = z.infolist()
        last = {}
        for i, inf in enumerate(infos): last[inf.filename] = i
        out = f + '.tmp'
        zo = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
        for i, inf in enumerate(infos):
            if last[inf.filename] == i: zo.writestr(inf, z.read(inf))
        zo.close(); z.close()
        os.replace(out, f)
        print('fixed - kept the last copy of each part; original saved as', os.path.basename(f) + '.bak')
    return 0 if (not dupes and not timing) else 1

if __name__ == '__main__':
    sys.exit(main())
