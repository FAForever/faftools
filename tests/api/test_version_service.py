
from faftools.api.VersionService import VersionService

from flexmock import flexmock
from faftools.api.restservice import RestService
from faftools.api import initialize_faftools_api
import faftools.api

__author__ = 'Sheeo'

network_manager = flexmock()
signal_mock = flexmock(connect=lambda func: True)
restmock = flexmock(RestService)
rest_response_mock = flexmock(done=signal_mock, error=signal_mock)

initialize_faftools_api(network_manager, 'test.null')

def test_returns_default_versions_for_mod():
    restmock.should_receive('_get').with_args(faftools.api.SERVICE_URL.VERSION + "/default/faf") \
        .and_return(rest_response_mock()).once()
    VersionService.versions_for('faf')
