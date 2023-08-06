#    Pandoc Flow - Augments Pandoc with advanced pre-processing, automates routine
#    Copyright (C) 2021 Dmitry Berezovsky
#    The MIT License (MIT)
#
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
from typing import Any, Dict

from strome import const
from strome.core import process_strome_config
from strome.utils import yaml_file_to_dict, deepmerge_dict
from .pipeline import PandocFlowRuntime

LOGGER = logging.getLogger("core")


def read_config_yaml(yaml_file: str) -> PandocFlowRuntime:
    yaml_dict = yaml_file_to_dict(yaml_file)
    LOGGER.debug("Loaded pandoc config {} ".format(yaml_file))
    # loading dependencies
    if const.CONF_DEFAULTS in yaml_dict:
        defaults = yaml_dict[const.CONF_DEFAULTS]
        LOGGER.debug("Processing referenced yaml configs (pandoc defauls)")
        if isinstance(defaults, str):
            defaults = [defaults]
        referenced_config: Dict[str, Any] = {}
        for file_path in defaults:
            LOGGER.debug("\t\t{}".format(file_path))
            included_dict = yaml_file_to_dict(file_path)
            referenced_config = deepmerge_dict(included_dict, referenced_config, merge_lists=True)
        yaml_dict = deepmerge_dict(referenced_config, yaml_dict, merge_lists=True)
    flow_runtime = PandocFlowRuntime(yaml_file, yaml_dict)
    LOGGER.info("Loaded pandoc config {} with all dependencies".format(yaml_file))

    if flow_runtime.root_config_element in yaml_dict:
        process_strome_config(yaml_dict, flow_runtime)
    flow_runtime.init()
    return flow_runtime
