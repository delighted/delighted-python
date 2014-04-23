
class SurveyResponse(object):
    def __init__(self, master):
        self.master = master

    def create(self, person, score, person_properties=None, comment=None):
        """Create a survey response (i.e. a score and comment from a person).

        Args:
           person (string): The ID of the person responding. (required)
           person_properties (dict): Custom properties to associate with this
           response. You can add as many properties as you need. For each
           property you wish to add, pass a separate properties[key]=value
           parameter.

           For example, if you wanted to add a "Customer ID" and a "Location"
           to the response, you could pass 2 parameters,
           properties[customer_id]=123 and properties[location]=USA.

           This parameter is optional.
           score (int): Score of the response, from 0 to 10. (required)
           comment (string): An optional comment that the person left when
           responding.
        Returns:
           id (int)
           person (int)
           score (int)
           comment (string)
           created_at (int): unix timestamp

        Raises:
           DelightedError: A general Delighted error has occurred
           Unauthorized: No API key provided
           NotAcceptable: Request format was incorrect
           UnprocessableEntity: Request parameters were missing
           InternalServerError: Indicates that we are having trouble on our end
           ServiceUnavailable: Indicates that we are currently down for
           maintenance
        """

        _params = {
            'person': person,
            'score': score,
        }

        if person_properties is not None:
            _params['person_properties'] = person_properties

        if comment is not None and len(comment) > 0:
            _params['comment'] = comment

        return self.master.post('survey_responses', _params)

    def get(
            self,
            per_page=None,
            page=None,
            since=None,
            until=None,
            trend=None,
            person_email=None,
            order=None,
            expand=False):
        """Create a survey response (i.e. a score and comment from a person).

        Args:
           per_page (int): Number of results to return per page. The maximum
           is 100.
           page (int): The page number to return.
           since (int): An optional Unix timestamp to restrict responses to
           those created on or after this time. Formatting example (for 1
            hour ago): 1398189756.
           until (int): An optional Unix timestamp to restrict responses to
           those created on or before this time. Formatting example (for the
            current time): 1398193356.
           trend (string): An optional ID of a trend to restrict responses to
           that trend. To obtain the ID for a trend, visit the trends page.
           For example, if the URL for the desired trend ends with
           /trends/1234 the ID of that trend is 1234.
           person_email (string): An optional email to restrict responses to a
           specific person.
           order (string): An optional sort order for the responses. The
           default is asc, which will return responses in chronological order
           (oldest first). To get responses in reverse chronological order
           (newest first), specify desc.
           expand (array): Defaults to False, pass True if you want to get all
           of a person's parameters.
        Returns:
           array

        Raises:
           DelightedError: A general Delighted error has occurred
           Unauthorized: No API key provided
           NotAcceptable: Request format was incorrect
           UnprocessableEntity: Request parameters were missing
           InternalServerError: Indicates that we are having trouble on our end
           ServiceUnavailable: Indicates that we are currently down for
           maintenance
        """

        _params = {}

        if per_page is not None:
            _params['per_page'] = per_page

        if page is not None:
            _params['page'] = page

        if since is not None:
            _params['since'] = since

        if until is not None:
            _params['until'] = until

        if trend is not None:
            _params['trend'] = trend

        if person_email is not None:
            _params['person_email'] = person_email

        if order is not None:
            _params['order'] = order

        if expand is True:
            _params['expand[]'] = 'person'

        return self.master.get('survey_responses', _params)
