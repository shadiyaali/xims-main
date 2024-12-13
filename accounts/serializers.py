from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password



class CompanySerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)
    
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'company_admin_name','user_id', 'email_address', 'password', 
                  'phone_no1', 'phone_no2', 'company_logo', 'permissions']

    def create(self, validated_data):
        permissions = validated_data.pop('permissions')
        password = validated_data.get('password')     
        if password:
            validated_data['password'] = make_password(password)
        company = Company.objects.create(**validated_data)   
        company.permissions.set(permissions)
        return company

    
class CompanyGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)
    
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'company_admin_name', 'user_id', 'email_address', 'password', 
                  'phone_no1', 'phone_no2', 'company_logo', 'permissions']
    
    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions', None)

 
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)

 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

     
        if permissions is not None:
            instance.permissions.set(permissions)

        return instance