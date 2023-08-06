# Racetrack client context
`racetrack-client` is a CLI client tool for deploying workloads to Racetrack (IKP-RT).

Racetrack system allows to deploy jobs in a one step.
It transforms your code to in-operation workloads, e.g. Kubernetes workloads.
You write some code according to a set of coventions, you include the manifest file which explains the code, 
and you submit it to Racetrack. A short while after, the service calling your code is in operation.

# Quickstart
1. [Install](#installation) `racetrack` client: `pip3 install racetrack-client`
1. [Configure access token](#private-job-repositories) to your git repository: `racetrack config set-credentials REPO_URL USERNAME TOKEN`
1. [Deploy](#deploying) your job to Racetrack: `racetrack deploy . https://racetrack.example.com/ikp-rt/lifecycle`
1. You will see the URL of your deployed job in the output.

# Installation
Install racetrack-client using pip:
```bash
pip3 install racetrack-client
```

Python 3.8+ is required. So if you have any troubles, try with:
```
sudo apt install python3.8 python3.8-dev python3.8-venv
python3.8 -m pip install racetrack-client
```

This will install `racetrack` CLI tool. Verify installation by running `racetrack`.

# Usage
Run `racetrack --help` to see usage.

## Deploying
To deploy a job, just run in the place where `fatman.yaml` is located:
```bash
racetrack deploy . https://racetrack.example.com/ikp-rt/lifecycle
```

`racetrack deploy [WORKDIR] [LIFECYCLE_URL]` has 2 optional arguments:
- `WORKDIR` - a place where the `fatman.yaml` is, by default it's current directory
- `LIFECYCLE_URL` - URL address to Lifecycle API-server, where a job should be deployed. 
  If not given, it will be deployed to a URL configured in a local client config, 
  by default it's set to a local cluster at `http://127.0.0.1:7002`.

## Local client configuration
If you want to update client configuration (namely persist some preferences for later use), use the following command: 
```bash
racetrack config set [CONFIG_NAME] [VALUE]
```
Local client configuration is stored at `~/.racetrack/config.yaml`.

### Configuring default Racetrack URL
You can set default Racetrack URL address: 
```bash
racetrack config set lifecycle_api_url https://racetrack.example.com/ikp-rt/lifecycle
```
Then you can run just `racetrack deploy` command (without `LIFECYCLE_URL` argument), lifecycle_url will be inferred from client configuration.

### Private Job repositories
Before building & deploying a Job stored in a private git repository, you should make sure that Racetrack has access to it.
Add git credentials to access your repository using command:
```bash
racetrack config set-credentials REPO_URL USERNAME TOKEN
```

- `REPO_URL` can be a full URL of a git remote (eg. https://gitlab.com/git/namespace/ikp-rt)
or a general domain name (eg. https://gitlab.com) if you want to use same token for all repositories from there.
- `USERNAME` is your git account username
- `TOKEN` is a password to read from your repository.
  Use access tokens with `read_repository` scope instead of your real password!
  Here's [how to create personal access token in Gitlab](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token)


# Development setup
Clone IKP-RT repository and run it inside this directory:
```bash
make setup
```
