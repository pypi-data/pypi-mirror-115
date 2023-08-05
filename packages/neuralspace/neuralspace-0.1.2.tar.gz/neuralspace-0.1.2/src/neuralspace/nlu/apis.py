import json
import logging
from asyncio import sleep
from copy import copy
from datetime import datetime
from typing import Any, Dict, List, Text, Tuple

from prettytable import PrettyTable
from tqdm import tqdm

from neuralspace.apis import get_async_http_session
from neuralspace.constants import (
    AUTHORIZATION,
    COMMON_HEADERS,
    COMPLETED,
    COUNT,
    DATA,
    DEAD,
    ENTITIES,
    ENTITY_ACC,
    EXAMPLE,
    EXAMPLE_ID,
    EXAMPLES,
    FAILED,
    FILTER,
    INTENT,
    INTENT_ACCURACY,
    INTENT_CLASSIFIER_METRICS,
    LANGUAGE,
    LANGUAGES,
    LAST_STATUS_UPDATED,
    METRICS,
    MODEL_ID,
    MODEL_NAME,
    MODELS,
    N_REPLICAS,
    NER_METRICS,
    NUMBER_OF_EXAMPLES,
    NUMBER_OF_INTENTS,
    NUMBER_OF_MODELS,
    OUTPUT,
    PAGE_NUMBER,
    PAGE_SIZE,
    PREPARED,
    PROJECT_ID,
    PROJECT_NAME,
    PROJECTS,
    REPLICAS,
    SEARCH,
    TEXT,
    TIMED_OUT,
    TRAINING_STATUS,
    TRAINING_TIME,
    TYPE,
    neuralspace_url,
)
from neuralspace.nlu.constants import (
    CREATE_EXAMPLE_URL,
    CREATE_PROJECT_URL,
    DELETE_EXAMPLE_URL,
    DELETE_MODELS_URL,
    DELETE_PROJECT_URL,
    DEPLOY_MODEL_URL,
    LANGUAGE_CATALOG_URL,
    LIST_EXAMPLES_URL,
    LIST_MODELS_URL,
    LIST_PROJECTS_URL,
    PARSE_URL,
    SINGLE_MODEL_DETAILS_URL,
    TRAIN_MODEL_URL,
)
from neuralspace.utils import get_auth_token, is_success_status

logger = logging.getLogger(__name__)


async def get_languages() -> Dict[Text, Any]:
    logger.debug("Fetching all supported languages for NLU")
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().get(
        url=f"{neuralspace_url()}/{LANGUAGE_CATALOG_URL}",
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            logger.debug("Successfully created project")
            logger.info(f"{json.dumps(json_response, indent=4)}")
        else:
            logger.error("Failed to create project")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


async def create_project(project_name: Text, languages: List[Text]) -> Dict[Text, Any]:
    logger.info(
        f"Creating a project called {project_name} in languages: {', '.join(languages)}"
    )
    payload = {PROJECT_NAME: project_name, LANGUAGE: languages}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{CREATE_PROJECT_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            logger.info("Successfully created project")
            logger.info(f"Project details: \n {json.dumps(json_response, indent=4)}")
        else:
            logger.error("Failed to create project")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


async def delete_project(project_id: Text) -> Dict[Text, Any]:
    logger.info(f"Deleting project with id: {project_id}")
    payload = {PROJECT_ID: project_id}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().delete(
        url=f"{neuralspace_url()}/{DELETE_PROJECT_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            logger.info(f"Platform Response: \n{json.dumps(json_response, indent=4)}")
        else:
            logger.error("Failed to delete projects")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


def print_projects_table(projects: Dict[Text, Any]):
    table = PrettyTable()
    table.field_names = [
        "Project Name",
        "Project ID",
        "Number of Examples",
        "Number of Intents",
        "number of Models",
        "Languages",
    ]
    for data in projects[DATA][PROJECTS]:
        table.add_row(
            [
                data[PROJECT_NAME],
                data[PROJECT_ID],
                data[NUMBER_OF_EXAMPLES],
                data[NUMBER_OF_INTENTS],
                data[NUMBER_OF_MODELS],
                data[LANGUAGE],
            ]
        )
    logger.info(f"\n{table}")


async def list_projects(
    search: Text, page_size: int, page_number: int, languages: List[Text]
) -> Dict[Text, Any]:
    payload = {
        SEARCH: search,
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
        LANGUAGES: languages,
    }
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{LIST_PROJECTS_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            logger.info(
                f"Your projects for Page {page_number} with Page Size: {page_size}"
            )
            print_projects_table(json_response)
        else:
            logger.error("Failed to list projects")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


def print_examples_table(examples: Dict[Text, Any]):
    table = PrettyTable()
    table.field_names = ["Example ID", "Text", "Intent", "N Entities"]
    logger.info(f"Total Examples Count: {examples[DATA][COUNT]}")
    for data in examples[DATA][EXAMPLES]:
        text = data[TEXT][:20]
        if len(data[TEXT]) > 20:
            text = f"{text}..."
        table.add_row([data[EXAMPLE_ID], text, data[INTENT], len(data[ENTITIES])])
    logger.info(f"\n{table}")


async def list_examples(
    project_id: Text,
    language: Text,
    prepared: bool,
    type: Text,
    intent: Text,
    page_number: int,
    page_size: int,
) -> Dict[Text, Any]:
    logger.info(
        f"Fetching Examples with filter: Project ID: {project_id}; Language: {language}; "
        f"Prepared: {prepared}; type: {type}"
    )
    payload = {
        FILTER: {
            PROJECT_ID: project_id,
            LANGUAGE: language,
            PREPARED: prepared,
            TYPE: type,
        },
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
    }
    if intent:
        payload[FILTER][INTENT] = intent

    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{LIST_EXAMPLES_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            print_examples_table(json_response)
        else:
            logger.error("Failed to list examples")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


def print_models_table(models: Dict[Text, Any]):
    table = PrettyTable()
    table.field_names = [
        "Model ID",
        "Model Name",
        "Training Status",
        "Replicas",
        "Intent Acc",
        "Entity Acc",
        "Training Time (sec)",
        "Last Updated",
    ]
    logger.info(f"Total Models Count: {models[DATA][COUNT]}")
    for data in models[DATA][MODELS]:
        table.add_row(
            [
                data[MODEL_ID],
                data[MODEL_NAME],
                data[TRAINING_STATUS],
                data[REPLICAS],
                "{:.3f}".format(
                    data[METRICS][INTENT_CLASSIFIER_METRICS][INTENT_ACCURACY]
                )
                if data[TRAINING_STATUS] == COMPLETED
                else 0.0,
                "{:.3f}".format(data[METRICS][NER_METRICS][ENTITY_ACC])
                if data[TRAINING_STATUS] == COMPLETED
                else 0.0,
                data[TRAINING_TIME] if data[TRAINING_STATUS] == COMPLETED else 0.0,
                data[LAST_STATUS_UPDATED],
            ]
        )
    logger.info(f"\n{table}")


async def list_models(
    project_id: Text,
    language: Text,
    training_status: List[Text],
    page_number: int,
    page_size: int,
) -> Dict[Text, Any]:
    logger.info(
        f"Fetching models with filter: Project ID: {project_id}; Language: {language}; "
        f"Training Statuses: {training_status}"
    )
    payload = {
        FILTER: {PROJECT_ID: project_id, LANGUAGE: language},
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
    }
    if training_status:
        payload[FILTER][TRAINING_STATUS] = training_status

    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{LIST_MODELS_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            print_models_table(json_response)
        else:
            logger.error("Failed to list models")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


async def delete_examples(example_ids: List[Text]) -> Dict[Text, Any]:
    logger.info(f"Deleting Example with id: {example_ids}")
    payload = {EXAMPLE_ID: example_ids}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().delete(
        url=f"{neuralspace_url()}/{DELETE_EXAMPLE_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            logger.info(f"Platform Response: \n{json.dumps(json_response, indent=4)}")
        else:
            logger.error("Failed to delete examples")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


async def upload_dataset(
    nlu_data: List[Dict[Text, Text]],
    project_id: Text,
    language: Text,
    skip_first: int = 0,
    ignore_errors: bool = False,
) -> List[Dict[Text, Any]]:
    responses = []
    error_examples = []
    logger.info(
        f"Uploading {len(nlu_data) - skip_first} examples for project {project_id} and language {language}"
    )
    logger.info(f"Skipping first {skip_first} examples")
    for chunk_id, example in tqdm(enumerate(nlu_data[skip_first:])):
        batch = {PROJECT_ID: project_id, LANGUAGE: language, EXAMPLE: example}
        HEADERS = copy(COMMON_HEADERS)
        HEADERS[AUTHORIZATION] = get_auth_token()
        async with get_async_http_session().post(
            url=f"{neuralspace_url()}/{CREATE_EXAMPLE_URL}",
            data=json.dumps(batch, ensure_ascii=False),
            headers=HEADERS,
        ) as response:
            json_response = await response.json(encoding="utf-8")
            if is_success_status(response.status):
                responses.append(json_response)
            else:
                logger.error(f"Failed to upload example with text {example['text']}")
                logger.debug(
                    f"Failed on examples: \n {json.dumps(example, indent=4, ensure_ascii=False)}"
                )
                logger.error(
                    f"Platform response: \n {json.dumps(json_response, indent=4)}"
                )
                error_examples.append(example)
                if ignore_errors:
                    continue
                else:
                    break
    logger.info(f"Uploaded {len(responses)} examples")
    logger.info(f"Failed on {len(error_examples)} examples")
    with open("failed_examples.json", "w") as f:
        json.dump(error_examples, f, ensure_ascii=False)
        logger.info("Writing failed examples into failed_examples.json")
    return responses


async def wait_till_training_completes(
    model_id: Text, wait: bool, wait_interval: int
) -> Dict[Text, Any]:
    if wait:
        payload = {
            MODEL_ID: model_id,
        }
        HEADERS = copy(COMMON_HEADERS)
        HEADERS[AUTHORIZATION] = get_auth_token()
        logger.info(f"Waiting for training job to get done for model id: {model_id}")
        while True:
            async with get_async_http_session().get(
                url=f"{neuralspace_url()}/{SINGLE_MODEL_DETAILS_URL}",
                params=payload,
                headers=HEADERS,
            ) as response:
                json_response = await response.json(encoding="utf-8")
                if is_success_status(response.status):
                    logger.info(
                        f"Current Status: {json_response[DATA][TRAINING_STATUS]}"
                    )
                    if (
                        json_response[DATA][TRAINING_STATUS] == COMPLETED
                        or json_response[DATA][TRAINING_STATUS] == FAILED
                        or json_response[DATA][TRAINING_STATUS] == TIMED_OUT
                        or json_response[DATA][TRAINING_STATUS] == DEAD
                    ):
                        break
                    logger.info(f"Waiting for {wait_interval} seconds")

                else:
                    logger.error("Failed to fetch model details")
                    logger.error(
                        f"Platform Response: \n {json.dumps(json_response, indent=4)}"
                    )
                    break
            await sleep(wait_interval)
    return json_response


async def train_model(
    project_id: Text,
    language: Text,
    model_name: Text,
    wait: bool = True,
    wait_time: int = 1,
) -> Tuple[Dict[Text, Any], Dict[Text, Any]]:
    logger.info(
        f"Queuing training job for: Project ID: {project_id}; Language: {language}; "
        f"Model Name: {model_name}"
    )
    payload = {PROJECT_ID: project_id, LANGUAGE: language, MODEL_NAME: model_name}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()

    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{TRAIN_MODEL_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            logger.info("Training job queued successfully")
            logger.info(f"Platform Response: \n{json_response}")
            model_id = json_response[DATA]["model_id"]
            last_model_status = await wait_till_training_completes(
                model_id, wait, wait_time
            )
        else:
            logger.error("Failed to queue training job")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
            last_model_status = None
    return json_response, last_model_status


async def delete_models(model_id: Text) -> Dict[Text, Any]:
    logger.info(f"Deleting model with id: {model_id}")
    payload = {MODEL_ID: model_id}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().delete(
        url=f"{neuralspace_url()}/{DELETE_MODELS_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            logger.info(f"Platform Response: \n{json.dumps(json_response, indent=4)}")
        else:
            logger.error("Failed to delete models")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


async def deploy(model_id: Text, n_replicas: int) -> Dict[Text, Any]:
    logger.info(f"Deploying: Model ID: {model_id}; Replicas: {n_replicas};")
    payload = {MODEL_ID: model_id, N_REPLICAS: n_replicas}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()

    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{DEPLOY_MODEL_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            logger.info("Model deployed successfully")
            logger.info(f"Platform Response: \n{json.dumps(json_response, indent=4)}")
        else:
            logger.error("Failed to deploy model")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


def print_nlu_response(nlu_response: Dict[Text, Any], response_time: float):
    table = PrettyTable()
    table.field_names = [
        "Text",
        "Intent",
        "Intent Confidence",
        "Entities[type|value|start-idx:end-idx]",
        "Response Time (sec)",
    ]
    table.add_row(
        [
            nlu_response[DATA][OUTPUT]["result"]["text"][:30] + "[...]",
            nlu_response[DATA][OUTPUT]["result"]["intent"]["name"],
            nlu_response[DATA][OUTPUT]["result"]["intent"]["confidence"],
            "; ".join(
                [
                    f"{e['entity']}|{e['value']}|{e['start']}:{e['end']} "
                    for e in nlu_response[DATA][OUTPUT]["result"]["entities"]
                ]
            ),
            response_time / 1000,
        ]
    )
    logger.info(f"\n{table}")
    intent_ranking_table = PrettyTable()
    intent_ranking_table.field_names = ["Intent", "Confidence"]

    for row in nlu_response[DATA][OUTPUT]["result"]["intent_ranking"]:
        intent_ranking_table.add_row(
            [
                row["name"],
                row["confidence"],
            ]
        )
    logger.info(f"\nIntent Ranking \n{intent_ranking_table}")


async def parse(model_id: Text, input_text: Text) -> Dict[Text, Any]:
    logger.info(f"Parsing text: {input_text}, using Model ID: {model_id}")
    payload = {MODEL_ID: model_id, DATA: {TEXT: input_text}}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()

    start = datetime.now()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{PARSE_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        end = datetime.now()
        response_time = (end - start).microseconds
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            logger.debug(
                f"Platform Response: \n{json.dumps(json_response, indent=4, ensure_ascii=False)}"
            )
            print_nlu_response(json_response, response_time)
        else:
            logger.error("Failed to parse model")
            logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response
