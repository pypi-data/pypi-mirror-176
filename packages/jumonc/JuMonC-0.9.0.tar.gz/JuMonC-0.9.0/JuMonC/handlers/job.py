import logging

from flask import abort, jsonify, make_response, Response

from typing import Dict, List, Union


from JuMonC.handlers.base import api_version_path, check_version, RESTAPI, generate_cache_id, get_prefer_id_description
from JuMonC.models import pluginInformation
from JuMonC.tasks import job
from JuMonC.authentication import scopes
from JuMonC.authentication.check import check_auth


logger = logging.getLogger(__name__)

links:        List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
status_links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
config_links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []

job_path = "/job"

@RESTAPI.route(api_version_path + job_path, methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnJobLinks(version: int) -> Response:
    logging.debug("Accessed /v%i/job/", version)
    return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)

@RESTAPI.route(api_version_path + job_path + "/status", methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnJOBStatusLinks(version: int) -> Response:
    logging.debug("Accessed /v%i/job/status", version)
    return make_response(jsonify(sorted(status_links, key=lambda dic: dic['link'])), 200)

@RESTAPI.route(api_version_path + job_path + "/config", methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnJOBConfigLinks(version: int) -> Response:
    logging.debug("Accessed /v%i/job/config", version)
    return make_response(jsonify(sorted(config_links, key=lambda dic: dic['link'])), 200)


def registerRestApiPaths(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    if pluginInformation.pluginIsWorking("JuMonC_JOBPlugin") is True:
        links.append(registerStatusLinks(version))
        links.append(registerConfigLinks(version))
    return {
        "link": "/v" + str(version) + job_path,
        "isOptional": False,
        "description": "Gather information concering this job",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }


def registerStatusLinks(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:   
    return {
        "link": "/v" + str(version) + job_path + "/status",
        "isOptional": False,
        "description": "Gather information concerning the job status",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }


def registerConfigLinks(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    types : List[str] = ['Nodename']
    descriptions : List[str] = ['retrieve the name of a node, to enable better debugging']
    if pluginInformation.pluginIsWorking("JuMonC_CPUPlugin") is True:
        for i, typeStr in enumerate(types):
            config_links.append({
            "link": "/v" + str(version) + job_path + "/config/" + typeStr,
            "isOptional": True,
            "description": descriptions[i],
            "parameters": [
                {"name": "node",
                "description": "When this parameter is not present data of all nodes is presented, otherwise only from the choosen node"},
                {"name": "token",
                "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
                })
        
        @RESTAPI.route(api_version_path + job_path + "/config/<string:datatype>", methods=["GET"])
        @check_version
        @check_auth(scopes["compute_data"])
        def returnJOBConfig(version: int, datatype:str) -> Response:
            logging.debug("Accessed /v%i/job/config/%s", version, datatype)
            data = job.plugin.getConfigData(dataType = datatype)            
            
            if len(data) > 0:
                return make_response(jsonify(data), 200)
            
            logging.warning("Accessed /v%i/job/config/%s, but not avaiable", version, datatype)
            abort(404)
            return make_response("",404)
        
    return {
        "link": "/v" + str(version) + job_path + "/config",
        "isOptional": False,
        "description": "Gather information concerning the job config",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }