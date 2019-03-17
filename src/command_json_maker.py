import json


class CommandJsonMaker():
    def __init__(self, en_command_file, ko_command_file, output_path):
        self.en_command_file = en_command_file
        self.ko_command_file = ko_command_file
        self.command_output = output_path + './commands.json'
        self.function_output = output_path + './speaker_function.json'
        self.commands_dic = {'en':{}, 'ko':{}}
        self.speakers_dic = {'alexa':{'language':'en', 'call':'Alexa', 'function':[]},
                            'googlehome':{'language':'en', 'call':'ok, google', 'function':[]},
                            'clova':{'language':'ko', 'call':'헤이 클로바', 'function':[]},
                            'kakao':{'language':'ko', 'call':'헤이 카카오', 'function':[]},
                            'nugu':{'language':'ko', 'call':'아리야', 'function':[]}}

    def make_jsons(self):
        with open(self.en_command_file, 'r') as en_command_file, \
            open(self.ko_command_file, 'r') as ko_command_file:
                en_command = en_command_file.readlines()[1:]
                ko_command = ko_command_file.readlines()[1:]
                self._make_commands_json(en_command, ko_command)
                self._make_speaker_function_json(en_command, ko_command)

    def _make_commands_json(self, en_command, ko_command):
        self._append_commands('en', en_command)
        self._append_commands('ko', ko_command)
        with open(self.command_output, 'w') as output:
            json.dump(self.commands_dic, output)
    
    def _append_commands(self, language, command_lines):
        for line in command_lines:
            line_split = line.strip().split('\t')
            function = line_split[2].strip()
            commands = [command.strip() for command in line_split[3:]]
            self.commands_dic[language][function] = commands
    
    def _make_speaker_function_json(self, en_command, ko_command):
        self._append_function(en_command)
        self._append_function(ko_command)
        with open(self.function_output, 'w') as output:
            json.dump(self.speakers_dic, output)
    
    def _append_function(self, command_lines):
        for line in command_lines:
            line_split = line.strip().split('\t')
            speakers = line_split[0].strip().split(',')
            function = line_split[2].strip()
            for speaker in speakers: self.speakers_dic[speaker]['function'].append(function)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--enfile-path',
                        help='english command file path',
                        type=str,
                        required=True)
    parser.add_argument('-k', '--kofile-path',
                        help='korean command file path',
                        type=str,
                        required=True)
    parser.add_argument('-o', '--output',
                        help='output file path',
                        type=str,
                        default='./')
    ARGS = parser.parse_args()

    # 구글 드라이브 명령어 파일을 '탭으로 구분된 값(.tsv)'로 다운 받아 각 언어별로 -k 와 -e 옵션으로 넣어서 사용
    command_json_maker = CommandJsonMaker(ARGS.enfile_path, ARGS.kofile_path, ARGS.output)
    command_json_maker.make_jsons()

    