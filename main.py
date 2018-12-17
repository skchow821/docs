import sys
import argparse
import logging
import yaml
import os
import jinja2

def path_normalize(path):
    return os.path.abspath(os.path.expanduser(path))

def get_templates(template_abs_path):
    template_entities = [os.path.join(template_abs_path, obj) for obj in os.listdir(template_abs_path)]
    logging.debug(template_entities)
    return [template_file for template_file in template_entities if os.path.isfile(template_file) and template_file.endswith("jinja2")]

def render_with_template(yaml_data, template_path, template_id, target, output_dir):
    format_ext = (os.path.splitext(os.path.splitext(template_id)[0])[-1]).lower()
    target_name = target + format_ext
    target_path = os.path.join(output_dir, target_name)
    if not os.path.exists(output_dir):
        logging.debug("Creating {}".format(output_dir))
        os.makedirs(output_dir)

    logging.debug("Rendering with {} to {}".format(template_id, target_path))

    jinja2_template_loader = jinja2.FileSystemLoader(template_path)
    options = { "loader": jinja2_template_loader }
    if format_ext == ".tex":
        options["block_start_string"] =  '~<'
        options["block_end_string"] = '>~'
        options["variable_start_string"] = '<<'
        options["variable_end_string"] = '>>'
        options["comment_start_string"] = '<#'
        options["comment_end_string"] = '#>'
    jinja2_environment = jinja2.Environment(**options)
    template = jinja2_environment.get_template(template_id)
    rendered_output = template.render(resume = yaml_data).encode('utf-8')
    with open(target_path, 'w') as output:
        output.write(rendered_output)

# program logic
# From: inspired by https://github.com/bamos/cv/blob/master/generate.py
def parse_arguments():
    parser = argparse.ArgumentParser(description='Takes a resume in yaml format and formats with templates?')
    parser.add_argument('--input', '-i', dest='input_file', required=True, help='input yaml file for resume')
    parser.add_argument('--output', '-o',  dest='output_dir', default="products", help='output directory for formatted resumes')
    parser.add_argument('--template', '-t', dest='template_dir', required=True, help='directory of templates')

    return parser.parse_args()

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s, %(module)s, %(funcName)s, %(message)s")

def main():
    setup_logging()
    args = parse_arguments()
    template_files = get_templates(path_normalize(args.template_dir))
    logging.debug(template_files)
    with open(path_normalize(args.input_file), 'r') as yaml_input:
        yaml_data = yaml.safe_load(yaml_input)
        for template_file in template_files:
            render_with_template(yaml_data, path_normalize(args.template_dir),
                os.path.basename(template_file), "resume", path_normalize(args.output_dir))

if __name__ == '__main__':
    main()
