from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.views import APIView
from base.models import Docentes
from django.http import JsonResponse
import json

# Create your views here.
class Login(APIView):
    def post(self, request):
        httpRequest = request._request
        entryJson = json.loads(request.body)
        response = obtain_auth_token(httpRequest)
        user=authenticate(username=entryJson['username'],
                          password=entryJson['password'])
        
        if user is not None:
            name = None
            userType = None
            imgUrl = None
            sede = None
            codigo = None
            if (hasattr(user,'profesor')):
                name = "{} {} {}".format(user.profesor.nombre,user.profesor.apellido1,user.profesor.apellido2)
                if(Docentes.objects.filter(idprofesor=user.profesor).count() <= 0):
                    return JsonResponse({"response":"unsuccessful"})
                rol = Docentes.objects.get(idprofesor=user.profesor).rol.desrol
                userType = "PGC" if rol == "Coordinador" else "PG"
                sede = user.profesor.idsede.codigosede
                imgUrl = user.profesor.fotografia.url if str(user.profesor.fotografia) != '' else ''
                codigo = user.profesor.codigo
            elif (hasattr(user,'asistenteadministrativo')):
                name = "{} {} {}".format(user.asistenteadministrativo.nombre,
                                         user.asistenteadministrativo.apellido1,
                                         user.asistenteadministrativo.apellido2)
                sede = user.asistenteadministrativo.sede.codigosede
                imgUrl = ''
                userType = 'asist'
                codigo = user.asistenteadministrativo.idasistente


            elif (hasattr(user,'estudiante')):
                name = "{} {} {}".format(user.estudiante.nombre,
                                         user.estudiante.apellido1,
                                         user.estudiante.apellido2)
                sede = user.estudiante.sede.codigosede
                imgUrl = ''
                userType = 'estudiante'
                codigo = user.estudiante.idestudiante


            if userType is not None and name is not None and \
               sede is not None and imgUrl is not None and \
               codigo is not None:
                login(httpRequest,user)
                response.data['type'] = userType
                response.data['name'] = name
                response.data['sede'] = sede
                response.data['imgUrl'] = imgUrl
                response.data['codigo'] = codigo
                response.data['response'] = "successful"
                return JsonResponse(response.data)
            else:
                return JsonResponse({"response":"unsuccessful"})
        else:
            return JsonResponse({"response":"unsuccessful"})
        
class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            request.user.auth_token.delete()
            logout(request)
        except:
            return JsonResponse({"response":"unsuccessful"})
        return JsonResponse({"response":"successful"})

class ResetPasswordRequest(APIView):
    
    def post(self, request):

        httpRequest = request._request
        jsonRequest = json.loads(request.body)
        try:
            jsonRequest = { 'email' : User.objects.get(username=jsonRequest['username']).email }
        except User.DoesNotExist:
            return JsonResponse({"response":"unsuccessful"})
        
        
        print(jsonRequest)

        httpRequest._body = json.dumps(jsonRequest).encode('utf-8')

        response = reset_password_request_token(request._request)

        print(response.data)
    

        return JsonResponse({"response":"successful"})
    
class ResetPassword(APIView):
    
    def post(self, request):
        response = reset_password_confirm(request._request)

        print(response.data)

        if "status" not in response.data:
            return JsonResponse(
                {"response":"unsuccessful",
                 "message" : response.data["password"][0].title()}
                )

        return JsonResponse({"response":"successful"})
