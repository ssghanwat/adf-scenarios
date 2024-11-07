# Databricks notebook source
dbutils.fs.ls("/")

# COMMAND ----------

# MAGIC %md
# MAGIC ####Retrieve secrets from key vaul

# COMMAND ----------

storage_account_name = "sasandeepadls"
container_name = "raw"
mount_point = f"/mnt/{storage_account_name}/{container_name}"

client_id = dbutils.secrets.get(scope="ProjectScope", key="ClientId")
client_secret = dbutils.secrets.get(scope="ProjectScope", key="ClientSecret")
tenant_id = dbutils.secrets.get(scope="ProjectScope", key="TenantId")


# COMMAND ----------

# MAGIC %md
# MAGIC ####Create Mount Point For Bronze silver and gold

# COMMAND ----------

def mount_adls(storage_account_name, container_name, client_id, tenant_id, client_secret, mount_point):
    try:
        # Define the source URI and configuration for mounting
        source_uri = f"abfss://{container_name.strip()}@{storage_account_name.strip()}.dfs.core.windows.net"
        configs = {
            "fs.azure.account.auth.type": "OAuth",
            "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
            "fs.azure.account.oauth2.client.id": client_id,
            "fs.azure.account.oauth2.client.secret": client_secret,
            "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
        }

        # Check if mount point already exists
        if any(mount.mountPoint == mount_point for mount in dbutils.fs.mounts()):
            print(f"Mount point {mount_point} already exists.")
        else:
            # Mount the storage
            dbutils.fs.mount(
                source=source_uri,
                mount_point=mount_point,
                extra_configs=configs
            )
            print(f"Mounted {source_uri} at {mount_point}")
    except Exception as e:
        print(f"Error mounting ADLS: {e}")

# Call the function
mount_adls(storage_account_name, container_name, client_id, tenant_id, client_secret, mount_point)


# COMMAND ----------

dbutils.fs.mounts()

# COMMAND ----------

dbutils.fs.ls(mount_point)
