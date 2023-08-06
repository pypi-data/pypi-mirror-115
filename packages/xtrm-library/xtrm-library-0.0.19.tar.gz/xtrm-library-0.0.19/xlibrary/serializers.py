# import sys
from rest_framework import serializers
from .utils import SendMail
from rest_framework.response import Response
# from rest_framework import status
#from datetime import date
class ExtraFieldsSerializer(serializers.ModelSerializer):
    # vdate=serializers.SerializerMethodField('getDate')
    # def getDate(self,*args,**kwargs):
    #     return date.today()
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ExtraFieldsSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
    class Meta:
        # extra_fields=['vdate']
        # read_only_fields=('vdate')
        abstract=True

class Recipient:
    def __init__(self,emailid):
        self.emailid=emailid

class RecipientSerializer(serializers.Serializer):
    emailid=serializers.EmailField()
    def create(self, validated_data):
        return Recipient(**validated_data)

class Email:
    def send(self,attachment_list=None):
        try:
            SendMail(self.subject, self.htmlbody,self.sender, recipient_list=[i["emailid"] for i in self.recipients], attachment_list=attachment_list)
        except:
            # print("Unexpected error:", sys.exc_info()[0])
            raise
        return Response({'status': 'Email sent successfully.'})
    def __init__(self,sender,recipients,subject,htmlbody):
        self.sender = sender
        self.recipients=recipients
        self.subject=subject
        self.htmlbody=htmlbody

class Sender(object):
    def __init__(self,id,name,emailid,verified):
        self.id=id
        self.name=name
        self.emailid=emailid
        self.verified=verified

class SenderSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False,allow_null=True)
    name=serializers.CharField()
    emailid=serializers.EmailField()
    verified = serializers.BooleanField(default=False, allow_null=True)
    class Meta:
        resource_name=Sender

class EmailSerializer(serializers.Serializer):
    sender=serializers.CharField()
    recipients=RecipientSerializer(many=True,read_only=False)
    subject=serializers.CharField()
    htmlbody=serializers.CharField()
    def validate(self, data):
        if not 'recipients' in self.initial_data:
            raise serializers.ValidationError(
                {'recipients': ['Recipients may not be blank']})
        elif not len(self.initial_data['recipients']):
            raise serializers.ValidationError(
                {'recipients': ['Recipients may not be blank']})
        return super().validate(data)

    def create(self, validated_data):
        rec_data = validated_data.pop('recipients', None)
        r=RecipientSerializer(data=rec_data,many=True)
        if r.is_valid():
            r.save()
            i = Email(recipients=r.data, **validated_data)
        else:
            i=Email(**validated_data)
        return i
        
class NumericField(serializers.DecimalField):
    """
    We wanted to be able to receive an empty string ('') for a decimal field
    and in that case turn it into a None number
    """
    def to_internal_value(self, data):
        if data == '':
            return None

        return super(NumericField, self).to_internal_value(data)


