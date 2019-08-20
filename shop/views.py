from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json
#from django.views.decorators.csrf import csrf_exempt
#from paytm import checksum
#MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
# Create your views here.
def index(request):
	#products=Product.objects.all()
	#n=len(products)
	#nSlides=n//4 + ceil((n/4)-(n//4))
	#params={'no_of_slides':nSlides,'range':range(1,nSlides),'products':products}
	# used for categorisation
	#allProds=[[products,range(1,nSlides),nSlides],[products,range(1,nSlides),nSlides]]
	allProds=[]
	catprods=Product.objects.values('category','id')
	cats={item['category'] for item in catprods}
	for cat in cats:
		prod=Product.objects.filter(category=cat)
		n=len(prod)
		nSlides=n//4 + ceil((n/4)-(n//4))
		allProds.append([prod,range(1,nSlides),nSlides])
	
	params={'allProds':allProds}
	return render(request,'shop/index.html',params)
def searchmatch(query,item):
	if query in item.desc or query in item.product_name or query in item.category:
		return True
	else:
		return False

def search(request):
	query=request.GET.get('search')
	allProds=[]
	catprods=Product.objects.values('category','id')
	cats={item['category'] for item in catprods}
	for cat in cats:
		prodtemp=Product.objects.filter(category=cat)
		prod=[item for item in prodtemp if searchmatch(query,item)]
		n=len(prod)
		nSlides=n//4 + ceil((n/4)-(n//4))
		if len(prod)!=0:
			allProds.append([prod,range(1,nSlides),nSlides])
	
	params={'allProds':allProds,'msg':''}
	if len(allProds)==0 or len(query)<4:
		params={'msg':'please enter correct spelling of product to be searched'}
	return render(request,'shop/index.html',params)

def about(request):
	return render(request,'shop/about.html')


def contact(request):
	thank=False
	if(request.method=="POST"):
		print(request)
		name=request.POST.get('name','default')
		email=request.POST.get('email','default')
		query=request.POST.get('query','default')
		thank=True
		contact=Contact(name=name,email=email,desc=query)
		contact.save()
	return render(request,'shop/contact.html',{'thank':thank})


def tracker(request):
	if(request.method=="POST"):
		orderid=request.POST.get('orderid','default')
		email=request.POST.get('email','default')
		try:
			order=Orders.objects.filter(order_id=orderid,email=email)
			if(len(order)>0):
				update=OrderUpdate.objects.filter(order_id=orderid)
				updates=[]
				for item in update:
					updates.append({'text1':item.update_desc,'time':item.timestamp})
					response=json.dumps({"status":"success","updates":updates,"item_json":order[0].items_json},default=str)
				return HttpResponse(response)
			else:
				return HttpResponse('{"status":"noitem"}')
		except:
			return HttpResponse('{"status":"error"}')


	return render(request,'shop/tracker.html')




def productview(request,myid):
	product=Product.objects.filter(id=myid)
	#above product contains list i.e. why niche [0] use kiya hai
	return render(request,'shop/productview.html',{'product':product[0]})


def checkout(request):
	if(request.method=="POST"):
		print(request)
		name=request.POST.get('name','default')
		amount=request.POST.get('amount')
		items=request.POST.get('itemjson','default')
		email=request.POST.get('email','default')
		address=request.POST.get('address1','default')
		address1=request.POST.get('address2','default')
		city=request.POST.get('city','default')
		state=request.POST.get('state','default')
		zip_code=request.POST.get('zip_code','default')
		order=Orders(items_json=items,name=name,amount=amount,email=email,address=address,address1=address1,city=city,state=state,zip_code=zip_code)
		order.save()
		update=OrderUpdate(order_id=order.order_id,update_desc="Your Order has been placed")
		update.save()
		thank=True
		id=order.order_id
		return render(request,'shop/checkout.html',{'thank':thank,'id':id})
		#request paytm to transfer amount to your account after payment by user
		#param_dict = {
         #   'MID':'WorldP64425807474247',
         #   'ORDER_ID':id,
         #   'TXN_AMOUNT':str(amount),
         #   'CUST_ID':email,
         #   'INDUSTRY_TYPE_ID':'Retail',
          #  'WEBSITE':'WEBSTAGING',
         #   'CHANNEL_ID':'WEB',
	    #	'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest',
       # }
        #param_dict['CHECKSUMHASH']=checksum.generate_checksum(param_dict,MERCHANT_KEY)
        #return render(request,'shop/paytm.html',{'param_dict':param_dict})
	return render(request,'shop/checkout.html')

#@csrf_exempt
#def handlerequest(request):
	#return(HttpResponse('done'))
	#pass
	#