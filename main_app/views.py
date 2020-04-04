from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.core import serializers

from . import models

def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    context = {}
    next_level = []
    
    if request.method == 'POST':
        reliefAmount = int(request.POST.get('relief_amount'))
        reliefTo = request.POST.get('relief_to')
        donateTo = request.POST.get('donate_to')

        sender = request.session.get('user_type')
        nid = request.session.get('nid')
        # ministry_relif
        # city_meyor
        # district_comissioner
        # upazila_officer
        # upazila_uno
        # ward_comissioner
        if sender == 'ministry_relif':
            obj = models.ministry_relief.objects.get(nid=nid)
            if obj.relief_quantity - int(reliefAmount) < 0:
                context['Error'] = "Insufficient Relief In This Account. Current Stock {}".format(obj.relief_quantity)
            else:
                dObj = None
                try:
                    dObj = models.district_comissioner.objects.get(nid=donateTo)
                    obj.relief_quantity -= reliefAmount
                    dObj.relief_quantity += reliefAmount
                    obj.save()
                    dObj.save()
                    context['Success'] = "Donation Operation Successful"
                except:
                    try:
                        dObj = models.city_meyor.objects.get(nid=donateTo)
                        obj.relief_quantity -= reliefAmount
                        dObj.relief_quantity += reliefAmount 
                        obj.save()
                        dObj.save()
                        context['Success'] = "Donation Operation Successful"
                    except:
                        context['Error'] = "An Unknow Error Happened"
                

        elif sender == 'city_meyor':
            obj = models.city_meyor.objects.get(nid=nid)
            if obj.relief_quantity - int(reliefAmount) < 0:
                context['Error'] = "Insufficient Relief In This Account. Current Stock {}".format(obj.relief_quantity)
            else:
                try:
                    dObj = models.word_comissioner.objects.get(nid=donateTo)
                    obj.relief_quantity -= reliefAmount
                    dObj.relief_quantity += reliefAmount 
                    obj.save()
                    dObj.save()
                    context['Success'] = "Donation Operation Successful"
                except:
                    context['Error'] = "An Unknow Error Happened"

        elif sender == 'district_comissioner':
            obj = models.district_comissioner.objects.get(nid=nid)
            if obj.relief_quantity - int(reliefAmount) < 0:
                context['Error'] = "Insufficient Relief In This Account. Current Stock {}".format(obj.relief_quantity)
            else:
                try:
                    dObj = models.upazila_officer.objects.get(nid=donateTo)
                    obj.relief_quantity -= reliefAmount
                    dObj.relief_quantity += reliefAmount 
                    obj.save()
                    dObj.save()
                    context['Success'] = "Donation Operation Successful"
                except:
                    context['Error'] = "An Unknow Error Happened"

        elif sender == 'upazila_officer':
            obj = models.upazila_officer.objects.get(nid=nid)
            if obj.relief_quantity - int(reliefAmount) < 0:
                context['Error'] = "Insufficient Relief In This Account. Current Stock {}".format(obj.relief_quantity)
            else:
                try:
                    dObj = models.upazila_uno.objects.get(nid=donateTo)
                    obj.relief_quantity -= reliefAmount
                    dObj.relief_quantity += reliefAmount 
                    obj.save()
                    dObj.save()
                    context['Success'] = "Donation Operation Successful"
                except:
                    context['Error'] = "An Unknow Error Happened"

        elif sender == 'upazila_uno':
            obj = models.upazila_uno.objects.get(nid=nid)
            if obj.relief_quantity - int(reliefAmount) < 0:
                context['Error'] = "Insufficient Relief In This Account. Current Stock {}".format(obj.relief_quantity)
            else:
                try:
                    dObj = models.relief_consumer.objects.get(nid=donateTo)
                    obj.relief_quantity -= reliefAmount
                    dObj.relief_quantity += reliefAmount 
                    obj.save()
                    dObj.save()
                    context['Success'] = "Donation Operation Successful"
                except:
                    context['Error'] = "An Unknow Error Happened"


        elif sender == 'ward_comissioner':
            obj = models.word_comissioner.objects.get(nid=nid)
            if obj.relief_quantity - int(reliefAmount) < 0:
                context['Error'] = "Insufficient Relief In This Account. Current Stock {}".format(obj.relief_quantity)
            else:
                try:
                    dObj = models.relief_consumer.objects.get(nid=donateTo)
                    obj.relief_quantity -= reliefAmount
                    dObj.relief_quantity += reliefAmount 
                    obj.save()
                    dObj.save()
                    context['Success'] = "Donation Operation Successful"
                except:
                    context['Error'] = "An Unknow Error Happened"
        else:
            pass

    # Ministry
    try:
        tuser = models.ministry_relief.objects.get(user=request.user)
        context["next"] = ['District Comissioner', 'City Meyor']
        return render(request, 'main_app/home.html', context)
    except:
        pass

    # District Comissioner
    try:
        tuser = models.district_comissioner.objects.get(user=request.user)
        context["next"] = ['Upazila Officer']
        return render(request, 'main_app/home.html', context)
    except:
        pass

    # City Meyor
    try:
        tuser = models.city_meyor.objects.get(user=request.user)
        context["next"] = ['Ward Commissioner']
        return render(request, 'main_app/home.html', context)
    except:
        pass

    # Upazila Officer
    try:
        tuser = models.upazila_officer.objects.get(user=request.user)
        context["next"] = ['Upazila Uno']
        return render(request, 'main_app/home.html', context)
    except:
        pass

    # Word Comissioner
    try:
        tuser = models.word_comissioner.objects.get(user=request.user)
        context["next"] = ['Relief Consumer']
        return render(request, 'main_app/home.html', context)
    except:
        pass

    # Upazila Uno
    try:
        tuser = models.upazila_uno.objects.get(user=request.user)
        context["next"] = ['Relief Consumer']
        return render(request, 'main_app/home.html', context)
    except:
        pass

    return render(request, 'main_app/home.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def login(request):
    error = {}
    if request.method == 'POST':
        nid = request.POST.get('nid')
        password = request.POST.get('password')
        
        #minstry check
        try:
            usertemp = models.ministry_relief.objects.get(nid=nid)
            user = authenticate(username=usertemp.user.username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    request.session['user_type'] = 'ministry_relif'
                    request.session['nid'] = nid
                    return HttpResponseRedirect(reverse('home'))
                else:
                    error['Message'] = 'Account Disabled'
                    return render(request, 'main_app/login.html', error)
            else:
                error['Message'] = 'Invalid NID or Password'
                render(request, 'main_app/login.html', error)
        except models.ministry_relief.DoesNotExist:
            pass

        #Meyor check
        try:
            usertemp = models.city_meyor.objects.get(nid=nid)
            user = authenticate(username=usertemp.user.username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    request.session['user_type'] = 'city_meyor'
                    request.session['nid'] = nid
                    return HttpResponseRedirect(reverse('home'))
                else:
                    error['Message'] = 'Account Disabled'
                    return render(request, 'main_app/login.html', error)
            else:
                error['Message'] = 'Invalid NID or Password'
                render(request, 'main_app/login.html', error)
        except models.city_meyor.DoesNotExist:
            pass

        #DC check
        try:
            usertemp = models.district_comissioner.objects.get(nid=nid)
            user = authenticate(username=usertemp.user.username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    request.session['user_type'] = 'district_comissioner'
                    request.session['nid'] = nid
                    return HttpResponseRedirect(reverse('home'))
                else:
                    error['Message'] = 'Account Disabled'
                    return render(request, 'main_app/login.html', error)
            else:
                error['Message'] = 'Invalid NID or Password'
                render(request, 'main_app/login.html', error)
        except models.district_comissioner.DoesNotExist:
            pass

        
        #Upozila officer check
        try:
            usertemp = models.upazila_officer.objects.get(nid=nid)
            user = authenticate(username=usertemp.user.username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    request.session['user_type'] = 'upazila_officer'
                    request.session['nid'] = nid
                    return HttpResponseRedirect(reverse('home'))
                else:
                    error['Message'] = 'Account Disabled'
                    return render(request, 'main_app/login.html', error)
            else:
                error['Message'] = 'Invalid NID or Password'
                render(request, 'main_app/login.html', error)
        except models.upazila_officer.DoesNotExist:
            pass

        
        #Upazila uno check
        try:
            usertemp = models.upazila_uno.objects.get(nid=nid)
            user = authenticate(username=usertemp.user.username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    request.session['user_type'] = 'upazila_uno'
                    request.session['nid'] = nid
                    return HttpResponseRedirect(reverse('home'))
                else:
                    error['Message'] = 'Account Disabled'
                    return render(request, 'main_app/login.html', error)
            else:
                error['Message'] = 'Invalid NID or Password'
                render(request, 'main_app/login.html', error)
        except models.upazila_uno.DoesNotExist:
            pass

        #Word Comissioner check
        try:
            usertemp = models.word_comissioner.objects.get(nid=nid)
            user = authenticate(username=usertemp.user.username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    request.session['user_type'] = 'ward_comissioner'
                    request.session['nid'] = nid
                    return HttpResponseRedirect(reverse('home'))
                else:
                    error['Message'] = 'Account Disabled'
                    return render(request, 'main_app/login.html', error)
            else:
                error['Message'] = 'Invalid NID or Password'
                render(request, 'main_app/login.html', error)
        except models.word_comissioner.DoesNotExist:
            pass

        error['Message'] = 'Invalid NID or Password'
        render(request, 'main_app/login.html', error)


    return render(request, 'main_app/login.html', error)

# District Comissioner
# City Meyor
# Upazila Officer
# Ward Commissioner
# Upazila Uno
# Relief Consumer

def userList(request):
    user_type = request.GET.get('user_type')

    if user_type == 'District Comissioner':
        data = models.district_comissioner.objects.all()
        data = serializers.serialize('json', data, use_natural_foreign_keys=True)
        return HttpResponse(data, content_type="application/json")
    if user_type == 'City Meyor':
        data = models.city_meyor.objects.all()
        data = serializers.serialize('json', data, use_natural_foreign_keys=True)
        return HttpResponse(data, content_type="application/json")
    if user_type == 'Upazila Officer':
        data = models.upazila_officer.objects.all()
        data = serializers.serialize('json', data, use_natural_foreign_keys=True)
        return HttpResponse(data, content_type="application/json")
    if user_type == 'Ward Commissioner':
        data = models.word_comissioner.objects.all()
        data = serializers.serialize('json', data, use_natural_foreign_keys=True)
        return HttpResponse(data, content_type="application/json")
    if user_type == 'Upazila Uno':
        data = models.upazila_uno.objects.all()
        data = serializers.serialize('json', data, use_natural_foreign_keys=True)
        return HttpResponse(data, content_type="application/json")
    if user_type == 'Relief Consumer':
        data = models.relief_consumer.objects.all()
        data = serializers.serialize('json', data, use_natural_foreign_keys=True)
        return HttpResponse(data, content_type="application/json")
    else:
        return JsonResponse(status=404, data={'status': 'false'})
