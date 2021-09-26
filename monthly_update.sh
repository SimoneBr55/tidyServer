#!/bin/bash

## monthly_update

source .set_env_vars

python3 $hash_start_py || true

chown -R www-data:www-data $path_to_allow2 || true
setfacl -R -m u:www-data:rwx $path_to_allow2 || true

shutdown -h +5 "Server is shutting down in 5 minutes. Please wrap up your work, or type '# shutdown -c' to cancel it."
