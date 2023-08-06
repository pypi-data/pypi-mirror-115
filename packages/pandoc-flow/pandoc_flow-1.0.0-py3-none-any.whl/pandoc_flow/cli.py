#!/bin/env python

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

import argparse

from cli_rack import CLI, ansi, stats
from pandoc_flow.__version__ import __version__ as VERSION
from pandoc_flow.core import read_config_yaml
from pandoc_flow.processors.jinja2 import Jinja2Processor
from pandoc_flow.processors.pandoc import PandocProcessor
from strome import const
from strome import processors
from strome.core import setup_pipeline, load_libs, load_context_path, preload_modules, run_pipeline

arg_parser = argparse.ArgumentParser("pandoc_jinja2")
arg_parser.add_argument("config_file", type=str, action="store")

processors.REGISTRY.register(Jinja2Processor)
processors.REGISTRY.register(PandocProcessor)


def main():
    CLI.setup()
    CLI.debug_mode()
    CLI.print_info("\nPandoc-Flow version {}\n".format(VERSION), ansi.Mod.BOLD)
    args = arg_parser.parse_args()
    # return run_filter(action, prepare=prepare, doc=doc)
    CLI.print_info("Launching pipeline")
    try:
        app_timer = stats.ExecutionTimer()
        flow_runtime = read_config_yaml(args.config_file)
        if not flow_runtime.is_configured:
            raise ValueError("Pandoc flow is not configured")
        # Load libs and setup context path
        load_libs(flow_runtime)
        load_context_path(flow_runtime)
        # Setup pipeline
        preload_modules(flow_runtime)
        pipeline = setup_pipeline(flow_runtime.flow_config.get(const.CONF_PIPELINE, []), flow_runtime)
        run_pipeline(pipeline, flow_runtime)
        app_timer.stop()
        CLI.print_info("Pipeline finished execution in {} seconds".format(app_timer.format_elapsed()))
    except Exception as e:
        CLI.print_error(e)


if __name__ == "__main__":
    main()
