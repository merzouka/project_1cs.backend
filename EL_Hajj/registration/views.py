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
from .models import  Baladiya, Tirage, Haaj, Winners,WaitingList
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render
import random 
from django.utils import timezone
import datetime
from registration.serializers import WinnersSerializer






@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
        
        if first_baladiya and first_baladiya.tirage and first_baladiya.tirage.tirage_défini:
            return JsonResponse({'message': 'Tirage déjà fini'}, status=200)

        condidats = []

        for baladiya_name in baladiya_names:
            haajs_in_city = Haaj.objects.filter(user__city=baladiya_name)
            condidats.extend(haajs_in_city)
        
        condidats2 =[]
    


        for haaj in condidats:
    
             times_to_add = haaj.user.nombreInscription
    
             condidats2.extend([haaj] * times_to_add)

        condidats2_over_60 = []
        condidats2_under_60 = []

  
        for haaj in condidats2:
    
           
           user_age_days = (datetime.date.today() - haaj.user.dateOfBirth).days
           user_age_years = user_age_days / 365.2425 
    
    
           if user_age_years > 60:
        
              condidats2_over_60.append(haaj)
           else:
        
              condidats2_under_60.append(haaj)

        id_tirage = first_baladiya.tirage.id
        number_of_winners_needed = Tirage.objects.get(id=id_tirage).nombre_de_place
        type_de_tirage = Tirage.objects.get(id=id_tirage).type_tirage
        Tirage.objects.get(id=id_tirage).tirage_défini= True
        number_of_waiting_needed=Tirage.objects.get(id=id_tirage).nombre_waiting
       
        selected_winners = []
        selected_waiting=[]

        if type_de_tirage == 1:
            while len(selected_winners) < number_of_winners_needed:
                selected_condidat = random.choice(condidats2)
                if selected_condidat.user.gender == 'M':
                    selected_condidat.user.winner = True 
                    selected_condidat.user.winning_date= timezone.now()  
                    selected_winners.append({
                        'first_name': selected_condidat.user.first_name,
                        'last_name': selected_condidat.user.last_name,
                        'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                    })
                    #condidats2.remove(selected_condidat)
                    condidats2 = list(filter((selected_condidat).__ne__, condidats2))
                    Winners.objects.create(nin=selected_condidat.user.id)
                elif selected_condidat.user.gender == 'F':
                  if len(selected_winners) == number_of_winners_needed - 1:
                        # Ensure the last selected winner is male
                        last_male_condidat = random.choice([condidat for condidat in condidats2 if condidat.user.gender == 'M'])
                        last_male_condidat.user.winner = True 
                        last_male_condidat.user.winning_date = timezone.now()  
                        selected_winners.append({
                            'first_name': last_male_condidat.user.first_name,
                            'last_name': last_male_condidat.user.last_name,
                            'personal_picture': last_male_condidat.personal_picture.url if last_male_condidat.personal_picture else None
                        })
                        condidats2 = list(filter((last_male_condidat).__ne__, condidats2))
                        Winners.objects.create(nin=last_male_condidat.user.id)
                  else:
                    selected_condidat.user.winner = True 
                    selected_condidat.user.winning_date= timezone.now()  
                    selected_winners.append({
                        'first_name': selected_condidat.user.first_name,
                        'last_name': selected_condidat.user.last_name,
                        'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                    })
                    #condidats2.remove(selected_condidat)
                    condidats2 = list(filter((selected_condidat).__ne__, condidats2))
                    Winners.objects.create(nin=selected_condidat.user.id)
                    
                    maahram_instance = user.objects.get(id=selected_condidat.maahram_id)
                    if maahram_instance not in selected_winners:
                        maahram_instance.winner = True 
                        maahram_instance.winning_date= timezone.now()
                        selected_winners.append({
                            'first_name': maahram_instance.first_name,
                            'last_name': maahram_instance.last_name,
                            'personal_picture': maahram_instance.personal_picture.url if maahram_instance.personal_picture else None
                        })
                        Winners.objects.create(nin=maahram_instance.id)
                        if maahram_instance in condidats2:
                                condidats2 = list(filter((maahram_instance).__ne__, condidats2))


           #witing list code................
            while len(selected_waiting) < number_of_waiting_needed:
                selected_condidat = random.choice(condidats2)
                if selected_condidat.user.gender == 'M':
                    
                      
                    selected_waiting.append({
                        'first_name': selected_condidat.user.first_name,
                        'last_name': selected_condidat.user.last_name,
                        'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                    })
                    
                    condidats2 = list(filter((selected_condidat).__ne__, condidats2))
                    WaitingList.objects.create(nin=selected_condidat.user.id)
                elif selected_condidat.user.gender == 'F':
                    if len(selected_waiting) == number_of_waiting_needed - 1:
                        
                        last_male_condidat = random.choice([condidat for condidat in condidats2 if condidat.user.gender == 'M'])
                         
                          
                        selected_waiting.append({
                            'first_name': last_male_condidat.user.first_name,
                            'last_name': last_male_condidat.user.last_name,
                            'personal_picture': last_male_condidat.personal_picture.url if last_male_condidat.personal_picture else None
                        })
                        condidats2 = list(filter((last_male_condidat).__ne__, condidats2))
                        WaitingList.objects.create(nin=last_male_condidat.user.id)
                    else:
                         
                         
                        selected_waiting.append({
                            'first_name': selected_condidat.user.first_name,
                            'last_name': selected_condidat.user.last_name,
                            'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                        })
                        
                        condidats2 = list(filter((selected_condidat).__ne__, condidats2))
                        WaitingList.objects.create(nin=selected_condidat.user.id)
                        
                        maahram_instance = user.objects.get(id=selected_condidat.maahram_id)
                        if maahram_instance not in selected_waiting:
                             
                            
                            selected_waiting.append({
                                'first_name': maahram_instance.first_name,
                                'last_name': maahram_instance.last_name,
                                'personal_picture': maahram_instance.personal_picture.url if maahram_instance.personal_picture else None
                            })
                            WaitingList.objects.create(nin=maahram_instance.id)
                            if maahram_instance in condidats2:
                                condidats2 = list(filter((maahram_instance).__ne__, condidats2))
                                

        elif type_de_tirage == 2:
            selected_winners1 = []
            selected_winners2 = []
            selected_waiting1=[]
            selected_waiting2=[]
            tranche_age = Tirage.objects.get(id=id_tirage).tranche_age
            nombre_old = int((tranche_age * number_of_winners_needed) / 100)
            nombre_new = number_of_winners_needed-nombre_old


            #pour waiting list
            nombre_old1 = int((tranche_age * number_of_waiting_needed) / 100)
            nombre_new1 = number_of_waiting_needed-nombre_old1

            if condidats2_over_60:
                while len(selected_winners1) < nombre_old:
                    selected_condidat = random.choice(condidats2_over_60)
                    if selected_condidat.user.gender == 'M':
                        selected_condidat.user.winner = True 
                        selected_condidat.user.winning_date= timezone.now()  
                        selected_condidat.user.save() 
                        selected_winners1.append({
                            'first_name': selected_condidat.user.first_name,
                            'last_name': selected_condidat.user.last_name,
                            'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                        })
                        # condidats2_over_60.remove(selected_condidat)
                        condidats2_over_60 = list(filter((selected_condidat).__ne__, condidats2_over_60))
                        Winners.objects.create(nin=selected_condidat.user.id)
                        
                    elif selected_condidat.user.gender == 'F':
                        # Check if the current selection is the last one
                       if len(selected_winners1) == nombre_old - 1:
                            # Ensure the last selected winner is male
                            last_male_condidat = random.choice([condidat for condidat in condidats2_over_60 if condidat.user.gender == 'M'])
                            last_male_condidat.user.winner = True 
                            last_male_condidat.user.winning_date = timezone.now()  
                            last_male_condidat.user.save()
                            selected_winners1.append({
                                'first_name': last_male_condidat.user.first_name,
                                'last_name': last_male_condidat.user.last_name,
                                'personal_picture': last_male_condidat.personal_picture.url if last_male_condidat.personal_picture else None
                            })
                            condidats2_over_60 = list(filter((last_male_condidat).__ne__, condidats2_over_60))
                            Winners.objects.create(nin=last_male_condidat.user.id)
                       else:
                        selected_condidat.user.winner = True
                        selected_condidat.user.winning_date= timezone.now() 
                        selected_condidat.user.save()  
                        selected_winners1.append({
                            'first_name': selected_condidat.user.first_name,
                            'last_name': selected_condidat.user.last_name,
                            'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                        })
                        #condidats2_over_60.remove(selected_condidat)
                        condidats2_over_60 = list(filter((selected_condidat).__ne__, condidats2_over_60))
                        Winners.objects.create(nin=selected_condidat.user.id)
                        
                        maahram_instance = user.objects.get(id=selected_condidat.maahram_id)
                        if maahram_instance not in selected_winners1:
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
                            if condidats2_over_60:
                                if maahram_instance in condidats2_under_60:
                                   condidats2_over_60 = list(filter((maahram_instance).__ne__, condidats2_over_60))

            if condidats2_under_60:                           
                while len(selected_winners2) < nombre_new:
                    selected_condidat = random.choice(condidats2_under_60)
                    if selected_condidat.user.gender == 'M':
                        selected_condidat.user.winner = True
                        selected_condidat.user.winning_date= timezone.now() 
                        selected_condidat.user.save()  
                        selected_winners2.append({
                            'first_name': selected_condidat.user.first_name,
                            'last_name': selected_condidat.user.last_name,
                            'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                        })
                        #condidats2_under_60.remove(selected_condidat)
                        condidats2_under_60 = list(filter((selected_condidat).__ne__, condidats2_under_60))
                        Winners.objects.create(nin=selected_condidat.user.id)
                        
                    elif selected_condidat.user.gender == 'F':
                      # Check if the current selection is the last one
                      if len(selected_winners2) == nombre_new - 1:
                            # Ensure the last selected winner is male
                            last_male_condidat = random.choice([condidat for condidat in condidats2_under_60 if condidat.user.gender == 'M'])
                            last_male_condidat.user.winner = True 
                            last_male_condidat.user.winning_date = timezone.now()  
                            last_male_condidat.user.save()
                            selected_winners2.append({
                                'first_name': last_male_condidat.user.first_name,
                                'last_name': last_male_condidat.user.last_name,
                                'personal_picture': last_male_condidat.personal_picture.url if last_male_condidat.personal_picture else None
                            })
                            condidats2_under_60 = list(filter((last_male_condidat).__ne__, condidats2_under_60))
                            Winners.objects.create(nin=last_male_condidat.user.id)
                      else:
                        selected_condidat.user.winner = True  
                        selected_condidat.user.winning_date= timezone.now() 
                        selected_condidat.user.save()  
                        selected_winners2.append({
                            'first_name': selected_condidat.user.first_name,
                            'last_name': selected_condidat.user.last_name,
                            'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                        })
                        #condidats2_under_60.remove(selected_condidat)
                        condidats2_under_60 = list(filter((selected_condidat).__ne__, condidats2_under_60))
                        Winners.objects.create(nin=selected_condidat.user.id)

                        maahram_instance = user.objects.get(id=selected_condidat.maahram_id)
                        if (maahram_instance not in selected_winners1) and  (maahram_instance not in selected_winners2) :
                        #condidats.remove(maahram_instance)
                                maahram_instance.winner = True
                                maahram_instance.winning_date= timezone.now()  
                                maahram_instance.save()  
                                selected_winners2.append({
                                    'first_name': maahram_instance.first_name,
                                    'last_name': maahram_instance.last_name,
                                    'personal_picture': maahram_instance.personal_picture.url if maahram_instance.personal_picture else None
                                })
                                Winners.objects.create(nin=maahram_instance.id)
                                if condidats2_under_60:
                                    if maahram_instance in condidats2_under_60:
                                        condidats2_under_60 = list(filter((maahram_instance).__ne__, condidats2_under_60))





                #tirage  de waiting list........................;
            if condidats2_over_60:
                        while len(selected_waiting1) < nombre_old1:
                            selected_condidat = random.choice(condidats2_over_60)
                            if selected_condidat.user.gender == 'M':
                                
                                 
                                
                                selected_waiting1.append({
                                    'first_name': selected_condidat.user.first_name,
                                    'last_name': selected_condidat.user.last_name,
                                    'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                                })
                                
                                condidats2_over_60 = list(filter((selected_condidat).__ne__, condidats2_over_60))
                                WaitingList.objects.create(nin=selected_condidat.user.id)
                                
                            elif selected_condidat.user.gender == 'F':
                                
                               if len(selected_waiting1) == nombre_old1 - 1:
                                    # Ensure the last selected winner is male
                                    last_male_condidat = random.choice([condidat for condidat in condidats2_over_60 if condidat.user.gender == 'M'])
                                     
                                      
                                    
                                    selected_waiting1.append({
                                        'first_name': last_male_condidat.user.first_name,
                                        'last_name': last_male_condidat.user.last_name,
                                        'personal_picture': last_male_condidat.personal_picture.url if last_male_condidat.personal_picture else None
                                    })
                                    condidats2_over_60 = list(filter((last_male_condidat).__ne__, condidats2_over_60))
                                    WaitingList.objects.create(nin=last_male_condidat.user.id)
                            else:
                                
                                 
                                  
                                selected_waiting1.append({
                                    'first_name': selected_condidat.user.first_name,
                                    'last_name': selected_condidat.user.last_name,
                                    'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                                })
                                
                                condidats2_over_60 = list(filter((selected_condidat).__ne__, condidats2_over_60))
                                WaitingList.objects.create(nin=selected_condidat.user.id)
                                
                                maahram_instance = user.objects.get(id=selected_condidat.maahram_id)
                                if maahram_instance not in selected_winners1:
                                    
                                     
                                    
                                    
                                    selected_waiting1.append({
                                        'first_name': maahram_instance.first_name,
                                        'last_name': maahram_instance.last_name,
                                        'personal_picture': maahram_instance.personal_picture.url if maahram_instance.personal_picture else None
                                    })
                                    WaitingList.objects.create(nin=maahram_instance.id)
                                    if condidats2_over_60:
                                        if maahram_instance in condidats2_under_60:
                                           condidats2_over_60 = list(filter((maahram_instance).__ne__, condidats2_over_60))

            if condidats2_under_60:                           
                        while len(selected_waiting2) < nombre_new1:
                            selected_condidat = random.choice(condidats2_under_60)
                            if selected_condidat.user.gender == 'M':
                                
                                 
                                  
                                selected_waiting2.append({
                                    'first_name': selected_condidat.user.first_name,
                                    'last_name': selected_condidat.user.last_name,
                                    'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                                })
                                
                                condidats2_under_60 = list(filter((selected_condidat).__ne__, condidats2_under_60))
                                WaitingList.objects.create(nin=selected_condidat.user.id)
                                
                            elif selected_condidat.user.gender == 'F':
                            
                               if len(selected_waiting2) == nombre_new1 - 1:
                                    
                                    last_male_condidat = random.choice([condidat for condidat in condidats2_under_60 if condidat.user.gender == 'M'])
                                    
                                      
                                    
                                    selected_waiting2.append({
                                        'first_name': last_male_condidat.user.first_name,
                                        'last_name': last_male_condidat.user.last_name,
                                        'personal_picture': last_male_condidat.personal_picture.url if last_male_condidat.personal_picture else None
                                    })
                                    condidats2_under_60 = list(filter((last_male_condidat).__ne__, condidats2_under_60))
                                    WaitingList.objects.create(nin=last_male_condidat.user.id)
                            else:
                                  
                                 
                                 
                                selected_waiting2.append({
                                    'first_name': selected_condidat.user.first_name,
                                    'last_name': selected_condidat.user.last_name,
                                    'personal_picture': selected_condidat.personal_picture.url if selected_condidat.personal_picture else None
                                })
                                
                                condidats2_under_60 = list(filter((selected_condidat).__ne__, condidats2_under_60))
                                WaitingList.objects.create(nin=selected_condidat.user.id)

                                maahram_instance = user.objects.get(id=selected_condidat.maahram_id)
                                if (maahram_instance not in selected_waiting1) and  (maahram_instance not in selected_waiting2) :
                                
                                        
                                          
                                          
                                        selected_waiting2.append({
                                            'first_name': maahram_instance.first_name,
                                            'last_name': maahram_instance.last_name,
                                            'personal_picture': maahram_instance.personal_picture.url if maahram_instance.personal_picture else None
                                        })
                                        WaitingList.objects.create(nin=maahram_instance.id)
                                        if condidats2_under_60:
                                            if maahram_instance in condidats2_under_60:
                                                condidats2_under_60 = list(filter((maahram_instance).__ne__, condidats2_under_60))

        if type_de_tirage == 1:
            selected_winners = selected_winners
            selected_waiting = selected_waiting
        else:
            selected_winners = selected_winners1 + selected_winners2
            selected_waiting = selected_waiting1 + selected_waiting2

        return JsonResponse({'winners': selected_winners}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def participants_tirage(request, utilisateur_id):
    try:
        
        user_instance = get_object_or_404(user, id=utilisateur_id)
        user_city = user_instance.city
        baladiya_instance = get_object_or_404(Baladiya, name=user_city)
        baladiya_tirage_id = baladiya_instance.tirage_id
        baladiyat_in_tirage = Baladiya.objects.filter(tirage_id=baladiya_tirage_id)
        baladiya_names = [baladiya.name for baladiya in baladiyat_in_tirage]
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
        
        return JsonResponse(serialized_data, status=200)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['GET'])
def check_tirage_definition(request, utilisateur_id):
    try:
        user_instance = get_object_or_404(user, id=utilisateur_id)
        baladiya_ids = user_instance.baladiya_set.values_list('id', flat=True)

        if len(baladiya_ids) == 0:
            return JsonResponse({'tirage_definit': False}, status=200)

        for baladiya_id in baladiya_ids:
            baladiya = get_object_or_404(Baladiya, id=baladiya_id)
            if not baladiya.tirage_id:
                return JsonResponse({'tirage_definit': False}, status=200)

        
        return JsonResponse({'tirage_definit': True}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
def tirage_fini(request, utilisateur_id):
    try:
        baladiyat = Baladiya.objects.filter(id_utilisateur=utilisateur_id).first()
        if baladiyat and baladiyat.tirage and baladiyat.tirage.tirage_défini:
            return JsonResponse({'message': 'tirage défini'})
        else:
            return JsonResponse({'message': 'tirage non défini'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
   

#for visite medical...........................................
@api_view(['GET'])
def winners_by_baladiya(request, utilisateur_id):
    try:
        user_instance = get_object_or_404(user, id=utilisateur_id)
        
        baladiyas_in_group = Baladiya.objects.filter(id_utilisateur=user_instance)
        baladiya_names = [baladiya.name for baladiya in baladiyas_in_group]
        
        user_ids_in_city = user.objects.filter(city__in=baladiya_names).values_list('id', flat=True)
        winners = Winners.objects.filter(nin__in=user_ids_in_city)
        
        winners_data = []
        for winner in winners:
            winner_user = get_object_or_404(user, id=winner.nin)
            user_data = {
                'id_user': winner_user.id,
                'id_winner': winner.id,
                'first_name': winner_user.first_name,
                'last_name': winner_user.last_name,
                'personal_picture': winner_user.personal_picture.url if winner_user.personal_picture else None,
            }
            winners_data.append(user_data)
        
        return JsonResponse(winners_data, status=200, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@api_view(['POST'])
def visite_status(request):

    try:

        id_winner = request.data.get('id_winner')
        status = request.data.get('status')
            
        if not id_winner or not status:
            return JsonResponse({'error': 'Both id_winner and status are required'}, status=400)
            
        try:
            winner = Winners.objects.get(id=id_winner)
        except Winners.DoesNotExist:
            return JsonResponse({'error': 'Winner with the provided ID does not exist'}, status=404)
            
        if status.lower() == "accepted":
            winner.visite = True
            winner.save()
            return JsonResponse({'message': 'Winner visit status updated successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Status is not "accepted", no action taken'}, status=200)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
   
    
#for payment.....................
@api_view(['GET'])
def winners_accepted(request, utilisateur_id):
    try:
        
        user_instance = get_object_or_404(user, id=utilisateur_id)
        
        
        baladiyas_in_group = Baladiya.objects.filter(id_utilisateur=user_instance)
        
        
        baladiya_names = [baladiya.name for baladiya in baladiyas_in_group]
        
        
        winners = Winners.objects.filter(
            nin__in=user.objects.filter(city__in=baladiya_names).values('id'),
            visite=True
        )
        
        
        winners_data = []
        for winner in winners:
            winner_user = get_object_or_404(user, id=winner.nin)
            user_data = {
                'id_user': winner_user.id,
                'id_winner': winner.id,
                'first_name': winner_user.first_name,
                'last_name': winner_user.last_name,
                'personal_picture': winner_user.personal_picture.url if winner_user.personal_picture else None,
            }
            winners_data.append(user_data)
        
        return JsonResponse(winners_data, status=200, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
def payment_status(request):
    try:
        
        id_winner = request.data.get('id_winner')
        status = request.data.get('status')
        
        
        if not id_winner or not status:
            return JsonResponse({'error': 'Both id_winner and status are required'}, status=400)
        
        
        winner = get_object_or_404(Winners, id=id_winner)
        
        
        if status.lower() == "payé":
            
            winner.payement = True
            winner.save()
            return JsonResponse({'message': 'Winner payment status updated successfully'}, status=200)
        else:
            
            return JsonResponse({'message': 'Status is not "payé", no action taken'}, status=200)
    
    except Exception as e:
       
        return JsonResponse({'error': str(e)}, status=500)
