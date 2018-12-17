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

def create_environment(template_path, format_ext):
    jinja2_template_loader = jinja2.FileSystemLoader(template_path)
    options = { "loader": jinja2_template_loader }
    if format_ext == ".tex":
        options["block_start_string"] =  '~<'
        options["block_end_string"] = '>~'
        options["variable_start_string"] = '<<'
        options["variable_end_string"] = '>>'
        options["comment_start_string"] = '<#'
        options["comment_end_string"] = '#>'
    return jinja2.Environment(**options)

def render_with_template(resume_data, contact_data, template_path, template_id, output_dir):
    template_id_parts = template_id.split('.')
    if len(template_id_parts) < 3 or template_id_parts[2].lower() != "jinja2":
        logging.warning("template_id {} is not valid!".format(template_id))
        return

    target_name = os.path.splitext(template_id)[0]
    format_ext = os.path.splitext(target_name)[-1].lower()
    target_path = os.path.join(output_dir, target_name)

    logging.debug("Rendering with {} to {}".format(template_id, target_path))
    jinja2_environment = create_environment(template_path, format_ext)
    template = jinja2_environment.get_template(template_id)
    rendered_output = template.render(resume = resume_data, contact = contact_data).encode('utf-8')
    with open(target_path, 'w') as output:
        output.write(rendered_output)

# program logic
# From: inspired by https://github.com/bamos/cv/blob/master/generate.py
def parse_arguments():
    parser = argparse.ArgumentParser(description='Takes a resume in yaml format and formats with templates?')
    parser.add_argument('--input', '-i', dest='input_file', required=True, help='input yaml file for resume')
    parser.add_argument('--output', '-o',  dest='output_dir', default="products", help='output directory for formatted resumes')
    parser.add_argument('--contact_info', '-c', dest='contact_file', default=None, help='Optional contact info to be included for resume')
    parser.add_argument('--template', '-t', dest='template_dir', required=True, help='directory of templates')
    arguments = parser.parse_args()

    # Normalize paths.
    arguments.input_file = path_normalize(arguments.input_file)
    arguments.output_dir = path_normalize(arguments.output_dir)
    arguments.template_dir = path_normalize(arguments.template_dir)
    if arguments.contact_file is not None:
        arguments.contact_file = path_normalize(arguments.contact_file)
    return arguments

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s, %(module)s, %(funcName)s, %(message)s")

def main():
    setup_logging()
    args = parse_arguments()

    # Create output path
    if not os.path.exists(args.output_dir):
        logging.debug("Creating {}".format(args.output_dir))
        os.makedirs(args.output_dir)

    # Get list of valid jinja2 template files.
    template_files = get_templates(args.template_dir)
    logging.debug(template_files)

    with open(args.input_file, 'r') as yaml_input:
        resume_data = yaml.safe_load(yaml_input)
        contact_data = None
        if args.contact_file is not None:
            with open(args.contact_file, 'r') as contact_input:
                contact_data = yaml.safe_load(contact_input)
                logging.debug("contact info {} loaded".format(contact_input))

        for template_file in template_files:
            render_with_template(resume_data, contact_data, args.template_dir,
                os.path.basename(template_file), args.output_dir)

if __name__ == '__main__':
    main()
