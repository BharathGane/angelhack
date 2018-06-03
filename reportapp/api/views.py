from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.nlp.main import process_text
from .models import Report
# Create your views here.

@csrf_exempt
def get_session(request):
	context = {}
	faculty = ""
	semester = ""
	subject = ""
	topic = ""
	session = ""
	topics_covered_str = ""
	topics_not_covered_str = ""
	body_unicode = request.body.decode('utf-8')
	print(body_unicode)
	body = json.loads(body_unicode)
	if request.method == "POST":
		faculty = body["faculty"]
		semester = body["semester"]
		subject = body["subject"]
		topic = body["topic"]
		session = body["session"]
		#session = ["accleration is the rate of change of velocity","velocity change accleration rate"]
		x = process_text()
		report_dict = x.return_final(session)
		for i in report_dict["topics_covered"]:
			topics_covered_str = topics_covered_str + i
		for j in report_dict["topics_not_covered"]:
			topics_not_covered_str = topics_not_covered_str + j + " "
		report = Report(subject=subject,topic=topic,topics_covered=topics_covered_str,number_of_topics_covered=len(report_dict["topics_covered"]),
			topics_not_covered=topics_not_covered_str,percentage_covered=float((len(report_dict["topics_covered"])/len(report_dict["all_topics"]))*100),intensity=0)
		# text = ["Every object in a state of uniform motion tends to remain in that state of motion unless an external force is applied to it.","every action has an equal and opposite reaction"]
		# for i in text:
		# 	print(x.return_final(i))
		report.save()

	context["response"]={}
	print(context)
	return JsonResponse(context)


