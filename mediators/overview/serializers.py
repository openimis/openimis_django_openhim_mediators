from rest_framework import serializers
from .models import configs

class configsSerializer(serializers.ModelSerializer):
	class Meta:
		model = configs
		fields = '__all__'
