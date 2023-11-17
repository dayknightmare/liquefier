# Mongo

```docker exec -it liquefier-mongo mongosh```

```bash
config = {"_id":"liquefierReplica","members":[{"_id":0,"host":"mongo:27017"}]}
rs.initiate(config)
```