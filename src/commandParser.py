import os
import time
import json

from gtts import gTTS
from datetime import datetime

class CommandSpeeker():
	def __init__(self, speaker, json_path):
		self.speaker = speaker
		self.json_file = open(json_path, "r")
		self.command_json = json.load(self.json_file)
		self.language = self.command_json[self.speaker]['language']
		self.tts = None
		self.filename = "command.mp3"

	def _play_command_to_mp3(self, text):
		self.tts = gTTS(text, self.language)
		self.tts.save(self.filename)
		# if you don't install 'mpg123', should install by apt
		os.system("mpg123 " + self.filename)
	
	def _do_command(self, category):
		self._play_command_to_mp3(self.command_json[self.speaker]['call'])
		time.sleep(0.7)
		self._play_command_to_mp3(self.command_json[self.speaker]['command'][category])
		self.json_file.close()
	
	def start_command(self, category, write_record):
		start_time = time.time()
		try:
			self._do_command(category)
			if write_record: time.sleep(60)
		except KeyboardInterrupt:
			duration = time.time() - start_time
			if write_record: self._write_record(category, duration)
			os.remove(self.filename)
			self.json_file.close()
	
	def _write_record(self, category, duration):
		record_file = './'+datetime.today().strftime('%y%m%d')+'_test_record.csv'
		isfrist = True
		if os.path.exists(record_file): isfrist = False
		with open(record_file, 'a') as file:
			if isfrist: file.write('speeker, category, command, time\n')
			file.write(self.speaker+', '+category+', '+\
				self.command_json[self.speaker]['command'][category]+', '+\
				str(duration)+'\n')


if __name__=="__main__":
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument('-s', '--speeker',
						help='voice assistance speeker type',
						type=str,
						required=True)
	parser.add_argument('-j', '--json-path',
						help='command json file path',
						type=str,
						required=True)
	parser.add_argument('-c', '--category',
						help='kind of command category',
						type=str,
						required=True)
	parser.add_argument('-w', '--write-record',
						help='write test record',
						type=bool,
						default=False)
	ARGS = parser.parse_args()

	commandspeeker = CommandSpeeker(ARGS.speeker, ARGS.json_path)
	commandspeeker.start_command(ARGS.category, 
								ARGS.write_record)

