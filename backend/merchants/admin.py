from django.contrib import admin

from .models import MerchantBusiness, MerchantKYC


@admin.register(MerchantBusiness)
class MerchantBusinessAdmin(admin.ModelAdmin):
	list_display = (
		"merchant",
		"business_name",
		"business_email",
		"phone",
		"category",
		"kyc_verified",
		"created_at",
	)

	list_filter = (
		"category",
		"kyc_verified",
		"created_at",
	)

	search_fields = (
		"business_name",
		"business_email",
		"phone",
		"merchant__username",
	)

	readonly_fields = (
		"kyc_verified",
		"created_at",
		"updated_at",
	)

	ordering = ("-created_at",)


@admin.register(MerchantKYC)
class MerchantKYCAdmin(admin.ModelAdmin):
	list_display = (
		"merchant",
		"owner_name",
		"national_id",
		"status",
		"submitted_at",
		"verified_at",
	)

	list_filter = (
		"status",
		"submitted_at",
	)

	search_fields = (
		"merchant__business_name",
		"owner_name",
		"national_id",
	)

	readonly_fields = (
		"submitted_at",
		"verified_at",
	)

	ordering = ("-submitted_at",)
