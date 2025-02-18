import logging
import re
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

# Log dosyasına yazmak için logger oluştur
logger = logging.getLogger("security")

# SQL Injection, XSS gibi şüpheli girişleri belirleyen regex kalıpları
SUSPICIOUS_PATTERNS = [
    r"(<script>)",  # XSS saldırısı
    r"(SELECT|INSERT|UPDATE|DELETE).*FROM",  # SQL Injection
    r"(UNION\s+SELECT)",  # SQL Injection
    r"(--|\#|\/\*)",  # SQL yorum satırları
    r"(<|%3C|>|%3E)",  # HTML/JS injection
    r"(javascript:|data:text)",  # XSS URL exploitleri
]

class SecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Sadece API ve Admin'e izin ver, diğerlerini kontrol et
        if not (request.path.startswith("/api/") or request.path.startswith("/admin/")):
            
            
            
            user_ip = self.get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
            print(user_agent)
            logger.warning(f"Olmayan Linke istek atmak | IP: {user_ip} | PATH: {request.path} | User-Agent: {user_agent}")

            # Şüpheli istekleri kontrol et
            if self.is_suspicious(request):
                print("-*-*-*-*-*-*-*")
                logger.warning(f"SUSPICIOUS REQUEST | IP: {user_ip} | PATH: {request.path} | User-Agent: {user_agent}")

                # Opsiyonel: İsteği tamamen engelle
                return JsonResponse({"error": "Suspicious activity detected"}, status=403)

    def process_response(self, request, response):
        return response

    def is_suspicious(self, request):
        """Gelen isteğin şüpheli olup olmadığını kontrol eder"""
        for key, value in request.GET.items():
            if self.contains_suspicious_pattern(value):
                return True
        for key, value in request.POST.items():
            if self.contains_suspicious_pattern(value):
                return True
        return False

    def contains_suspicious_pattern(self, value):
        """Değerin içinde zararlı bir pattern olup olmadığını kontrol eder"""
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False

    def get_client_ip(self, request):
        """İstemcinin IP adresini döndür"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
