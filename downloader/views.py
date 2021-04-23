from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import youtube_dl
from .forms import DownloadForm
import re


def index(request):
    global context
    form = DownloadForm(request.POST or None)
    if form.is_valid():
        url = form.cleaned_data.get("url")
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
        if not re.match(regex,url):
            return HttpResponse("Enter correct youtube url")
        
        options = {}

        with youtube_dl.YoutubeDL(options) as ydl:
            meta = ydl.extract_info(url,download=False)
        video_streams = []

        for m in meta['formats']:
            file_size = m['filesize']
            if file_size is not None:
                file_size = f'{round(int(file_size) / 1000000,2)} MB'
            print(file_size)
            resolution = "Audio"
            if m['height'] is not None:
                resolution = f"{m['height']}x{m['width']}"
            
            video_streams.append({
                'resolution':resolution,
                'extension':m['ext'],
                'file_size':file_size,
                'video_url':m['url']
            })
            video_streams = video_streams[::-1]
            context = {
            'form': form,
            'title': meta['title'], 'streams': video_streams,
            'description': meta['description'], 'likes': meta['like_count'],
            'dislikes': meta['dislike_count'], 'thumb': meta['thumbnails'][3]['url'],
            'duration': round(int(meta['duration'])/60, 2), 'views': f'{int(meta["view_count"]):,}'
        }
        return render(request, 'home.html', context)
    return render(request,'home.html',{'form':form})