-- Cleanup script for RAG_App_AI_observability workspace and all associated resources

----------------------------------------------------------------------
-- 1. Suspend and drop SPCS services (notebook kernels, streamlit apps)
----------------------------------------------------------------------
-- Suspend notebook service if running [Replace with the service running in your python notebook]
ALTER SERVICE IF EXISTS USER$DEEPTIA.PUBLIC.DEEPTIA_SERVICE_1 SUSPEND;
DROP SERVICE IF EXISTS USER$DEEPTIA.PUBLIC.DEEPTIA_SERVICE_1;

----------------------------------------------------------------------
-- 2. Suspend compute pools (stops all idle credit burn)
----------------------------------------------------------------------
ALTER COMPUTE POOL IF EXISTS SYSTEM_COMPUTE_POOL_CPU SET AUTO_SUSPEND_SECS = 60;
ALTER COMPUTE POOL IF EXISTS SYSTEM_COMPUTE_POOL_CPU SUSPEND;
ALTER COMPUTE POOL IF EXISTS SYSTEM_COMPUTE_POOL_GPU SUSPEND;

----------------------------------------------------------------------
-- 3. Drop Cortex Search Service
----------------------------------------------------------------------
DROP CORTEX SEARCH SERVICE IF EXISTS CLINICAL_STUDY_AI_DB.RAG.CLINICAL_STUDY_SEARCH_SERVICE;

----------------------------------------------------------------------
-- 4. Drop stages
----------------------------------------------------------------------
DROP STAGE IF EXISTS CLINICAL_STUDY_AI_DB.RAG.DOCUMENT_STAGE;
DROP STAGE IF EXISTS CLINICAL_STUDY_AI_DB.RAG.EVALUATION_STAGE;

----------------------------------------------------------------------
-- 5. Drop schemas (CASCADE drops all tables, views, etc. within)
----------------------------------------------------------------------
DROP SCHEMA IF EXISTS CLINICAL_STUDY_AI_DB.OBSERVABILITY CASCADE;
DROP SCHEMA IF EXISTS CLINICAL_STUDY_AI_DB.RAG CASCADE;
DROP SCHEMA IF EXISTS CLINICAL_STUDY_AI_DB.PUBLIC CASCADE;

----------------------------------------------------------------------
-- 6. Drop the database
----------------------------------------------------------------------
DROP DATABASE IF EXISTS CLINICAL_STUDY_AI_DB;

----------------------------------------------------------------------
-- 7. Drop the dedicated warehouse
----------------------------------------------------------------------
DROP WAREHOUSE IF EXISTS CLINICAL_STUDY_AI_WH;

----------------------------------------------------------------------
-- 8. Verify cleanup
----------------------------------------------------------------------
-- These should return no results or errors confirming objects are gone
SHOW SERVICES IN ACCOUNT LIKE '%DEEPTIA%';
SHOW COMPUTE POOLS;
