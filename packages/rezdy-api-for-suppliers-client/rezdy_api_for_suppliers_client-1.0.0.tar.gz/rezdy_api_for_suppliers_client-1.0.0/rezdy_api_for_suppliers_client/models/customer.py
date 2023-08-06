import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.customer_gender import CustomerGender
from ..models.customer_title import CustomerTitle
from ..types import UNSET, Unset

T = TypeVar("T", bound="Customer")


@attr.s(auto_attribs=True)
class Customer:
    """The customer is the person making the booking, and most of the time paying for it.<br>It differs from Participants,
    who are the people attending a tour

        Attributes:
            about_us (Union[Unset, str]): How did you hear about us?
            address_line (Union[Unset, str]): Address
            address_line_2 (Union[Unset, str]): Extended Address
            city (Union[Unset, str]): City/Town/Suburb
            company_name (Union[Unset, str]): Company name
            country_code (Union[Unset, str]): 2 letter ISO country code
            dob (Union[Unset, datetime.datetime]): Date of birth
            email (Union[Unset, str]): Email
            fax (Union[Unset, str]): Fax number
            first_name (Union[Unset, str]): First name
            gender (Union[Unset, CustomerGender]): Gender: MALE or FEMALE
            id (Union[Unset, int]): Rezdy internal ID of the customer
            last_name (Union[Unset, str]): Last Name
            marketing (Union[Unset, bool]): Agree to receive marketing emails
            middle_name (Union[Unset, str]): Middle name
            mobile (Union[Unset, str]): Mobile phone number
            name (Union[Unset, str]): Full name - generated from first/middle/last names
            newsletter (Union[Unset, bool]): Subscribe to the newsletter
            phone (Union[Unset, str]): Preferred Phone number
            post_code (Union[Unset, str]): Postcode / ZIP
            preferred_language (Union[Unset, str]): Preferred language. Should be a 2 letter ISO country code
            skype (Union[Unset, str]): Skype alias
            state (Union[Unset, str]): State/County/Region
            title (Union[Unset, CustomerTitle]): Title
    """

    about_us: Union[Unset, str] = UNSET
    address_line: Union[Unset, str] = UNSET
    address_line_2: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    company_name: Union[Unset, str] = UNSET
    country_code: Union[Unset, str] = UNSET
    dob: Union[Unset, datetime.datetime] = UNSET
    email: Union[Unset, str] = UNSET
    fax: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    gender: Union[Unset, CustomerGender] = UNSET
    id: Union[Unset, int] = UNSET
    last_name: Union[Unset, str] = UNSET
    marketing: Union[Unset, bool] = UNSET
    middle_name: Union[Unset, str] = UNSET
    mobile: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    newsletter: Union[Unset, bool] = UNSET
    phone: Union[Unset, str] = UNSET
    post_code: Union[Unset, str] = UNSET
    preferred_language: Union[Unset, str] = UNSET
    skype: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    title: Union[Unset, CustomerTitle] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        about_us = self.about_us
        address_line = self.address_line
        address_line_2 = self.address_line_2
        city = self.city
        company_name = self.company_name
        country_code = self.country_code
        dob: Union[Unset, str] = UNSET
        if not isinstance(self.dob, Unset):
            dob = self.dob.isoformat()

        email = self.email
        fax = self.fax
        first_name = self.first_name
        gender: Union[Unset, str] = UNSET
        if not isinstance(self.gender, Unset):
            gender = self.gender.value

        id = self.id
        last_name = self.last_name
        marketing = self.marketing
        middle_name = self.middle_name
        mobile = self.mobile
        name = self.name
        newsletter = self.newsletter
        phone = self.phone
        post_code = self.post_code
        preferred_language = self.preferred_language
        skype = self.skype
        state = self.state
        title: Union[Unset, str] = UNSET
        if not isinstance(self.title, Unset):
            title = self.title.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if about_us is not UNSET:
            field_dict["aboutUs"] = about_us
        if address_line is not UNSET:
            field_dict["addressLine"] = address_line
        if address_line_2 is not UNSET:
            field_dict["addressLine2"] = address_line_2
        if city is not UNSET:
            field_dict["city"] = city
        if company_name is not UNSET:
            field_dict["companyName"] = company_name
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if dob is not UNSET:
            field_dict["dob"] = dob
        if email is not UNSET:
            field_dict["email"] = email
        if fax is not UNSET:
            field_dict["fax"] = fax
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if gender is not UNSET:
            field_dict["gender"] = gender
        if id is not UNSET:
            field_dict["id"] = id
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if marketing is not UNSET:
            field_dict["marketing"] = marketing
        if middle_name is not UNSET:
            field_dict["middleName"] = middle_name
        if mobile is not UNSET:
            field_dict["mobile"] = mobile
        if name is not UNSET:
            field_dict["name"] = name
        if newsletter is not UNSET:
            field_dict["newsletter"] = newsletter
        if phone is not UNSET:
            field_dict["phone"] = phone
        if post_code is not UNSET:
            field_dict["postCode"] = post_code
        if preferred_language is not UNSET:
            field_dict["preferredLanguage"] = preferred_language
        if skype is not UNSET:
            field_dict["skype"] = skype
        if state is not UNSET:
            field_dict["state"] = state
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        about_us = d.pop("aboutUs", UNSET)

        address_line = d.pop("addressLine", UNSET)

        address_line_2 = d.pop("addressLine2", UNSET)

        city = d.pop("city", UNSET)

        company_name = d.pop("companyName", UNSET)

        country_code = d.pop("countryCode", UNSET)

        _dob = d.pop("dob", UNSET)
        dob: Union[Unset, datetime.datetime]
        if isinstance(_dob, Unset):
            dob = UNSET
        else:
            dob = isoparse(_dob)

        email = d.pop("email", UNSET)

        fax = d.pop("fax", UNSET)

        first_name = d.pop("firstName", UNSET)

        _gender = d.pop("gender", UNSET)
        gender: Union[Unset, CustomerGender]
        if isinstance(_gender, Unset):
            gender = UNSET
        else:
            gender = CustomerGender(_gender)

        id = d.pop("id", UNSET)

        last_name = d.pop("lastName", UNSET)

        marketing = d.pop("marketing", UNSET)

        middle_name = d.pop("middleName", UNSET)

        mobile = d.pop("mobile", UNSET)

        name = d.pop("name", UNSET)

        newsletter = d.pop("newsletter", UNSET)

        phone = d.pop("phone", UNSET)

        post_code = d.pop("postCode", UNSET)

        preferred_language = d.pop("preferredLanguage", UNSET)

        skype = d.pop("skype", UNSET)

        state = d.pop("state", UNSET)

        _title = d.pop("title", UNSET)
        title: Union[Unset, CustomerTitle]
        if isinstance(_title, Unset):
            title = UNSET
        else:
            title = CustomerTitle(_title)

        customer = cls(
            about_us=about_us,
            address_line=address_line,
            address_line_2=address_line_2,
            city=city,
            company_name=company_name,
            country_code=country_code,
            dob=dob,
            email=email,
            fax=fax,
            first_name=first_name,
            gender=gender,
            id=id,
            last_name=last_name,
            marketing=marketing,
            middle_name=middle_name,
            mobile=mobile,
            name=name,
            newsletter=newsletter,
            phone=phone,
            post_code=post_code,
            preferred_language=preferred_language,
            skype=skype,
            state=state,
            title=title,
        )

        customer.additional_properties = d
        return customer

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
