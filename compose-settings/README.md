


## Rationale: 

[The twelve-factor app stores config in environment variables](https://12factor.net/config) (often shortened to *env vars* or *env*)

- app config defined as pydantic ``BaseSettings`` constructed exclusively via envs and secrets. 
    - NOTE that ``BaseSettings`` has other mechanims but we will avoid using them
- fields are *const* after construction (i.e. frozen or faux-immutable in python jargon)
- field names are capitalized to resemble the env names found in the ``.env`` file listings
- can print an .env list via the CLI



