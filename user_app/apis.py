from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import pyotp

from .serializers import UserSerializer

User = get_user_model()


class RegisterAPI(APIView):
    def post(self, request):
        print(request.data)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            user = User.objects.create_user(
                email=data["email"],
                password=data["password"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )

            return Response(
                {"message": "User registered successfully", "user": user.email}
            )
        return Response(
            {"message": "User registration failed", "errors": serializer.errors},
            status=400,
        )


class LoginAPI(APIView):
    def post(self, request):
        print(request.data)

        email = request.data["email"]
        password = request.data["password"]

        user = authenticate(email=email, password=password)
        if not user:
            return Response({"message": "Invalid credentials"}, status=401)

        user_serializer = UserSerializer(user)

        if user.is_2fa_enabled:
            return Response(
                {
                    "message": "2FA is enabled, please enter the OTP",
                    "user": user_serializer.data,
                }
            )

        user.last_login = timezone.now()
        refresh = RefreshToken.for_user(user)
        user.save()

        return Response(
            {
                "message": "User logged in successfully",
                "user": user_serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class Setup2FAAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # Assuming user is authenticated
        print(user, request.data)
        if user.is_2fa_enabled:
            return Response({"message": "2FA already enabled"}, status=400)

        # Generate new OTP secret
        otp_secret = pyotp.random_base32()
        totp = pyotp.TOTP(otp_secret)

        # Generate QR code URI
        provisioning_uri = totp.provisioning_uri(user.email, issuer_name="Sachin")

        # Save the secret but don't enable 2FA yet
        user.otp_secret = otp_secret
        user.save()

        return Response(
            {
                "message": "2FA setup initiated",
                "provisioning_uri": provisioning_uri,
                "otp_secret": otp_secret,
            }
        )

    def put(self, request):
        user = request.user
        print(user, request.data)

        otp = request.data["otp"]

        if not user.otp_secret:
            return Response({"message": "Please setup 2FA first"}, status=400)

        # Verify the OTP before enabling 2FA
        totp = pyotp.TOTP(user.otp_secret)
        print(totp, totp.now())
        if not totp.verify(otp):
            return Response({"message": "Invalid OTP"}, status=401)

        # Enable 2FA
        user.is_2fa_enabled = True
        user.save()

        return Response({"message": "2FA enabled successfully"})


class Verify2FAAPI(APIView):
    def post(self, request):
        print(request.data)

        user = User.objects.get(email=request.data["email"])
        otp = request.data["otp"]
        print(user)

        if not otp:
            return Response({"message": "OTP is required"}, status=401)

        totp = pyotp.TOTP(user.otp_secret)
        print(totp, totp.now())
        if not totp.verify(otp):
            return Response({"message": "Invalid OTP"}, status=401)

        user_serializer = UserSerializer(user)

        user.last_login = timezone.now()
        refresh = RefreshToken.for_user(user)
        user.save()

        return Response(
            {
                "message": "User logged in successfully",
                "user": user_serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class UpdateAPI(APIView):
    def post(self, request):
        print(request.data)
        return Response({"message": "User updated successfully"})
