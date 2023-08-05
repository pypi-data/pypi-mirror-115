import abc
import argparse
import json
from typing import Union, Dict, Any, List

import sys
from dataclasses import dataclass

from opentrons.hardware_control.emulation.settings import SmoothieSettings, \
    PipetteSettings, Settings
from opentrons.hardware_control.g_code_parsing.errors import UnparsableCLICommandError
from opentrons.hardware_control.g_code_parsing.g_code_differ import GCodeDiffer
from opentrons.hardware_control.g_code_parsing.g_code_program.supported_text_modes \
    import SupportedTextModes
from opentrons.hardware_control.g_code_parsing.protocol_runner import ProtocolRunner


class CLICommand(abc.ABC):
    """ABC which all CLI command classes should inherit from"""

    @abc.abstractmethod
    def execute(self) -> str:
        """Method execute the actual functionality of the command"""
        ...


@dataclass
class RunCommand(CLICommand):
    """The "run" command of the CLI."""
    protocol_file_path: str
    text_mode: str
    left_pipette_config: PipetteSettings
    right_pipette_config: PipetteSettings
    host: str = '0.0.0.0'

    def execute(self) -> str:
        """
        Loads pipette settings into emulator and runs the protocol against emulation.
        :return: Text explanation of G-Code program ran
        """
        smoothie_settings = SmoothieSettings(
            left=self.left_pipette_config,
            right=self.right_pipette_config
        )
        settings = Settings(
            smoothie=smoothie_settings,
            host=self.host
        )
        with ProtocolRunner(settings).run_protocol(self.protocol_file_path) as program:
            return program.get_text_explanation(self.text_mode)


@dataclass
class DiffCommand(CLICommand):
    """The "diff" command of the CLI"""
    file_path_1: str
    file_path_2: str

    def execute(self) -> str:
        """
        Opens both files and compares them to each other.
        :return: HTML encoded diff of files
        """
        with \
                open(self.file_path_1, 'r') as file_1, \
                open(self.file_path_2, 'r') as file_2:
            file_1_text = '\n'.join(file_1.readlines())
            file_2_text = '\n'.join(file_2.readlines())
            return GCodeDiffer(file_1_text, file_2_text).get_html_diff()


class GCodeCLI:
    """
    CLI for G-Code Parser.
    Takes input from command line, parses it and performs any post-processing.
    The provides run_command method to run passed input.
    """
    COMMAND_KEY = 'command'

    RUN_PROTOCOL_COMMAND = 'run'
    PROTOCOL_FILE_PATH_KEY = 'protocol_file_path'
    TEXT_MODE_KEY_NAME = 'text_mode'
    LEFT_PIPETTE_KEY_NAME = 'left_pipette'
    RIGHT_PIPETTE_KEY_NAME = 'right_pipette'

    DIFF_FILES_COMMAND = 'diff'
    FILE_PATH_1_KEY = 'file_path_1'
    FILE_PATH_2_KEY = 'file_path_2'
    DEFAULT_PIPETTE_CONFIG = SmoothieSettings()

    @classmethod
    def parse_args(cls, args: List[str]) -> Dict[str, Any]:
        """
        Parse args from arg list. This list is the command split on spaces
        For instance, running the command

        python cli.py run  --text-mode Concise  \
        --left-pipette '{"model": "p20_single_v2.0", "id": "P20SV202020070101"}' \
        $DATA_DIR/g_code_validation_protocols/smoothie_protocol.py

        will be split into:
        [
            'run',
            '--text-mode',
            'Concise',
            '--left-pipette',
            '{"model": "p20_single_v2.0", "id": "P20SV202020070101"}',
             '$DATA_DIR/g_code_validation_protocols/smoothie_protocol.py'
        ]
        """
        parsed_dict = vars(cls.parser().parse_args(args))
        return cls._post_process_args(parsed_dict)

    @classmethod
    def to_command(
            cls, processed_args
    ) -> CLICommand:
        """
        Parse passed arguments to a cli command class
        :param processed_args: Arguments that have been ran through both the
        parser and post-processor
        :return: Command class that inherits from CLICommand
        """
        passed_command_name = processed_args[cls.COMMAND_KEY]
        command: Union[RunCommand, DiffCommand]
        if cls.RUN_PROTOCOL_COMMAND == passed_command_name:
            command = RunCommand(
                protocol_file_path=processed_args[cls.PROTOCOL_FILE_PATH_KEY],
                text_mode=processed_args[cls.TEXT_MODE_KEY_NAME],
                left_pipette_config=processed_args[cls.LEFT_PIPETTE_KEY_NAME],
                right_pipette_config=processed_args[cls.RIGHT_PIPETTE_KEY_NAME]
            )
        elif cls.DIFF_FILES_COMMAND == passed_command_name:
            command = DiffCommand(
                file_path_1=processed_args[cls.FILE_PATH_1_KEY],
                file_path_2=processed_args[cls.FILE_PATH_2_KEY],
            )
        else:
            raise UnparsableCLICommandError(
                passed_command_name, [cls.RUN_PROTOCOL_COMMAND, cls.DIFF_FILES_COMMAND]
            )
        return command

    def __init__(self):
        self._args = self.parse_args(sys.argv[1:])

    @classmethod
    def _post_process_args(cls, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Method to run any post-processing on passed args
        :param args: Parsed arg dict
        :return:
        """
        if cls.LEFT_PIPETTE_KEY_NAME in args:
            left = PipetteSettings(**json.loads(args[cls.LEFT_PIPETTE_KEY_NAME]))
            args[cls.LEFT_PIPETTE_KEY_NAME] = left

        if cls.RIGHT_PIPETTE_KEY_NAME in args:
            right = PipetteSettings(**json.loads(args[cls.RIGHT_PIPETTE_KEY_NAME]))
            args[cls.RIGHT_PIPETTE_KEY_NAME] = right

        return args

    @classmethod
    def parser(cls) -> argparse.ArgumentParser:
        """
        Method to generate argparse ArgumentParser class for parsing command line
        input
        :return: Parser object
        """
        parser = argparse.ArgumentParser(
            description='CLI for G-Code Parser'
        )
        subparsers = parser.add_subparsers(
            title='Supported commands',
            dest=cls.COMMAND_KEY,
            required=True,
            metavar=f'{cls.RUN_PROTOCOL_COMMAND} | {cls.DIFF_FILES_COMMAND}'

        )

        run_parser = subparsers.add_parser(
            cls.RUN_PROTOCOL_COMMAND,
            help='Run a protocol against emulation',
            formatter_class=argparse.RawTextHelpFormatter

        )
        run_parser.add_argument(
            'protocol_file_path',
            type=str,
            help='Path to protocol you want to run'
        )
        run_parser.add_argument(
            '--text-mode',
            type=str,
            default=SupportedTextModes.CONCISE.value,
            choices=SupportedTextModes.get_valid_modes(),
            dest=cls.TEXT_MODE_KEY_NAME,
            help=f'{SupportedTextModes.DEFAULT.value}: Verbose output containing '
                 f'G-Code, Explanation, and Response'
                 f'\n{SupportedTextModes.CONCISE.value}: Same as default but all '
                 f'newlines, tabs, and headers removed'
                 f'\n{SupportedTextModes.G_CODE.value}: Only raw G-Code and raw '
                 f'response\n',
            metavar=' | '.join(SupportedTextModes.get_valid_modes())
        )
        run_parser.add_argument(
            '--left-pipette',
            type=str,
            default=json.dumps(SmoothieSettings().left.__dict__),
            help='Configuration for left pipette. Expects JSON string.'
                 f'\nDefaults to "{SmoothieSettings().left.model}" if not specified.'
                 '\nExample: {"model": "p20_multi_v2.0", "id": "P3HMV202020041605"}',
            metavar='left_pipette_config'
        )
        run_parser.add_argument(
            '--right-pipette',
            type=str,
            default=json.dumps(SmoothieSettings().right.__dict__),
            help='Configuration for right pipette. Expects JSON string.'
                 f'\nDefaults to "{SmoothieSettings().right.model}" if not specified.'
                 '\nExample: {"model": "p20_single_v2.0", "id": "P20SV202020070101"}',
            metavar='right_pipette_config'
        )

        diff_parser = subparsers.add_parser(
            cls.DIFF_FILES_COMMAND, help='Diff 2 G-Code files'
        )
        diff_parser.add_argument(
            cls.FILE_PATH_1_KEY, type=str, help='Path to first file'
        )
        diff_parser.add_argument(
            cls.FILE_PATH_2_KEY, type=str, help='Path to second file'
        )

        return parser

    def run_command(self):
        """
        Method to run passed command line command
        :return: Output of command
        """
        return self.to_command(self._args).execute()


if __name__ == '__main__':
    cli = GCodeCLI()
    print(cli.run_command())
