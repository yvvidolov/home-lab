'''
Merge multiple Portainer template.json files
You can use urls or filenames

TODO: add custom category to each one
'''

# Dependencies
import sys
import json
import requests
import argparse

# Settings
TEMPLATE_PATH = 'portainer-templates'
DEFAULT_URLS=[
    # 'https://raw.githubusercontent.com/yvvidolov/home-lab/main/portainer-templates/templates.json',
    TEMPLATE_PATH+'/templates.json', # Use local path instead of URL to avoid double publishing
    'https://raw.githubusercontent.com/Lissy93/portainer-templates/main/templates.json'
]

# Code
def merge_template_urls(urls, debug=True):
    merged_templates = None
    for url in urls:
        if 'http' in url:
            response = requests.get(url)
            template = response.json()
        else:
            with open(url, 'r', encoding='utf-8') as file:
                template = json.load(file)

        if debug:
            print(f"{len(template['templates'])} templates from: {url}")

        if merged_templates is None:
            merged_templates = template
        else:
            merged_templates['templates'].extend(template['templates'])

    if debug:
        print(f"Total Templates: {len(merged_templates['templates'])}")

    return merged_templates


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--output", default=[TEMPLATE_PATH+'/templates_merge.json'], nargs=1, help="Output JSON to file")
        args, args_remaining = parser.parse_known_args()
    except argparse.ArgumentError as e:
        parser.print_help()
        sys.exit(0)

    url_list = args_remaining if len(args_remaining) else DEFAULT_URLS

    templates = merge_template_urls(url_list)

    with open(args.output[0], 'w', encoding='utf-8') as f:
        template_json = json.dumps(templates, indent=2)
        f.write(template_json)
