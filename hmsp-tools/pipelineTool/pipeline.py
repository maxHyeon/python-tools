#README
#1. install python3, pip
#2. pip install ruamel.yaml
#3. pip install hvac
# code info : -b -> bootstrap, : -d -> deployment
import sys
import ruamel.yaml
import hvac

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
yaml.explicit_start = True

branch = str(sys.argv[1])
vaultToken = str(sys.argv[2])
vaultHost = str(sys.argv[3])
optionCode = str(sys.argv[4])


default_path = 'test-project'
default_mountpoint = 'test-project'

try:
    client = hvac.Client(
        url=vaultHost,
        token=vaultToken,
    )
except:
    print('vault auth fail')


def getHmspSecrets(kv_path,kv_mountpoint,secret):
    read_secret_result = client.secrets.kv.v1.read_secret(
        path=kv_path,
        mount_point=kv_mountpoint,
    )
    return str(read_secret_result['data'][secret])

def setupDeploy(branch,appname):
    containerRepoHost='test.test'
    print(containerRepoHost)
    if branch=='master':
        repoProject='test-project'
    else:
        repoProject='test-project-test'
    try:
        deploymentImage='{}/{}/{}:latest'.format(containerRepoHost,repoProject,appname) # harbor.test-projectprod02/test-project-test/discover-mservice:latest
        print(deploymentImage)
        with open('./deployment-{}.yml'.format(appname)) as stream:
            data = yaml.load(stream)
            try:
                containers = data['spec']['template']['spec']['containers']
                for container in containers:
                   if container['name'] == appname :
                       container['image'] = deploymentImage
            except:
                print('dont have container setting')
        with open('./deployment-{}.yml'.format(appname), 'wb') as stream:
            yaml.dump(data, stream)
    except:
        print('dont have deploy')

def setupBootstrap(branch):
    
    if branch=='master':
        env = 'prod'
        configSvrIP=getHmspSecrets(default_path,default_mountpoint,'prod-svr-ip')
        configSvcPort=getHmspSecrets(default_path,default_mountpoint,'config-msvc-port')
        configSvr = str('http://')+configSvrIP+':'+configSvcPort
    else:
        env = 'dev'
        configSvrIP=getHmspSecrets(default_path,default_mountpoint,'dev-svr-ip')
        configSvcPort=getHmspSecrets(default_path,default_mountpoint,'config-msvc-port')
        configSvr = str('http://')+configSvrIP+':'+configSvcPort
    try:    
        with open('./src/main/resources/bootstrap.yml') as stream:
            data = yaml.load(stream)
            try:
                profiles = data['spring']['profiles']
                profiles.update(dict(active=env))
            except:
                print('dont have profile')    
            try:
                profiles = data['spring']['cloud']['config']
                profiles.update(dict(uri=configSvr))
            except:
                print('spring config')

        with open('./src/main/resources/bootstrap.yml', 'wb') as stream:
            yaml.dump(data, stream)
    except:
        print('dont have bootstrap')

def main():
    if optionCode == '-b':
        setupBootstrap(branch)
    elif optionCode == '-d':
        appname = str(sys.argv[5])
        setupDeploy(branch,appname)


if __name__ == "__main__":
    main()
