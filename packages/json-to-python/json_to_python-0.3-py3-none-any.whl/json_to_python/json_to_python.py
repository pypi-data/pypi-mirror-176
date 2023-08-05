import inspect
from importlib import import_module
from pathlib import Path
import sys


RESPONSE_OBJECTS_PY = 'response_objects.py'


class GeneralResponse:

    def __init__(self, json_data=None):
        json_data = (json_data or {}).copy()
        for name, attr_type in self.__dict__.items():
            if name not in json_data.keys():
                json_data[name] = None
            if attr_type is None:
                pass
            elif isinstance(attr_type, list) and issubclass(attr_type[0], GeneralResponse):
                try:
                    json_data[name] = [attr_type[0](x) for x in json_data[name]]
                except TypeError:
                    pass
            elif issubclass(attr_type, GeneralResponse):
                json_data[name] = attr_type(json_data[name])
        if json_data:
            self.__dict__.update(json_data)


class Formatter:

    def __init__(self, init_param_name=None, base_class=None):
        self.init_param_name = init_param_name or 'json_data'
        self.base_class = base_class or 'general response'

    @staticmethod
    def class_format(string):

        if ' ' in string or '_' in string:
            return string.title().replace(' ', '').replace('_', '')
        else:
            return string[0].upper() + string[1:]

    def class_statement(self, class_name, parent_name=None):
        parent_name = parent_name or self.base_class
        return 'class {}({}):\n\n'.format(self.class_format(class_name), self.class_format(parent_name))

    def init_statement(self):
        return '\tdef __init__(self, {}=None):\n\n'.format(self.init_param_name)

    @staticmethod
    def attribute_statement(name, var_type):
        return '\t\tself.{0} = {1}\n\t\t""":type : {1}"""\n'.format(name, var_type)

    @staticmethod
    def attribute_list_statement(name, var_type):
        return '\t\tself.{0} = [{1}]\n\t\t""":type : list[{1}]"""\n'.format(name, var_type)

    def super_statement(self):
        return '\t\tsuper().__init__({})\n\n\n'.format(self.init_param_name)

    def bass_class(self):
        class_ = inspect.getsource(GeneralResponse)\
            .replace('GeneralResponse', '{1}')\
            .replace('json_data', '{0}')\
            .replace('{}', '{{}}')
        return class_.format(self.init_param_name, self.class_format(self.base_class)) + '\n\n'


class JsonToPython:

    def __init__(self, formatter=None, file_name=RESPONSE_OBJECTS_PY):

        self.formatter = formatter or Formatter()
        self.file = Path(file_name)
        self.file_exists = self.file.exists() and self.file.stat().st_size != 0
        self.existing_subclasses = self._get_subclasses()

    def _get_subclasses(self):
        path = str(self.file.parent.resolve())
        module_name = self.file.stem

        if path not in sys.path:
            sys.path.append(path)
        try:
            module = import_module(module_name)
        except ModuleNotFoundError:
            return {}

        return self._dictionarify(module)

    @staticmethod
    def _dictionarify(module):
        big_d = {}
        module_dict = module.__dict__.copy()
        general_response = module_dict.pop(GeneralResponse.__name__)
        for key, value in module_dict.items():
            if type(value) == type and issubclass(value, general_response):
                big_d[key] = {k: v for k, v in value().__dict__.items() if not k.startswith('_')}
        return big_d

    @staticmethod
    def compare_dict_keys(dict1, dict2):
        result = True
        for key in dict1:
            result = result and (key in dict2.keys())
        return result and len(dict1) == len(dict2)

    def is_in_subclasses(self, dict1, subclasses):
        for key, entry in subclasses.items():
            if self.compare_dict_keys(dict1, entry):
                return key

    def convert(self, class_name, json_data):

        def handle_dict(key, value, is_list=False):
            nonlocal result
            formate = self.formatter.attribute_list_statement if is_list else self.formatter.attribute_statement
            if value:
                new_class_name = self.is_in_subclasses(value, self.existing_subclasses)
                if new_class_name:
                    result += formate(key, new_class_name)
                else:
                    new_class_name = self.formatter.class_format(key + ' ' + class_name)
                    subclasses[new_class_name] = value
                    self.existing_subclasses[new_class_name] = value
                    result += formate(key, new_class_name)

            else:
                result += formate(key, 'None')

        result = ''
        subclasses = {}
        result += self.formatter.class_statement(class_name)
        result += self.formatter.init_statement()
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                if value is None:
                    result += self.formatter.attribute_statement(key, 'None')
                elif isinstance(value, dict):
                    handle_dict(key, value)
                elif isinstance(value, list):
                    if not value:
                        result += self.formatter.attribute_statement(key, value.__class__.__name__)
                    elif isinstance(value[0], dict):
                        handle_dict(key, value[0], True)
                    else:
                        result += self.formatter.attribute_list_statement(key, value[0].__class__.__name__)

                else:
                    result += self.formatter.attribute_statement(key, value.__class__.__name__)
        elif isinstance(json_data, list):
            self.convert(class_name, json_data[0])
        else:
            raise ValueError('the function only works with parsed json data')

        result += self.formatter.super_statement()

        result = result.replace('\t', '    ')

        for key, entry in subclasses.items():
            result += self.convert(class_name=key, json_data=entry)

        return result

    def write_code_file(self, class_name, json_data):
        s = self.convert(class_name, json_data)
        with self.file.open('a') as f:
            if not self.file_exists:
                f.write(self.formatter.bass_class())
            f.write(s)