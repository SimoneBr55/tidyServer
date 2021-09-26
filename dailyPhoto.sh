#!/bin/bash

## Daily Photos ##

# This script risks to shutdown your server while you are using it!

source .set_env_vars

python3 $dailyPhoto_py_path || true

bash $ffmpeg_creator_path || true

chown -R www-data:www-data $path_to_allow1 || true
setfacl -m u:www-data:rwx $path_to_allow1 || true

chown -R www-data:www-data $path_to_allow2 || true
setfacl -R -m u:www-data:rwx $path_to_allow2 || true

shutdown -h +5 "Server is shutting down in 5 minutes. Please wrap up your work, or type '# shutdown -c' to cancel it."
