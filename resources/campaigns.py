from tornado.gen import coroutine
from resources.pages import paginate
import schemas.campaigns
from tornado_resource.crypto import authenticated_async
from tornado_resource.resource import Resource, APIError
from base import BaseHandler
from tornado_resource.validation import validate
from util.mapper import convert_keys, upper_to_lower_camel, lower_to_upper_camel


class UserCampaignList(Resource):

    name = "campaign_list"
    url = "/campaigns/(.*)"

    class Handler(BaseHandler):

        @authenticated_async()
        @coroutine
        def get(self, username: str):
            if self.user['username'] != username and "admins" not in self.user['groups']:
                raise APIError(code=403, message="Недостаточно прав для просмотра этих кампаний")
            page = self.get_argument("page", 0)
            if isinstance(page, str) and page.isdigit():
                page = int(page)
            elif isinstance(page, int):
                pass
            else:
                page = 0
            campaigns = self.yd.list_campaigns(self.user['username'])
            if len(campaigns) == 0:
                raise APIError(code=404, message="Кампаний не найдено")
            campaigns = list(paginate(campaigns, self.per_page))
            try:
                campaigns = campaigns[page]
            except IndexError:
                raise APIError(code=404, message="Кампаний не найдено")
            for i, campaign in enumerate(campaigns):
                campaigns[i] = convert_keys(campaign, upper_to_lower_camel)
            return 200, campaigns

        @authenticated_async()
        @validate(input_schema=schemas.campaigns.campaign)
        @coroutine
        def post(self, username: str):
            if self.user['username'] != username and "admins" not in self.user['groups']:
                raise APIError(code=403, message="Недостаточно прав для добавления кампаний пользователю")
            campaign_data = convert_keys(self.input, lower_to_upper_camel)
            override_data = {
                "Login": username,
                "FIO": "%s %s" % (self.user['firstName'], self.user['lastName']),
                'CampaignID': 0
            }
            campaign_data.update(override_data)
            self.yd.create_campaign(campaign_data)
            return 201, None


class UserCampaign(Resource):

    name = "campaign"
    url = "/campaigns/(.*)/(.*)"

    class Handler(BaseHandler):

        @authenticated_async()
        @coroutine
        def get(self, username: str, campaign_id: str):
            if self.user['username'] != username and "admins" not in self.user['groups']:
                raise APIError(code=403, message="Недостаточно прав для просмотра данной кампании")
            if not campaign_id.isdigit():
                raise APIError(code=400, message="Некорректный ID кампании")
            campaign_id = int(campaign_id)
            campaign = self.yd.get_campaign(campaign_id)
            campaign = convert_keys(campaign, upper_to_lower_camel)
            return 200, campaign

        @authenticated_async()
        @validate(input_schema=schemas.campaigns.campaign)
        @coroutine
        def put(self, username: str, campaign_id: str):
            if self.user['username'] != username and "admins" not in self.user['groups']:
                raise APIError(code=403, message="Недостаточно прав для изменения данной кампании")
            if not campaign_id.isdigit():
                raise APIError(code=400, message="Некорректный ID кампании")
            campaign_id = int(campaign_id)
            campaign_data = self.input
            override_data = {
                "Login": username,
                "FIO": "%s %s" % (self.user['firstName'], self.user['lastName']),
                "CampaignID": campaign_id,
            }
            campaign_data.update(override_data)
            self.yd.update_campaign(campaign_data)
            return 204, None


class UserCampaignArchive(Resource):

    name = "campaign_archive"
    url = "/campaigns/(.*)/(.*)/archive"

    class Handler(BaseHandler):

        @authenticated_async()
        @coroutine
        def post(self, username: str, campaign_id: str):
            if self.user['username'] != username and "admins" not in self.user['groups']:
                raise APIError(code=403, message="Недостаточно прав для архивирования данной кампании")
            if not campaign_id.isdigit():
                raise APIError(code=400, message="Некорректный ID кампании")
            campaign_id = int(campaign_id)
            self.yd.archive_campaign(campaign_id)
            return 204, None

        @authenticated_async()
        @coroutine
        def delete(self, username: str, campaign_id: str):
            if self.user['username'] != username and "admins" not in self.user['groups']:
                raise APIError(code=403, message="Недостаточно прав для восстановления данной кампании из архива")
            if not campaign_id.isdigit():
                raise APIError(code=400, message="Некорректный ID кампании")
            campaign_id = int(campaign_id)
            self.yd.unarchive_campaign(campaign_id)
            return 204, None


class UserCampaignStop(Resource):

    name = "campaign_stop"
    url = "/campaigns/(.*)/(.*)/stop"

    class Handler(BaseHandler):

        @authenticated_async()
        @coroutine
        def post(self, username: str, campaign_id: str):
            if self.user['username'] != username and "admins" not in self.user['groups']:
                raise APIError(code=403, message="Недостаточно прав для остановки данной кампании")
            if not campaign_id.isdigit():
                raise APIError(code=400, message="Некорректный ID кампании")
            campaign_id = int(campaign_id)
            self.yd.stop_campaign(campaign_id)
            return 204, None

        @authenticated_async()
        @coroutine
        def delete(self, username: str, campaign_id: str):
            if self.user['username'] != username and "admins" not in self.user['groups']:
                raise APIError(code=403, message="Недостаточно прав для продолжения данной кампании")
            if not campaign_id.isdigit():
                raise APIError(code=400, message="Некорректный ID кампании")
            campaign_id = int(campaign_id)
            self.yd.resume_campaign(campaign_id)
            return 204, None
