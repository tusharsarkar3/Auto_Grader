#from semantic_text_similarity.models import WebBertSimilarity
from semantic_text_similarity.models import ClinicalBertSimilarity

#web_model = WebBertSimilarity(device='cpu', batch_size=10) #defaults to GPU prediction

clinical_model = ClinicalBertSimilarity(device='cpu', batch_size=10) #defaults to GPU prediction

print(clinical_model.predict([("Nishit plays badminton","Badminton is played by Nishit")])/5)