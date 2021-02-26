import os

# package opencv-python!
import cv2


class camera():
	def __init__(self):
		# setup environment

		self.root_dir = os.getcwd()
		self.result_dir = os.path.join(self.root_dir, 'result')
		if not os.path.isdir(self.result_dir):
			os.mkdir(self.result_dir)
		self.counterSave = 0
		self.option = 'CV_LOAD_IMAGE_COLOR'

	def set_video_env(*, object=None, frame=None, option='c'):
		# set properties
		# set the resolution
		object.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		object.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

		return object

	def capture(self):
		# create object for capturing images
		cameraVideoObject = cv2.VideoCapture(0)
		# cameraVideoObject=cv2.VideoCapture(cv2.CAP_FFMPEG)

		if not (cameraVideoObject.isOpened()):
			print('Could not open video device')
		else:
			print('video device opened')

		while True:
			# create instance
			# check, frame = cameraVideoObject.read(cv2.IMREAD_GRAYSCALE	)
			check, frame = cameraVideoObject.read(cv2.IMREAD_GRAYSCALE)

			if check == True:
				if self.option == 'grey':
					grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
					frame = grey
				else:
					pass

				cv2.imshow('Captering', frame)

				read_key = cv2.waitKey(1)
				if read_key == ord('q'):
					break
				if read_key == ord('s'):
					self.counterSave += 1
					file = os.path.join(self.result_dir, 'capture_{}_.png'.format(self.counterSave))
					cv2.imwrite(filename=file, img=frame)
					print('Wrote successful {}'.format(file))

				if read_key == ord('g'):
					self.option = 'grey'
				if read_key == ord('c'):
					self.option = 'colour'

			else:
				break

			camera.set_video_env(object=cameraVideoObject, frame=frame)

		# release instance for capturing images
		cameraVideoObject.release()
		cv2.destroyAllWindows()


env = camera()
env.capture()
