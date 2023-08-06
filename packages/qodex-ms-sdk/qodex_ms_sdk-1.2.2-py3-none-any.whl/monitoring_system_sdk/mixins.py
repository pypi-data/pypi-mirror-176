import requests


class UrlWorker:
    host = None
    port = None

    def get_full_url(self, url):
        return f"{self.host}:{self.port}/{url}"


class AuthMe:
    auth_url = None
    ms_auth_username = None
    ms_auth_password = None

    def authorize(self):
        data_dict = {"username": self.ms_auth_username,
                     "password": self.ms_auth_password,
                     }
        return requests.post(self.auth_url,
                             data=data_dict)

    def get_token(self):
        return self.authorize().json()['access_token']


class HeaderHandler:
    token = None

    def get_headers(self):
        return {"accept": "application/json",
                "Authorization": f"Bearer {self.token}"}


class MethodsHandler(HeaderHandler):
    ping_all_url = None
    get_all_apps_url = None
    get_deep_analyze_url = None
    reboot_core_pc_ulr = None
    restart_ar_url = None
    turn_off_cm_url = None
    update_gravity_url = None
    gate_control_url = None
    close_cm_url = None
    get_video_url = None

    def get_method_result(self, url, **kwargs):
        return requests.get(url,
                            headers=self.get_headers(),
                            **kwargs)

    def post_method_result(self, url, params=None, **kwargs):
        return requests.post(url,
                             headers=self.get_headers(),
                             params=params,
                             **kwargs)

    def ping_all_apps(self):
        return self.get_method_result(self.ping_all_url)

    def get_all_apps(self):
        return self.get_method_result(self.get_all_apps_url)

    def get_deep_analyze(self, app_id):
        return self.get_method_result(self.get_deep_analyze_url,
                                      params={'gravity_id': app_id})

    def reboot_core_pc(self, app_id):
        return self.get_method_result(self.reboot_core_pc_ulr,
                                      params={'gravity_id': app_id})

    def restart_ar(self, app_id):
        return self.get_method_result(self.restart_ar_url,
                                      params={'gravity_id': app_id})

    def turn_off_cm(self, app_id):
        return self.get_method_result(self.turn_off_cm_url,
                                      params={'gravity_id': app_id})

    def update_gravity(self, app_id):
        return self.get_method_result(self.update_gravity_url,
                                      params={'gravity_id': app_id})

    def open_external_gate(self, app_id):
        return self.post_method_result(self.gate_control_url,
                                       params={'gravity_id': app_id,
                                               'gate_name': 'ext',
                                               'operation': 'open'})

    def open_internal_gate(self, app_id):
        return self.post_method_result(self.gate_control_url,
                                       params={'gravity_id': app_id,
                                               'gate_name': 'int',
                                               'operation': 'open'})

    def close_external_gate(self, app_id):
        return self.post_method_result(self.gate_control_url,
                                       params={'gravity_id': app_id,
                                               'gate_name': 'ext',
                                               'operation': 'close'})

    def close_internal_gate(self, app_id):
        return self.post_method_result(self.gate_control_url,
                                       params={'gravity_id': app_id,
                                               'gate_name': 'int',
                                               'operation': 'close'})

    def close_cm(self, app_id):
        return self.post_method_result(self.close_cm_url,
                                       params={'gravity_id': app_id})

    def get_video(self, cam_id, time_start, time_end):
        return self.get_method_result(self.get_video_url,
                                      params={'cam_id': cam_id,
                                              'time_start': time_start,
                                              'time_end': time_end})
