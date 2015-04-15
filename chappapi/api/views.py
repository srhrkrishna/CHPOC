from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework import views, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import zlib
import base64

class VideoView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        video_file = open('/home/ubuntu/files/test.mp4', 'rb')
        response = HttpResponse(FileWrapper(video_file), content_type='application/video')
        response['Content-Disposition'] = 'attachment; filename="%s"' % 'test1.mp4'
        return response


# class VideoUpload(views.APIView):
#     permission_classes = [FileUploadParser, ]
#
#     def put(self, request):
#         new_video = Video(fileData=self.data['file'])
#         new_video.save()
#
#         # file_obj = request.data['file']
#         # filename = request.FILES['filename'].name
#         # with open(filename, 'wb') as output:
#         #     pickle.dump(file_obj, filename, pickle.HIGHEST_PROTOCOL)
#         # file_obj.save("/home/ubuntu/files/uploaded/")
#         return Response('', status=status.HTTP_201_CREATED)
class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser, )

    def put(self, request):
        up_file = request.data.get('file', '')
        try:
            auth_token = request.META.get('HTTP_X_A12N')
            if auth_token != "711722bf-1fb4-43e1-b23b-00c755aeeeab":
                return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)

        except:
            return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)

        destination = open('/home/ubuntu/files/' + up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
            destination.close()

        #thumbnail = request.META.get('HTTP_THUMBNAIL')
        #thumbnail_name = request.META.get('HTTP_THUMBNAILNAME')
        #str1 = zlib.decompress(base64.b64decode(thumbnail))
        #destination1 = open('/home/ubuntu/files/'+thumbnail_name, 'wb+')
        #destination1.write(str1)
        #destination1.close()

        # ...
        # do some stuff with uploaded file
        # ...
        return Response("test", status.HTTP_201_CREATED)



class UserView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        response = Response(data='{}', status=status.HTTP_202_ACCEPTED)
        response['x-a12n'] = '711722bf-1fb4-43e1-b23b-00c755aeeeab'
        return response


class List(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response(data='{"Links":["TestVideo1.mp4", "Test2.mp4"]}', status=status.HTTP_200_OK)
