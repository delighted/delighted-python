
class People(object):
    def __init__(self, master):
        self.master = master

    def create(self, email, name=None, delay=0, properties=None, send=True):
        """Create or update a person and schedule a survey email.

        You can add properties to a person by passing the
        properties[key]=value parameter. Sending this data is useful for
        filtering responses on the dashboard (e.g. you might send "Location").
        You can also use it to integrate the API across different systems
        (e.g. you might send a unique "Customer ID"). You can add as many
        properties as you like for each person.

        You can create a person without scheduling a survey email by passing
        the send=false parameter. This is useful if you wish to handle
        surveying the person yourself and add your own survey response data
        via our API.

        Args:
           email (string): Email of the person. (required)
           name (string): Name of the person.
           delay (int) The amount of seconds to wait before sending the survey
           email. The default is 0 (i.e. it will send immediately). This
           parameter will be ignored if you set send=false. There is no
           maximum delay.
           properties (dict) Custom properties to associate with the sent
           survey. You can add as many properties as you need. For each
           property you wish to add, pass a separate properties[key]=value
           parameter.

           For example, if you wanted to add a "Customer ID" and a "Location",
           you could pass 2 parameters, properties[customer_id]=123 and
           properties[location]=USA.

           You can optionally set a custom Question Product Name to be used in
           the survey question. For example, passing
           properties[question_product_name]=Apple Genius Bar would result in
           the following question being shown in the survey: "How likely are
           you to recommend Apple Genius Bar to a friend?".
           send    (boolean) Set to false if you do not want to send a survey
           email.  The default is true.
        Returns:
           dict
               id (int): the id of the person created
               email (string): email address of person
               name (string): name of person
               survey_scheduled_at (int): unix timestamp

        Raises:
           DelightedError: A general Delighted error has occurred
           Unauthorized: No API key provided
           NotAcceptable: Request format was incorrect
           UnprocessableEntity: Request parameters were missing
           InternalServerError: Indicates that we are having trouble on our end
           ServiceUnavailable: Indicates that we are currently down for
           maintenance
        """

        if send is True:
            send = 'true'
        else:
            send = 'false'

        _params = {
            'email': email,
            'send': send,
            'delay': delay,
        }

        # 'name': name,
        # 'properties': properties,

        return self.master.post('people', _params)

    def delete(self, email):
        """Remove all pending (i.e. scheduled in the future, but not yet sent)
        survey requests for a given person.

        Args:
           person_email (string): Email of the person. (required)
        Returns:
           ok: (boolean)

        Raises:
           DelightedError: A general Delighted error has occurred
           Unauthorized: No API key provided
           NotAcceptable: Request format was incorrect
           UnprocessableEntity: Request parameters were missing
           InternalServerError: Indicates that we are having trouble on our end
           ServiceUnavailable: Indicates that we are currently down for
           maintenance
        """

        path = 'people/%s/survey_requests/pending' % email

        return self.master.delete(path, {})
