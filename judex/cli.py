from judex.audit import CodebaseAuditor
from judex.arg_parser import build_parser

import importlib
import sys
import pkgutil
from judex.strategies.base import AuditStrategy
from judex.engines.base import LLMEngine


def listStrategies():
    strategies = []

    import judex.strategies

    for finder, name, ispkg in pkgutil.iter_modules(judex.strategies.__path__):
        full_module_name = f"{judex.strategies.__name__}.{name}"
        module = importlib.import_module(full_module_name)

        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if (
                isinstance(attribute, type)
                and issubclass(attribute, AuditStrategy)
                and attribute is not AuditStrategy
            ):
                strategies.append(attribute)

    return strategies


def listEngines():
    engines = []

    import judex.engines

    for finder, name, ispkg in pkgutil.iter_modules(judex.engines.__path__):
        full_module_name = f"{judex.engines.__name__}.{name}"
        module = importlib.import_module(full_module_name)

        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if (
                isinstance(attribute, type)
                and issubclass(attribute, LLMEngine)
                and attribute is not LLMEngine
            ):
                engines.append(attribute)

    return engines


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    actual_args = argv if argv is not None else sys.argv[1:]
    total_args_passed = len(actual_args)

    has_strategy_flag = "-s" in actual_args or "--strategy" in actual_args
    has_engine_flag = "-e" in actual_args or "--engine" in actual_args

    if args.list and has_strategy_flag and total_args_passed == 2:
        strategies = listStrategies()
        print("\nAvailable Strategies:")
        for strategy in strategies:
            print(f" - {strategy.__name__}")
        return 0

    elif args.list and has_engine_flag and total_args_passed == 2:
        engines = listEngines()
        print("\nAvailable Engines:")
        for engine in engines:
            print(f" - {engine.__name__}")
        return 0

    engine: LLMEngine = None
    strategy: AuditStrategy = None

    for eng in listEngines():
        if eng.__name__ == args.engine:
            engine = eng(model_name=args.model)
            break

    for stg in listStrategies():
        if stg.__name__ == args.strategy:
            strategy = stg()
            break

    if not engine:
        print(f"{args.engine} not available!")
        exit()

    if not strategy:
        print(f"{args.strategy} not available!")
        exit()

    auditor = CodebaseAuditor(engine, strategy, output_name=args.output_name)
    return auditor.execute(args.target_path)
