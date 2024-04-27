import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.serializers import userSerializer
from .serializers import HaajSerializer 
from authentication.models import user 
from rest_framework.permissions import IsAuthenticated
from .models import  Baladiya, Tirage, Haaj, Winners
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render
import random 
from django.utils import timezone
import datetime






@api_view(['GET', 'POST'])
def registration(request):
    authenticated_user = request.user  
    if request.method == 'GET':
        utilisateur_data = {
            'emailUtilisateur': authenticated_user.email,
            'first_name': authenticated_user.first_name,
            'last_name': authenticated_user.last_name,
            'dateOfBirth': authenticated_user.dateOfBirth,
            'city' : authenticated_user.city,
            'gender' : authenticated_user.gender
        }
        return JsonResponse(utilisateur_data)

    elif request.method == 'POST':
        if authenticated_user.winner:
            last_winning_date = authenticated_user.winning_date
            ten_years_ago = datetime.now() - datetime.timedelta(days=365 * 10)
            if last_winning_date > ten_years_ago:
                return Response("You cannot register for the draw as you have won in the last 10 years.", status=status.HTTP_400_BAD_REQUEST)
        
        serializer_data = request.data.copy() 
        haaj_serializer = HaajSerializer(data=serializer_data, context={'request': request})
        if haaj_serializer.is_valid():
            haaj_instance = haaj_serializer.save()
            return Response("Success", status=status.HTTP_201_CREATED)
        return Response(haaj_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    









@api_view(['GET'])
@parser_classes([JSONParser])
def baladiya_names_by_utilisateur(request, utilisateur_id):
    try:
        utilisateur_obj = get_object_or_404(user, id=utilisateur_id)
        baladiya_names = utilisateur_obj.baladiya_set.values_list('name', flat=True)
        return Response({'baladiya_names': list(baladiya_names)}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)





@api_view(['POST'])
@parser_classes([JSONParser])
def associate_tirage_with_baladiyas(request):
    
    utilisateur_id = request.data.get('utilisateur_id')
    type_tirage = request.data.get('type_tirage')
    nombre_de_place = request.data.get('nombre_de_place')
    tranche_age = request.data.get('tranche_age')
    
    utilisateur_obj = get_object_or_404(user, id=utilisateur_id)

    
    baladiya_ids = utilisateur_obj.baladiya_set.values_list('id', flat=True)

    
    tirage = Tirage.objects.create(
        type_tirage=type_tirage,
        nombre_de_place=nombre_de_place,
        tranche_age=tranche_age 
    )

    
    for baladiya_id in baladiya_ids:
        baladiya = get_object_or_404(Baladiya, id=baladiya_id)
        baladiya.tirage = tirage
        baladiya.save()

 
    return Response({'message': 'Tirage information associated with Baladiyas successfully'}, status=201)





@api_view(['GET'])
def fetch_winners(request, id_utilisateur):
    try:
        user_instance = get_object_or_404(user, id=id_utilisateur)
        baladiyas_in_group = Baladiya.objects.filter(id_utilisateur=user_instance)
        baladiya_names = [baladiya.name for baladiya in baladiyas_in_group]
        first_baladiya = Baladiya.objects.filter(id_utilisateur=id_utilisateur).first()

        condidats = []

        for baladiya_name in baladiya_names:
            haajs_in_city = Haaj.objects.filter(user__city=baladiya_name)
            condidats.extend(haajs_in_city)

        id_tirage = first_baladiya.tirage.id
        number_of_winners_needed = Tirage.objects.get(id=id_tirage).nombre_de_place
        type_de_tirage = Tirage.objects.get(id=id_tirage).type_tirage

        selected_winners = []

        if type_de_tirage == 1:
            while len(selected_winners) < number_of_winners_needed:
                selected_condidat = random.choice(condidats)
                if selected_condidat.user.gender == 'M':
                    selected_condidat.user.winner = True 
                    selected_condidat.user.winning_date= timezone.now()  
                    selected_winners.append({
                        'first_name': selected_condidat.user.first_name,
                        'last_name': selected_condidat.user.last_name,
                        'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                    })
                    condidats.remove(selected_condidat)
                    Winners.objects.create(nin=selected_condidat.user.id)
                elif selected_condidat.user.gender == 'F':
                    selected_condidat.user.winner = True 
                    selected_condidat.user.winning_date= timezone.now()  
                    selected_winners.append({
                        'first_name': selected_condidat.user.first_name,
                        'last_name': selected_condidat.user.last_name,
                        'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                    })
                    condidats.remove(selected_condidat)
                    Winners.objects.create(nin=selected_condidat.user.id)
                    maahram_instance = user.objects.get(id=selected_condidat.maahram_id)
                    maahram_instance.winner = True 
                    maahram_instance.winning_date= timezone.now()
                    selected_winners.append({
                        'first_name': maahram_instance.first_name,
                        'last_name': maahram_instance.last_name,
                        'personal_picture': maahram_instance.personal_picture.url if maahram_instance.personal_picture else None
                    })
                    Winners.objects.create(nin=maahram_instance.id)
        elif type_de_tirage == 2:
            selected_winners1 = []
            selected_winners2 = []
            tranche_age = Tirage.objects.get(id=id_tirage).tranche_age
            nombre_old = (tranche_age * number_of_winners_needed) / 100
            new = 100 - tranche_age
            nombre_new = (new * number_of_winners_needed) / 100

            while len(selected_winners1) < nombre_old:
                selected_condidat = random.choice(condidats)
                if selected_condidat.user.gender == 'M':
                    selected_condidat.user.winner = True 
                    selected_condidat.user.winning_date= timezone.now()  
                    selected_condidat.user.save() 
                    selected_winners1.append({
                        'first_name': selected_condidat.user.first_name,
                        'last_name': selected_condidat.user.last_name,
                        'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                    })
                    condidats.remove(selected_condidat)
                    Winners.objects.create(nin=selected_condidat.user.id)
                    
                elif selected_condidat.user.gender == 'F':
                    selected_condidat.user.winner = True
                    selected_condidat.user.winning_date= timezone.now() 
                    selected_condidat.user.save()  
                    selected_winners1.append({
                        'first_name': selected_condidat.user.first_name,
                        'last_name': selected_condidat.user.last_name,
                        'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                    })
                    condidats.remove(selected_condidat)
                    Winners.objects.create(nin=selected_condidat.user.id)
                    
                    maahram_instance = user.objects.get(id=selected_condidat.maahram_id)
                    #condidats.remove(maahram_instance)
                    maahram_instance.winner = True 
                    maahram_instance.winning_date= timezone.now()
                    maahram_instance.save()
                    selected_winners1.append({
                        'first_name': maahram_instance.first_name,
                        'last_name': maahram_instance.last_name,
                        'personal_picture': maahram_instance.personal_picture.url if maahram_instance.personal_picture else None
                    })
                    Winners.objects.create(nin=maahram_instance.id)

            while len(selected_winners2) < nombre_new:
                selected_condidat = random.choice(condidats)
                if selected_condidat.user.gender == 'M':
                    selected_condidat.user.winner = True
                    selected_condidat.user.winning_date= timezone.now() 
                    selected_condidat.user.save()  
                    selected_winners2.append({
                        'first_name': selected_condidat.user.first_name,
                        'last_name': selected_condidat.user.last_name,
                        'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                    })
                    condidats.remove(selected_condidat)
                    Winners.objects.create(nin=selected_condidat.user.id)
                    
                elif selected_condidat.user.gender == 'F':
                    selected_condidat.user.winner = True  
                    selected_condidat.user.winning_date= timezone.now() 
                    selected_condidat.user.save()  
                    selected_winners2.append({
                        'first_name': selected_condidat.user.first_name,
                        'last_name': selected_condidat.user.last_name,
                        'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                    })
                    condidats.remove(selected_condidat)
                    Winners.objects.create(nin=selected_condidat.user.id)

                    maahram_instance = user.objects.get(id=selected_condidat.maahram_id)
                    if maahram_instance not in selected_winners1:
                    #condidats.remove(maahram_instance)
                          maahram_instance.winner = True
                          maahram_instance.winner = True  
                          maahram_instance.save()  
                          selected_winners2.append({
                               'first_name': maahram_instance.first_name,
                               'last_name': maahram_instance.last_name,
                               'personal_picture': maahram_instance.personal_picture.url if maahram_instance.personal_picture else None
                          })
                          Winners.objects.create(nin=maahram_instance.id)

        
        if type_de_tirage == 1:
            selected_winners = selected_winners
        else:
            selected_winners = selected_winners1 + selected_winners2

        return JsonResponse({'winners': selected_winners}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def participants_tirage(request, utilisateur_id):
    try:
        
        user_instance = get_object_or_404(user, id=utilisateur_id)
        baladiyas_in_group = Baladiya.objects.filter(id_utilisateur=user_instance)
        baladiya_names = [baladiya.name for baladiya in baladiyas_in_group]
        serialized_data = []

        
        for baladiya_name in baladiya_names:
            haajs_in_city = Haaj.objects.filter(user__city=baladiya_name)
            for haaj in haajs_in_city:
                haaj_data = {
                    'id': haaj.id,
                    'first_name_arabic': haaj.first_name_arabic,
                    'last_name_arabic': haaj.last_name_arabic,
                    'mother_name': haaj.mother_name,
                    'father_name': haaj.father_name,
                    'NIN': haaj.NIN,
                    'card_expiration_date': haaj.card_expiration_date,
                    'passport_id': haaj.passport_id,
                    'passport_expiration_date': haaj.passport_expiration_date,
                    'nationality': haaj.nationality,
                    'phone_number': haaj.phone_number,
                    'personal_picture': haaj.personal_picture.url if haaj.personal_picture else None,
                    'user': userSerializer(haaj.user).data  # Serialize user associated with Haaj
                }
                serialized_data.append(haaj_data)
        
        return Response(serialized_data, status=200)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)
