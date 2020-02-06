from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Message

def index(request):
	latest_msg_list = Message.objects.order_by('-pub_date')[:10]
	context = {
		'latest_msg_list': latest_msg_list,
	}
	return render(request, 'main_index.html', context)

def detail(request, msg_id):
	msg = get_object_or_404(Message, pk=msg_id)
	response_list = msg.response_set.all()
	context = {
		'response_list': response_list,
	}
	return render(request, 'main_detail.html', context)