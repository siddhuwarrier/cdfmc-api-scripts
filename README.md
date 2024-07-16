## Install

- Ensure you have Pyenv installed. Follow the instructions in https://github.com/pyenv/pyenv (make sure you have added the right lines to your zshrc).
- Install the required local version of Pyenv by running `pyenv local`
- Install poetry by running `curl -sSL https://install.python-poetry.org | python -`

## Run fmc-ha-status-monitor

- Change directory to the app directory; for example: `cd fmc-ha-status-monitor`
- Install the dependencies by running `poetry install`
- Generate a CDO API token following the instructions here: https://developer.cisco.com/docs/cisco-defense-orchestrator/authentication/
- Run the application by running:

```
poetry run fmc-ha-status-monitor <us|eu|aus|in|apj> -t <your-generated-token>
```

### Example output

```json
[
    {
        "name": "Ottawa",
        "primary": {
            "status": "Active",
            "deviceUid": "bd4b8168-0d0c-11ed-812c-ba0975920cf4"
        },
        "secondary": {
            "status": "Standby",
            "deviceUid": "d8fa773c-0d18-11ed-a96f-e06e43f1d09e"
        },
        "configStatus": "HEALTHY_CONFIG"
    },
    {
        "name": "SanAntonio",
        "primary": {
            "status": "Active",
            "deviceUid": "c105d4e4-e691-11ec-a8e1-d276d744cc27"
        },
        "secondary": {
            "status": "Standby",
            "deviceUid": "16905b96-e692-11ec-bbad-e65a6308e687"
        },
        "configStatus": "HEALTHY_CONFIG"
    }
]
```