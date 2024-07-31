# Parse .env file to fill parameters: value = pair # description
# Parse docker-compose.yml comments to fill template information, (everything except name is optional):
#name template_and_stack_name
#category filter_cat_1 filter_cat_2
#brief short description visible in template list
#info html description of the stack including configuration and first run information
#logo url to image

# NOTE: run from root repository path

import os
import json
import subprocess
import markdown

stacks_path = 'docker-compose'
template_path = 'portainer-templates'

if not os.path.exists(stacks_path):
    print("[Error] Please run script from the repository root directory")
    exit(1)

# Get git remote repo to fill composer links or use manual input
try:
    git_stdout = subprocess.check_output("git config remote.origin.url", shell=True, stderr=subprocess.STDOUT, universal_newlines=True).strip()
    repo_url = 'https://'+git_stdout.split('@')[-1].replace('.git', '').replace(':', '/')
except subprocess.CalledProcessError as e:
    print('[Warning] Cannot find git repo to fill docker-compose links, please input manually: https://github.com/yvvidolov/home-lab')
    repo_url = input()


debug = True

template = {}
template['version'] = '2'
template['templates'] = []

stacks = os.listdir(stacks_path)
for stack in stacks:
    if debug: print(f'# Stack: {stack}')

    env_list = []
    env_file = f'{stacks_path}/{stack}/.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' not in line: continue
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
    readme_file = f'{stacks_path}/{stack}/README.md'
    note_html = None
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            markdown_data = f.read()
            note_html = markdown.markdown(markdown_data)

    # Parse .yml file and find metadata describing the package
    yml_data = {}
    compose_file = f'{stacks_path}/{stack}/docker-compose.yml'
    if os.path.exists(compose_file):
        with open(compose_file, 'r', encoding='utf-8') as f:
            contents = f.read()
            content_lines = contents.split('\n')

            lines_start_char = [1 if len(c) > 1 and c[0] == '#' else 0 for c in content_lines]
            first_non_comment_line = lines_start_char.index(0)
            comment_block = content_lines[0:first_non_comment_line]
            
            for line in comment_block:
                if 'platform' in line and ':' in line:
                    yml_data['platform'] = line.split(':')[-1].strip()
                if 'categories' in line and ':' in line:
                    yml_data['categories'] = line.split(':')[-1].strip()
                if 'logo' in line and ':' in line:
                    yml_data['logo'] = line.split(':')[-1].strip()
                if 'note' in line and ':' in line:
                    yml_data['note'] = line.split(':')[-1].strip()
                if 'description' in line and ':' in line:
                    yml_data['description'] = line.split(':')[-1].strip()
    # yml
            
    get_yml_data = lambda data, default: yml_data[data] if data in yml_data else default

    entry = {}
    entry["type"] = 3 # 3 means stack
    entry["title"] = stack # name in the template list
    entry["name"] = stack # the name of the stack after deployment
    entry["categories"] = get_yml_data('categories', '').split() # For filtering in portainer
    entry["description"] = get_yml_data('description', '') # Visible in the template list
    entry["logo"] = get_yml_data('logo', '')
    entry["note"] = note_html if note_html is not None else get_yml_data('note', '') # Visible when selected for deployment
    entry["platform"] = get_yml_data('platform', '')
    entry["env"] = env_list
    entry["repository"] = {
        "stackfile": f"{stacks_path}/{stack}/docker-compose.yml",
        "url": repo_url,
      }

    template['templates'].append(entry)
# for stack in stacks

template_json = json.dumps(template, indent=2)

with open(template_path+'/templates.json', 'w', encoding='utf-8') as f:
    f.write(template_json)

print()
print(template_json)
