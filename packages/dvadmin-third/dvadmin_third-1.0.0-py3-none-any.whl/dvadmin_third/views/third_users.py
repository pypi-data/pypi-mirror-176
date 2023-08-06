import mimetypes
import os
import uuid
from wsgiref.util import FileWrapper

from pathlib import Path
from user_agents import parse

from application import dispatch
from dvadmin.system.models import LoginLog
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.request_util import get_request_ip, get_ip_analysis, get_browser, get_os
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin_third.models import ThirdUsers
from rest_framework.decorators import action
from django.shortcuts import render
from django.core.cache import cache
from django.http import StreamingHttpResponse, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken


class ThirdUsersSerializer(CustomModelSerializer):
    """
    第三方登录-序列化器
    """

    class Meta:
        model = ThirdUsers
        exclude = ['session_key']
        read_only_fields = ["id"]


class ThirdUsersViewSet(CustomModelViewSet):
    """
    第三方登录接口
    """
    queryset = ThirdUsers.objects.all()
    serializer_class = ThirdUsersSerializer


def static(request):
    path = os.path.join(Path(__file__).resolve().parent.parent, "templates", "h5", "static",
                        request.path_info.replace('/api/dvadmin_third/index/static/', ''))
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    return resp


def index(request):
    return render(request, 'h5/index.html')


def check_file(request, file_name):
    txt = ''
    if file_name:
        wx_check_file_list = dispatch.get_system_config_values("third.wx_check_file")
        for ele in wx_check_file_list:
            if ele.get('key') == file_name:
                txt = ele.get('value')
                break
    return HttpResponse(txt)


class ThirdUsersLoginViewSet(CustomModelViewSet):
    """
    第三方登录接口
    """
    queryset = ThirdUsers.objects.all()
    serializer_class = ThirdUsersSerializer
    authentication_classes = []

    @action(methods=["GET"], detail=False, permission_classes=[])
    def scan_login_url(self, request):
        """
        获取扫码地址
        :param request:
        :return:
        """
        login_uid = uuid.uuid4().hex
        ip = get_request_ip(request=self.request)
        data = {
            "ip": ip,
            "browser": get_browser(request),
            "os": get_os(request),
            "state": 1  # 0 无效，1 未扫，2 已扫，3 扫码完成,并返回token
        }
        cache.set(f"third_login_uid_{login_uid}", data, 12000)
        cache.set(f"third_login_uid_{login_uid}_state", 1, 12000)
        url = f"api/dvadmin_third/index/#/?login_uid={login_uid}"
        login_type = self.request.query_params.get('login_type')
        if login_type:
            url = f"api/dvadmin_third/index/?t={login_type}#/?login_uid={login_uid}"
        return DetailResponse(data={"url": url, "login_uid": login_uid},
                              msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[])
    def get_scan_info(self, request):
        """
        获取扫码登录页面详情
        :param request:
        :return:
        """
        login_uid = request.GET.get('login_uid')
        if not login_uid:
            return ErrorResponse(msg="无效二维码")
        login_data = cache.get(f"third_login_uid_{login_uid}")
        if not login_data:
            return ErrorResponse(msg="二维码已过期，请重新扫码")
        analysis_data = get_ip_analysis(login_data.get('ip'))
        cache.set(f"third_login_uid_{login_uid}_state", 2)
        return DetailResponse(data={"analysis_data": analysis_data, "login_data": login_data})

    @action(methods=["POST"], detail=False, permission_classes=[])
    def verify_whether_scan(self, request):
        """
        校验是否被扫
        :param request:
        :return:
        """
        login_uid = self.request.data.get('login_uid')
        if not login_uid:
            return DetailResponse(data={"state": 0}, msg="无效二维码")
        login_state = cache.get(f"third_login_uid_{login_uid}_state")
        if not login_state:
            return DetailResponse(data={"state": 0}, msg="二维码已过期请重新扫码")
        # 如果 state == 3，进行登录，
        token = ''
        if login_state == 3:
            token = cache.get(f"third_login_uid_{login_uid}_token")
        return DetailResponse(data={"state": login_state, "token": token}, msg="获取成功")


class ConfirmLoginViewSet(CustomModelViewSet):
    """
    第三方登录接口-确认登录接口
    """
    queryset = ThirdUsers.objects.all()
    serializer_class = ThirdUsersSerializer

    @action(methods=["POST"], detail=False, permission_classes=[])
    def confirm_login(self, request):
        """
        扫码确认
        :param request:
        :return:
        """
        login_uid = self.request.data.get('login_uid')
        if not login_uid:
            return DetailResponse(data={"state": 0}, msg="无效二维码")
        login_state = cache.get(f"third_login_uid_{login_uid}_state")
        if not login_state:
            return DetailResponse(data={"state": 0}, msg="二维码已过期请重新扫码")
        if login_state == 3:
            return DetailResponse(data={"state": 3}, msg="二维码已扫过")
        cache.set(f"third_login_uid_{login_uid}_state", 3)
        # 进行颁发token，并记录登录日志
        ip = get_request_ip(request=request)
        analysis_data = get_ip_analysis(ip)
        analysis_data['username'] = request.user.username
        analysis_data['ip'] = ip
        analysis_data['agent'] = str(parse(request.META['HTTP_USER_AGENT']))
        analysis_data['browser'] = get_browser(request)
        analysis_data['os'] = get_os(request)
        analysis_data['creator_id'] = request.user.id
        analysis_data['dept_belong_id'] = getattr(request.user, 'dept_id', '')
        analysis_data['login_type'] = 2
        LoginLog.objects.create(**analysis_data)

        refresh = RefreshToken.for_user(self.request.user)
        cache.set(f"third_login_uid_{login_uid}_token", str(refresh.access_token), 20)
        return DetailResponse(msg="确认完成!")
