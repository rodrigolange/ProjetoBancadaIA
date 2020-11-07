from django.contrib.auth.models import User
from gangorra.models import ExperimentoGangorra

user = User.objects.get(username='lange')
r = ExperimentoGangorra(author=user, title='teste 0011', csvArquivo='dados12.txt', videoArquivo='dados12.mp4')
r.publish()

