from office365.runtime.client_request import ClientRequest
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions


class ODataV4BatchRequest(ClientRequest):
    """ JSON batch request """

    def __init__(self, context):
        super(ODataV4BatchRequest, self).__init__(context)

    def build_request(self):
        url = "{0}/$batch".format(self.context.service_root_url())
        request = RequestOptions(url)
        request.method = HttpMethod.Post
        request.ensure_header('Content-Type', "application/json")
        request.ensure_header('Accept', "application/json")
        request.data = self._prepare_payload()
        return request

    def process_response(self, response):
        """Parses an HTTP response.

        :type response: requests.Response
        """
        json = response.json()
        for resp in json["responses"]:
            self._validate_response(resp)
            sub_qry = self.current_query.get(int(resp["id"]))
            self.context.pending_request().map_json(resp["body"], sub_qry.return_type)

    def _validate_response(self, json):
        if int(json['status']) >= 400:
            raise ValueError(json['body'])

    def _prepare_payload(self):
        """
        Serializes a batch request body.
        """

        requests_json = []
        for qry in self.current_query.queries:
            request_id = str(len(requests_json))
            request = qry.build_request()
            requests_json.append(self._normalize_request(request, request_id))

        return {"requests": requests_json}

    def _normalize_request(self, request, _id, depends_on=None):
        """

        :type request: RequestOptions
        :type _id: str
        :type depends_on:  list[str] or None
        """
        allowed_props = ["id", "method", "headers", "url", "body"]
        json = dict((k, v) for k, v in vars(request).items() if v is not None and k in allowed_props)
        json["id"] = _id
        if depends_on is not None:
            json["dependsOn"] = depends_on
        json["url"] = json["url"].replace(self.context.service_root_url(), "")
        return json

    @property
    def current_query(self):
        """
        :rtype: office365.runtime.queries.batch_query.BatchQuery
        """
        return self._current_query
