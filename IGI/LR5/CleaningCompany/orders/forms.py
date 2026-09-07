import datetime
from datetime import timedelta
from django import forms
from django.core.exceptions import ValidationError
from services.models import Service
from users.models import User

class OrderCreateForm(forms.Form):
    address = forms.CharField(label='Address', max_length=120)
    work_date = forms.DateField(label='Work Date', widget=forms.DateInput(attrs={'type': 'date'}))
    promo_code = forms.CharField(label='Promo Code', max_length=120, required=False)
    employee = forms.ModelChoiceField(queryset=User.objects.filter(user_type='employee'))

    def __init__(self, *args, **kwargs):
        cart = kwargs.pop('cart', {})
        super().__init__(*args, **kwargs)

        services = Service.objects.all()
        for service in services:
            initial_quantity = cart.get(str(service.id), 0)

            self.fields[f'quantity_{service.id}'] = forms.IntegerField(
                min_value=0,
                initial=initial_quantity,
                label=f'{service.name} ({service.price}) BYN',
            )

        self.fields['address'].widget.attrs['required'] = True
        self.fields['work_date'].widget.attrs['required'] = True
        self.fields['employee'].label_from_instance = lambda employee: f"{employee.get_full_name()} - {', '.join(s.name for s in employee.employee_profile.specializations.all())}"

    def clean_work_date(self):
        work_date = self.cleaned_data['work_date']
        if work_date < datetime.date.today():
            raise ValidationError("Date can't be in the past")
        if work_date > datetime.date.today() + timedelta(days=30):
            raise ValidationError("You can't order more than 30 days ahead")
        return work_date

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        if employee:
            specializations = set(employee.employee_profile.specializations.all())
            for field_name, quantity in cleaned_data.items():
                if field_name.startswith('quantity_') and quantity > 0:
                    service_id = int(field_name.split('_')[1])
                    service = Service.objects.get(id=service_id)
                    category_match = any(s.name.lower() == service.category.name.lower() for s in specializations)

                    if not category_match:
                        raise ValidationError(f"{employee.get_full_name()} can't complete the service")

        return cleaned_data


    def get_services_with_quantity(self):
        services = []
        for field_name, quantity in self.cleaned_data.items():
            if field_name.startswith('quantity_') and quantity > 0:
                service_id = int(field_name.split('_')[1])
                services.append((Service.objects.get(id=service_id), quantity))
        return services
