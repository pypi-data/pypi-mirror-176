import json
import logging
import typing

import pydantic
import requests

from .util import IDMNotReachableError

if typing.TYPE_CHECKING:
    from requests import Response


DATA_TYPE = str | list | dict | None


class IDMRequest(pydantic.BaseModel):
    username: str
    password: str
    api_url: str = "https://idm.gwdg.de/api/v3"

    def run_request(
        self, func: typing.Callable[..., "Response"], url: str, data: DATA_TYPE = None
    ) -> "Response":
        try:
            return func(
                url,
                auth=(self.username, self.password),
                timeout=60,  # Needs to be this high to allow for an all-objects query
                headers={
                    "Accept": "application/json",
                    "Accept-Language": "en",
                    "Content-Type": "application/json",
                },
                data=data,
            )
        except Exception as e:
            raise IDMNotReachableError(
                f"Could not connect to IDM: IDM not reachable!\n{e}"
            )

    def get_request(self, url: str) -> "Response":
        return self.run_request(requests.get, url)

    def put_request(self, url: str, data: DATA_TYPE) -> "Response":
        return self.run_request(requests.put, url, data)

    def post_request(self, url: str, data: DATA_TYPE) -> "Response":
        return self.run_request(requests.post, url, data)


class ChangeTemplate(pydantic.BaseModel):
    id: str

    @staticmethod
    def update_json(name: str, value: list[str] | str) -> str:
        data = {
            "name": name,
            "value": [value] if not isinstance(value, list) else value,
        }
        return json.dumps({"attributes": [data]})

    @pydantic.root_validator(pre=True)
    def validate_results(cls, provided_values):
        type_dict = {key: value.type_ for key, value in cls.__fields__.items()}

        output_dict = {}
        for key, type_val in type_dict.items():
            if key in provided_values:
                cur_val = provided_values[key]
                if isinstance(cur_val, type_val):
                    value = cur_val
                elif type_val is str and isinstance(cur_val, list):
                    if len(cur_val) > 1:
                        logging.warning(
                            "\n"
                            "  str expected, but found list: Using first element\n"
                            "  Please check your class specifications.\n"
                            f"  User: {provided_values['goesternSAMAccountName']}\n"
                            f"  Key: {key}"
                            f"  Value: {cur_val}"
                        )
                    try:
                        value = cur_val[0]
                    except IndexError:
                        logging.warning(
                            "  str expected, but empty list found: Set to empty string\n"
                            "  Please check your class specifications.\n"
                            f"  User: {provided_values['goesternSAMAccountName']}\n"
                            f"  Key: {key}"
                            f"  Value: {cur_val}"
                        )
                        value = ""
                else:
                    assert False, (
                        "  Only str and list types are supported so far!"
                        f"  User: {provided_values['goesternSAMAccountName']}\n"
                        f"  Key: {key}"
                        f"  Value: {cur_val}"
                    )

            else:
                value = type_val()
            output_dict[key] = value

        return output_dict

    @classmethod
    def from_json(cls, json: dict) -> "ChangeTemplate":
        response_dict: dict[str, list[str]]

        response_dict = {
            "id": [json["id"]],
            "dn": [json["dn"]],
        }
        response_dict.update(
            {entry["name"]: entry["value"] for entry in json["attributes"]}
        )

        return cls(**response_dict)  # type: ignore


class CreateTemplate(pydantic.BaseModel):
    create_template_name: str

    def to_json(self) -> str:
        data = [
            {
                "name": key.removeprefix("_"),
                "value": [value] if not isinstance(value, list) else value,
            }
            for key, value in self.dict().items()
            if key != "create_template_name"
        ]
        return json.dumps({"attributes": data})


class BaseGWDGUser(ChangeTemplate):
    # Common fields
    ou: str
    employeeNumber: str
    mpgEmployeeNumber: str
    employeeType: str
    employeeStatus: str
    accountType: str
    uid: str
    oldUid: list
    goesternSAMAccountName: str
    ou: str
    goesternUserType: str
    givenName: str
    sn: str
    goesternGWDGadDisplayName: str
    description: str
    departmentNumber: str
    title: str
    telephoneNumber: str
    mobile: str
    facsimileTelephoneNumber: str
    roomNumber: str
    street: str
    postalCode: str
    city: str
    st: str
    l: str
    goesternProxyAddresses: list
    mail: str
    goesternExchangeQuota: str
    goesternMailboxServer: str
    goesternMailboxZugehoerigkeit: str
    exchangeTargetAddress: str
    goesternMailRoutingAddresses: list
    goesternExchHideFromAddressLists: str
    externalEmailAddress: list
    filterAttribute1: list
    filterAttribute2: list
    filterAttribute3: list
    goesternExpirationDate: str
    isScheduledForDeletion: str
    goesternUserStatus: str
    goesternDisableReason: str
    goesternDisableDate: str
    goesternRemoveDate: str
    goesternLockoutTime: str
    ownCloudQuota: str
    memberOfStaticExchangeDistGrp: list
    isInitialPassword: str
    createTimestamp: str
    modifyTimeStamp: str
    pwdChangedTime: str
    passwordExpirationTime: str
    isInitialAdditionalPassword: str
    additionalPasswordModifyTime: str
    additionalPasswordExpirationTime: str
    eduPersonPrincipalName: str
    effectivePrivilege: list
    responsiblePerson: list
