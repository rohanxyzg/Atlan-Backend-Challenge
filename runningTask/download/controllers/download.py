from threading import Thread

from rest_framework.response import Response
from rest_framework.views import APIView

from  ..managers.download import DownloadManager

global manager


class DownloadStartController(APIView):
    def post(self, request):
        """Method to start download of a csv file into the database.
        """
        data = request.data
        global userId
        userId = data["userid"]

        global manager
        manager = DownloadManager(userId)

        thread = Thread(manager.start())
        thread.start()

        return Response("Status : Download Started")


class DownloadPauseController(APIView):
    """Controller for pausing download"""

    def post(self, request):
        """Method to pause download of a csv file being uploaded into the database.
        """
        global manager
        manager.pause()
        return Response("Status : Download Paused")


class DownloadResumeController(APIView):

    def post(self, request):
        """Method to resume download of a paused csv file.
        """
        global manager
        manager.resume()
        return Response("Status : Download Resumed")


class DownloadTerminateController(APIView):
    """Controller for terminating download"""

    def post(self, request):
        """Method to terminate and rollback download of a csv file.
        """
        global manager
        manager.terminate()
        return Response("Status : Download Terminated")


class DownloadProgressController(APIView):
    """Controller for fetching the percentage of download complete"""

    def get(self, request):
        global manager
        progress = manager.get_progress()
        return Response(progress)
