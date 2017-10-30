#
# build-faculty-profiles.py
#
# Convert a CSV file of faculty information to Markdown files appropriate for
# consumption by Jekyll.
#

import invoke
import csv
import requests
from jinja2 import Template, Environment, FileSystemLoader

FACULTY_CSV_URL = 'https://docs.google.com/spreadsheets/export?format=csv&id=1WW7S0t6qUcFabLL4I9bE1uLex8wQmA40KfNEfXqCma4'
OUTPUT_DIR = './_people/faculty-auto/'

@invoke.task()
def build_faculty_profiles():
  env = Environment(
    loader=FileSystemLoader(searchpath='./_people')
  )
  template = env.get_template('_template.j2')
  csv_file = requests.get(FACULTY_CSV_URL).text.splitlines();
  reader = csv.reader(csv_file, delimiter=',')
  headers = next(reader)
  
  ctx = {
    'role': 'faculty',

    # TODO: determine TBD fields, which will depend on which fields we require
    #       via the input form.
    'tbds': []
  }
  for row in reader:
    for i in range(len(headers)):
      ctx[headers[i].lower().replace(" ", "_")] = row[i].strip()
    
    if ctx['affiliations']:
      ctx['affiliations'] = [affil.strip() for affil in ctx['affiliations'].split(",")]

    outfile = ctx['last_name'].lower() + '-' + ctx['first_name'].lower() + '.md'
    with open(OUTPUT_DIR + outfile, 'w') as fhand:
      fhand.write(template.render(ctx))
    
    fhand.close()
