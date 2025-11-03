from rest_framework import serializers

class SellerDashboardSerializer(serializers.Serializer):
    wallet_balance = serializers.IntegerField()
    services_count = serializers.IntegerField()
    active_orders_count = serializers.IntegerField()
    total_earnings = serializers.FloatField()
    monthly_earnings = serializers.FloatField()
    completion_rate = serializers.FloatField()
    top_service = serializers.CharField(allow_null=True)
    recent_transactions = serializers.ListField()
    average_rating = serializers.DictField()
    active_orders_deadlines = serializers.ListField()
