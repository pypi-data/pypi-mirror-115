# from django.core.mail import send_mail
from io import StringIO
import json
# from django.db.models import fields
from rest_framework import status,viewsets
from .permissions import IsAdmin,IsStaff,UserHasViewRights
from django.core import serializers as djserializers
# from rest_framework import response
from xtrm_drest.viewsets import DynamicModelViewSet
from .serializers import EmailSerializer,SenderSerializer
from rest_framework.response import Response
from django.db import IntegrityError
# render_filter_obj,render_to_pdf
from .utils import render_filter_obj, render_to_pdf
from django.http import HttpResponse
from rest_framework.decorators import action, permission_classes
# from .utils import SendMail
import csv
from django.conf import settings
from sendgrid import SendGridAPIClient
from .utils import get_recipient_model
RecipientModel = get_recipient_model()
SENDGRID_API_KEY=getattr(settings,'SENDGRID_API_KEY')
# import logging
class SenderViewset(viewsets.ViewSet):
    serializer_class=SenderSerializer
    permission_classes=[IsAdmin]
    reporttitle = 'Email Accounts'
    orientation = 'portrait'
    options = {'canAdd': 1, 'canPrint': 0}
    permActions = []
    # rowActions = [{'label': 'Edit', 'type': 'edit'},{'label': 'Delete', 'type': 'delete'},{'label': 'Re-send Verification', 'type': 'backend','endpoint':'v1/email/senders/#var/resend/','eval':['id'],'method':'get','success':'Verfication email being sent successfully.'}]
    rowActions = [{'label': 'Edit', 'type': 'edit'},{'label': 'Delete', 'type': 'delete'}]
    restrictedMethods = []
    restrictedActions = ['sendpdf','sendexcel']
    filters = []
    columns = [
        {'title': 'id', 'name': 'id','visible':False,'sortable':False,'searchable':False},
        {'title': 'Name', 'name': 'name','sortable':False,'searchable':False},
        {'title': 'Email Id', 'name': 'emailid','sortable':False,'searchable':False},
        {'title': 'Verified', 'name': 'verified',
            'sortable': False, 'searchable': False,'alignment':'center','type': 'boolean', 'booltype': 'VERIFIED/NOT-VERIFIED', 'badge': True},
    ]
    def getSenders(self):
        try:
            sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
            response = sendgrid_client.client.marketing.senders.get()
            r= json.loads(response.body)
            i=[]
            for x in r:
                i.append({"id":x["id"],"name":x["from"]["name"],"emailid":x["from"]["email"],"verified":x["verified"]["status"]})
            return i
        except Exception as e:
            import logging
            logging.error(e)
            return {'status': 'Unable to list email accounts'}
    def getSender(self,id):
        try:
            sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
            response = sendgrid_client.client.marketing.senders._(str(id)).get()
            r=json.loads(response.body)
            i={"id":r["id"],"name":r["from"]["name"],"emailid":r["from"]["email"],"verified":r["verified"]["status"]}
            return {"senders":i}
        except Exception as e:
            import logging
            logging.error(e)
            return {'status': 'Unable to get email account'}
    
    def deleteSender(self,id):
        try:
            sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
            sendgrid_client.client.marketing.senders._(str(id)).delete()
            return ''
        except Exception as e:
            import logging
            logging.error(e)
            return {'status': 'Unable to delete email account'}
    
    def addSender(self,name, emailid):
        data = {
            "address": "Gandhidham",
            "city": "Gandhidham",
            "country": "India",
            "from": {
                "email": emailid,
                "name": name
            },
            "nickname": name,
            "reply_to": {
                "email": emailid,
                "name": name
            },
        }
        try:
            sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
            response = sendgrid_client.client.marketing.senders.post(
                request_body=data)
            r= json.loads(response.body)
            i={}
            i["id"]=r["id"]
            i["name"]=r["from"]["name"]
            i["emailid"]=r["from"]["email"]
            i["verified"]=r["verified"]["status"]
            return i
        except Exception as e:
            import logging
            logging.error(e)
            return {'status': 'Unable to create email account'}

    def updateSender(self,id, name, emailid):
        data = {
            "address": "Gandhidham",
            "city": "Gandhidham",
            "country": "India",
            "from": {
                "email": emailid,
                "name": name
            },
            "nickname": name,
            "reply_to": {
                "email": emailid,
                "name": name
            },
        }
        try:
            sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
            response = sendgrid_client.client.marketing.senders._(str(id)).patch(
                request_body=data)
            return response.body
        except Exception as e:
            import logging
            logging.error(e)
            return {'status': 'Unable to update email account'}
    def resendVerification(self,id):
        try:
            sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
            sendgrid_client.client.marketing.senders._(
                str(id)).resend_verification.post()
            return '' #response.body
        except Exception as e:
            import logging
            logging.error(e)
            return {'status': 'Unable to re-send verification email'}
    
    def list(self,request):
        return Response(self.getSenders())
    
    def create(self,request):
        i=SenderSerializer(data=request.data)
        if i.is_valid():
            name=request.data.get('name')
            emailid=request.data.get('emailid')
            # return Response(self.addSender(name,emailid))
            rtn = self.addSender(name, emailid)
            if 'id' in rtn.keys():
                return Response(rtn,status=status.HTTP_200_OK)
            else:
                return Response(rtn,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(i.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,pk=None):
        i = SenderSerializer(data=request.data)
        if i.is_valid():
            name=request.data.get('name')
            emailid=request.data.get('emailid')
            if pk:
                rtn=self.updateSender(pk,name,emailid)
                return Response(rtn)
            else:
                return Response({"status:Unable to update email account"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status:Unable to update email account"},status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        if pk:
            rtn=self.getSender(pk)
            return Response(rtn)
        else:
            return Response({"status:Unable to update email account"}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        if pk:
            rtn = self.deleteSender(pk)
            if rtn:
                return Response(rtn,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"status:Unable to delete email account"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def report(self, request, *args, **kwargs):
        serializer = self.getSenders()
        respond = {
            'options': self.options,
            'filters': self.filters,
            'rowactions': self.rowActions,
            'restrictedactions': self.restrictedActions,
            'columns': self.columns,
            'status': status.HTTP_200_OK,
            'message': self.reporttitle,
            'response': {
                "count": len(serializer),
                "next": None,
                "previous": None,
                "results":
                    {"senders":serializer},
                "meta": {
                    "total_results": len(serializer),
                    "total_pages": 1,
                    "page": 1,
                    "per_page": 50
                }
                }
            
        }
        return Response(respond)

    @action(detail=True)
    def resend(self, request,pk=None):
        if pk:
            rtn = self.resendVerification(pk)
            if rtn:
                return Response(rtn, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"status:Unable to re-send verification email"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,permission_classes=[IsStaff])
    def emailids(self, request):
        senderobj=self.getSenders()
        recsobj=[]
        if RecipientModel:
            recsobj = djserializers.serialize('json', list(RecipientModel.objects.exclude(
            emailid__isnull=True).exclude(emailid__exact='')),fields=('name','emailid'))
        if recsobj:
            recsobj= json.loads(recsobj)
        i=[]
        for x in recsobj:
            i.append({"name":x["fields"]["name"],"emailid":x["pk"]})
        return Response({'senders':senderobj,'recipients':i},status=status.HTTP_200_OK)

    @action(detail=False)
    def labels(self, request, *args, **kwargs):
        respond = {}
        respond['model__title'] = "Email Accounts"
        respond["id"] = "id"
        respond["name"] = "Name"
        respond["emailid"] = "Email Id"
        respond["verified"] = "Verified"

        return Response(respond)

    @action(detail=False)
    def pdf(self, request, *args, **kwargs):
        import datetime
        columns = self.columns.copy()
        r = self.getSenders()
        filter=[]
        for x in r:
            filter.append(tuple(x.values()))
        pdf_obj = render_to_pdf('reports/report.html', {'data': filter, 'columns': columns, 'period': 'As On ' + datetime.date.today().strftime(
            '%d/%m/%Y'), 'orientation': self.orientation, 'companyname': 'Extreme Solutions', 'reporttitle': self.reporttitle, 'filter': []})
        if pdf_obj:
            response = HttpResponse(
                pdf_obj, content_type='application/pdf')
            filename = self.reporttitle + '-' + \
                str(datetime.date.today()) + '.pdf'
            content = "inline; filename=%s" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
    
    @action(detail=False)
    def excel(self, request, *args, **kwargs):
        import datetime
        colheaders = []
        for col in self.columns:
            colheaders.append(col['title'])
        r = self.getSenders()
        response = HttpResponse(content_type='text/csv')
        file_name = self.reporttitle + '-' + \
            str(datetime.date.today()) + '.csv'
        writer = csv.writer(response)
        writer.writerow(colheaders)
        
        for x in r:
            writer.writerow(list(x.values()))
        response['Content-Disposition'] = 'attachment; filename = "' + \
            file_name + '"'
        return response

class ModelViewset(DynamicModelViewSet):
    reporttitle = 'Report'
    orientation = 'portrait'
    options = {'canAdd': 0, 'canPrint': 0}
    permActions = []
    rowActions = []
    restrictedMethods=[]
    restrictedActions=[]

    def get_queryset(self):
        serializer = self.get_serializer()
        if self.action == 'report':
            applabel = serializer.Meta.model._meta.label_lower
            strarray = applabel.split(".")
            user = self.request.user
            self.permActions = []
            if user.has_perm(strarray[0] + ".change_" + strarray[1]) and 'put' not in self.restrictedMethods:
                self.permActions.append({'label': 'Edit', 'type': 'edit'})
            if user.has_perm(strarray[0] + ".delete_" + strarray[1]) and 'delete' not in self.restrictedMethods:
                self.permActions.append({'label': 'Delete', 'type': 'delete'})
            self.request.query_params.add('exclude[]', '*')
            excludeFields = []
            for col in self.columns:
                x = col['name'].split('.')
                z = ''
                for y in range(len(x)-1):
                    if z == '':
                        z = z + x[y]
                    else:
                        z = z + '.' + x[y]
                    if (z in excludeFields) == False:
                        excludeFields.append(z)
                        self.request.query_params.add('exclude[]', z + '.*')
                self.request.query_params.add('include[]', col['name'])

        if hasattr(serializer.Meta.model.objects, 'for_user'):
            return serializer.Meta.model.objects.for_user(self.request.user, self.request.method)
        # if self.queryset:
        #     return self.queryset
        # return serializer.Meta.model.objects.all()
        return super().get_queryset()

    def perform_create(self, serializer):
        if 'user_modified' in serializer.fields:
            serializer.save(user_created=self.request.user,
                            user_modified=self.request.user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if 'user_modified' in serializer.fields:
            serializer.save(user_modified=self.request.user)
        else:
            serializer.save()

    @action(detail=False,permission_classes=[UserHasViewRights])
    def excel(self, request, *args, **kwargs):
        import datetime
        colheaders = []
        colfields = []
        for col in self.columns:
            isvisible = True
            if 'visible' in col:
                if col['visible'] == False:
                    isvisible = False
            if isvisible:
                colheaders.append(col['title'])
                colfields.append(col['name'].replace('.', '__'))
        serializer = self.get_serializer()
        filter = self.filter_queryset(
            serializer.Meta.model.objects.values_list(*colfields))
        response = HttpResponse(content_type='text/csv')
        file_name = self.reporttitle + '-' + \
            str(datetime.date.today()) + '.csv'
        writer = csv.writer(response)
        writer.writerow(colheaders)
        for i in filter:
            writer.writerow(i)
        response['Content-Disposition'] = 'attachment; filename = "' + \
            file_name + '"'
        return response

    @action(detail=False)
    def report(self, request, *args, **kwargs):
        # logging.error(self.columns)
        opts=self.options.copy()
        serializer = self.get_serializer()
        applabel = serializer.Meta.model._meta.label_lower
        strarray = applabel.split(".")
        user = self.request.user
        if opts['canAdd'] and not (user.has_perm(strarray[0] + ".add_" + strarray[1]) and 'add' not in self.restrictedMethods):
            opts['canAdd']=0
        rAction = self.rowActions.copy()
        for i in self.permActions:
            if i['type'].lower() == 'edit':
                rAction.insert(0, i)
            else:
                rAction.append(i)

        serializer = super(ModelViewset, self).list(
            self, request, *args, **kwargs)
        respond = {
            'options': opts,
            'filters': self.filters,
            'rowactions': rAction,
            'restrictedactions': self.restrictedActions,
            'columns': self.columns,
            'status': status.HTTP_200_OK,
            'message': self.reporttitle,
            'response': serializer.data
        }
        return Response(respond)

    @action(detail=False)
    def labels(self, request, *args, **kwargs):
        # logging.error(self.columns)
        serializer = self.get_serializer()
        this_model = serializer.Meta.model._meta
        respond = {}
        respond['model__title'] = this_model.verbose_name.title()
        for f in this_model.fields:
            respond[f.name] = f.verbose_name

        return Response(respond)

    @action(detail=False,permission_classes=[UserHasViewRights])
    def pdf(self, request, *args, **kwargs):
        import datetime
        colfields = []
        columns = self.columns.copy()
        for col in self.columns:
            isvisible = True
            if 'visible' in col:
                if col['visible'] == False:
                    isvisible = False
            if isvisible:
                colfields.append(col['name'].replace('.', '__'))
            else:
                columns.remove(col)
        query = render_filter_obj(self.filters, request.query_params)
        serializer = self.get_serializer()
        filter = self.filter_queryset(
            serializer.Meta.model.objects.values_list(*colfields))
        pdf_obj = render_to_pdf('reports/report.html', {'data': filter, 'columns': columns, 'period': 'As On ' + datetime.date.today().strftime(
            '%d/%m/%Y'), 'orientation': self.orientation, 'companyname': 'Extreme Solutions', 'reporttitle': self.reporttitle, 'filter': query})
        if pdf_obj:
            response = HttpResponse(
                pdf_obj, content_type='application/pdf')
            filename = self.reporttitle + '-' + \
                str(datetime.date.today()) + '.pdf'
            content = "inline; filename=%s" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response

    @action(detail=False,methods=['post'],permission_classes=[UserHasViewRights])
    def sendpdf(self, request, *args, **kwargs):
        import datetime
        colfields = []
        columns = self.columns.copy()
        for col in self.columns:
            isvisible = True
            if 'visible' in col:
                if col['visible'] == False:
                    isvisible = False
            if isvisible:
                colfields.append(col['name'].replace('.', '__'))
            else:
                columns.remove(col)
        query = render_filter_obj(self.filters, request.query_params)
        serializer = self.get_serializer()
        filter = self.filter_queryset(
            serializer.Meta.model.objects.values_list(*colfields))
        pdf_obj = render_to_pdf('reports/report.html', {'data': filter, 'columns': columns, 'period': 'As On ' + datetime.date.today().strftime(
            '%d/%m/%Y'), 'orientation': self.orientation, 'companyname': 'Extreme Solutions', 'reporttitle': self.reporttitle, 'filter': query})
        if pdf_obj:
            filename = self.reporttitle + '-' + \
                str(datetime.date.today()) + '.pdf'
            m=EmailSerializer(data=request.data)
            if m.is_valid():
                x=m.save()
                return x.send([{'name': filename, 'content': pdf_obj, 'content_type': 'application/pdf'}])
            else:
                return Response(m.errors)
        return Response({'status': 'Unable to send email as there is not data available'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[UserHasViewRights])
    def sendexcel(self, request, *args, **kwargs):
        import datetime
        colheaders = []
        colfields = []
        for col in self.columns:
            isvisible = True
            if 'visible' in col:
                if col['visible'] == False:
                    isvisible = False
            if isvisible:
                colheaders.append(col['title'])
                colfields.append(col['name'].replace('.', '__'))
        serializer = self.get_serializer()
        filter = self.filter_queryset(
            serializer.Meta.model.objects.values_list(*colfields))
        file_name = self.reporttitle + '-' + \
            str(datetime.date.today()) + '.csv'
        csvfile=StringIO()
        # with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(colheaders)
        for i in filter:
            writer.writerow(i)
        if csvfile:
            m = EmailSerializer(data=request.data)
            if m.is_valid():
                x=m.save()
                return x.send([{'name': file_name, 'content': csvfile.getvalue(), 'content_type': 'text/csv'}])
            else:
                return Response(m.errors)
        return Response({'status': 'Unable to send email as there is not data available'}, status=status.HTTP_400_BAD_REQUEST)



    def destroy(self, request, *args, **kwargs):
        """
        If foreign key has Protected on delete mode, DRF can't process this.
        """
        instance = self.get_object()
        try:
            instance.delete()
            return_status = status.HTTP_204_NO_CONTENT
            msg = None
        except IntegrityError:
            return_status = status.HTTP_403_FORBIDDEN
            # fields_dict = instance._meta.fields_map
            # msg = dict()
            # msg['message'] = "One of the following fields prevent deleting this instance: {}"\
            #     .format(", ".join(fields_dict.keys()))
            # msg['fields'] = fields_dict.keys()
            msg = dict()
            msg['message'] = "Can not delete, This is in use !!!"
        return Response(status=return_status, data=msg)

    class Meta:
        abstract = True
