# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inels_mqtt_wrapper', 'inels_mqtt_wrapper._device_interfaces']

package_data = \
{'': ['*']}

install_requires = \
['asyncio-mqtt>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'inels-mqtt-wrapper',
    'version': '0.3.2',
    'description': 'A Python library to work with Inels devices over MQTT (using Asyncio)',
    'long_description': '# Inels MQTT wrapper\n\nA Python library to work with Inels smart home devices over MQTT (using Asyncio).\n\n> **WARNING**: THIS PACKAGE IS PUBLISHED ONLY FOR TESTING THE PUBLIC INTERFACE AND IS NOT READY TO USE. MOST OF THE \n> FEATURES ARE ONLY STUBS FOR NOW AND ARE NOT IMPLEMENTED YET. IMPLEMENTED FEATURES HAVE NOT RECEIVED ANY TESTING \n> YET. DO NOT DOWNLOAD THIS PACKAGE IF YOU ARE AN OUTSIDE DEVELOPER NOT INVOLVED IN THE LIBRARY DEVELOPMENT.\n\n---\n\n## Demo code\n\nBelow is a simple code snippet to demonstrate the basic interaction with this library.\n\n```python\nimport asyncio\n\nimport asyncio_mqtt as aiomqtt\n\nfrom inels_mqtt_wrapper import RFDAC71B, DeviceStatusUnknownError\n\n\nasync def main() -> None:\n    """Entrypoint"""\n\n    async with aiomqtt.Client("localhost") as client:\n        device = RFDAC71B(\n            mac_address="00:00:00:00:00:00",  # Your gateway\'s MAC address\n            device_address="01207D",  # Your device\'s address (found on the device\'s top case)\n            mqtt_client=client,  # An instance of asyncio_mqtt.Client\n        )\n        print("Connected:", device.is_connected)  # True\n\n        try:\n            print(device.status)  # A dict containing device-specific status data\n        except DeviceStatusUnknownError as e:\n            print(e)  # Print the error if the device status is unknown\n\n        await device.set_brightness_percentage(50)  # Set the device\'s brightness to 50%\n        await device.without_function()  # Apply the before set brightness percentage\n\n        try:\n            print(device.status)  # Check the device status again\n        except DeviceStatusUnknownError as e:\n            print(e)  # Print the error if the device status is unknown\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n',
    'author': 'arseniiarsenii',
    'author_email': 'arseniivelichko2@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Multi-Agent-io/inels-mqtt-wrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
