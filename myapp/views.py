from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import AccountBrand, AccountCreator, Campaign, CampaignAcceptance, Deliverable
from .serializers import AccountBrandSerializer, AccountCreatorSerializer, CampaignSerializer, CampaignAcceptanceSerializer, DeliverableSerializer

# Create your views here.
# @api_view(['GET'])
# def brand_list(request):
#     if request.method == 'GET':
#         brand = AccountBrand.objects.all()
#         serializer = AccountBrandSerializer(brand, many=True)
#         return Response(serializer.data)

def index(request):

    return render(request, 'myapp/index.html')