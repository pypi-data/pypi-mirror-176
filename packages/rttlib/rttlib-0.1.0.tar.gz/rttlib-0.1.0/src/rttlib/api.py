import requests      as rqs
import typing        as t
import rttlib.models as models
import json

from pydantic import BaseModel, ValidationError

class RttApi(BaseModel):
    api_username: str
    api_password: str
    api_url: str = "https://api.rtt.io/api/v1/json"

    def station_search(self, code: str, departures: bool = True) -> models.StationSearchRes:
        """search for station"""
        # make request to api endpoint
        r = rqs.get(f"{self.api_url}/search/{code}", auth = (self.api_username, self.api_password))
        # raise on non-200 status
        r.raise_for_status()
        # convert to json
        j = r.json()
        # pass json as kwargs to StationSearchRes
        return models.StationSearchRes(**j)

    def service_search(self, uid: str, date: str) -> models.ServiceSearchRes:
        """search for specific service"""
        # format date properly for url
        date = date.replace("-", "/")
        # make request to api endpoint
        r = rqs.get(f"{self.api_url}/service/{uid}/{date}", auth = (self.api_username, self.api_password))
        # raise on non-200 status
        r.raise_for_status()
        # convert to json
        j = r.json()
        # pass to ServiceSearchRes
        return models.ServiceSearchRes(**j)

    def origin(_, cls: models.ServiceSearchRes | models.StationServiceDetail) -> str | list[str] | None:
        """return origin(s) of service"""
        if len(cls.origin) == 1:
            return cls.origin[0].description
        elif len(cls.origin) > 1:
            return [o.description for o in cls.origin]
        else:
            return None
        
    def destination(_, cls: models.ServiceSearchRes | models.StationServiceDetail) -> str | list[str] | None:
        """return destination of service"""
        if len(cls.destination) == 1:
            return cls.destination[0].description
        elif len(cls.destination) > 1:
            return [o.description for o in cls.destination]
        else:
            return None

    def stops(self, cls: models.StationService | models.ServiceSearchRes) -> list[str]:
        """return all stops a service calls at"""
        # if the class passed is a StationService
        if isinstance(cls, models.StationService):
            # resolve to a ServiceSearchRes
            cls = self.service_search(cls.serviceUid, cls.runDate)
        # return names for every location on the service
        return [loc.description for loc in cls.locations]

