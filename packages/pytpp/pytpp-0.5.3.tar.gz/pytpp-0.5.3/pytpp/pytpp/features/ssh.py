from typing import List, Union
from pytpp.vtypes import Config
from pytpp.properties.config import CertificateClassNames, CertificateAttributes, CertificateAttributeValues
from pytpp.features.bases.feature_base import FeatureBase, FeatureError, feature


@feature()
class SSH(FeatureBase):
    """
    This feature provides high-level interaction with TPP SSH objects.
    """

    def __init__(self, api):
        super().__init__(api)

    def _get(self, certificate: Union['Config.Object', str]):
        certificate_guid = self._get_guid(certificate)
        result = self._api.websdk.Certificates.Guid(certificate_guid).get()
        result.assert_valid_response()

        return result

    def create_keyset(self):
        pass

    def move_keyset(self):
        pass

    def delete_keyset(self):
        pass

    def get_keysets(self):
        pass

    def add_authorized_key(self):
        pass

    def add_private_key(self):
        pass

    def get_keyset_details(self):
        pass

    def rotate(self):
        pass

    def retry(self):
        pass

    def cancel(self):
        pass

