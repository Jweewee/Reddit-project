'''reddit keys'''
username = "hehethrowaway7654321"
password = "God5lessme@@"
client_id = "EPAfVwndSboRYapVa5lSlg"
client_secret = "_LJjY0igGJnusH6PYMqeKR234ug70w"

# Confluent 
def read_config():
  # reads the client configuration from client.properties
  # and returns it as a key-value map
  config = {}
  with open("client.properties") as fh:
    for line in fh:
      line = line.strip()
      if len(line) != 0 and line[0] != "#":
        parameter, value = line.strip().split('=', 1)
        config[parameter] = value.strip()
  return config

# Twitch
TMI_TOKEN='lqmxercufphuasp7ieh4p5ziqmtcvv'
CLIENT_ID='5ptlhyjetbti68xyl0p5clqd77idkc'
BOT_NICK="redditbot"
BOT_PREFIX="!"
CHANNEL="jweewee"