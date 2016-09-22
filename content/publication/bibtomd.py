# coding=utf-8
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--infile", type=str,
                    help="In-file in bibtext format")
args = parser.parse_args()

pubs = []
with open(args.infile) as infile:
    pub = {}
    for line in infile:
        if line.startswith('@'):
            pubs.append(pub)
            pub = {}
        m = re.match('^\s*([^\=]*)\=(.*)$', line)
        if m:
            pub[m.group(1).strip()] = m.group(2).strip(' {},').replace(r'{\"O}','Ö').replace(r'{\"A}','Ä').replace(r'{\AA}', 'Å').replace(r'{\"o}','ö').replace(r'{\"a}','ä').replace(r'{\aa}', 'å').replace(r'{\&}amp;', '&').replace(r'{\’e;}', 'é').replace(r'{\"u}', 'ü').replace(r'{\’a;}', 'á').replace(' :', ':').replace(r'\&', '&').replace('{','').replace('}','').replace('\\','')
    pubs.append(pub)

for pub in pubs:
    if not 'title' in pub:
        print "Warning! no title in: " + str(pub)
    else:
        pub['title'] = pub['title'].replace('.', '')
        filename = pub['title'].lower().replace(' ', '-').replace(':','').replace('\'','').replace('(','').replace(')','') + '.md'
        print filename
        with open(filename, 'w') as outfile:
            outfile.write('+++\n')
            for k, v in pub.iteritems():
                if k == 'url':
                    k = 'url_html'
                outfile.write(k + ' = "' + v + '"\n')
            outfile.write('+++\n\n')

