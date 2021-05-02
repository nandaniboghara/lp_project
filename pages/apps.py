from django.apps import AppConfig
from django.conf import settings
import os
import pickle


class PagesConfig(AppConfig):
   path = os.path.join(settings.MODELS, 'models.p')

   # load models into separate variables
   # these will be accessible via this class
   with open(path, 'rb') as pickled:
      data = pickle.load(pickled)
   classifier = data['classifier']
   name = 'pages'
