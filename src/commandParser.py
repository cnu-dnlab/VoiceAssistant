import os
import time
import json

from gtts import gTTS


class CommandSpeeker():
	def __init__(self, speeker):
		self.json_file = open("./"+speeker+".json", "r")
		self.speaker = json.load(self.json_file)
		self.language = self.speaker['language']
		self.tts = None
		self.filename = "command.mp3"

	def _play_command_to_mp3(self, text):
		self.tts = gTTS(text, self.language)
		self.tts.save(self.filename)
		# if you don't install 'mpg123', should install by apt
		os.system("mpg123 " + self.filename)
	
	def start_command(self, command, order_number):
		self._play_command_to_mp3(self.speaker['call'])
		time.sleep(0.7)
		self._play_command_to_mp3(self.speaker["command"][command][order_number])
		self.json_file.close()


if __name__=="__main__":
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument('-s', '--speeker',
						help='voice assistance speeker type',
						type=str,
						required=True)
	parser.add_argument('-c', '--command',
						help='kind of command',
						type=str,
						required=True)
	parser.add_argument('-o', '--order-number',
						help='command to order',
						type=int,
						default=0)
	ARGS = parser.parse_args()

	commandspeeker = CommandSpeeker(ARGS.speeker)
	commandspeeker.start_command(ARGS.command, ARGS.order_number)

