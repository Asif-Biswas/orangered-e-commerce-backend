
from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.decorators import authentication_classes
from .serializers import *
import json
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes

# Create your views here.

@api_view(['POST'])
def getCategoryProduct(request):
    list = []
    excludeId = request.data['list']
    excludeId = json.loads(excludeId)
    if len(excludeId) != 0:
        list = list + excludeId
    
    category = Category.objects.all().order_by('?').exclude(id__in=list)[:1]

    product = Product.objects.filter(category=category).order_by('?')[:10]
    serializer = ProductSerializer(product, many=True, context={"request": request})

    return Response(serializer.data)


@api_view(['POST'])
def getProduct(request):
    '''companyList = []
    categoryList = []'''

    excludeCompanyId = request.data['companyList']
    excludeCompanyId = json.loads(excludeCompanyId)

    excludeCategoryId = request.data['categoryList']
    excludeCategoryId = json.loads(excludeCategoryId)


    #myCart, __ = Cart.objects.get_or_create(user=request.user)
    #cartItem = myCart.product.all() 

    '''if len(excludeCompanyId) != 0:
        companyList = companyList + excludeCompanyId
    if len(excludeCategoryId) != 0:
        categoryList = categoryList + excludeCategoryId'''
    
    try:
        category = Category.objects.all().exclude(id__in=excludeCategoryId).order_by('?').first()
        categoryName = category.name
        categoryProduct = Product.objects.filter(category=category).order_by('?')[:10]
        #print(categoryProduct)
        categorySerializer = ProductSerializer(categoryProduct, many=True, context={"request": request}).data
    except:
        categorySerializer = {}
        categoryName = ''

    try:
        company = Company.objects.all().exclude(id__in=excludeCompanyId).order_by('?').first()
        companyName = company.name
        companyProduct = Product.objects.filter(company=company).order_by('?')[:10]
        #print(companyProduct[0].company)
        #for i in companyProduct:
        #    print(i.company)
        companySerializer = ProductSerializer(companyProduct, many=True, context={"request": request}).data
    except:
        companySerializer = {}
        companyName = ''

    resp = [{'name': categoryName, 'data': categorySerializer}, {'name': companyName, 'data': companySerializer}]
    return Response(resp)
#{"companyList":"[]","categoryList":"[]"}

@api_view(['POST'])
def getCompanyProduct(request):
    #list = []
    excludeId = request.data['l']
    excludeId = json.loads(excludeId)
    
    company = Company.objects.all().exclude(id__in=excludeId).order_by('?').first()
    print(company)
    #product = Product.objects.filter(company=company).order_by('?')[:10]
    #serializer = ProductSerializer(product, many=True, context={"request": request})

    return Response({'r':'r'})


@api_view(['GET'])
def forYou(request):
    #print(request.session.session_key)
    product = Product.objects.all().order_by('?')[:10]
    serializer = ProductSerializer(product, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(['GET'])
def getCategoryName(request):
    category = Category.objects.all().order_by('?')
    company = Company.objects.all().order_by('?')
    categorySerializer = CategorySerializer(category, many=True)
    companySerializer = CompanySerializer(company, many=True)

    

    resp = {'category': categorySerializer.data, 'company': companySerializer.data}
    return Response(resp)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
#@permission_classes((IsAuthenticated,))
def youMayLikeOnCart(request):
    user = request.user
    companyList = []
    categoryList = []
    mycart, __ = Cart.objects.get_or_create(user=user)
    if mycart.product.exists():
        for i in mycart.product.all():
            companyList.append(i.company)
            categoryList.append(i.category.first())
    else:
        companyList.append(Company.objects.all().order_by('?').first())
        categoryList.append(Category.objects.all().order_by('?').first())

    companyList = set(companyList)
    categoryList = set(categoryList)

    companyItems = Product.objects.filter(company__in=companyList).order_by('?')[:10]
    categoryItems = Product.objects.filter(category__in=categoryList).order_by('?')[:10]
    
    categorySerializer = ProductSerializer(categoryItems, many=True, context={"request": request}).data
    companySerializer = ProductSerializer(companyItems, many=True, context={"request": request}).data

    categoryName = 'You may like'
    companyName = 'You may also like'
    
    resp = [{'name': categoryName, 'data': categorySerializer}, {'name': companyName, 'data': companySerializer}]
    #print(resp)
    return Response(resp)

@api_view(['GET'])
#@authentication_classes([TokenAuthentication])
def productDetails(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, context={"request": request})
    return Response(serializer.data)


#@permission_classes((IsAuthenticated,))
@api_view(['GET'])
@authentication_classes([TokenAuthentication,])
def addToCart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    mycart, __ = Cart.objects.get_or_create(user=request.user)
    mycart.product.add(product)
    

    return Response({'response':'ok'})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def myAllCartItems(request):
    mycart, __ = Cart.objects.get_or_create(user=request.user)
    if not mycart.product.exists():
        return Response({'response':'noItem'})
    else:
        my_product = mycart.product.all()
        quantity = 1
        for i in my_product:
            if Quantity.objects.filter(user=request.user, product=i).exists():
                quantity = Quantity.objects.get(user=request.user, product=i).quantity
            
            i.quantity = quantity
        serializer = ProductSerializer(my_product, many=True, context={"request": request})
        return Response(serializer.data)

#@permission_classes((IsAuthenticated,))
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def totalItemInCart(request):
    mycart, __ = Cart.objects.get_or_create(user=request.user)
    total = mycart.product.all().count()
    return Response({'totalItemInCart': total})


#@permission_classes((IsAuthenticated,))
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def myCartDetails(request):
    def cartDetails(mycart):
        if not mycart.product.exists():
            return ({'response':'noItem'})
        else:
            my_product = mycart.product.all()
            #serializer = ProductSerializer(my_product, many=True, context={"request": request}).data
            
            totalItem = my_product.count()
            total = 0
            totalNow = 0
            for i in my_product:
                price = i.price
                quantity = 1
                if Quantity.objects.filter(user=request.user, product=i).exists():
                    quantity = Quantity.objects.get(user=request.user, product=i).quantity
                    
                total += i.price * quantity
                discount = i.discount
                priceNow = price - int(price*discount/100)
                totalNow += priceNow * quantity

            saving = total - totalNow
            
            resp = [{'total': totalNow, 'saving': saving, 'totalItem': totalItem}]

            return resp

    mycart, __ = Cart.objects.get_or_create(user=request.user)
    return Response(cartDetails(mycart))
    '''if request.user.is_authenticated:
        mycart, __ = Cart.objects.get_or_create(user=request.user)
        return Response(cartDetails(mycart))
    else:
        mycart, __ = Cart.objects.get_or_create(session_key=request.session.session_key)
        return Response(cartDetails(mycart))'''
    #return Response({'response':'ok'})        

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def deleteCartItem(request, pk):
    if Quantity.objects.filter(user=request.user, product = Product.objects.get(id=pk)).exists():
        Quantity.objects.get(user=request.user, product = Product.objects.get(id=pk)).delete()
    def reducerFunction(mycart, pk):
        if mycart.product.filter(pk=pk).exists():
            mycart.product.remove(pk)
            return ({'response':'deleted'})
        else:
            return ({'response':'deleted'})

    if request.user.is_authenticated:
        mycart, __ = Cart.objects.get_or_create(user=request.user)
        return Response(reducerFunction(mycart, pk))
    else:
        mycart, __ = Cart.objects.get_or_create(session_key=request.session.session_key)
        return Response(reducerFunction(mycart, pk))
    #return Response({'response':'ok'}) 

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def undoDeletedCartItem(request, pk):
    def reducerFunction(mycart, pk):
        if mycart.product.filter(pk=pk).exists():
            return ({'response':'ok'})
        else:
            mycart.product.add(pk)
            return ({'response':'ok'})

    if request.user.is_authenticated:
        mycart, __ = Cart.objects.get_or_create(user=request.user)
        return Response(reducerFunction(mycart, pk))
    else:
        mycart, __ = Cart.objects.get_or_create(session_key=request.session.session_key)
        return Response(reducerFunction(mycart, pk))
    #return Response({'response':'ok'})



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def myDetails(request):
    user = request.user
    if user.is_authenticated:
        full_name = ''
        if len(user.first_name)>0:
            full_name = user.first_name + ' ' + user.last_name
        email = user.email
    else:
        full_name = request.session.get('full_name')
        email = request.session.get('email')
    full_address = request.session.get('full_address')
    phone = request.session.get('phone')
    serializer = {'full_name': full_name, 'full_address': full_address, 'email': email, 'phone': phone}
    return Response(serializer)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def purchase(request):
    if request.user.is_authenticated:
        Quantity.objects.filter(user=request.user).delete()
        mycart, __ = Cart.objects.get_or_create(user=request.user)
        if mycart.product.exists():
            mycart.product.clear()
            return Response({'response':'clear'})
    else:
        mycart, __ = Cart.objects.get_or_create(session_key=request.session.session_key)
        if mycart.product.exists():
            mycart.product.clear()
            return Response({'response':'clear'})
    
    return Response({'response':'noItem'})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def increaseQuantity(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    quantity, __ = Quantity.objects.get_or_create(user=user, product=product)
    quantity.quantity = quantity.quantity + 1
    quantity.save()
    return Response({'response':'increased'})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def decreaseQuantity(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    quantity, __ = Quantity.objects.get_or_create(user=user, product=product)
    quantity.quantity = quantity.quantity - 1
    quantity.save()
    return Response({'response':'decreased'})


@api_view(['GET'])
def search(request, str):
    r = Product.objects.filter(Q(name__icontains=str) | Q (company__name__icontains=str) | Q (category__name__icontains=str))#.filter().filter()
    serializer = ProductSerializer(r, many=True, context={"request": request})
    return Response(serializer.data)

















@api_view(['GET'])
def home(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

#def access(request):
#    return render(request, 'home.html')

def handleLike(request):
    likes = request.session.get('likes', 0)
    request.session['likes'] = likes+1
    return JsonResponse({'likes': likes+1})

def getLikes(request):
    likes = request.session.get('likes', 0)
    print(request.session.session_key)
    print(likes)
    return JsonResponse({'likes': likes})

'''class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''


