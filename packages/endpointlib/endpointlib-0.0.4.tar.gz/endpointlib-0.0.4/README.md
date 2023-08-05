<h1 align="left">Endpointlib</h1>

<p align="left">MQTT Endpoint library</p>

## Links

- [GitHub](https://github.com/afranco-astro/endpoint-lib "GitHub Repository")
- [PyPI](https://pypi.org/project/endpointlib "PyPI Project")

## How to install

From your virtual environment run:

### `pip install endpointlib`

## How to use

### Basic example

This example just creates an enpoint to publish some data to the mqtt broker:
   
    import asyncio
    import logging
    import random
    import sys
    
    from endpointlib.clients.mqtt_async_client import MQTTAsyncClient
    from endpointlib.endpoint_factory import EndpointFactory
    
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('demo')
    
    async def demo():
        endpoint = EndpointFactory.basic_endpoint(('test.mosquitto.org', 1883), main_callback=main_entry_point)
        await endpoint.run_forever()
    
    async def main_entry_point(client: MQTTAsyncClient):
    
        logger.info('[main_entry_poiny]')
    
        #async loop
        while True:
            #call other async services
            data = random.randrange(10, 52, 1)
            data_topic = 'endpoint/data/sample'
            await client.publish(data_topic, data, qos=1, retain=True)
    
            await asyncio.sleep(5)
    
    asyncio.run(demo())

### Advanced example

This example creates an endpoint that monitors a tcp socket device. This implementation uses a simple echo tcp server to simulate the responses, this server is not included in the package.

    import asyncio
    import logging
    import sys
    
    import inspect, os, sys
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(os.path.dirname(currentdir))
    sys.path.insert(0, parentdir)
    import utils.echo_socket_server as server
    
    from endpointlib.devices.socket_device import SocketDevice
    from endpointlib.clients.mqtt_async_client import MQTTAsyncClient
    from endpointlib.endpoint_factory import EndpointFactory
    
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('demo')
    
    async def demo():
        myCallbacks = dict()
        myCallbacks['endpoint/control/device1/operation01'] = on_operation_01
        myCallbacks['endpoint/control/device1/operation02'] = on_operation_02
    
        broker = ('test.mosquitto.org', 1883)
        cmd = ':MONITOR1234!'
        # ('host_to_monitor', 'port', 'monitor_interval', 'command_to_monitor', 'on_monitor_callback')
        monitor = ('localhost', 10001, 10, cmd, on_monitor)
    
        endpoint = EndpointFactory.socket_monitor_endpoint(mqtt_connection=broker, socket_monitor=monitor, handlers=myCallbacks)
        await endpoint.run_forever()
    
    async def on_monitor(status: str, client: MQTTAsyncClient):
        logger.info('[on_monitor]: ' + status)
        await client.publish('endpoint/control/device1/response/01', '1234')
    
    async def on_operation_01(topic: str, payload: str, device: SocketDevice):
        response = await device.send_command(':M11!')
        logger.info('[on_operation_01]Response from device: ' + response)
    
    async def on_operation_02(topic: str, payload: str, device: SocketDevice):
        response = await device.send_command(':R00!')
        logger.info('[on_operation_02]Response from device: ' + response)
    
    async def main():
        await asyncio.gather(server.echo_socket_server(port=10001), demo())
    
    asyncio.run(main())

 
# Development setup

[TODO: Development setup instructions]

## Built With

- Pyhton

## Author

**Alfonso Franco**

- [Profile](https://github.com/afranco-astro "Alfonso Franco")
- [Email](mailto:afranco@astro.unam.mx)
