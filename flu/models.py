from django.db import models
from django.utils import timezone

class FluStatistic(models.Model):
    """Model to store flu statistics that can be updated through admin"""
    season = models.CharField(max_length=20, default='2024-2025', help_text='Flu season (e.g., 2024-2025)')
    cases = models.CharField(max_length=20, default='43M', help_text='Number of symptomatic cases')
    deaths = models.CharField(max_length=20, default='38K', help_text='Number of deaths')
    hospitalizations = models.CharField(max_length=20, default='560K', help_text='Number of hospitalizations')
    severity = models.CharField(
        max_length=20, 
        choices=[
            ('Low', 'Low'),
            ('Moderate', 'Moderate'),
            ('High', 'High'),
        ],
        default='High'
    )
    notes = models.TextField(blank=True, help_text='Additional notes about the season')
    is_active = models.BooleanField(default=True, help_text='Set this to display on the website')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Flu Statistic'
        verbose_name_plural = 'Flu Statistics'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.season} Season Statistics"

    def save(self, *args, **kwargs):
        # Ensure only one active statistic at a time
        if self.is_active:
            FluStatistic.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class PreventionTip(models.Model):
    """Model for prevention tips"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=50, 
        default='flaticon-patient',
        help_text='Icon class name (e.g., flaticon-patient, flaticon-hand-washing)'
    )
    order = models.IntegerField(default=0, help_text='Display order (lower numbers appear first)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Prevention Tip'
        verbose_name_plural = 'Prevention Tips'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Symptom(models.Model):
    """Model for flu symptoms"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=100, 
        default='symptom_high-fever.png',
        help_text='Icon filename (e.g., symptom_high-fever.png)'
    )
    is_emergency = models.BooleanField(
        default=False, 
        help_text='Mark this if it requires immediate medical attention'
    )
    order = models.IntegerField(default=0, help_text='Display order (lower numbers appear first)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Symptom'
        verbose_name_plural = 'Symptoms'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class RiskGroup(models.Model):
    """Model for high-risk groups"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=50, 
        default='flaticon-patient',
        help_text='Icon class name'
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Risk Group'
        verbose_name_plural = 'Risk Groups'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class FAQItem(models.Model):
    """Model for Frequently Asked Questions"""
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General'),
            ('vaccination', 'Vaccination'),
            ('symptoms', 'Symptoms'),
            ('prevention', 'Prevention'),
        ],
        default='general'
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'FAQ Item'
        verbose_name_plural = 'FAQ Items'
        ordering = ['order', 'question']

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    """Model to store contact form submissions"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Inquiry'),
            ('vaccination', 'Vaccination Information'),
            ('symptoms', 'Symptoms Question'),
            ('prevention', 'Prevention Tips'),
            ('other', 'Other'),
        ]
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False, help_text='Mark as read after reviewing')
    replied = models.BooleanField(default=False, help_text='Mark as replied after responding')
    notes = models.TextField(blank=True, help_text='Internal notes about this message')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"