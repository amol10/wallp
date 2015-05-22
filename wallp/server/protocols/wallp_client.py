from time import time, sleep

from .blocking_fixed_length_message import BlockingFixedLengthMessage
from ..proto.server_pb2 import Response
from ..proto.client_pb2 import Request


class ImageNone(Exception):
	pass


class ImageChanging(Exception):
	pass


class ImageAbort(Exception):
	pass


class WallpClient(BlockingFixedLengthMessage):

	def __init__(self):
		BlockingFixedLengthMessage.__init__(self)


	def get_frequency(self):
		self.send_request(Request.FREQUENCY)
		response = self.recv_response()

		return response.frequency.value


	def get_last_change(self):
		self.send_request(Request.LAST_CHANGE)
		response = self.recv_response()

		return response.frequency.value


	def get_image(self):
		self.send_request(Request.IMAGE)
		response = self.recv_response()

		if response.type == Response.NONE:
			raise ImageNone()
		if response.type == Response.CHANGING:
			raise ImageChanging()

		image_info = response.image_info
		yield image_info.extension, image_info.length, image_info.chunk_count

		chunk_count = image_info.chunk_count
		while chunk_count > 0:
			response = self.recv_response()

			if response.type == Response.IMAGE_CHUNK:
				yield response.image_chunk.data
			elif response.type == Response.IMAGE_ABORT:
				raise ImageAbort()

			chunk_count -= 1


	def send_request(self, request_type):
		request = Request()
		request.type = request_type

		self.sendMessage(request.SerializeToString())


	def recv_response(self):
		message = self.receiveMessage()

		response = Response()
		response.ParseFromString(message)

		return response
