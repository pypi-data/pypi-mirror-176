"""Automates creation of requests to, and parsing of response from Google's geocoding API."""

__version__ = "0.2.1"
__author__ = "Anders Petersson <petersson@chillservices.com>"


import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self
import requests
from gloc.geocoordinates import Geocoordinates


def _load_api_key() -> str:
    if (path := Path("google_api_key.txt")).exists():
        with open(path, "r", encoding="utf-8") as key_file:
            return key_file.readline()
    return os.environ.get("GOOGLE_API_KEY")


_GOOGLE_API_KEY = _load_api_key()


def request(param: str, api_key: str = None) -> dict:
    if (api_key := api_key or _GOOGLE_API_KEY) is None:
        raise IOError("Unable to load api key.")
    return requests.get(f"{_ENDPOINT_URL}?{param}&language=en&key={api_key}").json()


def _create_address_param(address: str) -> str:
    return f"address={address.replace(' ', '%20')}"


def _create_coordinates_param(lat: float, lng: float) -> str:
    return f"latlng={lat},{lng}"


def _parse_address_components(address_components: list) -> dict:
    name_by_types = {tuple(v.get("types")): v.get("long_name") for v in address_components}
    return {
        "street": f"{name_by_types.get(('route',))} {name_by_types.get(('street_number',))}",
        "zip": name_by_types.get(("postal_code",)),
        "city": name_by_types.get(("locality", "political"), name_by_types.get(("postal_town",))),
        "country": name_by_types.get(("country", "political"))
    }


_ENDPOINT_URL = "https://maps.googleapis.com/maps/api/geocode/json"
ADDRESS_KEYS = ["street", "zip", "city", "country"]


def formatted_address(street: str = None, zip: str = None, city: str = None, country: str = None) -> str:
    if all(p is None for p in [street, zip, city, country]):
        return None
    return ", ".join(x for x in [street, " ".join(y for y in [zip, city] if y), country] if x)


@dataclass
class Location:

    street: str
    zip: str
    city: str
    country: str
    formatted_address: str
    geocoordinates: Geocoordinates
    place_id: str = field(repr=False)

    @classmethod
    def _from_search_result(cls, search_result: dict) -> Self:
        return cls(**{
            **_parse_address_components(search_result.get("address_components")),
            "formatted_address": search_result.get("formatted_address"),
            "geocoordinates": Geocoordinates(**search_result["geometry"]["location"]),
            "place_id": search_result.get("place_id")
        })

    @classmethod
    def from_api_response(cls, api_response: dict) -> Self:
        if error_message := api_response.get("error_message"):
            status = api_response.get("status")
            raise IOError(f"Request failed. {error_message=}, {status=}")
        if len(api_response["results"]) == 0:
            return
        return cls._from_search_result(api_response["results"][0])

    @classmethod
    def from_address(cls, address: str, api_key=None) -> Self:
        return cls.from_api_response(request(_create_address_param(address), api_key))

    @classmethod
    def from_coordinates(cls, lat: float, lng: float, api_key=None) -> Self:
        return cls.from_api_response(request(_create_coordinates_param(lat, lng), api_key))

    def distance_to(self, other) -> float:
        return self.geocoordinates.distance_to(other.geocoordinates)
