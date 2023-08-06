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
from typing import Optional

import pandoc_flow.const
from strome.pipeline import StromeRuntime

LOGGER = logging.getLogger("preprocessor")


class PandocFlowRuntime(StromeRuntime):
    def __init__(self, pandoc_config_path: str, pandoc_config: Optional[dict] = None) -> None:
        super().__init__(pandoc_config_path, pandoc_config, root_element_name=pandoc_flow.const.CONF_PANDOC_FLOW)
        self.pandoc_config_generated_path: Optional[str] = None
        self.context.update(
            {
                pandoc_flow.const.RUNTIME_PANDOC_META: {},
                pandoc_flow.const.RUNTIME_PANDOC_VARS: {},
            }
        )

    def register_pandoc_var(self, name: str, value: str):
        self.context[pandoc_flow.const.RUNTIME_PANDOC_VARS][name] = value

    def register_pandoc_meta(self, name: str, value: str):
        self.context[pandoc_flow.const.RUNTIME_PANDOC_META][name] = value
