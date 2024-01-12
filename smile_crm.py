import sys, os, re, argparse, importlib
import time
import ast
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class Manage_options(object):
    def __init__(self):
        
        self.options_dict = {}
        
    def validate_scenario_dir(self, dir):
        if not os.path.isdir(f'{os.path.dirname(__file__)}/{dir}'):
            raise  argparse.ArgumentTypeError(f'{dir} isn\'t a directory')
        else:
            return dir       

    def build_options_dict(self, option, value):
        if option in ["headless"]:
            self.options_dict[option] = value
        if option in [
                "scenarios_dir",
                "scenario",
            ]:
            
            if len(value) > 0:
                self.options_dict[option] = value
            else:
                raise  argparse.ArgumentTypeError(\
                    f"Option {option.replace('_','-')} can not be empty string"
                ) 

class Scenario(object):
    def __init__(self, options):

        options = webdriver.ChromeOptions()
        service = webdriver.ChromeService()
        self.driver = webdriver.Chrome(service=service, options=options)

    
class Main(object):
    
    def __init__(self):
        self.manage_options = Manage_options()
    
    def __call__(self):
        parser = argparse.ArgumentParser(description="Utilisation selenium-client.py")
         
        parser.add_argument("--scenarios-dir", required=True, metavar='<directory path>',\
            help= 'ex: scenarios', type=self.manage_options.validate_scenario_dir)

        parser.add_argument("--scenario", required=True, type=str, metavar='<scenario name without .py on end>',\
            help="ex: myfirstscenario")
        
        parser.add_argument('--headless', action='store_true')
        
        args = parser.parse_args()

        for option in args.__dict__:
            value = getattr(args, option)
            if value != None:
                self.manage_options.build_options_dict(option, value)

        sys.path.append(f'{os.path.dirname(__file__)}/{self.manage_options.options_dict["scenarios_dir"]}')

        try:
            scenario = importlib.import_module(getattr(args, "scenario"))
        except ModuleNotFoundError as e:
            sys.exit(1)
            
        self.set_import_from_scenario(scenario)

        class ScenarioRunner(Scenario, scenario.ScenarioCustom):
            def __init__(self, options):
                super().__init__(options)
            def run(self):
                self.scenario_steps()
        
        scenario_instance = ScenarioRunner(self.manage_options.options_dict)
            # display.start()
        scenario_instance.run()

    def set_import(self, module,name,alias):
        setattr(
                __import__(__name__),
                alias,
                eval(
                    f'importlib.import_module("{module}").{name}'
                ),
        )
    
    def set_import_from_scenario(self, scenario):
        filename = scenario.__file__

        with open(filename, "r") as file:
            source = file.read()
            tree = ast.parse(source)

        for node in tree.body:
            if isinstance(node, ast.ImportFrom):
                for name in node.names:
                    if name.asname:
                        self.set_import(node.module, name.name, name.asname)
                    else:
                        self.set_import(node.module, name.name, name.name)

if __name__ == "__main__":
    main = Main()
    main()
