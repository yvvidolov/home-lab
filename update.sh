python portainer-templates/tools/gen_all.py -f $(pwd)/portainer-templates/templates.json
python portainer-templates/tools/merge_template_urls.py https://raw.githubusercontent.com/Lissy93/portainer-templates/main/templates.json portainer-templates/templates.json -o portainer-templates/templates_merge.json
