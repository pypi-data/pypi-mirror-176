#!/usr/bin/env python

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

import typer
from datamodel_code_generator import LiteralType, PythonVersion, chdir
from datamodel_code_generator.format import CodeFormatter
from datamodel_code_generator.imports import Import, Imports
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.types import DataType
from jinja2 import Environment, FileSystemLoader

from fastapi_code_generator.parser import OpenAPIParser, Operation
import os
import re
os.chdir(str(Path(__file__).parent.parent))
import sys
sys.path.append(str(Path(__file__).parent.parent))
import settings
app = typer.Typer()

BUILTIN_TEMPLATE_DIR = Path(__file__).parent / "jinja"

MODEL_PATH: Path = Path("Models.py")



def _get_most_of_reference(data_type: DataType) -> Optional[Reference]:
    if data_type.reference:
        return data_type.reference
    for data_type in data_type.data_types:
        reference = _get_most_of_reference(data_type)
        if reference:
            return reference
    return None


def trimmode(input:str)->str:
    def f(matchs:Any)->str:
        return ''
    s = re.sub(r'(class DB.*?)(?=class)', f, input,0,re.DOTALL|re.MULTILINE)
    return s

def generate_code(
    apiprefix: str,
    input_text: str,
    output_dir: Path,
    controllerName:str,
    template_dir: Optional[Path],
    model_path: Optional[Path] = None,
    enum_field_as_literal: Optional[str] = None,
) -> None:
    if not model_path:
        mode_name=controllerName.replace("Controller",'Shema')
        if not mode_name.endswith('.py'):
            mode_name+='.py'
        model_path = Path(mode_name)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    if not template_dir:
        template_dir = BUILTIN_TEMPLATE_DIR
    if 1:
        parser = OpenAPIParser(input_text, enum_field_as_literal='all',field_constraints=True)
    else:
        parser = OpenAPIParser(input_text)
    with chdir(output_dir):
        Models = parser.parse()
    if not Models:
        return
    elif isinstance(Models, str):
        output = output_dir / model_path
        modules = {output: (trimmode(Models), 'tmp.txt')}

    else:
        raise Exception('Modular references are not supported in this version')

    environment: Environment = Environment(
        loader=FileSystemLoader(
            template_dir if template_dir else f"{Path(__file__).parent}/template",
            encoding="utf8",
        ),
    )
    imports = Imports()
    imports.update(parser.imports)
    for data_type in parser.data_types:
        reference = _get_most_of_reference(data_type)
        if reference:
            imports.append(data_type.all_imports)
            imports.append(
                Import.from_full_path(f'.{model_path.stem}.{reference.name}')
            )
    for from_, imports_ in parser.imports_for_fastapi.items():
        imports[from_].update(imports_)
    results: Dict[str, str] = {}
    code_formatter = CodeFormatter(PythonVersion.PY_38, Path().resolve())

    # sorted_operations: List[Operation] = sorted(
    #     parser.operations.values(), key=lambda m: m.path
    # )
    sorted_operations=parser.operations.values()


    for target in template_dir.rglob("*"):
        relative_path = target.relative_to(template_dir)
        result = environment.get_template(str(relative_path)).render(
            operations=sorted_operations, imports=imports, info=parser.parse_info(),apiprefix=apiprefix
        )
        results[controllerName] = code_formatter.format_code(result)

    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    header = f"""# generated timestamp: {timestamp}"""

    for path_tmp, code in results.items():
        path=str(path_tmp)
        realname=path if path.endswith('.py') else path + '.py'
        if output_dir.joinpath(realname).exists():
            realname=realname.replace('.py',datetime.now().strftime("%Y%m%d%H%M%S")+'.py')
        with output_dir.joinpath(realname).open("wt") as file:
            print(header, file=file)
            print("", file=file)
            print(code.rstrip(), file=file)


    header = f'#   timestamp: {timestamp}'

    for path2, body_and_filename in modules.items():
        body, filename = body_and_filename
        if path2 is None:
            file = None
        else:
            if not path2.parent.exists():
                path2.parent.mkdir(parents=True)
            if path2.exists():
                path2=Path(path2.__str__().replace('.py',datetime.now().strftime("%Y%m%d%H%M%S")+'.py'))
            file = path2.open('wt', encoding='utf8')

        print(header.format(filename=filename), file=file)
        if body:
            print('', file=file)
            newbody=body.rstrip().replace('from __future__ import annotations','from __future__ import annotations\nfrom typing import Literal\n')
            enumarr = re.findall(r'(^class (\w+)\(Enum\)(.*?)^\n)', body, re.M | re.DOTALL)
            if enumarr:
                enumdict={}
                for item in enumarr:
                    total,key,txt=item
                    values = re.findall(r'    (.*?) ', txt)
                    if values:
                        enumdict[key] =[total, "Literal[" + ','.join([v.__repr__() for v in values]) + "]"]
                for classname in enumdict:
                    newbody=newbody.replace(enumdict[classname][0], '')
                    newbody = re.sub(rf'{classname}(?!\w+)', enumdict[classname][1], newbody)


            print(newbody, file=file)
        if file is not None:
            file.close()

import json

from collections import defaultdict
import os
import copy
import sys
def mymain(content:str | bytes)->None:
    data=json.loads(content)
    paths=data["paths"]

    groups=defaultdict(dict)#type: ignore


    for item in paths:

        for method in paths[item]:
            itemdata=paths[item][method]
            if "requestBody" in itemdata:
                itemdata["requestBody"]["required"]=True
            if "parameters" in itemdata:
                itemdata["parameters"]=[tmp for tmp in itemdata["parameters"] if not (tmp['name']=='token' and tmp['in']=='header')]

            if not itemdata["parameters"]:
                del itemdata["parameters"]

            if "responses" in itemdata:
                codes=[code for code in itemdata["responses"]]
                for code in codes:
                    if code!='200':
                        del itemdata["responses"][code]
            folder=itemdata["x-apifox-folder"]
            controller=itemdata["operationId"]

            groups[(folder,controller)][item]=paths[item]

    def createdir(dirpath:Path)->None:

        if not dirpath.exists():
            if not dirpath.parent.exists():
                createdir(dirpath.parent)
            dirpath.mkdir(parents=False,exist_ok=True)

            inipath: Path = dirpath.joinpath('__init__.py')
            with inipath.open('wt', encoding='utf8') as inifile:
                prefix = '/api' + str(dirpath).replace(str(Path(settings.BASE_DIR).joinpath('modules')),'')
                prefix=prefix.replace('\\','/')
                inifile.write(
                    f"from .. import dependencies as praentdependencies\nfrom fastapi import Depends\nfrom typing import List,Callable,Any\ndependencies:List[Callable[...,Any]]=praentdependencies+[]")

        else:
            pass
    for folder,controllerName in groups:
        deepdir=Path(settings.BASE_DIR).joinpath('modules',folder)
        APIPREFIX=''
        createdir(deepdir)


        newdata=copy.deepcopy(data)
        newdata["paths"]=groups[(folder,controllerName)]
        generate_code(APIPREFIX, json.dumps(newdata), Path(settings.BASE_DIR).joinpath('modules',folder), controllerName,template_dir=Path(__file__).parent / "jinja")
if __name__ == "__main__":
    content=open(sys.argv[1],'r',encoding='utf8').read()
    mymain(content)
        # if not os.path.exists(os.path.join(settings.BASE_DIR,folder,controllerName+'.py')):
        #     print('make dir')
        #     os.makedirs(os.path.join(settings.BASE_DIR,folder,controllerName+'.py'),exist_ok=True)

    #generate_code('33.json',tt, Path(__file__).parent,template_dir=None)
