# AJO API Coverage

This table tracks parity between the OpenAPI specs published in
[`vondras/journey-optimizer-apis/static`](https://github.com/vondras/journey-optimizer-apis/tree/main/static)
and the corresponding `aepp` Python wrapper modules.

**Status legend**
| Symbol | Meaning |
|--------|---------|
| ⬜ outstanding | No aepp module exists yet |
| 🚧 in progress | A PR / issue is open |
| ✅ implemented | An aepp module covers the spec |

---

## Coverage Table

| Spec file | Title | Tags | Ops | Base path | aepp status | Issue |
|-----------|-------|------|-----|-----------|-------------|-------|
| [`campaigns-retrieve.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/campaigns-retrieve.yaml) | Retrieve & filter Action Campaigns | Metadata Resource, Workflow Resource, Campaign Resource | 10 | `/journey/campaigns` | ✅ implemented (`aepp.campaigns.Campaigns`) | — |
| [`campaigns-retrieve-old.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/campaigns-retrieve-old.yaml) | Retrieve & filter Action Campaigns *(legacy)* | Metadata Resource, Workflow Resource, Campaign Resource, + 13 more | 114 | `/journey/campaigns` | ⬜ outstanding (superseded by `campaigns-retrieve.yaml`) | — |
| [`content.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/content.yaml) | Content templates & fragments API | Content template API, Content fragment API | 14 | `/ajo/content` | ✅ implemented (`aepp.content.Content`) | — |
| [`journey-retrieve.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/journey-retrieve.yaml) | Retrieve Journeys using APIs | Journeys | 2 | `/ajo/journey` | ✅ implemented (`aepp.journey.Journey`) | — |
| [`journeys-throttling.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/journeys-throttling.yaml) | Journeys throttling configurations APIs | Capping configuration, Throttling configuration | 16 | `/journey/orchestration` | ✅ implemented (`aepp.orchestration.Orchestration`) | — |
| [`loyalty-challenges.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/loyalty-challenges.yaml) | AJO Customer Loyalty Challenge State API | Challenge-State | 10 | `/ajo/loyalty` | ✅ implemented (`aepp.loyalty.Loyalty`) | — |
| [`messaging.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/messaging.yaml) | Trigger campaigns using APIs | execution | 7 | `/ajo/im/executions` | ✅ implemented (`aepp.messaging.Messaging`) | — |
| [`messagingold.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/messagingold.yaml) | Trigger campaigns using APIs *(legacy)* | execution | 1 | `/imp/message` | ⬜ outstanding (superseded by `messaging.yaml`) | — |
| [`orchestrated-campaign-dataset.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/orchestrated-campaign-dataset.yaml) | Orchestrated campaigns extension for datasets | DatasetEnablement | 3 | `/ajo/relational` | ✅ implemented (`aepp.orchestrateddataset.OrchestratedDataset`) | — |
| [`simulations.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/simulations.yaml) | Simulation API | Campaign Proof API, Campaign Preview API | 3 | `/ajo/simulations` | ✅ implemented (`aepp.simulations.Simulations`) | — |
| [`suppression.yaml`](https://github.com/vondras/journey-optimizer-apis/blob/main/static/suppression.yaml) | Suppression API | Suppression | 13 | `/ajo/config/suppression` | ✅ implemented (`aepp.suppression.Suppression`) | — |

---

## Spec Details

### `campaigns-retrieve.yaml`
- **Title:** Retrieve & filter Action Campaigns
- **Version:** v1.79
- **Description:** Retrieve & filter Action Campaigns
- **Tags:** Metadata Resource, Workflow Resource, Campaign Resource
- **Operations:** 10
- **Prod server:** `https://platform.adobe.io/journey/campaigns`
- **Key paths:** `GET /service/campaigns`, `GET /service/campaigns/{id}`, `GET /service/campaigns/{id}/messages/...`
- **aepp module:** `aepp.campaigns.Campaigns`
- **Implemented methods:**
  - `getCampaigns(count, page, orderby, property, full, actions)` — `GET /service/campaigns`
  - `getCampaign(campaignId)` — `GET /service/campaigns/{campaignId}`
  - `getCampaignVersions(campaignId, count, page, orderby, property, full, actions)` — `GET /service/campaigns/{campaignId}/versions`
  - `getCampaignMessage(campaignId, messageId)` — `GET /service/campaigns/{campaignId}/messages/{messageId}`
  - `getCampaignMessageVariant(campaignId, messageId, channel, variantId)` — `GET /service/campaigns/{campaignId}/messages/{messageId}/{channel}/variants/{variantId}`
  - `getCampaignPublishingNotifications(campaignId, count, page, orderby, property)` — `GET /service/campaigns/{campaignId}/publish/validation`
  - `getCampaignPackage(campaignId, packageId)` — `GET /service/campaigns/{campaignId}/packages/{packageId}`
  - `getWorkflow(workflowId)` — `GET /service/workflows/{workflowId}`
  - `getSurfaces(count, page, orderby, channel, property, type)` — `GET /service/metadata/surfaces`
  - `getSurface(channel, surfaceId, type)` — `GET /service/metadata/surfaces/{channel}/{surfaceId}`

### `campaigns-retrieve-old.yaml`
- **Title:** Retrieve & filter Action Campaigns *(legacy — superseded by `campaigns-retrieve.yaml`)*
- **Version:** v1.79
- **Description:** Retrieve & filter Action Campaigns (older, larger spec with 114 operations)
- **Tags:** Metadata Resource, Content Service Template Proxy, Workflow Resource, Decision Resource, Version Resource, Campaign Resource, Campaign Tracker Resource, Approval Resource, Inline Campaign Resource, Inline Message Service Proxy, Multilingual Content Proxy, Bulk Campaign Resource, Bulk Validate Resource, Health Resource, Multilingual Resource, Experiment Resource
- **Operations:** 114
- **Prod server:** `https://platform.adobe.io/journey/campaigns`

### `content.yaml`
- **Title:** Content templates & fragments API
- **Version:** 0.0.1
- **Description:** Create and manage content templates and fragments reusable across Journey Optimizer campaigns and journeys.
- **Tags:** Content template API, Content fragment API
- **Operations:** 14
- **Prod server:** `https://platform.adobe.io/ajo/content`
- **Key paths:** `GET, POST /templates`, `GET, PUT, PATCH, DELETE /templates/{id}`, `GET, POST /fragments`, `GET, PUT, PATCH, DELETE /fragments/{id}`, `POST /fragments/publications`, `GET /fragments/{id}/live`, `GET /fragments/{id}/publications/latest`
- **aepp module:** `aepp.content.Content`
- **Implemented methods:**
  - `createTemplate(data)` — `POST /templates`
  - `listTemplates(limit, start, orderBy, property)` — `GET /templates`
  - `getTemplate(templateId)` — `GET /templates/{id}`
  - `putTemplate(templateId, data, if_match)` — `PUT /templates/{id}`
  - `patchTemplate(templateId, operations, if_match)` — `PATCH /templates/{id}`
  - `deleteTemplate(templateId)` — `DELETE /templates/{id}`
  - `createFragment(data)` — `POST /fragments`
  - `listFragments(limit, start, orderBy, property)` — `GET /fragments`
  - `getFragment(fragmentId)` — `GET /fragments/{id}`
  - `putFragment(fragmentId, data, if_match)` — `PUT /fragments/{id}`
  - `patchFragment(fragmentId, operations, if_match)` — `PATCH /fragments/{id}`
  - `publishFragment(data)` — `POST /fragments/publications`
  - `getLiveFragment(fragmentId)` — `GET /fragments/{id}/live`
  - `getLastPublicationStatus(fragmentId)` — `GET /fragments/{id}/publications/latest`

### `journey-retrieve.yaml`
- **Title:** Retrieve Journeys using APIs
- **Version:** 1.0.0
- **Description:** Retrieve Journeys and their associated campaigns.
- **Tags:** Journeys
- **Operations:** 2
- **Prod server:** `https://platform.adobe.io/ajo/journey`
- **Key paths:** `GET /journeys`, `GET /journeys/{journeyId}`
- **aepp module:** `aepp.journey.Journey`
- **Implemented methods:**
  - `getJourneys(filter, page, pageSize, fields, sort)` — `GET /journeys`
  - `getJourney(journeyId, include)` — `GET /journeys/{journeyId}`

### `journeys-throttling.yaml`
- **Title:** Journeys throttling configurations APIs
- **Version:** v1
- **Description:** Manage capping and throttling configurations for Journeys integration with external systems.
- **Tags:** Capping configuration, Throttling configuration
- **Operations:** 16
- **Prod server:** `https://platform.adobe.io/journey/orchestration`
- **Key paths:** `POST /endpointConfigs`, `GET, PUT, DELETE /endpointConfigs/{uid}`, `GET /endpointConfigs/{uid}/canDeploy`, `POST /endpointConfigs/{uid}/deploy`, `POST /endpointConfigs/{uid}/undeploy`, `POST /list/endpointConfigs`, `POST /throttlingConfigs`, `GET, PUT, DELETE /throttlingConfigs/{uid}`, `GET /throttlingConfigs/{uid}/canDeploy`, `POST /throttlingConfigs/{uid}/deploy`, `POST /throttlingConfigs/{uid}/undeploy`, `POST /list/throttlingConfigs`
- **aepp module:** `aepp.orchestration.Orchestration`
- **Implemented methods:**
  - `createEndpointConfig(data)` — `POST /endpointConfigs`
  - `getEndpointConfig(uid)` — `GET /endpointConfigs/{uid}`
  - `putEndpointConfig(uid, data)` — `PUT /endpointConfigs/{uid}`
  - `deleteEndpointConfig(uid)` — `DELETE /endpointConfigs/{uid}`
  - `canDeployEndpointConfig(uid)` — `GET /endpointConfigs/{uid}/canDeploy`
  - `deployEndpointConfig(uid)` — `POST /endpointConfigs/{uid}/deploy`
  - `undeployEndpointConfig(uid)` — `POST /endpointConfigs/{uid}/undeploy`
  - `listEndpointConfigs(data)` — `POST /list/endpointConfigs`
  - `createThrottlingConfig(data)` — `POST /throttlingConfigs`
  - `getThrottlingConfig(uid)` — `GET /throttlingConfigs/{uid}`
  - `putThrottlingConfig(uid, data)` — `PUT /throttlingConfigs/{uid}`
  - `deleteThrottlingConfig(uid)` — `DELETE /throttlingConfigs/{uid}`
  - `canDeployThrottlingConfig(uid)` — `GET /throttlingConfigs/{uid}/canDeploy`
  - `deployThrottlingConfig(uid)` — `POST /throttlingConfigs/{uid}/deploy`
  - `undeployThrottlingConfig(uid)` — `POST /throttlingConfigs/{uid}/undeploy`
  - `listThrottlingConfigs(data)` — `POST /list/throttlingConfigs`

### `loyalty-challenges.yaml`
- **Title:** AJO Customer Loyalty Challenge State API
- **Version:** 1.1.0
- **Description:** APIs for the Loyalty Challenges feature (private beta). Manage and query loyalty challenge state.
- **Tags:** Challenge-State
- **Operations:** 10
- **Prod server:** `https://platform-va7.adobe.io/ajo`
- **Key paths:** `POST /loyalty/challenges/signup/{challengeId}`, `POST /loyalty/challenges/{profileId}/withdraw/{challengeId}`, `POST /loyalty/challenges/events`, `GET /loyalty/challenges/{profileId}`, `GET /loyalty/challenges/state`, `GET /loyalty/challenges/org`, `GET /loyalty/challenges/od`, `GET /loyalty/challenges/health`, `GET /actuator/liveness`, `GET /actuator/health`
- **aepp module:** `aepp.loyalty.Loyalty`
- **Implemented methods:**
  - `signupChallenge(challengeId, data)` — `POST /loyalty/challenges/signup/{challengeId}`
  - `withdrawChallenge(profileId, challengeId)` — `POST /loyalty/challenges/{profileId}/withdraw/{challengeId}`
  - `sendChallengeEvent(data)` — `POST /loyalty/challenges/events`
  - `getProfileChallenges(profileId, state)` — `GET /loyalty/challenges/{profileId}`
  - `getChallengeState(pid, cid, v)` — `GET /loyalty/challenges/state`
  - `getOrgChallenges()` — `GET /loyalty/challenges/org`
  - `getProfileChallengesOD(id, idNS, v)` — `GET /loyalty/challenges/od`
  - `getChallengeHealth()` — `GET /loyalty/challenges/health`
  - `getLiveness()` — `GET /actuator/liveness`
  - `getHealthCheck()` — `GET /actuator/health`

### `messaging.yaml`
- **Title:** Trigger campaigns using APIs
- **Version:** 1.0.1
- **Description:** Interactive Message Execution API for sending marketing or transactional messages using Email, SMS and Push channels.
- **Tags:** execution
- **Operations:** 7
- **Prod server:** `https://platform.adobe.io/ajo`
- **Key paths:** `POST /im/executions/unitary`, `POST /im/executions/audience`, `GET /im/executions/audience/{executionId}`, `GET /im/executions/schedules/{scheduleId}`, `DELETE /im/executions/schedules/{scheduleId}`, `POST /im/executions/highthroughput`, `GET /im/health`
- **aepp module:** `aepp.messaging.Messaging`
- **Implemented methods:**
  - `triggerUnitaryExecution(data)` — `POST /im/executions/unitary`
  - `triggerAudienceExecution(data)` — `POST /im/executions/audience`
  - `getAudienceExecutionStatus(executionId)` — `GET /im/executions/audience/{executionId}`
  - `getScheduledExecutionStatus(scheduleId)` — `GET /im/executions/schedules/{scheduleId}`
  - `deleteScheduledExecution(scheduleId)` — `DELETE /im/executions/schedules/{scheduleId}`
  - `triggerHighThroughputExecution(data)` — `POST /im/executions/highthroughput`
  - `getHealth()` — `GET /im/health`

### `messagingold.yaml`
- **Title:** Trigger campaigns using APIs *(legacy — superseded by `messaging.yaml`)*
- **Version:** (older)
- **Tags:** execution
- **Operations:** 1
- **Prod server:** `https://cjm.adobe.io/imp/message`

### `orchestrated-campaign-dataset.yaml`
- **Title:** Orchestrated campaigns extension for datasets
- **Version:** 1.0.0
- **Description:** Validate or enable the Orchestrated Campaign extension on a dataset, making it available for use with Orchestrated Campaigns in Adobe Journey Optimizer.
- **Tags:** DatasetEnablement
- **Operations:** 3
- **Prod server:** `https://platform.adobe.io/ajo/relational`
- **Key paths:** `GET /modeler/datasets/{datasetId}/extensions/validation`, `POST /modeler/datasets/extensions/enablement`, `GET /modeler/datasets/extensions/enablement/jobs/{jobId}`
- **aepp module:** `aepp.orchestrateddataset.OrchestratedDataset`
- **Implemented methods:**
  - `validateDatasetExtension(datasetId)` — `GET /modeler/datasets/{datasetId}/extensions/validation`
  - `enableDatasetExtension(data)` — `POST /modeler/datasets/extensions/enablement`
  - `getDatasetExtensionJob(jobId)` — `GET /modeler/datasets/extensions/enablement/jobs/{jobId}`

### `simulations.yaml`
- **Title:** Simulation API
- **Version:** 0.0.1
- **Description:** APIs for Campaign Preview and Proofs.
- **Tags:** Campaign Proof API, Campaign Preview API
- **Operations:** 3
- **Prod server:** `https://platform.adobe.io/ajo/simulations`
- **Key paths:** `POST /campaigns/{campaignId}/proofs`, `GET /campaigns/{campaignId}/proofs/{proofJobId}`, `POST /campaigns/{campaignId}/previews`
- **aepp module:** `aepp.simulations.Simulations`
- **Implemented methods:**
  - `triggerCampaignProof(campaignId, data)` — `POST /campaigns/{campaignId}/proofs`
  - `getCampaignProofStatus(campaignId, proofJobId)` — `GET /campaigns/{campaignId}/proofs/{proofJobId}`
  - `createCampaignPreview(campaignId, data)` — `POST /campaigns/{campaignId}/previews`

### `suppression.yaml`
- **Title:** Suppression API
- **Version:** 1.0.1
- **Description:** Control outgoing messages using suppression and allow lists. Manage suppression list for ISP feedback and allow list for development sandboxes.
- **Tags:** Suppression
- **Operations:** 13
- **Prod server:** `https://platform.adobe.io/ajo`
- **Key paths:** `GET, POST /config/suppression/addresses`, `GET, DELETE /config/suppression/addresses/{email}`, `GET, POST /config/suppression/domains`, `GET, DELETE /config/suppression/domains/{domain}`, `GET, POST /config/suppression/uploads`, `GET, DELETE /config/suppression/uploads/{jobId}`, `DELETE /config/suppression/admin/{imsOrgId}/{sandboxId}`
- **aepp module:** `aepp.suppression.Suppression`
- **Implemented methods:**
  - `listAddresses(type, orderby, limit, start, property)` — `GET /config/suppression/addresses`
  - `addAddresses(data, type)` — `POST /config/suppression/addresses`
  - `getAddress(email, type)` — `GET /config/suppression/addresses/{email}`
  - `deleteAddress(email, type)` — `DELETE /config/suppression/addresses/{email}`
  - `listDomains(type, orderby, limit, start, property)` — `GET /config/suppression/domains`
  - `addDomains(data, type)` — `POST /config/suppression/domains`
  - `getDomain(domain, type)` — `GET /config/suppression/domains/{domain}`
  - `deleteDomain(domain, type)` — `DELETE /config/suppression/domains/{domain}`
  - `uploadSuppression(file_path)` — `POST /config/suppression/uploads`
  - `listUploadJobs(orderby, limit, start, property)` — `GET /config/suppression/uploads`
  - `getUploadJob(jobId)` — `GET /config/suppression/uploads/{jobId}`
  - `deleteUploadJob(jobId)` — `DELETE /config/suppression/uploads/{jobId}`
  - `deleteAllSuppressions(imsOrgId, sandboxId)` — `DELETE /config/suppression/admin/{imsOrgId}/{sandboxId}`
