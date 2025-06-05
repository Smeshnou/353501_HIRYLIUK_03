from django.contrib import admin
from .models import FAQModel, VacancyModel, CommentsModel, GymModel, ScheduleModel, BookingModel, PromoModel

# Register your models here.

admin.site.register(FAQModel)
admin.site.register(VacancyModel)
admin.site.register(CommentsModel)
admin.site.register(GymModel)
admin.site.register(ScheduleModel)
admin.site.register(BookingModel)
admin.site.register(PromoModel)

# @admin.register(GymModel)
# class HallAdmin(admin.ModelAdmin):
#     list_display = ('name')
#     search_fields = ('name', 'description')

# @admin.register(ScheduleModel)
# class ScheduleAdmin(admin.ModelAdmin):
#     list_display = ('gym', 'trainer', 'start_time', 'end_time', 'is_available')
#     list_filter = ('gym')
#     date_hierarchy = 'start_time'
#     search_fields = ('gym__name')

# @admin.register(BookingModel)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('user', 'schedule', 'booked_at')
#     list_filter = ('is_confirmed',)
#     search_fields = ('user__username', 'schedule__name')