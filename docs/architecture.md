# Architecture

This project implements a hybrid cloud workflow for campus event submission processing.

## Required Components
1. Presentation Service (Container)
2. Workflow Service (Container)
3. Data Service (Container)
4. Submission Event Function (Serverless)
5. Processing Function (Serverless)
6. Result Update Function (Serverless)

## Workflow
User submits a form -> Workflow Service creates a submission record -> Submission Event Function turns the event into a processing request -> Processing Function evaluates the rules -> Result Update Function updates the submission record -> User views the result.

## Local Mode
In local mode, the three services can be started with Docker Compose. The Workflow Service calls the Python handler functions directly so the whole pipeline is easy to test on one machine.

## Cloud Mode
In cloud mode:

- the three services run as containers on Alibaba Cloud ECS
- the three functions run as HTTP-triggered serverless components on Alibaba Cloud Function Compute
- the Workflow Service dispatches the serverless chain in the background
- the Presentation Service auto-refreshes the result page while the record is still pending

## Cloud-Mode Communication
- `workflow-service` -> `submission_event_function`
- `submission_event_function` -> `processing_function`
- `processing_function` -> `result_update_function`
- `result_update_function` -> `data-service`

Function-to-function calls use a shared optional header token (`FUNCTION_AUTH_TOKEN`) for simple protection.
