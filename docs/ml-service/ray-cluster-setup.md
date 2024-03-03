# Setting up Ray Cluster

1. Install `lambda-stack` to get gpu running with same version across all the local machines.
2. Install `ray` using `pip install ray` on all the local machines with same versions.
3. Remove firwall rules for `ray` to work properly.
4. Generate ssh keys using `ssh-keygen` and copy the public key to all the local machines using `ssh-copy-id` command. passwordless ssh is good for `ray` to work properly with out config-file.
5. Run the ray-cluster.yaml config file using `ray up` command.

