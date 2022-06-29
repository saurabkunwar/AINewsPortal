from django_q.models import Schedule

Schedule.objects.create(func='tasks.crawl_kathmandu_post',
                        minutes=1,
                        repeats=-1
                        )