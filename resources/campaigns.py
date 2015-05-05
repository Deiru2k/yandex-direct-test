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
        def get(self, username):
            if self.user['username'] != username and "admins" not in self.user['groups']:
                raise APIError(code=403, message="Недостаточно прав для просмотра этих кампаний")
            page = self.get_argument("page", 0)
            if isinstance(page, str) and page.is_digit():
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
        def post(self, username):
            if self.user['username'] != username and "admins" not in self.user['groups']:
                raise APIError(code=403, message="Недостаточно прав для добавления кампаний пользователю")
            campaign_data = convert_keys(self.input, lower_to_upper_camel)
            campaign_data['Login'] = username
            campaign_data['FIO'] = "%s %s" % (self.user['firstName'], self.user['lastName'])
            campaign_data['CampaignID'] = 0
            self.yd.create_campaign(campaign_data)
            return 201, None
