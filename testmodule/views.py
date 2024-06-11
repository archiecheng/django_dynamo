from django.shortcuts import render

# Create your views here.
# testmodule/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Item
import json

item_model = Item()

from django.shortcuts import render

def item_form(request):
    return render(request, 'item_form.html')

@require_http_methods(["POST"])
def create_item(request):
    data = json.loads(request.body)
    item_id = data['item_id']
    name = data['name']
    description = data['description']
    response = item_model.create_item(item_id, name, description)
    return JsonResponse(response)

@require_http_methods(["GET"])
def get_item(request, item_id):
    item = item_model.get_item(item_id)
    if item:
        return JsonResponse(item)
    else:
        return JsonResponse({'error': 'Item not found'}, status=404)

@require_http_methods(["PUT"])
def update_item(request, item_id):
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    response = item_model.update_item(item_id, name, description)
    return JsonResponse(response)

@require_http_methods(["DELETE"])
def delete_item(request, item_id):
    response = item_model.delete_item(item_id)
    return JsonResponse(response)
