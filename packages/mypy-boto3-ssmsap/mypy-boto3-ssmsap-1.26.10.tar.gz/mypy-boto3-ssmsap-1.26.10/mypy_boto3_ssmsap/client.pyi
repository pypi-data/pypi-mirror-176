"""
Type annotations for ssmsap service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ssmsap.client import SsmSapClient

    session = Session()
    client: SsmSapClient = session.client("ssmsap")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListApplicationsPaginator, ListComponentsPaginator, ListDatabasesPaginator
from .type_defs import (
    ApplicationCredentialTypeDef,
    DeleteResourcePermissionOutputTypeDef,
    GetApplicationOutputTypeDef,
    GetComponentOutputTypeDef,
    GetDatabaseOutputTypeDef,
    GetOperationOutputTypeDef,
    GetResourcePermissionOutputTypeDef,
    ListApplicationsOutputTypeDef,
    ListComponentsOutputTypeDef,
    ListDatabasesOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutResourcePermissionOutputTypeDef,
    RegisterApplicationOutputTypeDef,
    UpdateApplicationSettingsOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("SsmSapClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SsmSapClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SsmSapClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#can_paginate)
        """
    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#close)
        """
    def delete_resource_permission(
        self,
        *,
        ResourceArn: str,
        ActionType: Literal["RESTORE"] = ...,
        SourceResourceArn: str = ...
    ) -> DeleteResourcePermissionOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/DeleteResourcePermission).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.delete_resource_permission)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#delete_resource_permission)
        """
    def deregister_application(self, *, ApplicationId: str) -> Dict[str, Any]:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/DeregisterApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.deregister_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#deregister_application)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#generate_presigned_url)
        """
    def get_application(
        self, *, ApplicationId: str = ..., ApplicationArn: str = ...
    ) -> GetApplicationOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/GetApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.get_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#get_application)
        """
    def get_component(self, *, ApplicationId: str, ComponentId: str) -> GetComponentOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/GetComponent).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.get_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#get_component)
        """
    def get_database(
        self,
        *,
        ApplicationId: str = ...,
        ComponentId: str = ...,
        DatabaseId: str = ...,
        DatabaseArn: str = ...
    ) -> GetDatabaseOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/GetDatabase).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.get_database)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#get_database)
        """
    def get_operation(self, *, OperationId: str) -> GetOperationOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/GetOperation).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.get_operation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#get_operation)
        """
    def get_resource_permission(
        self, *, ResourceArn: str, ActionType: Literal["RESTORE"] = ...
    ) -> GetResourcePermissionOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/GetResourcePermission).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.get_resource_permission)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#get_resource_permission)
        """
    def list_applications(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListApplicationsOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/ListApplications).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.list_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#list_applications)
        """
    def list_components(
        self, *, ApplicationId: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListComponentsOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/ListComponents).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.list_components)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#list_components)
        """
    def list_databases(
        self,
        *,
        ApplicationId: str = ...,
        ComponentId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListDatabasesOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/ListDatabases).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.list_databases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#list_databases)
        """
    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/ListTagsForResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#list_tags_for_resource)
        """
    def put_resource_permission(
        self, *, ActionType: Literal["RESTORE"], SourceResourceArn: str, ResourceArn: str
    ) -> PutResourcePermissionOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/PutResourcePermission).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.put_resource_permission)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#put_resource_permission)
        """
    def register_application(
        self,
        *,
        ApplicationId: str,
        ApplicationType: Literal["HANA"],
        Instances: Sequence[str],
        Credentials: Sequence[ApplicationCredentialTypeDef],
        SapInstanceNumber: str = ...,
        Sid: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> RegisterApplicationOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/RegisterApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.register_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#register_application)
        """
    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/TagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#tag_resource)
        """
    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/UntagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#untag_resource)
        """
    def update_application_settings(
        self,
        *,
        ApplicationId: str,
        CredentialsToAddOrUpdate: Sequence[ApplicationCredentialTypeDef] = ...,
        CredentialsToRemove: Sequence[ApplicationCredentialTypeDef] = ...
    ) -> UpdateApplicationSettingsOutputTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/ssmsap-2018-05-10/UpdateApplicationSettings).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.update_application_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#update_application_settings)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_components"]) -> ListComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_databases"]) -> ListDatabasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssmsap.html#SsmSap.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssmsap/client/#get_paginator)
        """
