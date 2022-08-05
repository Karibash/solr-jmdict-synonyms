import re
import argparse
import xml.etree.ElementTree as ET


def format_text(text: str):
    return re.sub(r'\(.*\)', '', text).replace('...', '').strip(' ')


def main():
    parser = argparse.ArgumentParser(prog='jmdict2es.py', description='convert JMDict to solr synonyms')
    parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    parser.add_argument('-p', '--output-predicate', action='store_true', help='output predicates')
    args = parser.parse_args()

    for file in args.files:
        tree = ET.parse(file)
        for entry in tree.iter('entry'):
            synonyms = []
            synonyms.extend([element.find('keb').text for element in entry.iter('k_ele')])
            synonyms.extend([element.find('reb').text for element in entry.iter('r_ele')])
            for element in entry.iter('sense'):
                synonyms.extend([format_text(gloss.text) for gloss in element.iter('gloss')])
            print(','.join(synonyms))


if __name__ == "__main__":
    main()
