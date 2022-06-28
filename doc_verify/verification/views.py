from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from .verification_process import Verification
from django.views.generic import CreateView
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from .forms import DocumentForm
from .models import Document

# Create your views here.
def document_view(request):
    
    if 'upload' in request.POST:
        
        # Upload
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                doc = form.save()
                verif = Verification(request, doc)
                verif.hash_data()
                tx_hash = verif.upload_hash()
                
                messages.success(request, f'https://mumbai.polygonscan.com/tx/{tx_hash}')
                
            except IntegrityError:
                raise ValidationError("Validation Errorr")
            
        else:
            form = DocumentForm()
        
        context = {
            'form': form,
        }
        
        return render(request, "verification/home.html", context)

    else:
        
        # Verify
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # print(request.FILES['document'].read())
                verif = Verification(request, file=request.FILES['document'])
                verif.hash_data()
                flag = verif.verify_hash()
                
                if flag:
                    messages.success(request, f'Document verified!')
                else:
                    messages.error(request, f'Document cannot be verified!')
                
            except IntegrityError:
                raise ValidationError("Validation Errorr")
        else:
            form = DocumentForm()

        context = {
            'form': form,
        }
        
        return render(request, "verification/home.html", context)
            
        # return render(request, "verification/home.html")    
        