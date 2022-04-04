from rest_framework.serializers import ModelSerializer, CharField

from webapp.models import Quote


class QuoteSerializer(ModelSerializer):
    status_display = CharField(max_length=20, source='get_status_display', read_only=True)


    class Meta:
        model = Quote
        fields = '__all__'
        read_only_fields = ['text', 'author', 'email', 'rating', 'status']


class QuoteCreateSerializer(QuoteSerializer):
    class Meta(QuoteSerializer.Meta):
        model = Quote
        read_only_fields = ['rating', 'status']


class QuoteUpdateSerializer(QuoteSerializer):
    class Meta(QuoteSerializer.Meta):
        model = Quote
        read_only_fields = ['author', 'email', 'rating']