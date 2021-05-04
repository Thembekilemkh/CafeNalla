import time

class CountDown():

	def start_CD(self, **kwargs):
		seconds = kwargs["seconds"]
		time_up = kwargs["time_up"]

		while seconds != 0:
			time.sleep(1)

			if seconds == 0:
				time_up = True
				