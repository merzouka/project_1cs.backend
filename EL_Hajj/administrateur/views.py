from django.shortcuts import render
from django.core.paginator import Paginator
from authentication.models import user
from registration.models import Baladiya
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db import transaction
# Create your views here.

@api_view(["GET"])
def user_list(request):
    users_list = user.objects.all()
    paginator = Paginator(users_list, 5)
    
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
def search_user(request,email):
    try:
        u = user.objects.get(email__iexact=email)
            
        serialized_user = {
            'id': u.id,
            'email': u.email,
            'role': u.role,
            'wilaya':u.province,
        }
        return JsonResponse({'user':serialized_user})
        
            
    except user.DoesNotExist:
            return JsonResponse({'error':'user not found'})
 
 
@api_view(["POST"])       
def role_baladiyet_assignement(request,user_id):
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
            return JsonResponse({'error':'invalide input'})
        return JsonResponse({'message':'association done'})
    except u.DoesNotExist:
        return JsonResponse({'error':'user not found'})
    
  
@api_view(["GET"])
def users_by_role_wilaya_baladiya(request):
    user_role = request.data.get('user_role')  
    role_baladiya = request.data.get('user_baladiya')
    role_wilaya = request.data.get('user_wilaya')
    
    serialized_users = []
    
    if user_role : 
        users = user.objects.filter(role=user_role)
        
    else:
        users = users = user.objects.all()
    for u in users:
        baladiyets = Baladiya.objects.filter(id_utilisateur=u.id)
           
        
        if role_wilaya or role_baladiya:
            if role_wilaya: 
                baladiyets = baladiyets.filter(wilaya=role_wilaya)
                
            if role_baladiya:
                baladiyets = baladiyets.filter(name__iexact=role_baladiya)     
            
        if baladiyets:        
            baladiyets_names = [
                    baladiya.name for baladiya in baladiyets
                ]
            baladiyets_wilaya = [
                    list(set(baladiya.wilaya for baladiya in baladiyets))
                    ]
            
            serialized_user = {
                'id': u.id,
                'email': u.email,
                'role': u.role,
                'wilaya':baladiyets_wilaya,
                "baladiyets":baladiyets_names
               }
            serialized_users.append(serialized_user)
            
    
    return JsonResponse({'users':serialized_users})
         

@api_view(["POST"])
def delete_baladiya_role_assignement(requset,user_id):
    try:
        u = user.objects.get(id=user_id)
        baladiyet_to_delete = Baladiya.objects.filter(id_utilisateur=user_id)
        
        chosen_baladiya = requset.data.get('chosen_baladiya')
        chosen_wilaya = requset.data.get('chosen_wilaya') 
        
        if chosen_wilaya:
            baladiyet_to_delete = baladiyet_to_delete.filter(wilaya=chosen_wilaya) 
            for baladiya in baladiyet_to_delete :
                baladiya.id_utilisateur.remove(u) 
                
        elif chosen_baladiya:
            baladiyet_to_delete = baladiyet_to_delete.filter(name__iexact=chosen_baladiya) 
            for baladiya in baladiyet_to_delete :
                baladiya.id_utilisateur.remove(u.id)
            
        else:
            return JsonResponse({"error":"invalide input"})
        
        rest_baladiyet_count = Baladiya.objects.filter(id_utilisateur=user_id).count()
        if rest_baladiyet_count == 0:
            u.role = "user"
            u.save()
        
        return JsonResponse({"message":"association deleted"})
    
    except u.DoesNotExist:
        return JsonResponse({"error":"user not existe"})
            
        
                
            
            