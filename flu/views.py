from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (
    FluStatistic, 
    PreventionTip, 
    Symptom, 
    RiskGroup, 
    FAQItem, 
    ContactMessage
)

def index(request):
    """Home page view"""
    # Get active statistics from database
    try:
        stats = FluStatistic.objects.filter(is_active=True).first()
        stats_data = {
            'cases': stats.cases if stats else '43M',
            'deaths': stats.deaths if stats else '38K',
            'hospitalizations': stats.hospitalizations if stats else '560K',
        }
    except:
        # Fallback to default values if database isn't set up yet
        stats_data = {
            'cases': '43M',
            'deaths': '38K',
            'hospitalizations': '560K',
        }
    
    context = {
        'page_title': 'Flu Prevention & Information',
        'stats': stats_data,
    }
    return render(request, 'flu/index.html', context)

def prevention(request):
    """Prevention tips page view"""
    # Get active prevention tips from database
    prevention_tips = PreventionTip.objects.filter(is_active=True).order_by('order')
    
    # Get statistics
    try:
        stats = FluStatistic.objects.filter(is_active=True).first()
        stats_data = {
            'cases': stats.cases if stats else '43M',
            'deaths': stats.deaths if stats else '38K',
            'hospitalizations': stats.hospitalizations if stats else '560K',
        }
    except:
        stats_data = {
            'cases': '43M',
            'deaths': '38K',
            'hospitalizations': '560K',
        }
    
    # Convert to list of dicts for template
    tips_list = [
        {
            'title': tip.title,
            'description': tip.description,
            'icon': tip.icon
        }
        for tip in prevention_tips
    ]
    
    context = {
        'prevention_tips': tips_list,
        'stats': stats_data,
    }
    return render(request, 'flu/prevention.html', context)

def symptoms(request):
    """Symptoms information page view"""
    # Get active symptoms from database
    symptoms = Symptom.objects.filter(is_active=True).order_by('order')
    
    # Separate regular and emergency symptoms
    regular_symptoms = symptoms.filter(is_emergency=False)
    emergency_symptoms = symptoms.filter(is_emergency=True)
    
    # Convert to list of dicts for template
    symptoms_list = [
        {
            'name': symptom.name,
            'description': symptom.description,
            'icon': symptom.icon
        }
        for symptom in regular_symptoms
    ]
    
    emergency_list = [symptom.name for symptom in emergency_symptoms]
    
    context = {
        'symptoms': symptoms_list,
        'emergency_symptoms': emergency_list,
    }
    return render(request, 'flu/symptoms.html', context)

def about(request):
    """About flu page view"""
    # Get statistics
    try:
        stats = FluStatistic.objects.filter(is_active=True).first()
        stats_data = {
            'cases': stats.cases if stats else '43M',
            'deaths': stats.deaths if stats else '38K',
            'hospitalizations': stats.hospitalizations if stats else '560K',
        }
        season_info = {
            'year': stats.season if stats else '2024-2025',
            'severity': stats.severity if stats else 'High',
            'note': stats.notes if stats and stats.notes else 'Most severe influenza season since 2017-18',
        }
    except:
        stats_data = {
            'cases': '43M',
            'deaths': '38K',
            'hospitalizations': '560K',
        }
        season_info = {
            'year': '2024-2025',
            'severity': 'High',
            'note': 'Most severe influenza season since 2017-18',
        }
    
    # Get risk groups from database
    risk_groups = RiskGroup.objects.filter(is_active=True).order_by('order')
    risk_groups_list = [
        {
            'name': group.name,
            'description': group.description,
            'icon': group.icon
        }
        for group in risk_groups
    ]
    
    # Get FAQ items
    faq_items = FAQItem.objects.filter(is_active=True, category='general').order_by('order')
    vaccination_facts = [
        {
            'question': faq.question,
            'answer': faq.answer
        }
        for faq in faq_items
    ]
    
    context = {
        'stats': stats_data,
        'season_info': season_info,
        'risk_groups': risk_groups_list,
        'flu_types': [
            {
                'name': 'Influenza A',
                'description': 'The most common type that causes seasonal epidemics. Can infect humans and animals.',
                'subtypes': ['H1N1', 'H3N2'],
            },
            {
                'name': 'Influenza B',
                'description': 'Only infects humans. Generally less severe but can still cause significant illness.',
                'lineages': ['B/Yamagata', 'B/Victoria'],
            },
        ],
        'vaccination_facts': vaccination_facts,
    }
    return render(request, 'flu/about.html', context)

def contact(request):
    """Contact form page view"""
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '')
        message_text = request.POST.get('message', '').strip()
        
        # Basic validation
        errors = []
        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if not email:
            errors.append('Email is required')
        if not subject:
            errors.append('Subject is required')
        if not message_text:
            errors.append('Message is required')
        
        if errors:
            context = {
                'errors': errors,
                'form_data': {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'subject': subject,
                    'message': message_text,
                }
            }
            return render(request, 'flu/contact.html', context)
        
        # Save to database
        try:
            ContactMessage.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                subject=subject,
                message=message_text
            )
            
            # Add success message
            messages.success(
                request, 
                f'{first_name}様、お問い合わせありがとうございます。できるだけ早くご返信いたします。'
                )
        except Exception as e:
            messages.error(
                request,
                '申し訳ございません。メッセージの送信中にエラーが発生しました。もう一度お試しください。'
            )
        
        # Redirect to avoid form resubmission
        return redirect('flu:contact')
    
    # GET request - show the form
    # Get FAQ items from database
    faq_items = FAQItem.objects.filter(is_active=True).order_by('order')[:4]
    faq_list = [
        {
            'question': faq.question,
            'answer': faq.answer
        }
        for faq in faq_items
    ]
    
    context = {
        'page_title': 'Contact Us - Flu Prevention & Information',
        'subject_options': [
            {'value': 'general', 'label': 'General Inquiry'},
            {'value': 'vaccination', 'label': 'Vaccination Information'},
            {'value': 'symptoms', 'label': 'Symptoms Question'},
            {'value': 'prevention', 'label': 'Prevention Tips'},
            {'value': 'other', 'label': 'Other'},
        ],
        'faq_items': faq_list,
    }
    return render(request, 'flu/contact.html', context)