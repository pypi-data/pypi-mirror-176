import os
import shutil
import logging
from modeldeploy_proxy_controller.rpc.log import create_adapter
from modeldeploy_proxy_controller.rpc.proxy import TRANSFORMER_UPLOAD_URL, REQUIREMENTS_UPLOAD_URL
from modeldeploy_proxy_controller.processors.nbprocessor import NotebookProcessor, REQUIREMENTS_TAG, PREPROCESSORS_TAG, POSTPROCESSORS_TAG, FUNCTIONS_TAG
from modeldeploy_proxy_controller.rpc.errors import RPCInternalError
import requests

NEW_LINES = '\n\n';

def parse_notebook(request, source_notebook_path):
    request.log.debug("parse_notebook {}".format(source_notebook_path))
    processor = NotebookProcessor(source_notebook_path)
    blocks = processor.parse_notebook()
    source = ''

    if len(blocks[PREPROCESSORS_TAG]) > 1:
        raise RuntimeError("Preprocess tag must be at most 1!")
    elif len(blocks[PREPROCESSORS_TAG]):
        if source:
            source = '{}{}{}'.format(source, NEW_LINES, blocks[PREPROCESSORS_TAG][0])
        else:
            source = '{}'.format(blocks[PREPROCESSORS_TAG][0])

    if len(blocks[POSTPROCESSORS_TAG]) > 1:
        raise RuntimeError("Postprocess tag must be at most 1!")
    elif len(blocks[POSTPROCESSORS_TAG]):
        if source:
            source = '{}{}{}'.format(source, NEW_LINES, blocks[POSTPROCESSORS_TAG][0])
        else:
            source = '{}'.format(blocks[POSTPROCESSORS_TAG][0])

    if len(blocks[FUNCTIONS_TAG]):
        for function in blocks[FUNCTIONS_TAG]:
            if source:
                source = '{}{}{}'.format(source, NEW_LINES, function)
            else:
                source = '{}'.format(function)
    transformer_path = processor.write_transformer_python(source);
    files = {'file': open(transformer_path, 'rb')}
    request.log.debug("POST {} with files...".format(TRANSFORMER_UPLOAD_URL))
    response = requests.post(TRANSFORMER_UPLOAD_URL, files=files)
    request.log.debug(response.json())

    requirements = ''
    if len(blocks[REQUIREMENTS_TAG]) > 1:
        raise RuntimeError("Requirements tag must be at most 1!")
    elif len(blocks[REQUIREMENTS_TAG]):
        if requirements:
            requirements = '{}{}{}'.format(source, NEW_LINES, blocks[REQUIREMENTS_TAG][0])
        else:
            requirements = '{}'.format(blocks[REQUIREMENTS_TAG][0])
    requirements_path = processor.write_requirements_file(requirements);
    files = {'file': open(requirements_path, 'rb')}
    request.log.debug("POST {} with files...".format(REQUIREMENTS_UPLOAD_URL))
    response = requests.post(REQUIREMENTS_UPLOAD_URL, files=files)
    request.log.debug(response.json())

    return blocks
