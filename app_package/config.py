import os
from dd07_config import ConfigLocal, ConfigDev, ConfigProd

match os.environ.get('FLASK_CONFIG_TYPE'):
    case 'dev':
        config = ConfigDev()
        print('- dashAndData07/app_pacakge/config: Development')
    case 'prod':
        config = ConfigProd()
        print('- dashAndData07/app_pacakge/config: Production')
    case _:
        config = ConfigLocal()
        print('- dashAndData07/app_pacakge/config: Local')

# if os.environ.get('FLASK_CONFIG_TYPE')=='local':
#     config = ConfigLocal()
#     print('- dashAndData07/app_pacakge/config: Local')
# elif os.environ.get('FLASK_CONFIG_TYPE')=='dev':
#     config = ConfigDev()
#     print('- dashAndData07/app_pacakge/config: Development')
# elif os.environ.get('FLASK_CONFIG_TYPE')=='prod':
#     config = ConfigProd()
#     print('- dashAndData07/app_pacakge/config: Production')

# print(f"webpackage location: {os.environ.get('WEB_ROOT')}")
# print(f"config location: {os.path.join(os.environ.get('CONFIG_PATH'),os.environ.get('CONFIG_FILE_NAME')) }")