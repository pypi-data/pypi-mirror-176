'''
# `ionoscloud_group`

Refer to the Terraform Registory for docs: [`ionoscloud_group`](https://www.terraform.io/docs/providers/ionoscloud/r/group).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf
import constructs


class Group(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-ionoscloud.group.Group",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/ionoscloud/r/group ionoscloud_group}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        access_activity_log: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        access_and_manage_certificates: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        access_and_manage_monitoring: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_backup_unit: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_datacenter: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_flow_log: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_internet_access: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_k8_s_cluster: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_pcc: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_snapshot: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        manage_dbaas: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        reserve_ip: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        s3_privilege: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GroupTimeouts", typing.Dict[str, typing.Any]]] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/ionoscloud/r/group ionoscloud_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#name Group#name}.
        :param access_activity_log: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#access_activity_log Group#access_activity_log}.
        :param access_and_manage_certificates: Privilege for a group to access and manage certificates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#access_and_manage_certificates Group#access_and_manage_certificates}
        :param access_and_manage_monitoring: Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#access_and_manage_monitoring Group#access_and_manage_monitoring}
        :param create_backup_unit: Create backup unit privilege. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_backup_unit Group#create_backup_unit}
        :param create_datacenter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_datacenter Group#create_datacenter}.
        :param create_flow_log: Create Flow Logs privilege. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_flow_log Group#create_flow_log}
        :param create_internet_access: Create internet access privilege. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_internet_access Group#create_internet_access}
        :param create_k8_s_cluster: Create Kubernetes cluster privilege. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_k8s_cluster Group#create_k8s_cluster}
        :param create_pcc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_pcc Group#create_pcc}.
        :param create_snapshot: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_snapshot Group#create_snapshot}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#id Group#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param manage_dbaas: Privilege for a group to manage DBaaS related functionality. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#manage_dbaas Group#manage_dbaas}
        :param reserve_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#reserve_ip Group#reserve_ip}.
        :param s3_privilege: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#s3_privilege Group#s3_privilege}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#timeouts Group#timeouts}
        :param user_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#user_id Group#user_id}.
        :param user_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#user_ids Group#user_ids}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id_: builtins.str,
                *,
                name: builtins.str,
                access_activity_log: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                access_and_manage_certificates: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                access_and_manage_monitoring: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_backup_unit: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_datacenter: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_flow_log: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_internet_access: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_k8_s_cluster: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_pcc: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_snapshot: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                id: typing.Optional[builtins.str] = None,
                manage_dbaas: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                reserve_ip: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                s3_privilege: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                timeouts: typing.Optional[typing.Union[GroupTimeouts, typing.Dict[str, typing.Any]]] = None,
                user_id: typing.Optional[builtins.str] = None,
                user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GroupConfig(
            name=name,
            access_activity_log=access_activity_log,
            access_and_manage_certificates=access_and_manage_certificates,
            access_and_manage_monitoring=access_and_manage_monitoring,
            create_backup_unit=create_backup_unit,
            create_datacenter=create_datacenter,
            create_flow_log=create_flow_log,
            create_internet_access=create_internet_access,
            create_k8_s_cluster=create_k8_s_cluster,
            create_pcc=create_pcc,
            create_snapshot=create_snapshot,
            id=id,
            manage_dbaas=manage_dbaas,
            reserve_ip=reserve_ip,
            s3_privilege=s3_privilege,
            timeouts=timeouts,
            user_id=user_id,
            user_ids=user_ids,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create Group#create}.
        :param default: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#default Group#default}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#delete Group#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#update Group#update}.
        '''
        value = GroupTimeouts(
            create=create, default=default, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessActivityLog")
    def reset_access_activity_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessActivityLog", []))

    @jsii.member(jsii_name="resetAccessAndManageCertificates")
    def reset_access_and_manage_certificates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessAndManageCertificates", []))

    @jsii.member(jsii_name="resetAccessAndManageMonitoring")
    def reset_access_and_manage_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessAndManageMonitoring", []))

    @jsii.member(jsii_name="resetCreateBackupUnit")
    def reset_create_backup_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateBackupUnit", []))

    @jsii.member(jsii_name="resetCreateDatacenter")
    def reset_create_datacenter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateDatacenter", []))

    @jsii.member(jsii_name="resetCreateFlowLog")
    def reset_create_flow_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateFlowLog", []))

    @jsii.member(jsii_name="resetCreateInternetAccess")
    def reset_create_internet_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateInternetAccess", []))

    @jsii.member(jsii_name="resetCreateK8SCluster")
    def reset_create_k8_s_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateK8SCluster", []))

    @jsii.member(jsii_name="resetCreatePcc")
    def reset_create_pcc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatePcc", []))

    @jsii.member(jsii_name="resetCreateSnapshot")
    def reset_create_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateSnapshot", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetManageDbaas")
    def reset_manage_dbaas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManageDbaas", []))

    @jsii.member(jsii_name="resetReserveIp")
    def reset_reserve_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReserveIp", []))

    @jsii.member(jsii_name="resetS3Privilege")
    def reset_s3_privilege(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Privilege", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @jsii.member(jsii_name="resetUserIds")
    def reset_user_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserIds", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GroupTimeoutsOutputReference":
        return typing.cast("GroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> "GroupUsersList":
        return typing.cast("GroupUsersList", jsii.get(self, "users"))

    @builtins.property
    @jsii.member(jsii_name="accessActivityLogInput")
    def access_activity_log_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "accessActivityLogInput"))

    @builtins.property
    @jsii.member(jsii_name="accessAndManageCertificatesInput")
    def access_and_manage_certificates_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "accessAndManageCertificatesInput"))

    @builtins.property
    @jsii.member(jsii_name="accessAndManageMonitoringInput")
    def access_and_manage_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "accessAndManageMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="createBackupUnitInput")
    def create_backup_unit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "createBackupUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="createDatacenterInput")
    def create_datacenter_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "createDatacenterInput"))

    @builtins.property
    @jsii.member(jsii_name="createFlowLogInput")
    def create_flow_log_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "createFlowLogInput"))

    @builtins.property
    @jsii.member(jsii_name="createInternetAccessInput")
    def create_internet_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "createInternetAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="createK8SClusterInput")
    def create_k8_s_cluster_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "createK8SClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="createPccInput")
    def create_pcc_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "createPccInput"))

    @builtins.property
    @jsii.member(jsii_name="createSnapshotInput")
    def create_snapshot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "createSnapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="manageDbaasInput")
    def manage_dbaas_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "manageDbaasInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="reserveIpInput")
    def reserve_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "reserveIpInput"))

    @builtins.property
    @jsii.member(jsii_name="s3PrivilegeInput")
    def s3_privilege_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "s3PrivilegeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["GroupTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["GroupTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdsInput")
    def user_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessActivityLog")
    def access_activity_log(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "accessActivityLog"))

    @access_activity_log.setter
    def access_activity_log(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessActivityLog", value)

    @builtins.property
    @jsii.member(jsii_name="accessAndManageCertificates")
    def access_and_manage_certificates(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "accessAndManageCertificates"))

    @access_and_manage_certificates.setter
    def access_and_manage_certificates(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessAndManageCertificates", value)

    @builtins.property
    @jsii.member(jsii_name="accessAndManageMonitoring")
    def access_and_manage_monitoring(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "accessAndManageMonitoring"))

    @access_and_manage_monitoring.setter
    def access_and_manage_monitoring(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessAndManageMonitoring", value)

    @builtins.property
    @jsii.member(jsii_name="createBackupUnit")
    def create_backup_unit(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "createBackupUnit"))

    @create_backup_unit.setter
    def create_backup_unit(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createBackupUnit", value)

    @builtins.property
    @jsii.member(jsii_name="createDatacenter")
    def create_datacenter(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "createDatacenter"))

    @create_datacenter.setter
    def create_datacenter(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createDatacenter", value)

    @builtins.property
    @jsii.member(jsii_name="createFlowLog")
    def create_flow_log(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "createFlowLog"))

    @create_flow_log.setter
    def create_flow_log(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createFlowLog", value)

    @builtins.property
    @jsii.member(jsii_name="createInternetAccess")
    def create_internet_access(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "createInternetAccess"))

    @create_internet_access.setter
    def create_internet_access(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createInternetAccess", value)

    @builtins.property
    @jsii.member(jsii_name="createK8SCluster")
    def create_k8_s_cluster(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "createK8SCluster"))

    @create_k8_s_cluster.setter
    def create_k8_s_cluster(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createK8SCluster", value)

    @builtins.property
    @jsii.member(jsii_name="createPcc")
    def create_pcc(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "createPcc"))

    @create_pcc.setter
    def create_pcc(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createPcc", value)

    @builtins.property
    @jsii.member(jsii_name="createSnapshot")
    def create_snapshot(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "createSnapshot"))

    @create_snapshot.setter
    def create_snapshot(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createSnapshot", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="manageDbaas")
    def manage_dbaas(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "manageDbaas"))

    @manage_dbaas.setter
    def manage_dbaas(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manageDbaas", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="reserveIp")
    def reserve_ip(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "reserveIp"))

    @reserve_ip.setter
    def reserve_ip(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reserveIp", value)

    @builtins.property
    @jsii.member(jsii_name="s3Privilege")
    def s3_privilege(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "s3Privilege"))

    @s3_privilege.setter
    def s3_privilege(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Privilege", value)

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value)

    @builtins.property
    @jsii.member(jsii_name="userIds")
    def user_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userIds"))

    @user_ids.setter
    def user_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userIds", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-ionoscloud.group.GroupConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "access_activity_log": "accessActivityLog",
        "access_and_manage_certificates": "accessAndManageCertificates",
        "access_and_manage_monitoring": "accessAndManageMonitoring",
        "create_backup_unit": "createBackupUnit",
        "create_datacenter": "createDatacenter",
        "create_flow_log": "createFlowLog",
        "create_internet_access": "createInternetAccess",
        "create_k8_s_cluster": "createK8SCluster",
        "create_pcc": "createPcc",
        "create_snapshot": "createSnapshot",
        "id": "id",
        "manage_dbaas": "manageDbaas",
        "reserve_ip": "reserveIp",
        "s3_privilege": "s3Privilege",
        "timeouts": "timeouts",
        "user_id": "userId",
        "user_ids": "userIds",
    },
)
class GroupConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
        name: builtins.str,
        access_activity_log: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        access_and_manage_certificates: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        access_and_manage_monitoring: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_backup_unit: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_datacenter: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_flow_log: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_internet_access: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_k8_s_cluster: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_pcc: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        create_snapshot: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        manage_dbaas: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        reserve_ip: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        s3_privilege: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GroupTimeouts", typing.Dict[str, typing.Any]]] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#name Group#name}.
        :param access_activity_log: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#access_activity_log Group#access_activity_log}.
        :param access_and_manage_certificates: Privilege for a group to access and manage certificates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#access_and_manage_certificates Group#access_and_manage_certificates}
        :param access_and_manage_monitoring: Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#access_and_manage_monitoring Group#access_and_manage_monitoring}
        :param create_backup_unit: Create backup unit privilege. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_backup_unit Group#create_backup_unit}
        :param create_datacenter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_datacenter Group#create_datacenter}.
        :param create_flow_log: Create Flow Logs privilege. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_flow_log Group#create_flow_log}
        :param create_internet_access: Create internet access privilege. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_internet_access Group#create_internet_access}
        :param create_k8_s_cluster: Create Kubernetes cluster privilege. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_k8s_cluster Group#create_k8s_cluster}
        :param create_pcc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_pcc Group#create_pcc}.
        :param create_snapshot: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_snapshot Group#create_snapshot}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#id Group#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param manage_dbaas: Privilege for a group to manage DBaaS related functionality. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#manage_dbaas Group#manage_dbaas}
        :param reserve_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#reserve_ip Group#reserve_ip}.
        :param s3_privilege: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#s3_privilege Group#s3_privilege}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#timeouts Group#timeouts}
        :param user_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#user_id Group#user_id}.
        :param user_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#user_ids Group#user_ids}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GroupTimeouts(**timeouts)
        if __debug__:
            def stub(
                *,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
                name: builtins.str,
                access_activity_log: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                access_and_manage_certificates: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                access_and_manage_monitoring: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_backup_unit: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_datacenter: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_flow_log: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_internet_access: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_k8_s_cluster: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_pcc: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                create_snapshot: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                id: typing.Optional[builtins.str] = None,
                manage_dbaas: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                reserve_ip: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                s3_privilege: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                timeouts: typing.Optional[typing.Union[GroupTimeouts, typing.Dict[str, typing.Any]]] = None,
                user_id: typing.Optional[builtins.str] = None,
                user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_activity_log", value=access_activity_log, expected_type=type_hints["access_activity_log"])
            check_type(argname="argument access_and_manage_certificates", value=access_and_manage_certificates, expected_type=type_hints["access_and_manage_certificates"])
            check_type(argname="argument access_and_manage_monitoring", value=access_and_manage_monitoring, expected_type=type_hints["access_and_manage_monitoring"])
            check_type(argname="argument create_backup_unit", value=create_backup_unit, expected_type=type_hints["create_backup_unit"])
            check_type(argname="argument create_datacenter", value=create_datacenter, expected_type=type_hints["create_datacenter"])
            check_type(argname="argument create_flow_log", value=create_flow_log, expected_type=type_hints["create_flow_log"])
            check_type(argname="argument create_internet_access", value=create_internet_access, expected_type=type_hints["create_internet_access"])
            check_type(argname="argument create_k8_s_cluster", value=create_k8_s_cluster, expected_type=type_hints["create_k8_s_cluster"])
            check_type(argname="argument create_pcc", value=create_pcc, expected_type=type_hints["create_pcc"])
            check_type(argname="argument create_snapshot", value=create_snapshot, expected_type=type_hints["create_snapshot"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument manage_dbaas", value=manage_dbaas, expected_type=type_hints["manage_dbaas"])
            check_type(argname="argument reserve_ip", value=reserve_ip, expected_type=type_hints["reserve_ip"])
            check_type(argname="argument s3_privilege", value=s3_privilege, expected_type=type_hints["s3_privilege"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument user_ids", value=user_ids, expected_type=type_hints["user_ids"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if access_activity_log is not None:
            self._values["access_activity_log"] = access_activity_log
        if access_and_manage_certificates is not None:
            self._values["access_and_manage_certificates"] = access_and_manage_certificates
        if access_and_manage_monitoring is not None:
            self._values["access_and_manage_monitoring"] = access_and_manage_monitoring
        if create_backup_unit is not None:
            self._values["create_backup_unit"] = create_backup_unit
        if create_datacenter is not None:
            self._values["create_datacenter"] = create_datacenter
        if create_flow_log is not None:
            self._values["create_flow_log"] = create_flow_log
        if create_internet_access is not None:
            self._values["create_internet_access"] = create_internet_access
        if create_k8_s_cluster is not None:
            self._values["create_k8_s_cluster"] = create_k8_s_cluster
        if create_pcc is not None:
            self._values["create_pcc"] = create_pcc
        if create_snapshot is not None:
            self._values["create_snapshot"] = create_snapshot
        if id is not None:
            self._values["id"] = id
        if manage_dbaas is not None:
            self._values["manage_dbaas"] = manage_dbaas
        if reserve_ip is not None:
            self._values["reserve_ip"] = reserve_ip
        if s3_privilege is not None:
            self._values["s3_privilege"] = s3_privilege
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_id is not None:
            self._values["user_id"] = user_id
        if user_ids is not None:
            self._values["user_ids"] = user_ids

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[cdktf.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[cdktf.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#name Group#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_activity_log(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#access_activity_log Group#access_activity_log}.'''
        result = self._values.get("access_activity_log")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def access_and_manage_certificates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Privilege for a group to access and manage certificates.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#access_and_manage_certificates Group#access_and_manage_certificates}
        '''
        result = self._values.get("access_and_manage_certificates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def access_and_manage_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#access_and_manage_monitoring Group#access_and_manage_monitoring}
        '''
        result = self._values.get("access_and_manage_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def create_backup_unit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Create backup unit privilege.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_backup_unit Group#create_backup_unit}
        '''
        result = self._values.get("create_backup_unit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def create_datacenter(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_datacenter Group#create_datacenter}.'''
        result = self._values.get("create_datacenter")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def create_flow_log(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Create Flow Logs privilege.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_flow_log Group#create_flow_log}
        '''
        result = self._values.get("create_flow_log")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def create_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Create internet access privilege.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_internet_access Group#create_internet_access}
        '''
        result = self._values.get("create_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def create_k8_s_cluster(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Create Kubernetes cluster privilege.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_k8s_cluster Group#create_k8s_cluster}
        '''
        result = self._values.get("create_k8_s_cluster")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def create_pcc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_pcc Group#create_pcc}.'''
        result = self._values.get("create_pcc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def create_snapshot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create_snapshot Group#create_snapshot}.'''
        result = self._values.get("create_snapshot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#id Group#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manage_dbaas(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Privilege for a group to manage DBaaS related functionality.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#manage_dbaas Group#manage_dbaas}
        '''
        result = self._values.get("manage_dbaas")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def reserve_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#reserve_ip Group#reserve_ip}.'''
        result = self._values.get("reserve_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def s3_privilege(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#s3_privilege Group#s3_privilege}.'''
        result = self._values.get("s3_privilege")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#timeouts Group#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GroupTimeouts"], result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#user_id Group#user_id}.'''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#user_ids Group#user_ids}.'''
        result = self._values.get("user_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-ionoscloud.group.GroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "default": "default",
        "delete": "delete",
        "update": "update",
    },
)
class GroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create Group#create}.
        :param default: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#default Group#default}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#delete Group#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#update Group#update}.
        '''
        if __debug__:
            def stub(
                *,
                create: typing.Optional[builtins.str] = None,
                default: typing.Optional[builtins.str] = None,
                delete: typing.Optional[builtins.str] = None,
                update: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if default is not None:
            self._values["default"] = default
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#create Group#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#default Group#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#delete Group#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/group#update Group#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-ionoscloud.group.GroupTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @default.setter
    def default(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GroupTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GroupTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GroupTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[GroupTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-ionoscloud.group.GroupUsers",
    jsii_struct_bases=[],
    name_mapping={},
)
class GroupUsers:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupUsersList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-ionoscloud.group.GroupUsersList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GroupUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GroupUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class GroupUsersOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-ionoscloud.group.GroupUsersOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="administrator")
    def administrator(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "administrator"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @builtins.property
    @jsii.member(jsii_name="forceSecAuth")
    def force_sec_auth(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "forceSecAuth"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GroupUsers]:
        return typing.cast(typing.Optional[GroupUsers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GroupUsers]) -> None:
        if __debug__:
            def stub(value: typing.Optional[GroupUsers]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Group",
    "GroupConfig",
    "GroupTimeouts",
    "GroupTimeoutsOutputReference",
    "GroupUsers",
    "GroupUsersList",
    "GroupUsersOutputReference",
]

publication.publish()
