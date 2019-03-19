import os
import time
import json

from gtts import gTTS
from datetime import datetime

class CommandSpeaker():
	def __init__(self, speaker, speaker_json_path, command_json_path):
		self.speaker = speaker
		self.language, self.call, self.functions = self._read_speeker_json(speaker_json_path)
		self.commands = self._read_command_json(command_json_path)
		self.tts = None
		self.filename = "command.mp3"
	
	def _read_speeker_json(self, speaker_json_path):
		with  open(speaker_json_path, 'r') as speaker_json_file:
			speaker_json = json.load(speaker_json_file)
			language = speaker_json[self.speaker]['language']
			call = speaker_json[self.speaker]['call']
			functions = speaker_json[self.speaker]['function']
		return (language, call, functions)

	def _read_command_json(self, command_json_path):
		with open(command_json_path, 'r') as command_json_file:
			command_json = json.load(command_json_file)
			commands = command_json[self.language]
		return commands

	def _play_command_to_mp3(self, text):
		self.tts = gTTS(text, self.language)
		self.tts.save(self.filename)
		# if you don't install 'mpg123', should install by apt
		os.system("mpg123 " + self.filename)
	
	def _do_command(self, category):
		self._play_command_to_mp3(self.call)
		time.sleep(1) # for noise check
		for command in self.commands[category]:
			if command=='call' : 
				self._play_command_to_mp3(self.call)
			elif command.split(' ')[0]=='delay': 
				time.sleep(int(command.split(' ')[1]))
			else: 
				self._play_command_to_mp3(command)
			time.sleep(1)
	
	def start_command(self, category, write_record):
		start_time = time.time()
		try:
			self._do_command(category)
			if write_record: time.sleep(30)
		except KeyboardInterrupt:
			duration = time.time() - start_time
			if write_record: self._write_record(category, duration)
			os.remove(self.filename)
	
	def _write_record(self, category, duration):
		record_file = './'+datetime.today().strftime('%y%m%d')+'_test_record.csv'
		isfrist = True
		if os.path.exists(record_file): isfrist = False
		with open(record_file, 'a') as file:
			if isfrist: file.write('speaker\tcategory\ttime\n')
			file.write(self.speaker+'\t'+category+'\t'+str(duration)+'\n')


if __name__=="__main__":
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument('-s', '--speaker',
						help='voice assistance speaker type',
						type=str,
						required=True)
	parser.add_argument('-j', '--json-path',
						help='the path of json file has speaker information',
						type=str,
						required=True)
	parser.add_argument('-c', '--command-json-path',
						help="the path of json file has commands",
						type=str,
						required=True)
	parser.add_argument('-f', '--function',
						help='kind of command function',
						type=str,
						required=True)
	parser.add_argument('-w', '--write-record',
						help='write test record',
						type=bool,
						default=False)
	ARGS = parser.parse_args()

	commandspeaker = CommandSpeaker(ARGS.speaker, ARGS.json_path, ARGS.command_json_path)
	commandspeaker.start_command(ARGS.function, ARGS.write_record)

