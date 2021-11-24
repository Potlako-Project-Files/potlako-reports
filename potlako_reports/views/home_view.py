from django.apps import apps as django_apps
from django.views.generic.base import TemplateView
from pip._internal import self_outdated_check

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from datetime import date
from dateutil.relativedelta import relativedelta



class HomeView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'home.html'
    navbar_selected_item = 'Enrollments Reports'
    navbar_name = 'potlako_reports'

    subject_screening_model = 'potlako_subject.subjectscreening'
    subject_consent_model = 'potlako_subject.subjectconsent'
    cancer_dx_tx = 'potlako_subject.cancerdxandtxendpoint'
    cancer_dx_tx_endpoint = 'potlako_subject.cancerdxandtxendpoint'
    cancer_dx_tx = 'potlako_subject.cancerdxandtx'

    @property
    def cancer_dx_tx_endpoint_cls(self):
        return django_apps.get_model(self.cancer_dx_tx_endpoint)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)
    
    @property
    def cancer_dx_tx_cls(self):
        return django_apps.get_model(self.cancer_dx_tx)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        screened_subjects = self.subject_screening_cls.objects.all().count()
        consented_subjects = self.subject_consent_cls.objects.all().count()
        enrolled_subjects = self.subject_consent_cls.objects.all().count()
        not_enrolled_subjects = self.subject_screening_cls.objects.filter(is_eligible=False).count()
        
        six_months = date.today() + relativedelta(months=-6)
        twelve_months = date.today() + relativedelta(months=-12)

        final_cancer_diagnosis_6 = self.cancer_dx_tx_endpoint_cls.objects.filter(diagnosis_date__lte=six_months).count()
        final_cancer_diagnosis_12 = self.cancer_dx_tx_endpoint_cls.objects.filter(diagnosis_date__lte=twelve_months).count()
        confirmed_cancer_diagnosis_6 = self.cancer_dx_tx_cls.objects.filter(diagnosis_date__lte=six_months).count()
        confirmed_cancer_diagnosis_12 = self.cancer_dx_tx_cls.objects.filter(diagnosis_date__lte=twelve_months).count()
        
        enrollments = [
            ['Screening',screened_subjects],
            ['Consented',consented_subjects],
            ['Not Enrolled',not_enrolled_subjects],
            ['Enrolled',enrolled_subjects],
        ]
        
        cancers = [
            ['Confirmed Cancer Diagnosis At 6 months',confirmed_cancer_diagnosis_6],
            ['Confirmed Cancer Diagnosis At 12 months',confirmed_cancer_diagnosis_12],
            ['Final Cancer Diagnosis At 6 months',final_cancer_diagnosis_6],
            ['Final Cancer Diagnosis At 12 months',final_cancer_diagnosis_12]
            ]

        context.update(
            screened_subjects=screened_subjects,
            consented_subjects=consented_subjects,
            not_enrolled_subjects=not_enrolled_subjects,
            enrolled_subjects=enrolled_subjects,
            
            final_cancer_diagnosis_6=final_cancer_diagnosis_6,
            final_cancer_diagnosis_12=final_cancer_diagnosis_12,
            confirmed_cancer_diagnosis_6=confirmed_cancer_diagnosis_6,
            confirmed_cancer_diagnosis_12=confirmed_cancer_diagnosis_12,
            
            enrollments=enrollments,
            cancers=cancers,
        )

        return context