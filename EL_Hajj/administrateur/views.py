from django.shortcuts import render
# from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from authentication.models import user
from rest_framework.response import Response
from registration.models import Baladiya
from rest_framework.decorators import api_view, renderer_classes
from django.http import JsonResponse
from .serializers import hotelSerializer,voleSerializer
from django.shortcuts import get_object_or_404
from .models import Vole,Hotel
from rest_framework.renderers import JSONRenderer


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def user_list(request):
    role = request.GET.get('role')
    province = request.GET.get('province')
    city = request.GET.get('city')
    print(type(province))
    users_list = user.objects.all()

    if role:
        users_list = users_list.filter(role=role)
    if city:
        users_list = users_list.filter(baladiya__id=city)
    if province and not city:
        users_list = users_list.filter(baladiya__wilaya=province)

    paginator = PageNumberPagination()
    paginator.page_size = 5
    users = paginator.paginate_queryset(users_list, request)
    
    serialized_user = [{
        'id': u.id,
        'email': u.email,
        'firstName': u.first_name,
        'lastName' : u.last_name,
        'role': u.role,
        'provinces':u.baladiya_set.values_list('wilaya', flat=True).distinct(),
        'cities': u.baladiya_set.values_list('id', flat=True),
    } for u in users] if users else []
    
    return paginator.get_paginated_response(serialized_user)
 
@api_view(["PATCH"])
@renderer_classes([JSONRenderer])
def role_baladiyet_assignement(request):
    try :
        user_id = request.data.get('user_id')
        u = user.objects.get(id=user_id)
        user_role = request.data.get('user_role')
        u.role = user_role
        u.save()
        
        chosen_baladiya = request.data.get('chosen_baladiya')
        existing_baladiyats = Baladiya.objects.filter(id_utilisateur=u)
        
        baladiyets = Baladiya.objects.filter(id__in=chosen_baladiya)

        for baladiya in baladiyets:
            baladiya.id_utilisateur.add(u)

        for baladiya in existing_baladiyats:
            if baladiya not in baladiyets:
                baladiya.id_utilisateur.remove(u)
            
        return Response({'message':'association done'})
    except u.DoesNotExist:
        return Response({'error':'user not found'})
    

@api_view(["GET"])
@renderer_classes([JSONRenderer])
def users_role_wilaya(request):
    print("view")
    user_role = request.GET.get('user_role')  
    role_wilaya = request.GET.get('user_wilaya')
    
    print("user_role:", user_role)
    print("role_wilaya:", role_wilaya)
    
    if role_wilaya:
        try:
            role_wilaya = int(role_wilaya)
        except ValueError:
            return Response({'error': 'Invalid role_wilaya value'}, status=400)
    
    serialized_users = []
    if user_role : 
        users = user.objects.filter(role=user_role)
        
    else:
        users = user.objects.all()
        
        
    for u in users:
        baladiyets_ids = []
        wilaya_ids = []
            
            
        if u.role in ["user", "hedj"] : 
            baladiyets_ids = []
            wilaya_ids = [u.province]
            
            if role_wilaya and role_wilaya !=u.province :
                continue
                
                
        else :
            baladiyets = Baladiya.objects.filter(id_utilisateur=u.id)
                
                
            if role_wilaya :
                baladiyets = baladiyets.filter(wilaya=role_wilaya) 
                    
                    
            baladiyets_ids = [
                baladiya.id for baladiya in baladiyets
                ]
                
            wilaya_ids = [
                list(set(baladiya.wilaya for baladiya in baladiyets))
                    ]
            
            if role_wilaya and [role_wilaya] not in wilaya_ids:
                continue
                
         
        serialized_user = {
                'id': u.id,
                'email': u.email,
                'role': u.role,
                'wilaya':wilaya_ids,
                "baladiyets":baladiyets_ids
            }
        serialized_users.append(serialized_user)
        
    paginator = Paginator(serialized_users,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    serialized_page = [{"users":page_obj.object_list}]
    
    return JsonResponse({'pagination_info':{
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'users_per_page': paginator.per_page,
        'total_users': paginator.count
    }, 'users':serialized_page})     
                
            
        

@api_view(["GET"])
@renderer_classes([JSONRenderer])
def winners_list(request):
    winners_list = Winners.objects.all()
    
    data = []
    for winner in winners_list:
        
        winner_data = {
            "nin": winner.nin,
            "paiement":winner.payement,
            "visite_medicale":winner.visite,
            "hedj_info": None,
            "user_info": None
        }
        
        
        
        try:
            user_ = user.objects.get(id=winner.nin)
        except Haaj.DoesNotExist:
            user_ = None

        if user_:
            winner_data['user_info'] = {
                    'last_name': user_.last_name,
                    'first_name': user_.first_name,
                    'email': user_.email
                }
            
            
            try:
                haaj = Haaj.objects.get(user_id=user_.id)
            except Haaj.DoesNotExist:
                haaj = None
             
                
            if haaj and user_.gender == "F":
                
                
                winner_data['hedj_info']={
                    "maahram_id":haaj.maahram_id if haaj.maahram_id else None
                }
                
            
        data.append(winner_data)
    
    return JsonResponse({'users':data})
    
    
    
@api_view(["POST"])
@renderer_classes([JSONRenderer])
def delete_baladiya_role_assignement(request):
    user_id = request.data.get('user_id') 
    try:
        u = user.objects.get(id=user_id)
        baladiyet_to_delete = Baladiya.objects.filter(id_utilisateur=user_id)
        
        chosen_baladiya = request.data.get('chosen_baladiya')
        chosen_wilaya = request.data.get('chosen_wilaya') 
        
        if chosen_wilaya:
            baladiyet_to_delete = baladiyet_to_delete.filter(wilaya=chosen_wilaya) 
            for baladiya in baladiyet_to_delete :
                baladiya.id_utilisateur.remove(u) 
                
        elif chosen_baladiya:
            baladiyet_to_delete = baladiyet_to_delete.filter(name__iexact=chosen_baladiya) 
            for baladiya in baladiyet_to_delete :
                baladiya.id_utilisateur.remove(u)
            
        else:
            return Response({"error":"invalide input"})
        
        rest_baladiyet_count = Baladiya.objects.filter(id_utilisateur=user_id).count()
        if rest_baladiyet_count == 0:
            u.role = "user"
            u.save()
        
        return Response({"message":"association deleted"})
    
    except u.DoesNotExist:
        return Response({"error":"user not existe"})

@api_view(["POST"]) 
@renderer_classes([JSONRenderer])      
def add_hotel(request):
    serializer = hotelSerializer(data=request.data) 
    
    if serializer.is_valid():
        serializer.save()
        
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=404) 


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def add_vol(request):
    serializer = voleSerializer(data=request.data)  
    
    if serializer.is_valid():
        serializer.save()
       
        
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=404)            

@api_view(["POST"])
@renderer_classes([JSONRenderer])
def associate_winner_vol_hotel(request):
    winner_id = request.data.get('winner_id')
    vol_id = request.data.get('vol_id')
    hotel_id = request.data.get('hotel_id')

    try:
        winner = get_object_or_404(Winners, nin=winner_id)
    except Exception as e:
        return Response({"message": "Winner not found"}, status=404)
    
    if hotel_id:
        try:
            hotel_ = get_object_or_404(Hotel, id=hotel_id)
            hotel_.winner_id.add(winner.nin)
        except Exception as e:
            return Response({"message": "Hotel not found"}, status=404)

    if vol_id:
        try:
            vol_ = get_object_or_404(Vole, id=vol_id)
            vol_.winner_id.add(winner.nin)
        except Exception as e:
            return Response({"message": "Vole not found"}, status=404)



    return Response({"message": "association done"})
    

@api_view(["POST"])
@renderer_classes([JSONRenderer])
def delete_vol_hotel_association(request):
    winner_id = request.data.get('winner_id')
    vol_id = request.data.get('vol_id')
    hotel_id = request.data.get('hotel_id')


    try:
        winner = get_object_or_404(Winners, nin=winner_id)
    except Exception as e:
        return Response({"message": "Winner not found"}, status=404)
    
    if hotel_id:
        try:
            hotel_ = get_object_or_404(Hotel, id=hotel_id)
            hotel_.winner_id.remove(winner.nin)
        except Exception as e:
            return Response({"message": "Hotel not found"}, status=404)

    if vol_id:
        try:
            vol_ = get_object_or_404(Vole, id=vol_id)
            vol_.winner_id.remove(winner.nin)
        except Exception as e:
            return Response({"message": "Vole not found"}, status=404)



    return Response({"message": "association deleted"})
    


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def list_hotel(request):
    hotels = Hotel.objects.all()
    serialized_hotels=[]

    
    for h in hotels:
        serialized_hotel = {
        "nom":h.nom,
        "adress":h.adress
    }
        
        serialized_hotels.append(serialized_hotel)
        
    
    
    paginator = Paginator(serialized_hotels,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    serialized_page = [{"users":page_obj.object_list}]
    
    return JsonResponse({'pagination_info':{
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'hotels_per_page': paginator.per_page,
        'total_hotels': paginator.count
    }, 'users':serialized_page})
    
  
@api_view(["GET"])
@renderer_classes([JSONRenderer])
def list_vole(request):
    voles= Vole.objects.all()
    serialized_voles=[]

    
    for v in voles:
        serialized_vole= {
            "nom":v.nom,
            "aeroport":v.aeroprt,
            "heure_depart":v.heur_depart,
            "heure_arrivee":v.heur_arrivee,
            "date_arrivee":v.date_arrivee,
            "date_depart":v.date_depart,
            "nombre_de_places":v.nb_places
        }
        serialized_voles.append(serialized_vole)
        
    return Response(serialized_voles)
    
    
@api_view(["GET"])
@renderer_classes([JSONRenderer])
def winners_hotel_vol(request):
    winners_list = Winners.objects.all()
    
    data = []
    for winner in winners_list:
        hotel = Hotel.objects.filter(winner_id=winner.nin).first()
        vole = Vole.objects.filter(winner_id=winner.nin).first()
        
        hotel_name = hotel.nom if hotel else "No hotel assigned"
        vole_name = vole.nom if vole else "No vole assigned"
        
        winner_data = {
            "nin": winner.nin,
            "paiement":winner.payement,
            "visite_medicale":winner.visite,
            "vole": vole_name,
            "hotel": hotel_name
        }
            
        data.append(winner_data)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 3)  # Show 10 winners per page
    winners_page = paginator.page(page)
    
    response_data = {
        'pagination_info': {
            'total_pages': paginator.num_pages,
            'current_page': winners_page.number,
            'users_per_page': paginator.per_page,
            'total_users': paginator.count,
        },
        'users': list(winners_page)
    }
    
    return JsonResponse(response_data)



  
@api_view(["GET"])
@renderer_classes([JSONRenderer])
def responsable_users(request):
    user_id = request.data.get('user_id')
    user_ = get_object_or_404(user,id=user_id)
    
    associated_baladiyas = Baladiya.objects.filter(id_utilisateur=user_.id)
    
    baladiya_names = associated_baladiyas.values_list('name',flat=True)
    
    users_in_baladiyas = user.objects.filter(baladiya__name__in=baladiya_names).distinct()
    serialized_users = [{
        'id': user.id,
        'email': user.email,
        'role': user.role,
        'city': user.city,
        'province': user.province
    } for user in users_in_baladiyas]
    
    return Response({'users': serialized_users})

