from django.shortcuts import render
from django.core.paginator import Paginator
from authentication.models import user
from registration.models import Winners,Baladiya,Haaj
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import hotelSerializer,voleSerializer
from django.shortcuts import get_object_or_404
from .models import Vole,Hotel
from rest_framework.renderers import JSONRenderer

# Create your views here.

@api_view(["GET"])
@renderer_classes([JSONRenderer])
def user_list(request):
    users_list = user.objects.all()
    paginator = Paginator(users_list, 10)
    
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    serialized_user = [{
        'id': u.id,
        'email': u.email,
        'role': u.role,
        'wilaya':u.province,
    }for u in users ]
    
    return JsonResponse({'users':serialized_user})

@api_view(["GET"])
@renderer_classes([JSONRenderer])
def search_user(request,email):
    try:
        u = user.objects.get(email__iexact=email)
            
        serialized_user = {
            'id': u.id,
            'email': u.email,
            'role': u.role,
            'wilaya':u.province,
        }
        return Response({'user':serialized_user})
        
            
    except user.DoesNotExist:
            return Response({'error':'user not found'})
 
 
@api_view(["POST"])  
@renderer_classes([JSONRenderer])     
def role_baladiyet_assignement(request):
    user_id = request.data.get('user_id') 
    try :
        u = user.objects.get(id=user_id)
        user_role = request.data.get('user_role')
        u.role = user_role
        u.save()
        
        chosen_baladiya = request.data.get('chosen_baladiya')
        chosen_wilaya = request.data.get('chosen_wilaya')
        
        
        
        if chosen_wilaya or chosen_baladiya:
            if chosen_wilaya:    
                baladiyets = Baladiya.objects.filter(wilaya=chosen_wilaya)
                
            else: 
                baladiyets = Baladiya.objects.filter(name__in=chosen_baladiya)
            
                
            for baladiya in baladiyets:
                baladiya.id_utilisateur.add(u)
            
        else:
            return Response({'error':'invalide input'})
        return Response({'message':'association done'})
    except u.DoesNotExist:
        return Response({'error':'user not found'})
    
  
@api_view(["GET"])
@renderer_classes([JSONRenderer])
def users_by_role_wilaya_baladiya(request):
    user_role = request.GET.get('user_role')  
    role_baladiya = request.GET.get('user_baladiya')
    role_wilaya = request.GET.get('user_wilaya')
    
    print("user_role:", user_role)
    print("role_baladiya:", role_baladiya)
    print("role_wilaya:", role_wilaya)

    
    serialized_users = []
    
    if user_role : 
        users = user.objects.filter(role=user_role)
        
    else:
        users = user.objects.all()
    for u in users:
        baladiyets_names = []
        baladiyets_wilaya = []
        
        if u.role in ["user", "hedj"] : 
                baladiyets_names = [u.city]
                baladiyets_wilaya = [u.province]
                
                if role_wilaya and role_wilaya !=u.province :
                    continue
                        
                if role_baladiya and role_baladiya!=u.city:
                    continue
                          
        else :
            baladiyets = Baladiya.objects.filter(id_utilisateur=u.id) 
        
            if role_wilaya or role_baladiya:
                if role_wilaya :
                    baladiyets = baladiyets.filter(wilaya=role_wilaya)
                
                if role_baladiya:
                    baladiyets = baladiyets.filter(name__iexact=role_baladiya)     
                
            baladiyets_names = [
                baladiya.name for baladiya in baladiyets
                ]
            baladiyets_wilaya = [
                list(set(baladiya.wilaya for baladiya in baladiyets))
                    ]
        
        
        if not(baladiyets_wilaya) or not(baladiyets_names):
            continue
            
            
            
        serialized_user = {
                'id': u.id,
                'email': u.email,
                'role': u.role,
                'wilaya':baladiyets_wilaya,
                "baladiyets":baladiyets_names
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

   
    
    