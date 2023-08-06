"""Automates creation of requests to, and parsing of response from Google's geocoding API."""

__version__ = "0.2.0"
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


def _send(param: str, api_key) -> dict:
    if api_key is None:
        raise IOError("Unable to load api key.")
    return requests.get(f"{_BASE_URL}?{param}&key={api_key}").json()


def _create_address_param(formatted_address: str) -> str:
    return f"address={formatted_address.replace(' ', '%20')}"


def _create_coordinates_param(lat: float, lng: float) -> str:
    return f"latlng={lat},{lng}"


def _parse(response) -> dict:
    if error_message := response.get("error_message"):
        status = response.get("status")
        raise IOError(f"Request failed. {error_message=}, {status=}")
    if len(response["results"]) == 0:
        return
    best_response = response["results"][0]
    name_by_types = {tuple(v.get("types")): v.get("long_name") for v in best_response.get("address_components")}
    return {
        "street_name": name_by_types.get(("route",)),
        "street_number": name_by_types.get(("street_number",)),
        "zip": name_by_types.get(("postal_code",)),
        "city": name_by_types.get(("locality", "political"), name_by_types.get(("postal_town",))),
        "country": name_by_types.get(("country", "political")),
        "formatted_address": best_response.get("formatted_address"),
        "geocoordinates": Geocoordinates(**best_response["geometry"]["location"]),
        "place_id": best_response.get("place_id"),
        "raw": response["results"]  # Included to simplify debugging
    }


_GOOGLE_API_KEY = _load_api_key()
_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
ADDRESS_KEYS = ["street", "zip", "city", "country"]


def create_address_string(street: str = None, zip: str = None, city: str = None, country: str = None) -> str:
    if all(p is None for p in [street, zip, city, country]):
        return None
    return ", ".join(x for x in [street, " ".join(y for y in [zip, city] if y), country] if x)


@dataclass
class Location:

    street_name: str
    street_number: str
    zip: str
    city: str
    country: str
    formatted_address: str
    geocoordinates: Geocoordinates
    place_id: str = field(repr=False)
    raw: dict = field(repr=False)

    @classmethod
    def from_address(cls, address: str, api_key=None) -> Self:
        return cls._create(_create_address_param(address), api_key=api_key)

    @classmethod
    def from_coordinates(cls, lat: float, lng: float, api_key=None) -> Self:
        return cls._create(_create_coordinates_param(lat, lng), api_key=api_key)

    @classmethod
    def _create(cls, param: str, api_key=None) -> Self:
        return cls(**respons) if (respons := _parse(_send(param, api_key=api_key or _GOOGLE_API_KEY))) else None

    def distance_to(self, other) -> float:
        return self.geocoordinates.distance_to(other.geocoordinates)
