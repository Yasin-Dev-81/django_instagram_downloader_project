import os
import shutil

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from config import settings
from insta_downloader import DirectoryDownload
from .models import InstagramData


def instagram_view(request):
    if request.method == "GET":
        return render(
            request=request,
            template_name='insta_web/instagram_search.html',
            context={'post_method': False, }
        )
    elif request.method == "POST":
        instagram_url = request.POST.get("instagram_link")
        cl = DirectoryDownload(
            sessionid_list=[obj.sessionid for obj in InstagramData.objects.filter(active=True)],
            folder_path=os.path.join(settings.MEDIA_ROOT, 'instagram_downloaded')
        )
        cl.type_inspector_with_url(url=instagram_url)
        cl.data_inspector_with_url()
        if request.user.is_authenticated:
            cl.start()
            print('---- download is started:)')
        return render(
            request=request,
            template_name='insta_web/instagram_search.html',
            context={
                'instagram_data': cl.data,
                'instagram_post_type': not cl.stories,
                'stories': cl.stories,
                'post_method': True,
                'instagram_url': instagram_url,
                'is_page': cl.page
            }
        )


@login_required
def instagram_download_view(request, pk, stories: bool):
    file_path = os.path.join(settings.MEDIA_ROOT, 'instagram_downloaded', '%s.zip' % pk)
    folder_path = os.path.join(settings.MEDIA_ROOT, 'instagram_downloaded', str(pk))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    elif os.path.exists(folder_path) and not os.path.exists(file_path):
        return render(request, 'insta_web/instagram_download.html', context={'pk': pk, 'stories': stories})
    else:
        cl = DirectoryDownload(
            sessionid_list=[obj.sessionid for obj in InstagramData.objects.filter(active=True)],
            folder_path=os.path.join(settings.MEDIA_ROOT, 'instagram_downloaded')
        )
        cl.type_inspector_with_pk(pk=pk, stories=stories)
        cl.start()
        return render(request, 'insta_web/instagram_download.html', context={'pk': pk, 'stories': stories})


@staff_member_required
def clean_media_view(request):
    folder = os.path.join(settings.MEDIA_ROOT, 'instagram_downloaded')
    if request.method == 'POST':
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        return render(request, 'insta_web/clean_media.html', context={'post_method': True})
    else:
        return render(request, 'insta_web/clean_media.html', context={'medias': os.listdir(folder), 'post_method': False})
