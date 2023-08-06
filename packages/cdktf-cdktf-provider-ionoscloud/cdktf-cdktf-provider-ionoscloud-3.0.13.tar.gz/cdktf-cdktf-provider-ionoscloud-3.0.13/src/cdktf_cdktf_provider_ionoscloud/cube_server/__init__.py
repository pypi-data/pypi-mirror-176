'''
# `ionoscloud_cube_server`

Refer to the Terraform Registory for docs: [`ionoscloud_cube_server`](https://www.terraform.io/docs/providers/ionoscloud/r/cube_server).
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


class CubeServer(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-ionoscloud.cubeServer.CubeServer",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server ionoscloud_cube_server}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        datacenter_id: builtins.str,
        name: builtins.str,
        nic: typing.Union["CubeServerNic", typing.Dict[str, typing.Any]],
        template_uuid: builtins.str,
        volume: typing.Union["CubeServerVolume", typing.Dict[str, typing.Any]],
        availability_zone: typing.Optional[builtins.str] = None,
        boot_cdrom: typing.Optional[builtins.str] = None,
        boot_image: typing.Optional[builtins.str] = None,
        cpu_family: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_password: typing.Optional[builtins.str] = None,
        ssh_key_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CubeServerTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server ionoscloud_cube_server} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param datacenter_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#datacenter_id CubeServer#datacenter_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.
        :param nic: nic block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#nic CubeServer#nic}
        :param template_uuid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#template_uuid CubeServer#template_uuid}.
        :param volume: volume block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#volume CubeServer#volume}
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#availability_zone CubeServer#availability_zone}.
        :param boot_cdrom: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#boot_cdrom CubeServer#boot_cdrom}.
        :param boot_image: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#boot_image CubeServer#boot_image}.
        :param cpu_family: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#cpu_family CubeServer#cpu_family}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#id CubeServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#image_name CubeServer#image_name}.
        :param image_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#image_password CubeServer#image_password}.
        :param ssh_key_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#ssh_key_path CubeServer#ssh_key_path}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#timeouts CubeServer#timeouts}
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
                datacenter_id: builtins.str,
                name: builtins.str,
                nic: typing.Union[CubeServerNic, typing.Dict[str, typing.Any]],
                template_uuid: builtins.str,
                volume: typing.Union[CubeServerVolume, typing.Dict[str, typing.Any]],
                availability_zone: typing.Optional[builtins.str] = None,
                boot_cdrom: typing.Optional[builtins.str] = None,
                boot_image: typing.Optional[builtins.str] = None,
                cpu_family: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                image_name: typing.Optional[builtins.str] = None,
                image_password: typing.Optional[builtins.str] = None,
                ssh_key_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                timeouts: typing.Optional[typing.Union[CubeServerTimeouts, typing.Dict[str, typing.Any]]] = None,
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
        config = CubeServerConfig(
            datacenter_id=datacenter_id,
            name=name,
            nic=nic,
            template_uuid=template_uuid,
            volume=volume,
            availability_zone=availability_zone,
            boot_cdrom=boot_cdrom,
            boot_image=boot_image,
            cpu_family=cpu_family,
            id=id,
            image_name=image_name,
            image_password=image_password,
            ssh_key_path=ssh_key_path,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putNic")
    def put_nic(
        self,
        *,
        lan: jsii.Number,
        dhcp: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        firewall: typing.Optional[typing.Union["CubeServerNicFirewall", typing.Dict[str, typing.Any]]] = None,
        firewall_active: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        firewall_type: typing.Optional[builtins.str] = None,
        ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lan: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#lan CubeServer#lan}.
        :param dhcp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#dhcp CubeServer#dhcp}.
        :param firewall: firewall block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#firewall CubeServer#firewall}
        :param firewall_active: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#firewall_active CubeServer#firewall_active}.
        :param firewall_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#firewall_type CubeServer#firewall_type}.
        :param ips: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#ips CubeServer#ips}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.
        '''
        value = CubeServerNic(
            lan=lan,
            dhcp=dhcp,
            firewall=firewall,
            firewall_active=firewall_active,
            firewall_type=firewall_type,
            ips=ips,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putNic", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#create CubeServer#create}.
        :param default: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#default CubeServer#default}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#delete CubeServer#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#update CubeServer#update}.
        '''
        value = CubeServerTimeouts(
            create=create, default=default, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVolume")
    def put_volume(
        self,
        *,
        disk_type: builtins.str,
        availability_zone: typing.Optional[builtins.str] = None,
        backup_unit_id: typing.Optional[builtins.str] = None,
        bus: typing.Optional[builtins.str] = None,
        image_password: typing.Optional[builtins.str] = None,
        licence_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        ssh_key_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#disk_type CubeServer#disk_type}.
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#availability_zone CubeServer#availability_zone}.
        :param backup_unit_id: The uuid of the Backup Unit that user has access to. The property is immutable and is only allowed to be set on a new volume creation. It is mandatory to provide either 'public image' or 'imageAlias' in conjunction with this property. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#backup_unit_id CubeServer#backup_unit_id}
        :param bus: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#bus CubeServer#bus}.
        :param image_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#image_password CubeServer#image_password}.
        :param licence_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#licence_type CubeServer#licence_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.
        :param ssh_key_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#ssh_key_path CubeServer#ssh_key_path}.
        :param user_data: The cloud-init configuration for the volume as base64 encoded string. The property is immutable and is only allowed to be set on a new volume creation. It is mandatory to provide either 'public image' or 'imageAlias' that has cloud-init compatibility in conjunction with this property. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#user_data CubeServer#user_data}
        '''
        value = CubeServerVolume(
            disk_type=disk_type,
            availability_zone=availability_zone,
            backup_unit_id=backup_unit_id,
            bus=bus,
            image_password=image_password,
            licence_type=licence_type,
            name=name,
            ssh_key_path=ssh_key_path,
            user_data=user_data,
        )

        return typing.cast(None, jsii.invoke(self, "putVolume", [value]))

    @jsii.member(jsii_name="resetAvailabilityZone")
    def reset_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZone", []))

    @jsii.member(jsii_name="resetBootCdrom")
    def reset_boot_cdrom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootCdrom", []))

    @jsii.member(jsii_name="resetBootImage")
    def reset_boot_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootImage", []))

    @jsii.member(jsii_name="resetCpuFamily")
    def reset_cpu_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuFamily", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageName")
    def reset_image_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageName", []))

    @jsii.member(jsii_name="resetImagePassword")
    def reset_image_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImagePassword", []))

    @jsii.member(jsii_name="resetSshKeyPath")
    def reset_ssh_key_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshKeyPath", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="bootVolume")
    def boot_volume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootVolume"))

    @builtins.property
    @jsii.member(jsii_name="firewallruleId")
    def firewallrule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallruleId"))

    @builtins.property
    @jsii.member(jsii_name="nic")
    def nic(self) -> "CubeServerNicOutputReference":
        return typing.cast("CubeServerNicOutputReference", jsii.get(self, "nic"))

    @builtins.property
    @jsii.member(jsii_name="primaryIp")
    def primary_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryIp"))

    @builtins.property
    @jsii.member(jsii_name="primaryNic")
    def primary_nic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryNic"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CubeServerTimeoutsOutputReference":
        return typing.cast("CubeServerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> "CubeServerVolumeOutputReference":
        return typing.cast("CubeServerVolumeOutputReference", jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="bootCdromInput")
    def boot_cdrom_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootCdromInput"))

    @builtins.property
    @jsii.member(jsii_name="bootImageInput")
    def boot_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootImageInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuFamilyInput")
    def cpu_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="datacenterIdInput")
    def datacenter_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datacenterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imagePasswordInput")
    def image_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imagePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nicInput")
    def nic_input(self) -> typing.Optional["CubeServerNic"]:
        return typing.cast(typing.Optional["CubeServerNic"], jsii.get(self, "nicInput"))

    @builtins.property
    @jsii.member(jsii_name="sshKeyPathInput")
    def ssh_key_path_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshKeyPathInput"))

    @builtins.property
    @jsii.member(jsii_name="templateUuidInput")
    def template_uuid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateUuidInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CubeServerTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CubeServerTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(self) -> typing.Optional["CubeServerVolume"]:
        return typing.cast(typing.Optional["CubeServerVolume"], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="bootCdrom")
    def boot_cdrom(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootCdrom"))

    @boot_cdrom.setter
    def boot_cdrom(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootCdrom", value)

    @builtins.property
    @jsii.member(jsii_name="bootImage")
    def boot_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootImage"))

    @boot_image.setter
    def boot_image(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootImage", value)

    @builtins.property
    @jsii.member(jsii_name="cpuFamily")
    def cpu_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuFamily"))

    @cpu_family.setter
    def cpu_family(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuFamily", value)

    @builtins.property
    @jsii.member(jsii_name="datacenterId")
    def datacenter_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datacenterId"))

    @datacenter_id.setter
    def datacenter_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datacenterId", value)

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
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imagePassword")
    def image_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imagePassword"))

    @image_password.setter
    def image_password(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imagePassword", value)

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
    @jsii.member(jsii_name="sshKeyPath")
    def ssh_key_path(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeyPath"))

    @ssh_key_path.setter
    def ssh_key_path(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeyPath", value)

    @builtins.property
    @jsii.member(jsii_name="templateUuid")
    def template_uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateUuid"))

    @template_uuid.setter
    def template_uuid(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateUuid", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-ionoscloud.cubeServer.CubeServerConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "datacenter_id": "datacenterId",
        "name": "name",
        "nic": "nic",
        "template_uuid": "templateUuid",
        "volume": "volume",
        "availability_zone": "availabilityZone",
        "boot_cdrom": "bootCdrom",
        "boot_image": "bootImage",
        "cpu_family": "cpuFamily",
        "id": "id",
        "image_name": "imageName",
        "image_password": "imagePassword",
        "ssh_key_path": "sshKeyPath",
        "timeouts": "timeouts",
    },
)
class CubeServerConfig(cdktf.TerraformMetaArguments):
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
        datacenter_id: builtins.str,
        name: builtins.str,
        nic: typing.Union["CubeServerNic", typing.Dict[str, typing.Any]],
        template_uuid: builtins.str,
        volume: typing.Union["CubeServerVolume", typing.Dict[str, typing.Any]],
        availability_zone: typing.Optional[builtins.str] = None,
        boot_cdrom: typing.Optional[builtins.str] = None,
        boot_image: typing.Optional[builtins.str] = None,
        cpu_family: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_password: typing.Optional[builtins.str] = None,
        ssh_key_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CubeServerTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param datacenter_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#datacenter_id CubeServer#datacenter_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.
        :param nic: nic block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#nic CubeServer#nic}
        :param template_uuid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#template_uuid CubeServer#template_uuid}.
        :param volume: volume block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#volume CubeServer#volume}
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#availability_zone CubeServer#availability_zone}.
        :param boot_cdrom: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#boot_cdrom CubeServer#boot_cdrom}.
        :param boot_image: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#boot_image CubeServer#boot_image}.
        :param cpu_family: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#cpu_family CubeServer#cpu_family}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#id CubeServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#image_name CubeServer#image_name}.
        :param image_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#image_password CubeServer#image_password}.
        :param ssh_key_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#ssh_key_path CubeServer#ssh_key_path}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#timeouts CubeServer#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(nic, dict):
            nic = CubeServerNic(**nic)
        if isinstance(volume, dict):
            volume = CubeServerVolume(**volume)
        if isinstance(timeouts, dict):
            timeouts = CubeServerTimeouts(**timeouts)
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
                datacenter_id: builtins.str,
                name: builtins.str,
                nic: typing.Union[CubeServerNic, typing.Dict[str, typing.Any]],
                template_uuid: builtins.str,
                volume: typing.Union[CubeServerVolume, typing.Dict[str, typing.Any]],
                availability_zone: typing.Optional[builtins.str] = None,
                boot_cdrom: typing.Optional[builtins.str] = None,
                boot_image: typing.Optional[builtins.str] = None,
                cpu_family: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                image_name: typing.Optional[builtins.str] = None,
                image_password: typing.Optional[builtins.str] = None,
                ssh_key_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                timeouts: typing.Optional[typing.Union[CubeServerTimeouts, typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument datacenter_id", value=datacenter_id, expected_type=type_hints["datacenter_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nic", value=nic, expected_type=type_hints["nic"])
            check_type(argname="argument template_uuid", value=template_uuid, expected_type=type_hints["template_uuid"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument boot_cdrom", value=boot_cdrom, expected_type=type_hints["boot_cdrom"])
            check_type(argname="argument boot_image", value=boot_image, expected_type=type_hints["boot_image"])
            check_type(argname="argument cpu_family", value=cpu_family, expected_type=type_hints["cpu_family"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_password", value=image_password, expected_type=type_hints["image_password"])
            check_type(argname="argument ssh_key_path", value=ssh_key_path, expected_type=type_hints["ssh_key_path"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "datacenter_id": datacenter_id,
            "name": name,
            "nic": nic,
            "template_uuid": template_uuid,
            "volume": volume,
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
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if boot_cdrom is not None:
            self._values["boot_cdrom"] = boot_cdrom
        if boot_image is not None:
            self._values["boot_image"] = boot_image
        if cpu_family is not None:
            self._values["cpu_family"] = cpu_family
        if id is not None:
            self._values["id"] = id
        if image_name is not None:
            self._values["image_name"] = image_name
        if image_password is not None:
            self._values["image_password"] = image_password
        if ssh_key_path is not None:
            self._values["ssh_key_path"] = ssh_key_path
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def datacenter_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#datacenter_id CubeServer#datacenter_id}.'''
        result = self._values.get("datacenter_id")
        assert result is not None, "Required property 'datacenter_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nic(self) -> "CubeServerNic":
        '''nic block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#nic CubeServer#nic}
        '''
        result = self._values.get("nic")
        assert result is not None, "Required property 'nic' is missing"
        return typing.cast("CubeServerNic", result)

    @builtins.property
    def template_uuid(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#template_uuid CubeServer#template_uuid}.'''
        result = self._values.get("template_uuid")
        assert result is not None, "Required property 'template_uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume(self) -> "CubeServerVolume":
        '''volume block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#volume CubeServer#volume}
        '''
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast("CubeServerVolume", result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#availability_zone CubeServer#availability_zone}.'''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def boot_cdrom(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#boot_cdrom CubeServer#boot_cdrom}.'''
        result = self._values.get("boot_cdrom")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def boot_image(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#boot_image CubeServer#boot_image}.'''
        result = self._values.get("boot_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_family(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#cpu_family CubeServer#cpu_family}.'''
        result = self._values.get("cpu_family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#id CubeServer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#image_name CubeServer#image_name}.'''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#image_password CubeServer#image_password}.'''
        result = self._values.get("image_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_key_path(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#ssh_key_path CubeServer#ssh_key_path}.'''
        result = self._values.get("ssh_key_path")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CubeServerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#timeouts CubeServer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CubeServerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CubeServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-ionoscloud.cubeServer.CubeServerNic",
    jsii_struct_bases=[],
    name_mapping={
        "lan": "lan",
        "dhcp": "dhcp",
        "firewall": "firewall",
        "firewall_active": "firewallActive",
        "firewall_type": "firewallType",
        "ips": "ips",
        "name": "name",
    },
)
class CubeServerNic:
    def __init__(
        self,
        *,
        lan: jsii.Number,
        dhcp: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        firewall: typing.Optional[typing.Union["CubeServerNicFirewall", typing.Dict[str, typing.Any]]] = None,
        firewall_active: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        firewall_type: typing.Optional[builtins.str] = None,
        ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lan: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#lan CubeServer#lan}.
        :param dhcp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#dhcp CubeServer#dhcp}.
        :param firewall: firewall block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#firewall CubeServer#firewall}
        :param firewall_active: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#firewall_active CubeServer#firewall_active}.
        :param firewall_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#firewall_type CubeServer#firewall_type}.
        :param ips: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#ips CubeServer#ips}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.
        '''
        if isinstance(firewall, dict):
            firewall = CubeServerNicFirewall(**firewall)
        if __debug__:
            def stub(
                *,
                lan: jsii.Number,
                dhcp: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                firewall: typing.Optional[typing.Union[CubeServerNicFirewall, typing.Dict[str, typing.Any]]] = None,
                firewall_active: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                firewall_type: typing.Optional[builtins.str] = None,
                ips: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument lan", value=lan, expected_type=type_hints["lan"])
            check_type(argname="argument dhcp", value=dhcp, expected_type=type_hints["dhcp"])
            check_type(argname="argument firewall", value=firewall, expected_type=type_hints["firewall"])
            check_type(argname="argument firewall_active", value=firewall_active, expected_type=type_hints["firewall_active"])
            check_type(argname="argument firewall_type", value=firewall_type, expected_type=type_hints["firewall_type"])
            check_type(argname="argument ips", value=ips, expected_type=type_hints["ips"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {
            "lan": lan,
        }
        if dhcp is not None:
            self._values["dhcp"] = dhcp
        if firewall is not None:
            self._values["firewall"] = firewall
        if firewall_active is not None:
            self._values["firewall_active"] = firewall_active
        if firewall_type is not None:
            self._values["firewall_type"] = firewall_type
        if ips is not None:
            self._values["ips"] = ips
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def lan(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#lan CubeServer#lan}.'''
        result = self._values.get("lan")
        assert result is not None, "Required property 'lan' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def dhcp(self) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#dhcp CubeServer#dhcp}.'''
        result = self._values.get("dhcp")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def firewall(self) -> typing.Optional["CubeServerNicFirewall"]:
        '''firewall block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#firewall CubeServer#firewall}
        '''
        result = self._values.get("firewall")
        return typing.cast(typing.Optional["CubeServerNicFirewall"], result)

    @builtins.property
    def firewall_active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#firewall_active CubeServer#firewall_active}.'''
        result = self._values.get("firewall_active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def firewall_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#firewall_type CubeServer#firewall_type}.'''
        result = self._values.get("firewall_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#ips CubeServer#ips}.'''
        result = self._values.get("ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CubeServerNic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-ionoscloud.cubeServer.CubeServerNicFirewall",
    jsii_struct_bases=[],
    name_mapping={
        "protocol": "protocol",
        "icmp_code": "icmpCode",
        "icmp_type": "icmpType",
        "name": "name",
        "port_range_end": "portRangeEnd",
        "port_range_start": "portRangeStart",
        "source_ip": "sourceIp",
        "source_mac": "sourceMac",
        "target_ip": "targetIp",
        "type": "type",
    },
)
class CubeServerNicFirewall:
    def __init__(
        self,
        *,
        protocol: builtins.str,
        icmp_code: typing.Optional[builtins.str] = None,
        icmp_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port_range_end: typing.Optional[jsii.Number] = None,
        port_range_start: typing.Optional[jsii.Number] = None,
        source_ip: typing.Optional[builtins.str] = None,
        source_mac: typing.Optional[builtins.str] = None,
        target_ip: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#protocol CubeServer#protocol}.
        :param icmp_code: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#icmp_code CubeServer#icmp_code}.
        :param icmp_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#icmp_type CubeServer#icmp_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.
        :param port_range_end: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#port_range_end CubeServer#port_range_end}.
        :param port_range_start: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#port_range_start CubeServer#port_range_start}.
        :param source_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#source_ip CubeServer#source_ip}.
        :param source_mac: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#source_mac CubeServer#source_mac}.
        :param target_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#target_ip CubeServer#target_ip}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#type CubeServer#type}.
        '''
        if __debug__:
            def stub(
                *,
                protocol: builtins.str,
                icmp_code: typing.Optional[builtins.str] = None,
                icmp_type: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                port_range_end: typing.Optional[jsii.Number] = None,
                port_range_start: typing.Optional[jsii.Number] = None,
                source_ip: typing.Optional[builtins.str] = None,
                source_mac: typing.Optional[builtins.str] = None,
                target_ip: typing.Optional[builtins.str] = None,
                type: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument icmp_code", value=icmp_code, expected_type=type_hints["icmp_code"])
            check_type(argname="argument icmp_type", value=icmp_type, expected_type=type_hints["icmp_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port_range_end", value=port_range_end, expected_type=type_hints["port_range_end"])
            check_type(argname="argument port_range_start", value=port_range_start, expected_type=type_hints["port_range_start"])
            check_type(argname="argument source_ip", value=source_ip, expected_type=type_hints["source_ip"])
            check_type(argname="argument source_mac", value=source_mac, expected_type=type_hints["source_mac"])
            check_type(argname="argument target_ip", value=target_ip, expected_type=type_hints["target_ip"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[str, typing.Any] = {
            "protocol": protocol,
        }
        if icmp_code is not None:
            self._values["icmp_code"] = icmp_code
        if icmp_type is not None:
            self._values["icmp_type"] = icmp_type
        if name is not None:
            self._values["name"] = name
        if port_range_end is not None:
            self._values["port_range_end"] = port_range_end
        if port_range_start is not None:
            self._values["port_range_start"] = port_range_start
        if source_ip is not None:
            self._values["source_ip"] = source_ip
        if source_mac is not None:
            self._values["source_mac"] = source_mac
        if target_ip is not None:
            self._values["target_ip"] = target_ip
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#protocol CubeServer#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def icmp_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#icmp_code CubeServer#icmp_code}.'''
        result = self._values.get("icmp_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icmp_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#icmp_type CubeServer#icmp_type}.'''
        result = self._values.get("icmp_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_range_end(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#port_range_end CubeServer#port_range_end}.'''
        result = self._values.get("port_range_end")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_range_start(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#port_range_start CubeServer#port_range_start}.'''
        result = self._values.get("port_range_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#source_ip CubeServer#source_ip}.'''
        result = self._values.get("source_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_mac(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#source_mac CubeServer#source_mac}.'''
        result = self._values.get("source_mac")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#target_ip CubeServer#target_ip}.'''
        result = self._values.get("target_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#type CubeServer#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CubeServerNicFirewall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CubeServerNicFirewallOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-ionoscloud.cubeServer.CubeServerNicFirewallOutputReference",
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

    @jsii.member(jsii_name="resetIcmpCode")
    def reset_icmp_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcmpCode", []))

    @jsii.member(jsii_name="resetIcmpType")
    def reset_icmp_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcmpType", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPortRangeEnd")
    def reset_port_range_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortRangeEnd", []))

    @jsii.member(jsii_name="resetPortRangeStart")
    def reset_port_range_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortRangeStart", []))

    @jsii.member(jsii_name="resetSourceIp")
    def reset_source_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceIp", []))

    @jsii.member(jsii_name="resetSourceMac")
    def reset_source_mac(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceMac", []))

    @jsii.member(jsii_name="resetTargetIp")
    def reset_target_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetIp", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="icmpCodeInput")
    def icmp_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "icmpCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="icmpTypeInput")
    def icmp_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "icmpTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portRangeEndInput")
    def port_range_end_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portRangeEndInput"))

    @builtins.property
    @jsii.member(jsii_name="portRangeStartInput")
    def port_range_start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portRangeStartInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIpInput")
    def source_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceIpInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceMacInput")
    def source_mac_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceMacInput"))

    @builtins.property
    @jsii.member(jsii_name="targetIpInput")
    def target_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetIpInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="icmpCode")
    def icmp_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "icmpCode"))

    @icmp_code.setter
    def icmp_code(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icmpCode", value)

    @builtins.property
    @jsii.member(jsii_name="icmpType")
    def icmp_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "icmpType"))

    @icmp_type.setter
    def icmp_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icmpType", value)

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
    @jsii.member(jsii_name="portRangeEnd")
    def port_range_end(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "portRangeEnd"))

    @port_range_end.setter
    def port_range_end(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portRangeEnd", value)

    @builtins.property
    @jsii.member(jsii_name="portRangeStart")
    def port_range_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "portRangeStart"))

    @port_range_start.setter
    def port_range_start(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portRangeStart", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="sourceIp")
    def source_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceIp"))

    @source_ip.setter
    def source_ip(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIp", value)

    @builtins.property
    @jsii.member(jsii_name="sourceMac")
    def source_mac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceMac"))

    @source_mac.setter
    def source_mac(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceMac", value)

    @builtins.property
    @jsii.member(jsii_name="targetIp")
    def target_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetIp"))

    @target_ip.setter
    def target_ip(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetIp", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CubeServerNicFirewall]:
        return typing.cast(typing.Optional[CubeServerNicFirewall], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CubeServerNicFirewall]) -> None:
        if __debug__:
            def stub(value: typing.Optional[CubeServerNicFirewall]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CubeServerNicOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-ionoscloud.cubeServer.CubeServerNicOutputReference",
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

    @jsii.member(jsii_name="putFirewall")
    def put_firewall(
        self,
        *,
        protocol: builtins.str,
        icmp_code: typing.Optional[builtins.str] = None,
        icmp_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port_range_end: typing.Optional[jsii.Number] = None,
        port_range_start: typing.Optional[jsii.Number] = None,
        source_ip: typing.Optional[builtins.str] = None,
        source_mac: typing.Optional[builtins.str] = None,
        target_ip: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#protocol CubeServer#protocol}.
        :param icmp_code: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#icmp_code CubeServer#icmp_code}.
        :param icmp_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#icmp_type CubeServer#icmp_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.
        :param port_range_end: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#port_range_end CubeServer#port_range_end}.
        :param port_range_start: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#port_range_start CubeServer#port_range_start}.
        :param source_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#source_ip CubeServer#source_ip}.
        :param source_mac: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#source_mac CubeServer#source_mac}.
        :param target_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#target_ip CubeServer#target_ip}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#type CubeServer#type}.
        '''
        value = CubeServerNicFirewall(
            protocol=protocol,
            icmp_code=icmp_code,
            icmp_type=icmp_type,
            name=name,
            port_range_end=port_range_end,
            port_range_start=port_range_start,
            source_ip=source_ip,
            source_mac=source_mac,
            target_ip=target_ip,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putFirewall", [value]))

    @jsii.member(jsii_name="resetDhcp")
    def reset_dhcp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDhcp", []))

    @jsii.member(jsii_name="resetFirewall")
    def reset_firewall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirewall", []))

    @jsii.member(jsii_name="resetFirewallActive")
    def reset_firewall_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirewallActive", []))

    @jsii.member(jsii_name="resetFirewallType")
    def reset_firewall_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirewallType", []))

    @jsii.member(jsii_name="resetIps")
    def reset_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIps", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="deviceNumber")
    def device_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deviceNumber"))

    @builtins.property
    @jsii.member(jsii_name="firewall")
    def firewall(self) -> CubeServerNicFirewallOutputReference:
        return typing.cast(CubeServerNicFirewallOutputReference, jsii.get(self, "firewall"))

    @builtins.property
    @jsii.member(jsii_name="mac")
    def mac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mac"))

    @builtins.property
    @jsii.member(jsii_name="pciSlot")
    def pci_slot(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pciSlot"))

    @builtins.property
    @jsii.member(jsii_name="dhcpInput")
    def dhcp_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "dhcpInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallActiveInput")
    def firewall_active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "firewallActiveInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallInput")
    def firewall_input(self) -> typing.Optional[CubeServerNicFirewall]:
        return typing.cast(typing.Optional[CubeServerNicFirewall], jsii.get(self, "firewallInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallTypeInput")
    def firewall_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsInput")
    def ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipsInput"))

    @builtins.property
    @jsii.member(jsii_name="lanInput")
    def lan_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lanInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcp")
    def dhcp(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "dhcp"))

    @dhcp.setter
    def dhcp(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dhcp", value)

    @builtins.property
    @jsii.member(jsii_name="firewallActive")
    def firewall_active(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "firewallActive"))

    @firewall_active.setter
    def firewall_active(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallActive", value)

    @builtins.property
    @jsii.member(jsii_name="firewallType")
    def firewall_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallType"))

    @firewall_type.setter
    def firewall_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallType", value)

    @builtins.property
    @jsii.member(jsii_name="ips")
    def ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ips"))

    @ips.setter
    def ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ips", value)

    @builtins.property
    @jsii.member(jsii_name="lan")
    def lan(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lan"))

    @lan.setter
    def lan(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lan", value)

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
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CubeServerNic]:
        return typing.cast(typing.Optional[CubeServerNic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CubeServerNic]) -> None:
        if __debug__:
            def stub(value: typing.Optional[CubeServerNic]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-ionoscloud.cubeServer.CubeServerTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "default": "default",
        "delete": "delete",
        "update": "update",
    },
)
class CubeServerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#create CubeServer#create}.
        :param default: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#default CubeServer#default}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#delete CubeServer#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#update CubeServer#update}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#create CubeServer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#default CubeServer#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#delete CubeServer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#update CubeServer#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CubeServerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CubeServerTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-ionoscloud.cubeServer.CubeServerTimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[CubeServerTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CubeServerTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CubeServerTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CubeServerTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-ionoscloud.cubeServer.CubeServerVolume",
    jsii_struct_bases=[],
    name_mapping={
        "disk_type": "diskType",
        "availability_zone": "availabilityZone",
        "backup_unit_id": "backupUnitId",
        "bus": "bus",
        "image_password": "imagePassword",
        "licence_type": "licenceType",
        "name": "name",
        "ssh_key_path": "sshKeyPath",
        "user_data": "userData",
    },
)
class CubeServerVolume:
    def __init__(
        self,
        *,
        disk_type: builtins.str,
        availability_zone: typing.Optional[builtins.str] = None,
        backup_unit_id: typing.Optional[builtins.str] = None,
        bus: typing.Optional[builtins.str] = None,
        image_password: typing.Optional[builtins.str] = None,
        licence_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        ssh_key_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#disk_type CubeServer#disk_type}.
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#availability_zone CubeServer#availability_zone}.
        :param backup_unit_id: The uuid of the Backup Unit that user has access to. The property is immutable and is only allowed to be set on a new volume creation. It is mandatory to provide either 'public image' or 'imageAlias' in conjunction with this property. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#backup_unit_id CubeServer#backup_unit_id}
        :param bus: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#bus CubeServer#bus}.
        :param image_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#image_password CubeServer#image_password}.
        :param licence_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#licence_type CubeServer#licence_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.
        :param ssh_key_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#ssh_key_path CubeServer#ssh_key_path}.
        :param user_data: The cloud-init configuration for the volume as base64 encoded string. The property is immutable and is only allowed to be set on a new volume creation. It is mandatory to provide either 'public image' or 'imageAlias' that has cloud-init compatibility in conjunction with this property. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#user_data CubeServer#user_data}
        '''
        if __debug__:
            def stub(
                *,
                disk_type: builtins.str,
                availability_zone: typing.Optional[builtins.str] = None,
                backup_unit_id: typing.Optional[builtins.str] = None,
                bus: typing.Optional[builtins.str] = None,
                image_password: typing.Optional[builtins.str] = None,
                licence_type: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                ssh_key_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_data: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument backup_unit_id", value=backup_unit_id, expected_type=type_hints["backup_unit_id"])
            check_type(argname="argument bus", value=bus, expected_type=type_hints["bus"])
            check_type(argname="argument image_password", value=image_password, expected_type=type_hints["image_password"])
            check_type(argname="argument licence_type", value=licence_type, expected_type=type_hints["licence_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ssh_key_path", value=ssh_key_path, expected_type=type_hints["ssh_key_path"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[str, typing.Any] = {
            "disk_type": disk_type,
        }
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_unit_id is not None:
            self._values["backup_unit_id"] = backup_unit_id
        if bus is not None:
            self._values["bus"] = bus
        if image_password is not None:
            self._values["image_password"] = image_password
        if licence_type is not None:
            self._values["licence_type"] = licence_type
        if name is not None:
            self._values["name"] = name
        if ssh_key_path is not None:
            self._values["ssh_key_path"] = ssh_key_path
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def disk_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#disk_type CubeServer#disk_type}.'''
        result = self._values.get("disk_type")
        assert result is not None, "Required property 'disk_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#availability_zone CubeServer#availability_zone}.'''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_unit_id(self) -> typing.Optional[builtins.str]:
        '''The uuid of the Backup Unit that user has access to.

        The property is immutable and is only allowed to be set on a new volume creation. It is mandatory to provide either 'public image' or 'imageAlias' in conjunction with this property.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#backup_unit_id CubeServer#backup_unit_id}
        '''
        result = self._values.get("backup_unit_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bus(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#bus CubeServer#bus}.'''
        result = self._values.get("bus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#image_password CubeServer#image_password}.'''
        result = self._values.get("image_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def licence_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#licence_type CubeServer#licence_type}.'''
        result = self._values.get("licence_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#name CubeServer#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_key_path(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#ssh_key_path CubeServer#ssh_key_path}.'''
        result = self._values.get("ssh_key_path")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''The cloud-init configuration for the volume as base64 encoded string.

        The property is immutable and is only allowed to be set on a new volume creation. It is mandatory to provide either 'public image' or 'imageAlias' that has cloud-init compatibility in conjunction with this property.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ionoscloud/r/cube_server#user_data CubeServer#user_data}
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CubeServerVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CubeServerVolumeOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-ionoscloud.cubeServer.CubeServerVolumeOutputReference",
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

    @jsii.member(jsii_name="resetAvailabilityZone")
    def reset_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZone", []))

    @jsii.member(jsii_name="resetBackupUnitId")
    def reset_backup_unit_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupUnitId", []))

    @jsii.member(jsii_name="resetBus")
    def reset_bus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBus", []))

    @jsii.member(jsii_name="resetImagePassword")
    def reset_image_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImagePassword", []))

    @jsii.member(jsii_name="resetLicenceType")
    def reset_licence_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenceType", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSshKeyPath")
    def reset_ssh_key_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshKeyPath", []))

    @jsii.member(jsii_name="resetUserData")
    def reset_user_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserData", []))

    @builtins.property
    @jsii.member(jsii_name="bootServer")
    def boot_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootServer"))

    @builtins.property
    @jsii.member(jsii_name="cpuHotPlug")
    def cpu_hot_plug(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "cpuHotPlug"))

    @builtins.property
    @jsii.member(jsii_name="deviceNumber")
    def device_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deviceNumber"))

    @builtins.property
    @jsii.member(jsii_name="discVirtioHotPlug")
    def disc_virtio_hot_plug(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "discVirtioHotPlug"))

    @builtins.property
    @jsii.member(jsii_name="discVirtioHotUnplug")
    def disc_virtio_hot_unplug(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "discVirtioHotUnplug"))

    @builtins.property
    @jsii.member(jsii_name="nicHotPlug")
    def nic_hot_plug(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "nicHotPlug"))

    @builtins.property
    @jsii.member(jsii_name="nicHotUnplug")
    def nic_hot_unplug(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "nicHotUnplug"))

    @builtins.property
    @jsii.member(jsii_name="pciSlot")
    def pci_slot(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pciSlot"))

    @builtins.property
    @jsii.member(jsii_name="ramHotPlug")
    def ram_hot_plug(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "ramHotPlug"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="backupUnitIdInput")
    def backup_unit_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupUnitIdInput"))

    @builtins.property
    @jsii.member(jsii_name="busInput")
    def bus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "busInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="imagePasswordInput")
    def image_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imagePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="licenceTypeInput")
    def licence_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sshKeyPathInput")
    def ssh_key_path_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshKeyPathInput"))

    @builtins.property
    @jsii.member(jsii_name="userDataInput")
    def user_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDataInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="backupUnitId")
    def backup_unit_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupUnitId"))

    @backup_unit_id.setter
    def backup_unit_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupUnitId", value)

    @builtins.property
    @jsii.member(jsii_name="bus")
    def bus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bus"))

    @bus.setter
    def bus(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bus", value)

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value)

    @builtins.property
    @jsii.member(jsii_name="imagePassword")
    def image_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imagePassword"))

    @image_password.setter
    def image_password(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imagePassword", value)

    @builtins.property
    @jsii.member(jsii_name="licenceType")
    def licence_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenceType"))

    @licence_type.setter
    def licence_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenceType", value)

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
    @jsii.member(jsii_name="sshKeyPath")
    def ssh_key_path(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeyPath"))

    @ssh_key_path.setter
    def ssh_key_path(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeyPath", value)

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userData"))

    @user_data.setter
    def user_data(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userData", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CubeServerVolume]:
        return typing.cast(typing.Optional[CubeServerVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CubeServerVolume]) -> None:
        if __debug__:
            def stub(value: typing.Optional[CubeServerVolume]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CubeServer",
    "CubeServerConfig",
    "CubeServerNic",
    "CubeServerNicFirewall",
    "CubeServerNicFirewallOutputReference",
    "CubeServerNicOutputReference",
    "CubeServerTimeouts",
    "CubeServerTimeoutsOutputReference",
    "CubeServerVolume",
    "CubeServerVolumeOutputReference",
]

publication.publish()
