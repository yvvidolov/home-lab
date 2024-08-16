'''
Parse docker-compose subdirectories to extract metadata information and compose a Portainer template JSON.

- Convert README.md from markdown to HTML and include in template note
- Parse .env file to fill parameters: value = pair # description
- Parse docker-compose.yml comments to fill template information, (everything except name is optional):
#name template_and_stack_name
#category filter_cat_1 filter_cat_2
#description short description visible in template list
#note html description of the stack including configuration and first run information
#logo url to image

NOTE: run from root repository path
'''

# Dependencies
import os
import sys
import json
import subprocess
import markdown
import argparse

# Settings
STACKS_PATH = 'docker-compose'
TEMPLATE_PATH = 'portainer-templates'

# Code
def parse_docker_dirs(debug=False):
    if not os.path.exists(STACKS_PATH):
        print("[Error] Please run script from the repository root directory")
        exit(1)

    # Get git remote repo to fill composer links or use manual input
    try:
        git_stdout = subprocess.check_output("git config remote.origin.url", shell=True, stderr=subprocess.STDOUT, universal_newlines=True).strip()
        repo_url = 'https://'+git_stdout.split('@')[-1].replace('.git', '').replace(':', '/')
    except subprocess.CalledProcessError as e:
        print('[Warning] Cannot find git repo to fill docker-compose links, please input manually: https://github.com/yvvidolov/home-lab')
        repo_url = input()

    template = {}
    template['version'] = '2'
    template['templates'] = []

    stacks = [d for d in os.listdir(STACKS_PATH) if os.path.isdir(f'{STACKS_PATH}/{d}')]
    for stack in stacks:
        if debug: print(f'# Stack: {stack}')

        env_list = []
        env_file = f'{STACKS_PATH}/{stack}/.env'
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' not in line: continue
                    if line[0] == '#': continue
                    line = line.strip()
                    name, value = line.split('=')
                    value, *description = value.split('#')
                    description = ''.join(description).strip() if description else ''
                    name = name.strip()
                    value = value.strip()
                    env_list.append({          
                        "label": name,
                        "name": name,
                        "default": value,
                        "description": description})
        # env

        # If we have a readme file, convert it to html and embed in template
        readme_file = f'{STACKS_PATH}/{stack}/README.md'
        note_html = None
        if os.path.exists(readme_file):
            with open(readme_file, 'r', encoding='utf-8') as f:
                markdown_data = f.read()
                note_html = markdown.markdown(markdown_data)

        # Parse .yml file and find metadata describing the package
        yml_data = {}
        compose_file = f'{STACKS_PATH}/{stack}/docker-compose.yml'
        if os.path.exists(compose_file):
            with open(compose_file, 'r', encoding='utf-8') as f:
                contents = f.read()
                content_lines = contents.split('\n')

                lines_start_char = [1 if len(c) > 1 and c[0] == '#' else 0 for c in content_lines]
                first_non_comment_line = lines_start_char.index(0)
                comment_block = content_lines[0:first_non_comment_line]
                
                for line in comment_block:
                    if '#name' in line and ':' in line:
                        yml_data['stack_name'] = ':'.join(line.split(':')[1:]).strip()
                    if '#platform' in line and ':' in line:
                        yml_data['platform'] = ':'.join(line.split(':')[1:]).strip()
                    if '#categories' in line and ':' in line:
                        yml_data['categories'] = ':'.join(line.split(':')[1:]).strip()
                    if '#logo' in line and ':' in line:
                        yml_data['logo'] = ':'.join(line.split(':')[1:]).strip()
                    if '#description' in line and ':' in line:
                        yml_data['description'] = ':'.join(line.split(':')[1:]).strip()
                    if '#note' in line and ':' in line:
                        yml_data['note'] = ':'.join(line.split(':')[1:]).strip()
        else:
            continue # don't add an entry if docker-compose.yml is missing
        # yml
                
        get_yml_data = lambda data, default: yml_data[data] if data in yml_data else default

        entry = {}
        entry["type"] = 3 # 3 means stack
        entry["title"] = get_yml_data('stack_name', stack) # name in the template list
        # entry["stack_name"] = get_yml_data('stack_name', stack) # the name of the stack after deployment
        entry["categories"] = get_yml_data('categories', '').split() # For filtering in portainer
        entry["description"] = get_yml_data('description', '') # Visible in the template list
        entry["logo"] = get_yml_data('logo', '')
        entry["note"] = note_html if note_html is not None else get_yml_data('note', '') # Visible when selected for deployment
        entry["platform"] = get_yml_data('platform', '')
        entry["env"] = env_list
        entry["repository"] = {
            "stackfile": f"{STACKS_PATH}/{stack}/docker-compose.yml",
            "url": repo_url,
        }
        
        entry["categories"].append('home-lab')

        template['templates'].append(entry)
    # for stack in stacks

    template_json = json.dumps(template, indent=2)
    return template_json
# parse docker dirs


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--console", action="store_true", help="Output JSON to stdout")
        parser.add_argument("-f", "--file", default=[TEMPLATE_PATH+'/templates.json'], nargs='*', help="Output JSON to file")
        # parser.add_argument("-h", "--help", action="help", help="Print help message") # This is default behaviour
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        parser.print_help()
        sys.exit(0)

    template_json = parse_docker_dirs()

    for filename in args.file:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(template_json)

    if args.console:
        print()
        print(template_json)
# main
