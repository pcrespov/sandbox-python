- a function
- a metadata file -> defines a function
- challenge:
- get metadata.yml -> create a function out of it
- type matching




-----------------

- remove DisplayOrder node-metadata.yaml
- services/catalog/src/simcore_service_catalog/services/frontend_services.py
key=f"{FRONTEND_SERVICE_KEY_PREFIX}/data-iterator/number"  as function
   - definition and implementation in the backend



simcore/service


- define meta-project: implicit by having meta-nodes
- create project snapshots from meta-project


Like the file-picker ----

parametrization_const_number
parametrization_const_int
parametrization_const_string

- schema in backend
- inputs defined in frontend
- outputs evaluated in frontend


parametrization_range_int


GET /projects/{id}/snapshots
GET /projects/{id}/snapshots/{id} <-> /projects/{project_id}  [invisible]
GET /projects/{id}/snapshots/{id}/parametrization  -> {x:3, y:0, ...}


- 
- set in put

new table
- snapshot project iwht parent meta-project
- parametrization
similar to {"sweeper": {"primaryStudyId": "9e840e48-da64-11eb-9253-02420a004c4c", "parameterValues": [{"x": 2}]}}



- DEVELOPMENT_FEATURE ??? <-->

espresso ---

GET /projects/{id}/parameters  -> { "x": "sin(y)", "y": "33" }
GET /projects/{id}/parameters/{x}/ -> { "name": x, "expression": "sin(y)", "result": "0.5" }


snapshot = a project that can run



- table with dependency and parameters
-





var1 = np.linspace(2,4)


x = var1*2
y = var1


----


x =
y =


----


- get project snapshot
- get snapshots table (i.e. iterated values??)



------------------------


- variable inputs/outputs
    - free or type contraint
    -> freeze to catalog

- return variable outputs as List[T] or OrderedDict[str, T]


- programmable cells
-

