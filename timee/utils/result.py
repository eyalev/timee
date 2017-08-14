import json
from collections import OrderedDict as odict

from timee.utils.dict_util import DictUtil


class Result(object):

    def __init__(self, success=None, data=None, error=None, errors=None, base_result=None):

        self._success = success
        self._data = data
        self._errors = []
        self._response_dict = None

        if error:
            self.add_error(error)

        elif errors:
            self._errors = errors

        if base_result is not None:
            self._base_result = base_result
            self._success = base_result.success
            self._data = base_result.data
            self._errors = base_result.errors

    def __nonzero__(self):
        return self.success

    def __repr__(self):
        output = '<Result> {status}'.format(
            status=self.status
        )
        return output

    @property
    def success(self):
        return self._success

    @success.setter
    def success(self, value):
        self._success = value

    @property
    def failed(self):
        return not self.success

    @property
    def failure(self):
        return not self.success

    @classmethod
    def failed_result(cls):
        result = Result(success=False)
        return result

    @property
    def status(self):
        return self._success

    @success.setter
    def success(self, value):
        self._success = value

    @property
    def errors(self):

        """
        :rtype: list of Error

        """
        return self._errors

    @property
    def errors_odict(self):

        errors = []

        for error in self.errors:
            errors.append(error.odict)

        result_odict = odict()
        result_odict['errors'] = errors

        return result_odict

    @property
    def errors_string(self):

        json_string = DictUtil(self.errors_odict).to_pretty_json_string()
        return json_string

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def response_dict(self):
        return self._response_dict

    @response_dict.setter
    def response_dict(self, value):
        self._response_dict = value

    @property
    def base_result(self):
        return self._base_result

    def set_failed(self):

        self.success = False
        return self

    def add_error(self, message):

        error = Error(message=message)

        self.errors.append(error)

        self.set_failed()

        return self

    @property
    def has_errors(self):

        if len(self.errors) > 0:
            return True

        else:
            return False

    @property
    def odict(self):

        """
        Trying to follow the jsonapi.org standard.

        """

        odict_result = odict()
        odict_result['data'] = self.data
        odict_result['success'] = self.success

        if self.has_errors:
            odict_result['errors'] = []
            for error in self.errors:
                odict_result['errors'].append(error.odict)

        return odict_result

    @property
    def json_object(self):
        return self.odict

    def set_response_dict(self, _dict):

        self.response_dict = _dict
        return self

    def set_data(self, value):

        self.data = value
        return self

    @property
    def pretty_json_string(self):

        pretty_json_string = json.dumps(self.odict, indent=4)
        return pretty_json_string

    @property
    def string(self):
        return self.pretty_json_string


def success_result():
    result = Result(success=True)
    return result


class ResultFailure(Result):

    def __init__(self, data=None, error=None, errors=None):
        success = False
        super(ResultFailure, self).__init__(success, data, error, errors)


class ResultSuccess(Result):

    def __init__(self, data=None, error=None, errors=None):
        success = True
        super(ResultSuccess, self).__init__(success, data, error, errors)


class Error(object):

    def __init__(self, message):

        self._message = message

    @property
    def message(self):
        return self._message

    @property
    def odict(self):

        error_odict = odict()
        error_odict['message'] = self.message

        return error_odict
