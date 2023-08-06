import click
import examples as inq_examples
import logging
import os
import pydoni
import pydoni
import PyInquirer as inq
import subprocess
import termtables as tt
import yaml
from .cli_main import cli as module_cli
from clint.textui import colored
from collections import OrderedDict
from itertools import chain
from pyfiglet import Figlet


logger = pydoni.logger_setup(name='pydonicliapp', level=logging.WARN)


def app_logger_setup(input_args_dict):
    """
    Define logger object depending on which commandline arguments are passed
    into the program. Commandline arguments may affect the flow of logging
    messages, as well as the logging level.
    """

    logger = logging.getLogger(__name__)
    logger_fmt = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
    formatter = logging.Formatter(logger_fmt)

    if isinstance(input_args_dict['logfile'], str):
        handler = logging.FileHandler(input_args_dict['logfile'])
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Set logger level. If debug flag was passed into commandline call,
    # set logger to DEBUG level. Otherwise, set to INFO level.
    if input_args_dict['debug']:
        logger.setLevel(logging.DEBUG)
    elif input_args_dict['verbose']:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    return logger


def failed_assertion(obj, objname, objdesiredtype):
    """
    Print informative message in `assert` statement.
    """
    return "Variable '{}' is of type '{}' and should be '{}', value: {}".format(
        objname, type(obj).__name__, objdesiredtype.__name__, str(obj))


class AppParameter(object):
    """
    Store information and modify app parameter data.
    """

    def __init__(self, name, dtype, default, required, multiple, override, ordinal_rank):
        """
        name: parameter name as string
        dtype: dtype of parameter as string
        default: default value of parameter
        required: boolean flag
        override: value found in override params YAML file to override `default`
        ordinal_rank: integer indicating priority, 1 = highest, 4 = lowest
        """
        assert isinstance(name, str), failed_assertion(name, 'name', str)
        assert isinstance(required, bool), failed_assertion(required, 'required', bool)
        assert isinstance(ordinal_rank, int), failed_assertion(ordinal_rank, 'ordinal_rank', int)

        # Attributes required on initialization
        self.name = name
        self.dtype = dtype
        self.default = default
        self.required = required
        self.multiple = multiple
        self.override = override
        self.ordinal_rank = ordinal_rank

        # Attributes calculated on initialization
        self.dtype_str = self.convert_click_type_to_string(click_type=self.dtype)
        self.final_value = self.override if self.override is not None else self.default
        self.good_to_go = self.is_good_to_go()

    def convert_click_type_to_string(self, click_type):
        """
        Translate raw click parameter type to a printable, human-readable string. For
        example, a click.option() type of `click.Path()` will be mapped to 'path'.
        'STRING' is mapped to 'string', and so on.
        """
        if isinstance(click_type, click.Tuple):
            return str(click_type.types).lower().replace('[', '').replace(']', '')

        elif isinstance(click_type, click.Path):
            exists = click_type.exists
            if exists:
                return click_type.name + ' exists'
            else:
                return click_type.name

        else:
            return str(click_type).lower()

    def is_good_to_go(self):
        """
        Is the parameter set for use, or must it be modified first? Return boolean flag.
        """
        if self.required is True and self.final_value is None:
            return False
        else:
            return True


class AppNavigation(object):
    """
    Handle navigating around the main screens of the app.
    """

    def __init__(self):
        pass

    def homepage(self, figlet=True):

        os.system('clear')
        logger.info('Cleared STDOUT')
        logger.info('Initializing Pydoni CLI')

        if figlet:
            self.print_figlet()

    def print_figlet(self):
        """
        Print app figlet header to console.
        """
        fig = Figlet(font='slant')
        pydoni.echo('----------------------- Welcome to ------------------------')
        print(colored.red(fig.renderText('pydoni-CLI')))
        pydoni.echo('')


class AppInput(object):
    """
    Handle prompting the user for input at any stage of application.
    """

    def __init__(self):
        pass

    def get_major_appcmds(self):
        """
        Retrieve a dictionary of major command names and objects.
        """
        return {k: v for k, v in module_cli.cli.commands.items() if k != 'app'}

    def get_minor_appcmds(self, major):
        """
        Given a major app command name, retrieve a dictionary of minor command names and objects.
        """
        major_appcmds = self.get_major_appcmds()
        selected_major = major_appcmds[major]
        return {k: v for k, v in selected_major.commands.items()}

    def prompt_major_appcmds(self):
        """
        Prompt user to select a major app command to run.
        """
        appcmd_names = [k for k, v in self.get_major_appcmds().items()]
        return pydoni.user_select_from_list_inq(appcmd_names, msg='Select a major app command')

    def prompt_minor_appcmds(self, major):
        """
        Prompt user to select a minor app command to run.
        """
        appcmd_names = [k for k, v in self.get_minor_appcmds(major).items()]
        return pydoni.user_select_from_list_inq(appcmd_names, msg='Select a minor app command')

    def read_override_params(self, app_overrides_file):
        """
        Read 'app_param_overrides.yaml' if is exists as dictionary.
        """
        if os.path.isfile(app_overrides_file):
            with open(app_overrides_file, 'r') as f:
                defaults = yaml.safe_load(f)

            return defaults
        else:
            logger.warning(f'App override parameters file not found, expected at "{app_overrides_file}"')
            return {}

    def print_paramers_ascii_table(self, major, minor, appcmd_params_dict, char_limit=None):
        """
        Print ascii parameters as a termtable to the console.
        """
        def colorize_click_type_string(click_type_string):
            """
            Receive output from `convert_click_type_to_string()` and assign the appropriate
            color for printing to console.
            """

            possible_types = ['path exists', 'path', 'string', 'int', 'float', 'bool']
            color_names = ['magenta', 'green', 'yellow', 'blue', 'bright_blue', 'cyan']

            for name, color in zip(possible_types, color_names):
                if name in click_type_string:
                    return color

            return 'white'

        print_lst = []
        for i, param in appcmd_params_dict.items():
            param_type = ', '.join(pydoni.ensurelist(param.dtype_str))
            param_val = str(param.final_value)
            param_val = '\\x08' if param_val == '\x08' else param_val
            param_color = colorize_click_type_string(param_type)
            param_type = click.style(param_type, fg=param_color)
            param_val = click.style(str(param_val), fg='red') if param_val == 'None' else param_val

            if char_limit and isinstance(param_val, str):
                if len(param_val) > char_limit:
                    if 'path' in param_type:
                        # Take final `char_limit` chars instead of first
                        param_val = '...' + param_val[-int(char_limit):]
                    else:
                        param_val = param_val[0:char_limit] + '...'

            print_lst.append([param.name, param_type, param_val])

        if len(print_lst):
            print(f'\nDefault parameter values for command: {click.style(major + "." + minor, underline=True)}\n')

            param_table = tt.to_string(
                print_lst,
                header=[click.style(x, bold=True) for x in ['Parameter', 'Datatype', 'Default Value']],
                style=tt.styles.ascii_thin_double,
                padding=(0, 1),
                alignment='ccr')

            print(param_table + '\n')

    def select_appcmd(self, major, minor):
        """
        From the homepage, ensure that a valid app command is selected, or, if no command
        was selected using the --major and --minor options, prompt user for a selection
        and return that app command name.
        """
        if major is None or minor is None:
            major = AppInput().prompt_major_appcmds()
            minor = AppInput().prompt_minor_appcmds(major)
            return major, minor
        else:
            valid_app_cmds_major = [k for k, v in AppInput().get_major_appcmds().items()]
            valid_app_cmds_minor = [k for k, v in AppInput().get_minor_appcmds(major).items()]

            assert major in valid_app_cmds_major, \
                f"'{major} is not a valid major app command! Must be one of: {valid_app_cmds_major}"

            assert minor in valid_app_cmds_minor, \
                f"'{minor} is not a valid minor app command! Must be one of: {valid_app_cmds_minor}"

            return major, minor

    def extract_parameter_objects(self, major, minor, override_params):
        """
        Extract and order parameters from click.command object.
        """
        appcmd_obj = [v for k, v in AppInput().get_minor_appcmds(major).items() if k == minor][0]
        param_obj_list = appcmd_obj.params

        appcmd_params_list = []
        for param_obj in param_obj_list:
            pdata = dict(name=None, default=None, type=None, required=None, override=None)
            easy_extract = ['name', 'default', 'type', 'required', 'multiple']
            for attr in easy_extract:
                pdata[attr] = getattr(param_obj, attr)

            if pdata['name'].replace('_', '-') in override_params.keys():
                pdata['override'] = override_params[pdata['name'].replace('_', '-')]

            # Ranking (1=highest): override nonflags, override flags, nonoverride nonflags, nonoverride flags
            # However, a rank of 0 is possible if the parameter is not 'good_to_go' This is designed
            # so that parameters that require user input are placed on top. Then the normal
            # ordinal ranking will take over from there.
            if pdata['override'] is not None:
                # Priority 1 or 2
                pdata['ordinal_rank'] = 1 if pdata['type'] != click.BOOL else 2
            else:
                # Priority 3 or 4
                pdata['ordinal_rank'] = 3 if pdata['type'] != click.BOOL else 4

            pdata = pydoni.rename_dict_keys(pdata, key_dict={'type': 'dtype'})
            pydonicli_param = AppParameter(**pdata)
            appcmd_params_list.append(pydonicli_param)

        # Crystallize the order of the application parameters
        appcmd_params_list = sorted(appcmd_params_list, key=lambda x: x.ordinal_rank)
        appcmd_params_dict = OrderedDict({i: item for i, item in enumerate(appcmd_params_list)})

        # Now organize parameters that are not 'good to go' on top
        ind_gtg = OrderedDict({i: p.good_to_go for i, p in appcmd_params_dict.items()})
        if not all([x for i, x in ind_gtg.items()]):
            not_gtg = [i for i, gtg in ind_gtg.items() if gtg is False]
            d1 = OrderedDict({k: v for k, v in appcmd_params_dict.items() if k in not_gtg})
            d2 = OrderedDict({k: v for k, v in appcmd_params_dict.items() if k not in not_gtg})
            appcmd_params_dict = OrderedDict(chain.from_iterable(d.items() for d in (d1, d2)))

        return appcmd_params_dict

    def prompt_user_fill_out_param_values(self, appcmd_params_dict):
        """
        Prompt user for parameter values that are not currently filled out. Return
        completed dictionary of app parameters.
        """
        choices = []
        for i, param in appcmd_params_dict.items():
            choices.append({'name': param.name, 'checked': not param.good_to_go})

        if len(choices):
            questions = [{
                'type': 'checkbox',
                'message': "Select parameter(s) to edit (hit 'enter' to proceed)",
                'name': 'edit_param_names',
                'choices': choices}]

            edit_param_names = inq.prompt(questions, style=inq_examples.custom_style_2)['edit_param_names']

            for pname in edit_param_names:
                pidx = [i for i, p in appcmd_params_dict.items() if p.name == pname][0]
                necessary_dtype = appcmd_params_dict[pidx].dtype_str
                value = pydoni.get_input("Enter value for '{}' {{{}}}".format(pname, necessary_dtype))
                testval = pydoni.test_value(value, dtype=necessary_dtype)

                while not testval:
                    value = pydoni.get_input('Incorrect datatype! Please re-enter')
                    testval = pydoni.test_value(value, dtype=necessary_dtype)

                coerced_val = pydoni.test_value(value, dtype=necessary_dtype, return_coerced_value=True)

                appcmd_params_dict[pidx].final_value = coerced_val
                appcmd_params_dict[pidx].good_to_go = True

        return appcmd_params_dict

    def build_commandline_call(self, major, minor, appcmd_params_dict):
        """
        Iterate over app parameters and build commandline call to execute.
        """
        cmd_list = ['doni', major, minor]
        for i, param in appcmd_params_dict.items():
            opt = '--' + param.name.replace('_', '-')
            if param.final_value is not None:
                if isinstance(param.final_value, bool):
                    if param.final_value is True:
                        cmd_list += [opt]

                elif param.multiple:
                    for item in param.final_value:
                        cmd_list += [opt]
                        cmd_list += [item]

                else:
                    cmd_list += [opt]
                    cmd_list += [param.final_value]

        return cmd_list


@click.option('--major', type=str, required=False, default=None,
              help='Optionally enter the name of the major command to run (photo, imessage, image, etc.)')
@click.option('--minor', type=str, required=False, default=None,
              help='Optionally enter the name of the minor (specific) command to run')
@click.option('-l', '--logfile', type=click.Path(exists=False), required=False, default=None,
              help='Direct output logging to a local file.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Log all app code actions to console with a timestamp.')
@click.option('--dry-run', is_flag=True, default=False,
              help='Do not execute any selected program code or log to SQL database.')
@click.option('--debug', is_flag=True, default=False,
              help='Set logging level to DEBUG.')

@click.command()
def app(major, minor, verbose, dry_run, debug, logfile):
    """
    Run Pydoni CLI application!
    """
    input_args_dict = locals()

    global logger
    logger = app_logger_setup(input_args_dict)

    AppNavigation().homepage()
    major, minor = AppInput().select_appcmd(major, minor)

    # Read override parameters and filter for selected app command
    app_overrides_file = os.path.join(os.path.dirname(__file__), 'cli', 'app_default_param_values.yaml')
    override_params = AppInput().read_override_params(app_overrides_file)
    override_key_string = major + ' ' + minor  # If overrides are specified, the key is in format "major minor"
    override_params = OrderedDict(override_params[override_key_string]) if override_key_string in override_params.keys() else OrderedDict()

    # Extract and override app command parameter objects (arguments passed into actual click command)
    appcmd_params_dict = AppInput().extract_parameter_objects(major, minor, override_params)

    # Now prompt user for parameters. Not 'good to go' parameters are on top, and will be
    # checked by default. All other parameters will be unchecked by default.
    AppInput().print_paramers_ascii_table(major, minor, appcmd_params_dict, char_limit=40)
    appcmd_params_dict = AppInput().prompt_user_fill_out_param_values(appcmd_params_dict)

    # Now `appcmd_params_dict` is finalized, and ready to build command string
    cmd_list = AppInput().build_commandline_call(major, minor, appcmd_params_dict)

    subprocess.call([str(x) for x in cmd_list], shell=False)
