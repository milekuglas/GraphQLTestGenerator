from textx import metamodel_from_file
import os
from os import listdir
import click

from generation.generators.main_generator import MainGenerator
from generation.generators.test_spec_generator import TestSpecGenerator
from preprocessor.model_preprocessor import convert_tag_values

def get_model(path):
    metamodel = metamodel_from_file('metamodel/graphql.tx', use_regexp_group=True)
    metamodel_full = metamodel_from_file('metamodel/graphql_validate.tx', use_regexp_group=True)
    metamodel.register_model_processor(convert_tag_values)
    models = {}

    for file in listdir(path):
        package = None
        if file.endswith('.test'):
            model = metamodel.model_from_file(path + '/' + file)
            metamodel_full.model_from_file(path + '/' + file)
            if model.package is not None:
                package = model.package.name
            if package is None:
                full_name = model.class_name.name
            else:
                full_name = package + '.' + model.class_name.name
            if full_name not in models:
                models[full_name] = [model]
            else:
                models[full_name].append(model)
    return models

def delete_files(path):
    try:
        for (dirpath, dirnames, filenames) in os.walk(path):
            for directory in dirnames:
                path = os.path.join(dirpath, directory)
                delete_files(path)
            for filename in filenames:
                if 'manual' not in dirpath:
                    os.remove(os.path.join(dirpath, filename))
    except Exception:
        pass

@click.command()
@click.option('--model', default='./examples', help='Path to the model directory.')
@click.option('--output', default='./output', help='Path to the output directory.')
def run(model, output):
    delete_files(output + '/test')
    main_generator = MainGenerator(output)
    test_spec_generator = TestSpecGenerator(main_generator)
    main_generator.add_generator(test_spec_generator)
    main_generator.generate_all(get_model(model))



if __name__ == '__main__':
    run()
