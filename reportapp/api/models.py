from django.db import models

# Create your models here.

class Session(models.Model):
	faculty = models.CharField('Facaulty', max_length=50)
	semester = models.CharField('Semester', max_length=50)
	subject = models.CharField('Subject',max_length=50)
	topic = models.CharField('Topic',max_length=50)
	sesion_topic = models.CharField('Session Topic',max_length=2000)

	class Meta:
		verbose_name_plural = "Sessions"

	def __str__(self):
		return "{}, {}".format(self.faculty, self.topic)

class Report(models.Model):
	subject = models.CharField("Subject",max_length=50)
	topic = models.CharField("Topic",max_length=50)
	topics_covered = models.CharField('Topics Covered', max_length=500)
	number_of_topics_covered = models.IntegerField('Number Of Topics covered')
	examples_for_covered_topics = models.CharField('Examples of covered topics',max_length=500, blank=True)
	topics_not_covered = models.CharField('Topics not covered', max_length=500)
	percentage_covered = models.IntegerField('Percentage Completion')
	intensity = models.IntegerField('Audio Intensity', blank=True)

	class Meta:
		verbose_name_plural = "Reports"

	def __str__(self):
		return "{}, {}".format(self.subject, self.topic)

class Notes(models.Model):
	subject = models.CharField("Subject",max_length=50)
	topic = models.CharField("Topic",max_length=50)
	important_points = models.CharField("Important Points",max_length=500)
	examples = models.CharField("Relevant Examples",max_length=500)

	class Meta:
		verbose_name_plural = "Notes"

	def __str__(self):
		return "{}, {}".format(self.subject, self.topic)


