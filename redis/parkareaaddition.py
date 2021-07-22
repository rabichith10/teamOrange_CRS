import redis

redis = redis.Redis(
     host= '127.0.0.1',
     port= '6379')


redis.geoadd("parklocation",53.238143, 10.463669, 'p1')
redis.geoadd("parklocation",52.434636, 10.772603, 'p2')
redis.geoadd("parklocation",52.341087, 8.033953, 'p3')