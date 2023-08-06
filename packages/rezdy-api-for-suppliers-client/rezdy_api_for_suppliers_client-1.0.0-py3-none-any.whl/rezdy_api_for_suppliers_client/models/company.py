from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.address import Address
from ..models.video import Video
from ..types import UNSET, Unset

T = TypeVar("T", bound="Company")


@attr.s(auto_attribs=True)
class Company:
    """Company object. Holds general details and information about a specific company.

    Attributes:
        address (Union[Unset, Address]): Address of a company, customer or product location.
        agent_description (Union[Unset, str]): Agent description, if the company is an agent.
        agent_registration_link (Union[Unset, str]): Agent registration link, if the company is an agent
        alias (Union[Unset, str]): Company alias. This is the unique identifier for this company
        booking_system (Union[Unset, str]): Company Booking System
        category (Union[Unset, str]): Company category
        company_description (Union[Unset, str]): Company description
        company_logo_url (Union[Unset, str]): URL of the company logo.
        company_name (Union[Unset, str]): Company name
        currency (Union[Unset, str]): Default currency used by this company.
        destination_country_code (Union[Unset, str]): Company destination. Country code.
        destination_name (Union[Unset, str]): Company destination. Name of the area.
        destination_path (Union[Unset, str]): Company destination. Destination path.
        facebook_page (Union[Unset, str]): Company facebook page
        fax (Union[Unset, str]): Company fax
        fb_page_id (Union[Unset, str]): Company facebook page id
        first_name (Union[Unset, str]): First name of company representative
        google_plus (Union[Unset, str]): Company google plus profile
        instagram (Union[Unset, str]): Company instagram profile
        last_name (Union[Unset, str]): Last name of company representative
        locale (Union[Unset, str]): Locale of this company.
        mobile (Union[Unset, str]): Company mobile
        opening_hours (Union[Unset, str]): Company opening hours
        phone (Union[Unset, str]): Company phone
        pinterest (Union[Unset, str]): Company pinterest profile
        privacy_policy (Union[Unset, str]): Privacy Policy
        skype (Union[Unset, str]): Company skype
        terms (Union[Unset, str]): General terms and conditions
        timezone (Union[Unset, str]): Timezone of this company.
        trip_advisor (Union[Unset, str]): Company trip advisor profile
        twitter (Union[Unset, str]): Company trip twitter profile
        video (Union[Unset, Video]): Video links.
        website (Union[Unset, str]): Company website
        yelp (Union[Unset, str]): Company yelp profile
        youtube_channel (Union[Unset, str]): Company youtube channel
    """

    address: Union[Unset, Address] = UNSET
    agent_description: Union[Unset, str] = UNSET
    agent_registration_link: Union[Unset, str] = UNSET
    alias: Union[Unset, str] = UNSET
    booking_system: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    company_description: Union[Unset, str] = UNSET
    company_logo_url: Union[Unset, str] = UNSET
    company_name: Union[Unset, str] = UNSET
    currency: Union[Unset, str] = UNSET
    destination_country_code: Union[Unset, str] = UNSET
    destination_name: Union[Unset, str] = UNSET
    destination_path: Union[Unset, str] = UNSET
    facebook_page: Union[Unset, str] = UNSET
    fax: Union[Unset, str] = UNSET
    fb_page_id: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    google_plus: Union[Unset, str] = UNSET
    instagram: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    locale: Union[Unset, str] = UNSET
    mobile: Union[Unset, str] = UNSET
    opening_hours: Union[Unset, str] = UNSET
    phone: Union[Unset, str] = UNSET
    pinterest: Union[Unset, str] = UNSET
    privacy_policy: Union[Unset, str] = UNSET
    skype: Union[Unset, str] = UNSET
    terms: Union[Unset, str] = UNSET
    timezone: Union[Unset, str] = UNSET
    trip_advisor: Union[Unset, str] = UNSET
    twitter: Union[Unset, str] = UNSET
    video: Union[Unset, Video] = UNSET
    website: Union[Unset, str] = UNSET
    yelp: Union[Unset, str] = UNSET
    youtube_channel: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        agent_description = self.agent_description
        agent_registration_link = self.agent_registration_link
        alias = self.alias
        booking_system = self.booking_system
        category = self.category
        company_description = self.company_description
        company_logo_url = self.company_logo_url
        company_name = self.company_name
        currency = self.currency
        destination_country_code = self.destination_country_code
        destination_name = self.destination_name
        destination_path = self.destination_path
        facebook_page = self.facebook_page
        fax = self.fax
        fb_page_id = self.fb_page_id
        first_name = self.first_name
        google_plus = self.google_plus
        instagram = self.instagram
        last_name = self.last_name
        locale = self.locale
        mobile = self.mobile
        opening_hours = self.opening_hours
        phone = self.phone
        pinterest = self.pinterest
        privacy_policy = self.privacy_policy
        skype = self.skype
        terms = self.terms
        timezone = self.timezone
        trip_advisor = self.trip_advisor
        twitter = self.twitter
        video: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.video, Unset):
            video = self.video.to_dict()

        website = self.website
        yelp = self.yelp
        youtube_channel = self.youtube_channel

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if address is not UNSET:
            field_dict["address"] = address
        if agent_description is not UNSET:
            field_dict["agentDescription"] = agent_description
        if agent_registration_link is not UNSET:
            field_dict["agentRegistrationLink"] = agent_registration_link
        if alias is not UNSET:
            field_dict["alias"] = alias
        if booking_system is not UNSET:
            field_dict["bookingSystem"] = booking_system
        if category is not UNSET:
            field_dict["category"] = category
        if company_description is not UNSET:
            field_dict["companyDescription"] = company_description
        if company_logo_url is not UNSET:
            field_dict["companyLogoUrl"] = company_logo_url
        if company_name is not UNSET:
            field_dict["companyName"] = company_name
        if currency is not UNSET:
            field_dict["currency"] = currency
        if destination_country_code is not UNSET:
            field_dict["destinationCountryCode"] = destination_country_code
        if destination_name is not UNSET:
            field_dict["destinationName"] = destination_name
        if destination_path is not UNSET:
            field_dict["destinationPath"] = destination_path
        if facebook_page is not UNSET:
            field_dict["facebookPage"] = facebook_page
        if fax is not UNSET:
            field_dict["fax"] = fax
        if fb_page_id is not UNSET:
            field_dict["fbPageId"] = fb_page_id
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if google_plus is not UNSET:
            field_dict["googlePlus"] = google_plus
        if instagram is not UNSET:
            field_dict["instagram"] = instagram
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if locale is not UNSET:
            field_dict["locale"] = locale
        if mobile is not UNSET:
            field_dict["mobile"] = mobile
        if opening_hours is not UNSET:
            field_dict["openingHours"] = opening_hours
        if phone is not UNSET:
            field_dict["phone"] = phone
        if pinterest is not UNSET:
            field_dict["pinterest"] = pinterest
        if privacy_policy is not UNSET:
            field_dict["privacyPolicy"] = privacy_policy
        if skype is not UNSET:
            field_dict["skype"] = skype
        if terms is not UNSET:
            field_dict["terms"] = terms
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if trip_advisor is not UNSET:
            field_dict["tripAdvisor"] = trip_advisor
        if twitter is not UNSET:
            field_dict["twitter"] = twitter
        if video is not UNSET:
            field_dict["video"] = video
        if website is not UNSET:
            field_dict["website"] = website
        if yelp is not UNSET:
            field_dict["yelp"] = yelp
        if youtube_channel is not UNSET:
            field_dict["youtubeChannel"] = youtube_channel

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _address = d.pop("address", UNSET)
        address: Union[Unset, Address]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = Address.from_dict(_address)

        agent_description = d.pop("agentDescription", UNSET)

        agent_registration_link = d.pop("agentRegistrationLink", UNSET)

        alias = d.pop("alias", UNSET)

        booking_system = d.pop("bookingSystem", UNSET)

        category = d.pop("category", UNSET)

        company_description = d.pop("companyDescription", UNSET)

        company_logo_url = d.pop("companyLogoUrl", UNSET)

        company_name = d.pop("companyName", UNSET)

        currency = d.pop("currency", UNSET)

        destination_country_code = d.pop("destinationCountryCode", UNSET)

        destination_name = d.pop("destinationName", UNSET)

        destination_path = d.pop("destinationPath", UNSET)

        facebook_page = d.pop("facebookPage", UNSET)

        fax = d.pop("fax", UNSET)

        fb_page_id = d.pop("fbPageId", UNSET)

        first_name = d.pop("firstName", UNSET)

        google_plus = d.pop("googlePlus", UNSET)

        instagram = d.pop("instagram", UNSET)

        last_name = d.pop("lastName", UNSET)

        locale = d.pop("locale", UNSET)

        mobile = d.pop("mobile", UNSET)

        opening_hours = d.pop("openingHours", UNSET)

        phone = d.pop("phone", UNSET)

        pinterest = d.pop("pinterest", UNSET)

        privacy_policy = d.pop("privacyPolicy", UNSET)

        skype = d.pop("skype", UNSET)

        terms = d.pop("terms", UNSET)

        timezone = d.pop("timezone", UNSET)

        trip_advisor = d.pop("tripAdvisor", UNSET)

        twitter = d.pop("twitter", UNSET)

        _video = d.pop("video", UNSET)
        video: Union[Unset, Video]
        if isinstance(_video, Unset):
            video = UNSET
        else:
            video = Video.from_dict(_video)

        website = d.pop("website", UNSET)

        yelp = d.pop("yelp", UNSET)

        youtube_channel = d.pop("youtubeChannel", UNSET)

        company = cls(
            address=address,
            agent_description=agent_description,
            agent_registration_link=agent_registration_link,
            alias=alias,
            booking_system=booking_system,
            category=category,
            company_description=company_description,
            company_logo_url=company_logo_url,
            company_name=company_name,
            currency=currency,
            destination_country_code=destination_country_code,
            destination_name=destination_name,
            destination_path=destination_path,
            facebook_page=facebook_page,
            fax=fax,
            fb_page_id=fb_page_id,
            first_name=first_name,
            google_plus=google_plus,
            instagram=instagram,
            last_name=last_name,
            locale=locale,
            mobile=mobile,
            opening_hours=opening_hours,
            phone=phone,
            pinterest=pinterest,
            privacy_policy=privacy_policy,
            skype=skype,
            terms=terms,
            timezone=timezone,
            trip_advisor=trip_advisor,
            twitter=twitter,
            video=video,
            website=website,
            yelp=yelp,
            youtube_channel=youtube_channel,
        )

        company.additional_properties = d
        return company

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
