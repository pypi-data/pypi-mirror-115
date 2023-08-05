[![PyPI](https://img.shields.io/pypi/v/mask-in-situ)](https://pypi.org/project/mask-in-situ)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mask-in-situ)](https://pypi.org/project/mask-in-situ)


# Mask in situ

Mask in situ makes it easy to encrypt only specific sections of files (for example, secrets such as password in configuration files).

The intended use is to allow config files to be shared in a partially-encrypted form, so that secrets are protected but the overall structure of the file, and the value of non-sensitive options are visible.


## Installation

You can install with `pip install mask-in-situ`, and then use the `mis` command (e.g., `mis generate-key`).

Alternatively, you can use the Docker image: `docker run jamesscottbrown/mask-in-situ "mis generate-key"`.

You can pass an environment key, and mount a directory as a volume, e.g.,

```
export CONFIG_KEY="THIS_IS_A_KEY"
docker run --user $(id -u):$(id -g) -v $(pwd):/config -e CONFIG_KEY="$CONFIG_KEY" jamesscottbrown/mask-in-situ "mis decrypt-dir -e CONFIG_KEY /config/masked /config/unmasked"
```


## Usage

![](./usage.png)

If you have a config file that contains secrets, indicate the values to be encrypted by enclosing them in `%MASK{..}`, then run the `encrypt` command providing the name of the input and output files as arguments.
You can then recover the original file using the `decrypt` command.

The  `encrypt-dir` and `decrypt-dir` commands act in the same way as `encrypt` and `decrypt`, but rather than transforming single files they transform every file in a directory (descending recursively into subdirectories).

You can generate a key using the `generate-key` subcommand.

You can provide the name of an environment variable containing the key as an option; if you do not, you will be prompted for the key interactively.


## Alternatives

Listing an alternative tool below is not an endorsement: it means I am aware that the tool exists, not that I have evaluated it.

### Encrypt part of config file

By default, [SOPS](https://github.com/mozilla/sops) encrypts every value (but not hhe keys) in a YAML/JSON file, but it can [optionally encrypt only specific values](https://github.com/mozilla/sops#encrypting-only-parts-of-a-file).

However, it works only for YAMl/JSON files (not arbitrary text files).

### Encrypt the whole file

A significant number of tools have bene developed to handle the encryption of single files; many of these support integration with Git.

* [age](https://github.com/FiloSottile/age)
* [tomb](https://www.dyne.org/software/tomb/) (GNU/linux only)

* [git-crypt](https://github.com/AGWA/git-crypt)
* [git-encrypt](https://github.com/shadowhand/git-encrypt) - deprecated
* [git-remote-crypt](https://github.com/spwhitton/git-remote-gcrypt)
* [git-secret](https://github.com/sobolevn/git-secret)
  

([git-nerps](https://github.com/mk-fg/git-nerps), [git-blur](https://github.com/acasajus/git-blur), [git-easy-crypt](https://github.com/taojy123/git-easy-crypt))
  
* [BlackBox](https://github.com/StackExchange/blackbox) - specifically intended for secrets

* [pass](https://www.passwordstore.org/)
* [transcrypt](https://github.com/elasticdog/transcrypt)
* [keyringer](https://keyringer.pw/)

As the whole file is encrypted, checking or editing a non-sensitive part of the file requires decrypting it.


### Manually remove the secrets

The original file could be edited to manually replace the secrets with placeholders, and the secrets could be stored separately in a passwword manager or encrypted file.

When a file containing plaintext secrets is required, they can be manually retrieved and re-added.

However, this requires manual effort.
In particular, whenever any change is made, it must be manually made to both the file containing the placeholders, and any versions containing plaintext secrets.


### Automatically fetch secrets from a vault

An alternative is not store secrets in any config files, and instead load them from a centralised store provided by a system like:

* [HashiCorp Vault](https://www.vaultproject.io/)
* Square's [Keywhiz](https://square.github.io/keywhiz/)
* [Akeyless Vault](https://www.akeyless.io/)
* [Thycotic Secret Server](https://thycotic.com/products/secret-server/)
* [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
* CloudFlare's [Red October](https://github.com/cloudflare/redoctober) ([announcement blog post](https://blog.cloudflare.com/red-october-cloudflares-open-source-implementation-of-the-two-man-rule/))

This provides advantages like auditing and the ability to more easily rotate credentials, but requires additional infrastructure.


### Tool-specific approaches

These typically involving extracting secrets from a config to a separate encrypted file that is then imported.

* [Ansible vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
* [Chef encrypted data bags](https://docs.chef.io/data_bags/#encrypt-a-data-bag-item)
* [Docker-compose secrets](https://docs.docker.com/compose/compose-file/compose-file-v3/#secrets)/[Docker swarm secrets](https://docs.docker.com/engine/swarm/secrets/)
* [Kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/) (and [sealed secrets](https://github.com/bitnami-labs/sealed-secrets))
* [Puppet hiera-eyaml](https://puppet.com/blog/encrypt-your-data-using-hiera-eyaml/)
...

