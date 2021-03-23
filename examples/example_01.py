#!/usr/bin/env python
"""Run a test calculation on localhost.

Usage: ./example_01.py
"""
from os import path
from aiida_adamant import helpers
from aiida import cmdline, engine
from aiida.plugins import DataFactory, CalculationFactory
import click

INPUT_DIR = path.join(path.dirname(path.realpath(__file__)), 'input_files')


def test_run(adamant_code):
    """Run a calculation on the localhost computer.

    Uses test helpers to create AiiDA Code on the fly.
    """
    if not adamant_code:
        # get code
        computer = helpers.get_computer()
        adamant_code = helpers.get_code(entry_point='adamant',
                                        computer=computer)

    # Prepare input parameters
    DiffParameters = DataFactory('adamant')
    parameters = DiffParameters({'ignore-case': True})

    SinglefileData = DataFactory('singlefile')
    file1 = SinglefileData(file=path.join(INPUT_DIR, 'file1.txt'))
    file2 = SinglefileData(file=path.join(INPUT_DIR, 'file2.txt'))

    # set up calculation
    inputs = {
        'code': adamant_code,
        'parameters': parameters,
        'file1': file1,
        'file2': file2,
        'metadata': {
            'description': "Test job submission with the aiida_adamant plugin",
        },
    }

    # Note: in order to submit your calculation to the aiida daemon, do:
    # from aiida.engine import submit
    # future = submit(CalculationFactory('adamant'), **inputs)
    result = engine.run(CalculationFactory('adamant'), **inputs)

    computed_diff = result['adamant'].get_content()
    print("Computed diff between files: \n{}".format(computed_diff))


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
def cli(code):
    """Run example.

    Example usage: $ ./example_01.py --code diff@localhost

    Alternative (creates diff@localhost-test code): $ ./example_01.py

    Help: $ ./example_01.py --help
    """
    test_run(code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter