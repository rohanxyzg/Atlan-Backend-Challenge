from threading import Thread

from rest_framework.response import Response
from rest_framework.views import APIView

from ..managers.upload import UploadManager

#global manager


class UploadStartController(APIView):
    """Controller for starting upload for a given user id."""

    def post(self, request):
        """Method to start upload of a csv file into the database.
        """
        data = request.data
        global userId
        userId = data["userid"]
        global manager
        manager = UploadManager(userId)
        thread = Thread(manager.begin())
        thread.start()

        return Response("Status : Upload Started")


class UploadPauseController(APIView):
    """Controller for pausing upload"""

    def post(self, request):
        """Method to pause upload of a csv file being uploaded into the database.
        """
        global manager
        manager.pause()
        return Response("Status : Upload Paused")


class UploadResumeController(APIView):
    """Controller for resuming upload"""

    def post(self, request):
        """Method to resume upload of a paused csv file.
        """
        global manager
        manager.resume()
        return Response("Status : Upload Resumed")


class UploadTerminateController(APIView):
    """Controller for terminating upload"""

    def post(self, request):
        """Method to terminate and rollback upload of a csv file.
        """
        global manager
        manager.terminate()
        return Response("Status : Upload Terminated")


class UploadProgressController(APIView):
    """Controller for fetching the percentage of completed upload"""

    def get(self, request):
        """Method to terminate and rollback upload of a csv file.

        """
        global manager
        completion = manager.get_progress()
        return Response(completion)


class TableExistController(APIView):
    """Controller for checking if a table exists"""

    def get(self, request, userid):
        """Method to check if a table exists
        """
        manager = UploadManager(userid)
        result = manager.table_exists()
        return Response(result)
