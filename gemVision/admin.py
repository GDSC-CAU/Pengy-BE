from django.contrib import admin
from .models import FireHazardAssessment

class FireHazardAssessmentAdmin(admin.ModelAdmin):
    list_display = ('my_space_detail', 'place_or_object_description', 'degree_of_fire_danger', 'display_hazards', 'display_measures')
    list_filter = ('degree_of_fire_danger', 'my_space_detail__nickname', 'my_space_detail')
    search_fields = ('my_space_detail__nickname', 'place_or_object_description', 'identified_fire_hazards', 'mitigation_measures', 'additional_recommendations', 'fact_check')
    fieldsets = (
        ('General Info', {
            'fields': ('my_space_detail', 'place_or_object_description', 'degree_of_fire_danger')
        }),
        ('Detailed Assessment', {
            'fields': ('identified_fire_hazards', 'mitigation_measures', 'additional_recommendations', 'fact_check'),
            'classes': ('collapse',),
        }),
    )

    def display_hazards(self, obj):
        return obj.identified_fire_hazards[:50] + "..." if len(obj.identified_fire_hazards) > 50 else obj.identified_fire_hazards

    def display_measures(self, obj):
        return obj.mitigation_measures[:50] + "..." if len(obj.mitigation_measures) > 50 else obj.mitigation_measures

    display_hazards.short_description = "Identified Hazards"
    display_measures.short_description = "Mitigation Measures"

admin.site.register(FireHazardAssessment, FireHazardAssessmentAdmin)
